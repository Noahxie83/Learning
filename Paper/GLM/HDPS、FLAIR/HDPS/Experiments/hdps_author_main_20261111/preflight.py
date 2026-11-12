"""CPU-only protocol, input and exact-resume checks; never allocate a GPU."""
import json
import os
from pathlib import Path
import random
import tempfile
import unittest

os.environ['CUDA_VISIBLE_DEVICES'] = ''
import numpy as np
import torch
from prepare_runtime import prepare
from recovery import Recovery
from run_experiments import datasets
import run_experiments as campaign

ROOT = Path(__file__).resolve().parent


def seed():
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)


class Preflight(unittest.TestCase):
    def test_all_released_solver_classes_unchanged(self):
        config = json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
        # prepare() asserts full AST equivalence for HDPS, FlowDPS and FLAIR.
        with tempfile.TemporaryDirectory() as directory:
            prepare(config, Path(directory)/'runtime.py')

    def test_complete_data_and_caption_pairing(self):
        config = json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
        selected, missing = datasets(config, 0)
        self.assertEqual(missing, [])
        self.assertEqual(sum(len(x['items']) for x in selected), 2800)
        self.assertEqual(sum(len(x['items']) for x in selected)*len(config['methods'])*len(config['tasks']), 42000)

    def test_exact_rng_and_shared_optimizer_parameter_resume(self):
        def run(steps, checkpoint=None):
            z = torch.tensor([.1, .2, .3], requires_grad=True)
            noise = torch.zeros(3)
            optimizers = [torch.optim.SGD([z], lr=.1), torch.optim.SGD([z], lr=.2)]
            start = 0
            if checkpoint is not None:
                variables = {'z':z, 'noise':noise}
                start = Recovery(checkpoint, 'job', 'protocol').restore(variables, optimizers)
                z, noise = variables['z'], variables['noise']
                self.assertIs(optimizers[0].param_groups[0]['params'][0], z)
                self.assertIs(optimizers[1].param_groups[0]['params'][0], z)
            for i in range(start, steps):
                for optimizer in optimizers:
                    perturbation = torch.randn_like(z) + random.random() + np.random.random()
                    (z*perturbation).sum().backward()
                    optimizer.step()
                    optimizer.zero_grad()
                noise = noise + torch.randn_like(noise)
                if checkpoint is not None:
                    Recovery(checkpoint, 'job', 'protocol', interval=1).save(i+1, {'z':z, 'noise':noise}, optimizers)
            return z.detach(), noise
        seed()
        expected = run(8)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'state.pt'
            seed()
            run(3, path)
            torch.randn(100)
            resumed = run(8, path)
            self.assertTrue(all(torch.equal(a,b) for a,b in zip(expected,resumed)))

    def test_metric_summary_deduplicates_results_and_excludes_resumed_timing(self):
        previous = campaign.ROOT, campaign.RESULT_CACHE
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'paper_table1_targets.json').write_bytes((ROOT/'paper_table1_targets.json').read_bytes())
            campaign.ROOT, campaign.RESULT_CACHE, campaign.np = root, None, np
            common = {'complete':True,'dataset':'FFHQ','task':'deblur_gauss','method':'hdps',
                      'ssim':.8,'lpips_code_vgg224_01':.1,'lpips_standard_vgg768_m11':.2,'peak_gpu_gib':5}
            first = dict(common, sample='a', psnr=20, sampling_seconds=20, resumed_from_step=0)
            second = dict(common, sample='b', psnr=30, sampling_seconds=10, resumed_from_step=5)
            try:
                campaign.aggregate(first, write=False)
                campaign.aggregate(first, write=False)
                campaign.aggregate(second, write=False)
                row = campaign.aggregate()[0]
                self.assertEqual(row['count'], 2)
                self.assertEqual(row['psnr'], 25)
                self.assertEqual(row['sampling_seconds'], 20)
                self.assertEqual(row['timed_samples'], 1)
            finally:
                campaign.ROOT, campaign.RESULT_CACHE = previous


if __name__ == '__main__':
    assert not torch.cuda.is_available()
    unittest.main(verbosity=2)
