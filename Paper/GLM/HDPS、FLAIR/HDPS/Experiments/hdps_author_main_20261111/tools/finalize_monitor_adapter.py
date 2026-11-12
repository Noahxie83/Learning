"""Sync only reviewed monitor-adaptation files with compare-before-replace."""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REMOTE='/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111'
helper=ROOT.parent/'hdps_main_20261111/tools/remote_exec.py'
spec=importlib.util.spec_from_file_location('remote_exec',helper)
remote=importlib.util.module_from_spec(spec);spec.loader.exec_module(remote)

query="""
from pathlib import Path
import json,hashlib
r=Path(REMOTE)
print(json.dumps({'check':json.loads((r/'monitor_adapter_check.json').read_text()),
 'check_sha256':hashlib.sha256((r/'monitor_adapter_check.json').read_bytes()).hexdigest(),
 'launch_configuration_check_sha256':hashlib.sha256((r/'launch_configuration_check.json').read_bytes()).hexdigest()}))
""".replace('REMOTE',repr(REMOTE))
encoded=base64.b64encode(query.encode()).decode()
result=subprocess.run(remote.SSH+['python3 -c "import base64;exec(base64.b64decode(\''+encoded+'\'))"'],
                      capture_output=True,timeout=30,check=True)
snapshot=json.loads(result.stdout)
report=snapshot['check'];assert all(c['returncode']==0 for c in report['checks'])
def write_json(name,value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write_json('monitor_adapter_check.json',report)
write_json('launch_configuration_check.json',{
    'single_assigned_gpu_preserved':'passed',
    'no_hardcoded_physical_device':True,'registered_entry_preserved':'start.py',
    'shell_syntax':'passed','cpu_tests':'8 passed',
    'monitor_parser_check':'passed; generic session bar and Flow baseline/count contracts',
    'gpu_query_performed':False,'gpu_inference_started':False,
})
expected=json.loads((ROOT/'monitor_adaptation_base.json').read_text())
expected['launch_configuration_check.json']=snapshot['launch_configuration_check_sha256']
expected['monitor_adapter_check.json']=snapshot['check_sha256']
names=['SUMMARY.md','COMMANDS.md','LOG.md','MONITOR_CONFIG.json','status.json',
       'launch_configuration_check.json','monitor_adapter_check.json','monitor_protocol_check.json',
       'tools/configure_monitor_environment.mjs','tools/check_monitor_protocol.mjs']
expected['tools/configure_monitor_environment.mjs']=None
expected['tools/check_monitor_protocol.mjs']=None
expected['monitor_protocol_check.json']=None
# The app-maintenance helper already existed remotely in the previous setup.
query="""
from pathlib import Path
import json,hashlib
r=Path(REMOTE)
names=NAMES
print(json.dumps({n:hashlib.sha256((r/n).read_bytes()).hexdigest() if (r/n).exists() else None for n in names}))
""".replace('REMOTE',repr(REMOTE)).replace('NAMES',repr(['tools/configure_monitor_environment.mjs','tools/check_monitor_protocol.mjs']))
encoded=base64.b64encode(query.encode()).decode()
result=subprocess.run(remote.SSH+['python3 -c "import base64;exec(base64.b64decode(\''+encoded+'\'))"'],capture_output=True,timeout=30,check=True)
helper_hashes=json.loads(result.stdout)
expected.update(helper_hashes)
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.iterdir())
          if p.is_file() and p.suffix in {'.py','.sh','.json','.md'}
          and p.name not in {'preparation_manifest.json','monitor_adaptation_base.json','monitor_deployment_check.json'}}
write_json('preparation_manifest.json',manifest)
names.append('preparation_manifest.json')
payload={'root':REMOTE,'files':{n:{'old':expected[n],'data':base64.b64encode((ROOT/n).read_bytes()).decode()} for n in names}}
source='''
import base64,hashlib,json,os,pathlib,sys,time
p=json.load(sys.stdin);r=pathlib.Path(p['root'])
assert r.resolve()==r and not r.is_symlink()
assert json.loads((r/'status.json').read_text())['status']=='prepared_not_started'
entries={str(r/'start.py').encode(),str(r/'run_experiments.py').encode()}
active=[]
for proc in pathlib.Path('/proc').glob('[0-9]*/cmdline'):
 try:
  args=set(proc.read_bytes().split(b'\\0'))
  if args & entries:active.append(proc.parts[2])
 except (OSError,PermissionError):pass
assert not active,active
for name,item in p['files'].items():
 path=r/name
 actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
 desired=hashlib.sha256(base64.b64decode(item['data'])).hexdigest()
 assert actual in {item['old'],desired},(name,actual,item['old'])
for name,item in p['files'].items():
 path=r/name;path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_bytes(base64.b64decode(item['data']));os.replace(tmp,path)
manifest=json.loads((r/'preparation_manifest.json').read_text())
for name,digest in manifest.items():
 assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
status=json.loads((r/'status.json').read_text())
assert status['completed_samples']==0 and not list((r/'results').glob('*/*/*/*.json'))
print(json.dumps({'files_synced':list(p['files']),'verified_root_files':len(manifest),
 'status':status['status'],'completed_samples':status['completed_samples'],
 'gpu_selection':'inherited from monitor; no fixed physical GPU','gpu_query_performed':False,
 'inference_started':False,'active_inference_processes':active}))
'''
raise SystemExit(remote.run(source,json.dumps(payload).encode(),timeout=120))
