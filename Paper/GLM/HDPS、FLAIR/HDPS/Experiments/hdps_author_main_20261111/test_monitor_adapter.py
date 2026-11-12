"""CPU-only integration tests for the monitor's actual startup/log contracts."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import start
from monitoring import Monitor, effective_steps
from run_experiments import atomic_json


class MonitorAdapterTests(unittest.TestCase):
    def test_any_single_monitor_gpu_is_preserved(self):
        for value in ['0','2','7','GPU-fake-first-card','GPU-fake-other-card','MIG-fake/1/0']:
            self.assertEqual(start.selected_gpu({'CUDA_VISIBLE_DEVICES':value}), value)
        for value in ['', '-1', '0,1', 'GPU-a,GPU-b', '0; echo bad']:
            with self.assertRaises(RuntimeError):
                start.selected_gpu({'CUDA_VISIBLE_DEVICES':value})

    def test_environment_does_not_override_device(self):
        with mock.patch.dict(os.environ, {'CUDA_VISIBLE_DEVICES':'GPU-selected-by-monitor'}):
            env = start.environment({})
        self.assertEqual(env['CUDA_VISIBLE_DEVICES'],'GPU-selected-by-monitor')
        self.assertEqual(env['HF_HUB_OFFLINE'],'1')

    def test_single_registered_entry_and_pid_survive_runpy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # Isolated synthetic fixture; the real batch driver is never executed.
            (root/'run_experiments.py').write_text(
                'import os,json\nfrom pathlib import Path\n'
                'Path("observed.json").write_text(json.dumps({"pid":os.getpid(),'
                '"cmdline":Path("/proc/self/cmdline").read_bytes().decode().split(chr(0)),'
                '"gpu":os.environ["CUDA_VISIBLE_DEVICES"]}))\n')
            fixture = root/'start.py'
            fixture.write_text('import sys\nsys.path.insert(0,'+repr(str(Path(start.__file__).parent))+')\n'
                               'import start as adapter\nfrom pathlib import Path\n'
                               'adapter.ROOT=Path('+repr(directory)+')\nadapter.run_registered_entry([])\n')
            env = dict(os.environ, CUDA_VISIBLE_DEVICES='GPU-fixture-device')
            result = subprocess.run([sys.executable,str(fixture)],env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            observed = json.loads((root/'observed.json').read_text())
            self.assertEqual(observed['cmdline'][1],str(fixture))
            self.assertEqual(observed['gpu'],'GPU-fixture-device')

    def test_monotonic_progress_resume_and_author_sr_budget(self):
        self.assertEqual(effective_steps('hdps','sr_bicubic',50),43)
        self.assertEqual(effective_steps('flair','sr_bicubic',50),50)
        total = 2800*sum(effective_steps(m,t,50) for m in ['hdps','flowdps','flair']
                         for t in ['deblur_gauss','inpainting','deblur_motion','sr_bicubic','sr_avgpool'])
        self.assertEqual(total,2060800)
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            path = Path(directory)/'status.json'
            monitor = Monitor(path,'hdps_author_main_20261111',93,50,
                              {'status':'running','total_samples':2,'completed_samples':1},
                              atomic_json,stream=output,start_thread=False,
                              identity={'pid':123,'startTicks':'456','hostBootId':'test-boot'})
            monitor.update(55,sampling_step=5,sampling_steps=43)
            monitor.emit()
            state=json.loads(path.read_text())
            self.assertEqual(state['taskId'],'hdps_author_main_20261111')
            self.assertEqual(state['resume_checkpoint_index'],50)
            self.assertEqual(state['target'],94)
            self.assertEqual(state['step'],55)
            self.assertIn('5/43 [',output.getvalue())
            self.assertNotIn('heartbeat',output.getvalue())
            with self.assertRaises(ValueError): monitor.update(54)
            monitor.update(93,completed_samples=2,status='completed')
            monitor.close()
            self.assertEqual(json.loads(path.read_text())['completed_outer_steps'],93)


if __name__ == '__main__':
    unittest.main(verbosity=2)
