import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from recovery import Recovery


def seed():
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)


class RecoveryTest(unittest.TestCase):
    def test_exact_restart_including_rng(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.pt"
            seed()
            expected = torch.zeros(8)
            for _ in range(10):
                expected += torch.randn_like(expected) + random.random() + np.random.random()
            seed()
            z = torch.zeros(8)
            recovery = Recovery(path, "job-a", "protocol-a", interval=5)
            for i in range(5):
                z += torch.randn_like(z) + random.random() + np.random.random()
                recovery.save(i + 1, {"z": z})
            torch.randn(100)  # Loading a model/initialization before restore consumes RNG.
            state = {"z": torch.zeros(8)}
            step = Recovery(path, "job-a", "protocol-a").restore(state)
            self.assertEqual(step, 5)
            for _ in range(step, 10):
                state["z"] += torch.randn_like(state["z"]) + random.random() + np.random.random()
            self.assertTrue(torch.equal(state["z"], expected))
            with self.assertRaisesRegex(RuntimeError, "fingerprint"):
                Recovery(path, "job-a", "changed-protocol").restore({"z": torch.zeros(8)})
            self.assertEqual(Recovery(path, "another-job", "protocol-a").restore({"z": torch.zeros(8)}), 0)

    def test_runtime_has_all_three_hooks(self):
        import ast
        from prepare_runtime import RuntimePatch
        config = {"profile": "paper_explicit_parameters", "model": "model",
                  "tiny_vae": "tiny", "flair_regularizer": "regularizer.npy"}
        source = "\n".join(
            "class " + name + ":\n"
            " def sample(self):\n"
            "  for i,t in pbar:\n"
            "   z=z+1\n"
            for name in ["SD3HDPS", "SD3FlowDPS", "SD3FLAIR"])
        patch = RuntimePatch(config)
        result = patch.visit(ast.parse(source))
        self.assertEqual(patch.recovery_loops, 3)
        compile(ast.fix_missing_locations(result), "test", "exec")


if __name__ == "__main__":
    unittest.main()
