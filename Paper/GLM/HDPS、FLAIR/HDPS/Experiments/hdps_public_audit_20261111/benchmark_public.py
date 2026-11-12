"""Bounded audit of the released HDPS algorithm on the same FFHQ input/GPU.

Only model paths, Tiny VAE's documented zero shift, unused PIQ construction,
frozen pretrained weights, and observer hooks differ from the released module.
All scientific constants/updates in SD3HDPS are asserted unchanged below.
"""
import ast
import gc
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parent
MAIN = ROOT.parent / 'hdps_main_20261111'
REPO = ROOT.parents[1]
sys.path[:0] = [str(MAIN), str(REPO)]
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from torchvision.utils import save_image
from munch import munchify
from pytorch_msssim import ssim
from prepare_runtime import prepare


def atomic_json(path, value):
    temp = Path(str(path)+'.tmp')
    temp.write_text(json.dumps(value, indent=2, allow_nan=False))
    os.replace(temp, path)


def seed_all(value):
    random.seed(value)
    np.random.seed(value)
    torch.manual_seed(value)
    torch.cuda.manual_seed_all(value)


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Observer:
    def restore(self, variables, optimizers=()):
        return 0

    def save(self, step, variables, optimizers=()):
        atomic_json(ROOT/'status.json', {'status':'benchmarking_public_code', 'pid':os.getpid(),
                                        'step':step, 'total':50, 'updated_at':time.time()})


def method_ast(source, name):
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name=='SD3HDPS')
    return ast.dump(next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name==name), include_attributes=False)


def decoder_timing(module, name, latent):
    module.requires_grad_(False).eval()
    dtype = next(module.parameters()).dtype
    latent = latent.to(dtype=dtype)
    def decode(value):
        value = value/module.config.scaling_factor + module.config.shift_factor
        return module.decode(value, return_dict=False)[0]
    with torch.no_grad():
        target = decode(latent).float() + .01
    forward = []
    forward_backward = []
    for iteration in range(6):
        torch.cuda.synchronize()
        start=time.monotonic()
        with torch.no_grad():
            result=decode(latent)
        torch.cuda.synchronize()
        f=time.monotonic()-start
        del result
        variable=latent.detach().clone().requires_grad_(True)
        torch.cuda.synchronize()
        start=time.monotonic()
        loss=torch.linalg.norm((decode(variable).float()-target).reshape(1,-1))
        gradient=torch.autograd.grad(loss,variable)[0]
        torch.cuda.synchronize()
        fb=time.monotonic()-start
        assert torch.isfinite(gradient).all()
        if iteration:
            forward.append(f)
            forward_backward.append(fb)
        del gradient,loss,variable
    return {'decoder':name,'forward_seconds_median':float(np.median(forward)),
            'forward_backward_seconds_median':float(np.median(forward_backward)),
            'timed_repetitions':5}


def main():
    assert os.environ.get('CUDA_VISIBLE_DEVICES')=='GPU-51dfeb46-24e7-8fd8-992d-ff14f7e32902'
    assert torch.cuda.device_count()==1
    torch.set_num_threads(4)
    torch.backends.cudnn.deterministic=True
    torch.backends.cudnn.benchmark=False
    config=json.loads((MAIN/'config.json').read_text())
    config['profile']='author_code'
    upstream_sha,runtime_sha=prepare(config,ROOT/'runtime_sampler.py')
    assert upstream_sha=='f8b709b49b7d8f3ec1904badade3510359f3ecf03bdf16522c4d32b1ae025992'
    original=(REPO/'sd3_sampler.py').read_text()
    adapted=(ROOT/'runtime_sampler.py').read_text()
    identical={name:method_ast(original,name)==method_ast(adapted,name)
               for name in ['data_consistency_x','data_consistency_z','get_pinv','calculate_v']}
    assert all(identical.values())
    specification=importlib.util.spec_from_file_location('public_hdps_runtime',ROOT/'runtime_sampler.py')
    runtime=importlib.util.module_from_spec(specification)
    specification.loader.exec_module(runtime)
    runtime._RECOVERY=Observer()
    atomic_json(ROOT/'status.json',{'status':'loading_models','pid':os.getpid()})
    solver=runtime.get_solver('hdps')
    for encoder in [solver.text_enc_1,solver.text_enc_2,solver.text_enc_3]: encoder.to('cuda')
    with torch.no_grad():
        prompt=solver.encode_prompt(['a photo of a closed face'])
        null=solver.encode_prompt([''])
    del solver.text_enc_1,solver.text_enc_2,solver.text_enc_3,encoder
    gc.collect()
    torch.cuda.empty_cache()
    solver.vae.to('cuda')
    solver.transformer.to('cuda')
    from functions.degradation import get_degradation
    tf=transforms.Compose([transforms.Resize(768),transforms.CenterCrop(768),transforms.ToTensor()])
    path=Path('/data2/cy/caoyi/datasets/FFHQ/val/00000.png')
    image=tf(Image.open(path).convert('RGB')).unsqueeze(0).cuda()*2-1
    seed_all(513319557)  # Same corruption seed/input as the slow completed run.
    deg=munchify({'channels':3,'image_size':768,'deg_scale':61})
    operator=get_degradation('deblur_gauss',deg,torch.device('cuda'))
    observation=operator.A(image)+.03*torch.randn_like(operator.A(image))
    initial_rng={'python':random.getstate(),'numpy':np.random.get_state(),
                 'torch':torch.get_rng_state(),'cuda':torch.cuda.get_rng_state_all()}
    original_decode=solver.decode
    counter=[0]
    def counted_decode(value):
        counter[0]+=1
        return original_decode(value)
    solver.decode=counted_decode
    records=[]
    for repeat in range(2):
        random.setstate(initial_rng['python']);np.random.set_state(initial_rng['numpy'])
        torch.set_rng_state(initial_rng['torch']);torch.cuda.set_rng_state_all(initial_rng['cuda'])
        before=counter[0]
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize();started=time.monotonic()
        output=solver.sample(measurement=observation,operator=operator,task='deblur_gauss',
                             prompts='a photo of a closed face',NFE=50,img_shape=(768,768),
                             cfg_scale=2.,step_size=15.,prompt_emb=prompt,null_emb=null,mask_type=None)
        torch.cuda.synchronize();elapsed=time.monotonic()-started
        assert torch.isfinite(output).all()
        result_path=ROOT/f'public_reconstruction_{repeat}.png'
        save_image(output,result_path,normalize=True)  # Exactly the released solve.py mapping.
        restored=transforms.ToTensor()(Image.open(result_path).convert('RGB')).unsqueeze(0).cuda()
        ref=((image+1)/2).clamp(0,1)
        ref=(ref*255+.5).clamp(0,255).to(torch.uint8).float()/255
        mse=float((restored-ref).square().mean())
        records.append({'repeat':repeat,'sampling_seconds':elapsed,'decoder_calls':counter[0]-before,
                        'psnr_public_mapping':float(-10*np.log10(mse)),
                        'ssim_public_mapping':float(ssim(restored*255,ref*255,data_range=255)),
                        'peak_gpu_gib':torch.cuda.max_memory_allocated()/1024**3,
                        'output_sha256':file_hash(result_path)})
        assert records[-1]['decoder_calls']==801
        atomic_json(ROOT/'benchmark_results.json',{'upstream_sha256':upstream_sha,
                    'runtime_sha256':runtime_sha,'unchanged_hdps_methods':identical,'samples':records})
        print('PUBLIC_RESULT '+json.dumps(records[-1]),flush=True)
        del output,restored,ref
        torch.cuda.empty_cache()
    with torch.no_grad(): latent=solver.encode(operator.At(observation).view(1,3,768,768).half())
    timings=[]
    timings.append(decoder_timing(solver.vae,'author_Tiny_FP16',latent))
    timings.append(decoder_timing(solver.vae.float(),'Tiny_FP32',latent))
    from diffusers import AutoencoderKL
    full=AutoencoderKL.from_pretrained(config['model'],subfolder='vae',torch_dtype=torch.float32).cuda()
    timings.append(decoder_timing(full,'full_SD3_VAE_FP32',latent))
    timings.append(decoder_timing(full.half(),'full_SD3_VAE_FP16',latent))
    report={'upstream_sha256':upstream_sha,'runtime_sha256':runtime_sha,
            'unchanged_hdps_methods':identical,'samples':records,'decoder_microbenchmarks':timings,
            'source_image':str(path),'source_sha256':file_hash(path),'corruption_seed':513319557,
            'full_slow_sample':json.loads((MAIN/'results/FFHQ/deblur_gauss/hdps/00000.json').read_text())}
    # Retain the complete trace in the report, print only bounded timing metadata.
    atomic_json(ROOT/'benchmark_results.json',report)
    atomic_json(ROOT/'status.json',{'status':'completed','pid':os.getpid(),'samples':len(records)})
    print('DECODER_TIMINGS '+json.dumps(timings),flush=True)


if __name__=='__main__':
    try: main()
    except Exception as error:
        atomic_json(ROOT/'status.json',{'status':'failed','pid':os.getpid(),'error':str(error)})
        raise
