"""Bridge actual outer sampling iterations into the existing monitor flow protocol."""
import json
import os
from pathlib import Path
import time
import threading


def duration(seconds):
    value = max(0, int(seconds))
    return f"{value // 3600:02d}:{value // 60 % 60:02d}:{value % 60:02d}"


class Monitor:
    def __init__(self, root, task_id, total_iterations, baseline, atomic_json):
        self.root = Path(root)
        self.atomic_json = atomic_json
        self.total = total_iterations
        self.baseline = baseline
        self.latest = baseline
        self.started = time.monotonic()
        self.log = (self.root / "logs/monitor.log").open("a", encoding="utf-8", buffering=1)
        stat = Path("/proc/self/stat").read_text().rsplit(")", 1)[1].split()
        self.identity = {"taskId": task_id, "hostId": "lab-campus",
                         "hostBootId": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
                         "pid": os.getpid(), "startTicks": stat[19]}
        self.sequence = 0
        self.details = {}
        self.lock = threading.RLock()
        threading.Thread(target=self.heartbeat, daemon=True).start()

    def heartbeat(self):
        while True:
            time.sleep(10)
            self.write()

    def write(self, completed=None, **details):
        with self.lock:
            return self._write(completed, **details)

    def _write(self, completed=None, **details):
        self.details.update(details)
        details = self.details
        if completed is not None:
            self.latest = max(self.latest, completed)
        self.sequence += 1
        elapsed = time.monotonic() - self.started
        n = self.latest - self.baseline
        target = self.total - self.baseline
        rate = n / elapsed if elapsed else 0
        remaining = (target - n) / rate if rate else 0
        # Step 0 is the completed initialization. Real inference iterations are 1..total.
        # The existing monitor's flow contract uses an exclusive upper loop index.
        state = {**self.identity, "sequence": self.sequence,
                 "resume_checkpoint_index": self.baseline,
                 "target": self.total + 1, "target_meaning": "exclusive_index",
                 "step": self.latest, "status": details.get("status", "running"),
                 "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                 "completed_sampling_iterations": self.latest,
                 "total_sampling_iterations": self.total,
                 "progress_unit": "outer_sampling_step", **details}
        self.atomic_json(self.root / "monitor_status.json", state)
        extra = " ".join(f"{k}={v}" for k, v in details.items())
        self.log.write(f"HDPS campaign {n}/{target} [{duration(elapsed)}<{duration(remaining)}, {rate:.4f}it/s] {extra}\n")
        self.log.flush()
