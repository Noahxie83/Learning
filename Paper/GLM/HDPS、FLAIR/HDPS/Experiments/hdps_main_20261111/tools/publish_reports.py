import base64
import json
from pathlib import Path
from remote_exec import run

root = Path(__file__).resolve().parents[1]
paths = list(root.glob("*.md")) + [root / "MONITOR_CONFIG.json", root / "paper_table1_targets.json"]
payload = {p.name: base64.b64encode(p.read_bytes()).decode() for p in paths}
script = '''
from pathlib import Path
import json,base64
root=Path('/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111')
for name,encoded in json.load(__import__('sys').stdin).items():
 assert Path(name).name==name
 p=root/name;data=base64.b64decode(encoded)
 if p.exists():assert p.read_bytes()==data,'Refusing to overwrite changed report: '+name
 else:
  with p.open('xb') as f:f.write(data)
print('Published protocol, comparability and monitor reports')
'''
raise SystemExit(run(script, json.dumps(payload).encode()))
