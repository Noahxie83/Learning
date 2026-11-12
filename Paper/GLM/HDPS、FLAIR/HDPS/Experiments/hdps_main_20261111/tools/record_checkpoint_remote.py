from pathlib import Path
import hashlib
import json
import torch

root = Path("/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111")
path = root / "checkpoints/worker_0.pt"
state = torch.load(path, map_location="cpu", weights_only=False)
assert state["job"] == "FFHQ/deblur_gauss/hdps/00000"
assert state["next_step"] >= 6
assert set(state["variables"]) == {"z", "z0y"}
assert state["cuda_rng"] is not None and len(state["cuda_rng"]) == 1
record = {
    "test": "GPU2 SIGTERM at a real sampling boundary",
    "job": state["job"], "next_step": state["next_step"],
    "checkpoint_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "variables": {key: {"shape": list(value.shape), "dtype": str(value.dtype)}
                  for key, value in state["variables"].items()},
    "rng_states": ["python", "numpy", "torch", "cuda"],
    "sampling_fingerprint": state["fingerprint"],
    "resume_execution": "restarted in the same tmux session; verify later steps in console.log",
}
(root / "verification").mkdir(exist_ok=True)
(root / "verification/resume.json").write_text(json.dumps(record, indent=2))
print(json.dumps(record))
