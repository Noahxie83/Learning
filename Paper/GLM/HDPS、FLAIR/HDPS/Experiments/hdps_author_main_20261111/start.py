"""Shared environment bootstrap for manual and TrainingMonitor launches.

--check validates dependencies/assets on CPU and never starts inference.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import re
import runpy
import sys

ROOT = Path(__file__).resolve().parent
VENV = Path('/data2/cy/xzn/envs/hdps_repro')
PYTHON = VENV/'bin/python'


def environment(config):
    return dict(os.environ,
                TORCH_HOME='/data2/cy/xzn/.cache/torch',
                HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                OMP_NUM_THREADS='4', MKL_NUM_THREADS='4',
                TOKENIZERS_PARALLELISM='false', PYTHONUNBUFFERED='1',
                CUBLAS_WORKSPACE_CONFIG=':4096:8')


def check(config, env):
    code = '''import sys,json,importlib
from pathlib import Path
modules={}
for name in ['torch','torchvision','diffusers','transformers','accelerate','lpips','pytorch_msssim','numpy','scipy','munch','PIL','safetensors','cv2','matplotlib']:
 m=importlib.import_module(name);modules[name]=getattr(m,'__version__','import_ok')
sys.path.insert(0,CONFIG['repo'])
importlib.import_module('functions.degradation')
import torch
assert not torch.cuda.is_available(), 'Environment check must remain CPU-only'
assets=[Path(CONFIG['model'])/'model_index.json',Path(CONFIG['model'])/'transformer/config.json',Path(CONFIG['tiny_vae'])/'config.json',Path(CONFIG['flair_regularizer'])]
assert all(p.is_file() for p in assets), 'Required model/regularizer asset missing'
assert list(Path(CONFIG['model']).glob('transformer/*.safetensors'))
assert list(Path(CONFIG['tiny_vae']).glob('*.safetensors'))
assert Path('/data2/cy/xzn/.cache/torch/hub/checkpoints/vgg16-397923af.pth').is_file()
print(json.dumps({'python':sys.executable,'prefix':sys.prefix,'packages':modules,'assets_checked':len(assets),'cuda_visible_devices':'','gpu_allocated':False}))
'''.replace('CONFIG', repr(config))
    # The probe's subprocess explicitly cannot see or allocate any GPU.
    result = subprocess.run([str(PYTHON), '-c', code], env=dict(env, CUDA_VISIBLE_DEVICES=''),
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        sys.stderr.write(result.stderr)
        raise RuntimeError('Environment check failed')
    report = json.loads(result.stdout)
    report.update(entry=str(ROOT/'run_experiments.py'), bootstrap=str(ROOT/'start.py'),
                  working_directory=str(ROOT), profile=config['profile'])
    print(json.dumps(report, indent=2))


def selected_gpu(environ):
    value = environ.get('CUDA_VISIBLE_DEVICES', '').strip()
    if not value:
        raise RuntimeError('监控器必须通过CUDA_VISIBLE_DEVICES分配一张卡；脚本不会自行选卡')
    tokens = value.split(',')
    if len(tokens) != 1 or not re.fullmatch(r'(?:[0-9]+|GPU-[A-Za-z0-9._:-]+|MIG-[A-Za-z0-9._:/-]+)', value):
        raise RuntimeError('本单卡入口只接受一张监控器分配的GPU: '+value)
    return value


def run_registered_entry(remaining):
    # Keep /proc/PID/cmdline registered as start.py and retain the same PID/FDs.
    # runpy only executes the existing batch driver; no solver update is replaced.
    os.chdir(ROOT)
    sys.argv = [str(ROOT/'run_experiments.py'), *remaining]
    runpy.run_path(str(ROOT/'run_experiments.py'), run_name='__main__')


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--check', action='store_true')
    options, remaining = parser.parse_known_args()
    config = json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
    assert config['profile'] == 'author_release'
    if not PYTHON.is_file():
        raise RuntimeError('Prepared Python environment not found: '+str(PYTHON))
    env = environment(config)
    if options.check:
        if remaining:
            raise ValueError('--check accepts no inference arguments')
        check(config, env)
        return
    # Re-exec first when called from the system Python; no torch import occurs there.
    if Path(sys.prefix) != VENV:
        os.execve(str(PYTHON), [str(PYTHON), '-u', str(ROOT/'start.py'), *remaining], env)
    assigned = selected_gpu(env)
    os.environ.update(env)
    print('GPU_ASSIGNMENT: CUDA_VISIBLE_DEVICES='+assigned+'; process logical device=cuda:0', flush=True)
    run_registered_entry(remaining)


if __name__ == '__main__':
    main()
