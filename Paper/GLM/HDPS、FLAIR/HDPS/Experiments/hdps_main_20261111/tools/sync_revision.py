"""Update only owned files whose deployed SHA256 still matches the reviewed version."""
import base64
import hashlib
import json
from pathlib import Path
from remote_exec import run

root = Path(__file__).resolve().parents[1]
expected = {
    "run_experiments.py": "13e70fac43a6cc08013a835c0ad5217ec0cedaf3d2f6c8d091d7f9a118f8678c",
    "prepare_runtime.py": "f72a55dff82f5994874604ab1f44528009491311302a477ff0a680e25e4b97b2",
}
files = {name: base64.b64encode((root / name).read_bytes()).decode() for name in expected}
script = '''
from pathlib import Path
import hashlib,base64,json,os,sys
root=Path('/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111')
payload=json.load(sys.stdin)
expected=payload['expected']
files=payload['files']
for name,encoded in files.items():
 p=root/name
 content=base64.b64decode(encoded)
 old=p.read_bytes()
 assert old==content or hashlib.sha256(old).hexdigest()==expected[name], 'Concurrent edit: '+name
 temporary=p.with_suffix('.deploy.tmp')
 temporary.write_bytes(content)
 os.replace(temporary,p)
print('Synchronized reviewed experiment revision')
'''
raise SystemExit(run(script, json.dumps({"expected": expected, "files": files}).encode()))
