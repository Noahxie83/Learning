"""Read the trusted checkpoint and live process; run with the remote venv Python."""
import hashlib
import json
from pathlib import Path
import time
import torch

root = Path('/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111')
state = torch.load(root/'checkpoints/worker_0.pt', map_location='cpu', weights_only=False)
status = json.loads((root/'status.json').read_text())
assert status['profile'] == 'paper_equations_v1' and status['status'] == 'running'
assert state['next_step'] >= 5 and set(state['variables']) == {'z', 'z0y'}
assert all(v.dtype == torch.float32 and list(v.shape) == [1,16,96,96] and torch.isfinite(v).all()
           for v in state['variables'].values())
assert len(state['cuda_rng']) == 1
record = {
    'recorded_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'status': status,
    'checkpoint_job': state['job'], 'checkpoint_next_step': state['next_step'],
    'latent_dtype': 'torch.float32', 'latent_shape': [1,16,96,96],
    'checkpoint_has_all_rng_states': all(k in state for k in ['python_rng','numpy_rng','torch_rng','cuda_rng']),
    'original_source_sha256': hashlib.sha256((root.parents[1]/'sd3_sampler.py').read_bytes()).hexdigest(),
}
(root/'verification').mkdir(exist_ok=True)
(root/'verification/paper_startup.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record))
