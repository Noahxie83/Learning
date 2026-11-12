"""Explicit user-authorized reset of the previous run, with scoped path checks."""
import base64
import hashlib
import json
from pathlib import Path
from remote_exec import run

root = Path(__file__).resolve().parents[1]
expected = json.loads((root / "revision_input_hashes.json").read_text(encoding="utf-8"))
names = list(expected) + ["paper_hdps.py", "monitor_bridge.py", "tests/test_paper.py"]
files = {name: base64.b64encode((root / name).read_bytes()).decode() for name in names}
source = r'''
from pathlib import Path
import base64, hashlib, json, os, shutil, subprocess, sys, time
root=Path('/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111')
assert root.resolve()==root and root.is_dir()
assert not any(p.is_symlink() for p in [root,*root.parents])
pane=subprocess.check_output(['tmux','list-panes','-t','hdps_main_gpu2','-F','#{pane_dead}'],text=True).strip()
assert pane=='1', 'Previous tmux process is active; refuse reset'
payload=json.load(sys.stdin)
for name, content in payload['files'].items():
 p=root/name
 assert p.resolve().is_relative_to(root) and not p.is_symlink()
 if p.exists():
  assert name in payload['expected'], 'New destination already exists: '+name
  assert hashlib.sha256(p.read_bytes()).hexdigest()==payload['expected'][name], 'Concurrent file edit: '+name
# Only former run-generated artifacts. Assets/models/code are deliberately absent.
targets=['results','checkpoints','logs','manifests','verification','status.json',
         'monitor_status.json','metrics_summary.csv','runtime_sampler.py','runtime_sampler.diff',
         'startup_evidence.json','__pycache__']
deleted=[]
counts={}
for name in targets:
 p=root/name
 assert p.resolve().is_relative_to(root) and not p.is_symlink()
 if p.is_dir():
  assert not any(c.is_symlink() for c in p.rglob('*')), 'Symlink inside generated artifacts'
  counts[name]=sum(x.is_file() for x in p.rglob('*'))
 elif p.exists(): counts[name]=1
 else: counts[name]=0
for name in targets:
 p=root/name
 if p.is_dir(): shutil.rmtree(p)
 elif p.exists(): p.unlink()
 if counts[name]: deleted.append(name)
for name, encoded in payload['files'].items():
 p=root/name
 p.parent.mkdir(parents=True,exist_ok=True)
 data=base64.b64decode(encoded)
 temporary=p.with_suffix(p.suffix+'.deploy.tmp')
 temporary.write_bytes(data)
 os.replace(temporary,p)
 assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(data).digest()
receipt={'time':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'reason':'Explicit user request: delete previous results and restart from paper',
         'deleted':deleted,'file_counts':counts,'profile':'paper_equations_v1',
         'source_untouched_sha256':hashlib.sha256((root.parents[1]/'sd3_sampler.py').read_bytes()).hexdigest()}
(root/'reset_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
'''
raise SystemExit(run(source, json.dumps({"expected": expected, "files": files}).encode(), timeout=120))
