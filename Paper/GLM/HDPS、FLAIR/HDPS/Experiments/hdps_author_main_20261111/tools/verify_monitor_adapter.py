"""Deploy reviewed LF-only shell launchers and verify without accessing a GPU."""
from pathlib import Path
import base64
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
helper = ROOT.parents[0]/'hdps_main_20261111/tools/remote_exec.py'
spec = importlib.util.spec_from_file_location('remote_exec', helper)
remote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(remote)
payload = {
    'root':'/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111',
    'old':json.loads((ROOT/'tools/shell_deploy_base.json').read_text()),
    'files':{name:base64.b64encode((ROOT/name).read_bytes()).decode()
             for name in ['worker.sh','launch_tmux.sh']},
}
source = '''
import base64,hashlib,json,os,pathlib,subprocess,sys,time
p=json.load(sys.stdin); root=pathlib.Path(p['root'])
assert json.loads((root/'status.json').read_text())['status']=='prepared_not_started'
for name,data in p['files'].items():
 path=root/name
 assert hashlib.sha256(path.read_bytes()).hexdigest()==p['old'][name], name
 assert b'\\r' not in base64.b64decode(data)
for name,data in p['files'].items():
 path=root/name; tmp=path.with_suffix(path.suffix+'.tmp')
 tmp.write_bytes(base64.b64decode(data));tmp.chmod(0o755);os.replace(tmp,path)
env=dict(os.environ,CUDA_VISIBLE_DEVICES='')
python='/data2/cy/xzn/envs/hdps_repro/bin/python'
checks=[]
for command in [[python,str(root/'test_monitor_adapter.py')],
                [python,str(root/'preflight.py')],
                ['bash','-n',str(root/'worker.sh')],
                ['bash','-n',str(root/'launch_tmux.sh')],
                [python,'-c','from diffusers.utils.logging import disable_progress_bar; from transformers.utils.logging import disable_progress_bar']]:
 result=subprocess.run(command,cwd=root,env=env,text=True,capture_output=True,timeout=120)
 checks.append({'command':command,'returncode':result.returncode,
                'stdout':result.stdout,'stderr':result.stderr})
report={'checked_at':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'checks':checks,
        'gpu_query_performed':False,'inference_started':False,
        'gpu_selection':'inherited single CUDA_VISIBLE_DEVICES from monitor',
        'registered_entry':'start.py','shell_line_endings':'LF'}
(root/'monitor_adapter_check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
assert all(c['returncode']==0 for c in checks)
'''
raise SystemExit(remote.run(source,json.dumps(payload).encode(),timeout=240))
