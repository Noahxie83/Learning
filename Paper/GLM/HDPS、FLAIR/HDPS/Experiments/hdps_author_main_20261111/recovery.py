"""Trusted, atomic outer-sampling-step recovery for this experiment."""
import os
from pathlib import Path
import random
import signal
import numpy as np
import torch


class InterruptedRun(Exception):
    pass


class Recovery:
    def __init__(self, path, job, fingerprint, interval=5, progress=None):
        self.path = Path(path)
        self.job = job
        self.fingerprint = fingerprint
        self.interval = interval
        self.progress = progress or (lambda step: None)
        self.stop_requested = False
        self.next_step = 0

    def request_stop(self, *_):
        self.stop_requested = True

    def install_signals(self):
        signal.signal(signal.SIGTERM, self.request_stop)
        signal.signal(signal.SIGINT, self.request_stop)

    def restore(self, variables, optimizers=()):
        if not self.path.is_file():
            return 0
        state = torch.load(self.path, map_location="cpu", weights_only=False)
        if state["job"] != self.job:
            return 0
        if state["fingerprint"] != self.fingerprint:
            raise RuntimeError("Checkpoint protocol/source fingerprint mismatch")
        for name, tensor in variables.items():
            saved = state["variables"][name].to(tensor.device, tensor.dtype)
            if tensor.requires_grad and optimizers:
                with torch.no_grad():
                    tensor.copy_(saved)
            else:
                variables[name] = saved
        for optimizer, saved in zip(optimizers, state.get("optimizers", [])):
            optimizer.load_state_dict(saved)
        random.setstate(state["python_rng"])
        np.random.set_state(state["numpy_rng"])
        torch.set_rng_state(state["torch_rng"])
        if state.get("cuda_rng") is not None:
            torch.cuda.set_rng_state_all(state["cuda_rng"])
        self.next_step = state["next_step"]
        self.progress(self.next_step)
        return self.next_step

    def save(self, next_step, variables, optimizers=()):
        self.progress(next_step)
        if next_step % self.interval and not self.stop_requested:
            return
        state = {
            "job": self.job, "fingerprint": self.fingerprint,
            "next_step": next_step,
            "variables": {k: v.detach().cpu() for k, v in variables.items()},
            "optimizers": [x.state_dict() for x in optimizers],
            "python_rng": random.getstate(), "numpy_rng": np.random.get_state(),
            "torch_rng": torch.get_rng_state(),
            "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp." + str(os.getpid()))
        with temporary.open("wb") as stream:
            torch.save(state, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, self.path)
        if self.stop_requested:
            raise InterruptedRun("Sampling state saved; stopped at an outer-step boundary")
