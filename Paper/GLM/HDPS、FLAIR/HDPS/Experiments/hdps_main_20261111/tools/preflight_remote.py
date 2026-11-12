from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import numpy as np

root = Path("/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111")
sys.path.insert(0, str(root))
from prepare_runtime import prepare
from run_experiments import datasets
config = json.loads((root / "config.json").read_text())
selected, missing = datasets(config, 0)
assert not missing, missing
assert sum(len(x["items"]) for x in selected) == 2800
upstream, runtime_hash = prepare(config, root / "runtime_sampler.py")
sys.path.insert(0, config["repo"])
specification = importlib.util.spec_from_file_location("preflight_runtime", root / "runtime_sampler.py")
module = importlib.util.module_from_spec(specification)
specification.loader.exec_module(module)
assert all(method in module.__SOLVER__ for method in config["methods"])
regularizer = np.load(config["flair_regularizer"], allow_pickle=False)
assert np.isfinite(regularizer).all()
vgg = Path("/data2/cy/xzn/.cache/torch/hub/checkpoints/vgg16-397923af.pth")
part = vgg.with_suffix(vgg.suffix + ".part")
print(json.dumps({
    "datasets": {x["name"]: len(x["items"]) for x in selected},
    "missing": missing, "sampling_jobs": 42000,
    "source_sha256": upstream, "runtime_sha256": runtime_hash,
    "regularizer_shape": list(regularizer.shape),
    "regularizer_sha256": hashlib.sha256(Path(config["flair_regularizer"]).read_bytes()).hexdigest(),
    "vgg_complete": vgg.is_file(),
    "vgg_transfer_bytes": part.stat().st_size if part.exists() else None,
    "solvers": config["methods"]}, indent=2))
print(subprocess.check_output(
    ["nvidia-smi", "--id=2", "--query-gpu=index,memory.free,utilization.gpu",
     "--format=csv,noheader,nounits"], text=True))
