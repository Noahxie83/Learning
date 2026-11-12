import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from paper_hdps import posterior_gradient, pixel_correction, align
from recovery import Recovery
from prepare_runtime import prepare


class Identity:
    def A(self, x):
        return x


class PaperTest(unittest.TestCase):
    def test_posterior_gradient_matches_closed_form(self):
        x = torch.tensor([0.2, 0.7])
        anchor = torch.tensor([0.4, 0.8])
        y = torch.tensor([0.1, 0.5])
        sigma, noise = 0.8, 0.03
        expected = (y-x)/noise**2 + (anchor-x)/(sigma**2/(1+sigma**2))
        torch.testing.assert_close(posterior_gradient(x, anchor, Identity(), y, sigma, noise), expected)

    def test_squared_alignment_and_langevin_rng(self):
        z, diagnostic = align(lambda x: 2*x, torch.tensor([0.1, 0.2]), torch.tensor([1.0, 1.0]), 15, 1.0)
        self.assertLess(diagnostic['alignment_final_sse'], diagnostic['alignment_initial_sse'])
        self.assertTrue(torch.isfinite(z).all())
        torch.manual_seed(9)
        actual = pixel_correction(torch.zeros(4), Identity(), torch.ones(4)*0.1, .8, .03, 1, 1e-4)
        torch.manual_seed(9)
        expected = 1e-4 * torch.ones(4)*.1/.03**2 + (2e-4)**.5*torch.randn(4)
        torch.testing.assert_close(actual, expected)

    def test_runtime_original_vae_and_paper_dc_budgets(self):
        config = json.loads((ROOT/'config.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            destination=Path(directory)/'runtime.py'
            prepare(config, destination)
            source=destination.read_text()
            self.assertNotIn('pipe.vae = AutoencoderTiny.from_pretrained',source)
            self.assertIn('num_iters = 3',source)
            tree=__import__('ast').parse(source)
            flair=next(x for x in tree.body if isinstance(x,__import__('ast').ClassDef) and x.name=='SD3FLAIR')
            self.assertFalse(any(isinstance(x,__import__('ast').Break) for x in __import__('ast').walk(flair)))


if __name__ == '__main__':
    unittest.main()
