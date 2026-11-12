"""Emit monotonic campaign progress through the monitor's existing log protocol."""
import os
from pathlib import Path
import threading
import time


def duration(seconds):
    n = max(0, int(seconds))
    return f'{n//3600:02d}:{n//60%60:02d}:{n%60:02d}'


class Monitor:
    def __init__(self, path, task_id, total, baseline, status, atomic_json, *,
                 stream=None, interval=10, start_thread=True, identity=None):
        import sys
        self.path, self.task_id = Path(path), task_id
        self.total, self.baseline, self.actual = total, baseline, baseline
        self.status, self.atomic_json = dict(status), atomic_json
        self.stream = stream or sys.stdout
        self.started = time.monotonic()
        self.sequence = 0
        self.lock = threading.RLock()
        self.stopped = threading.Event()
        if identity is None:
            fields = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
            identity = {'pid':os.getpid(), 'startTicks':fields[19],
                        'hostBootId':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
        self.identity = dict(identity)
        self.interval = interval
        self.emit()
        if start_thread:
            threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while not self.stopped.wait(self.interval):
            self.emit()

    def _state(self):
        return {**self.status, **self.identity, 'taskId':self.task_id, 'hostId':'lab-campus',
                'sequence':self.sequence, 'resume_checkpoint_index':self.baseline,
                # The app's Flow contract uses a completed initialization at step 0.
                'target':self.total+1, 'target_meaning':'exclusive_index', 'step':self.actual,
                'completed_outer_steps':self.actual, 'total_outer_steps':self.total,
                'updated_at':time.strftime('%Y-%m-%dT%H:%M:%S%z')}

    def update(self, actual, **changes):
        with self.lock:
            if actual < self.actual or actual > self.total:
                raise ValueError('Campaign progress must be monotonic and bounded')
            stage_changed = changes.get('status', self.status.get('status')) != self.status.get('status')
            self.actual = actual
            self.status.update(changes)
            self.sequence += 1
            self.atomic_json(self.path, self._state())
            if stage_changed:
                self.emit()

    def emit(self):
        with self.lock:
            self.sequence += 1
            state = self._state()
            self.atomic_json(self.path, state)
            elapsed = time.monotonic()-self.started
            n, target = self.actual-self.baseline, self.total-self.baseline
            rate = n/elapsed if elapsed > 0 else 0
            remaining = (target-n)/rate if rate else 0
            # Both generic and Flow log parsers can recognize this single global bar.
            text = (f'HDPS {n}/{target} [{duration(elapsed)}<{duration(remaining)}, {rate:.5f}it/s] '
                    f'global_step={self.actual} stage={state.get("status","starting")} '
                    f'images={state.get("completed_samples",0)}/{state.get("total_samples",0)} '
                    f'job={state.get("job","initializing")} '
                    f'sample_step={state.get("sampling_step",0)}/{state.get("sampling_steps",0)}')
            self.stream.write(text+'\n')
            self.stream.flush()

    def close(self):
        self.stopped.set()
        self.emit()


def effective_steps(method, task, nfe):
    return min(nfe, 43) if method == 'hdps' and 'sr' in task else nfe
