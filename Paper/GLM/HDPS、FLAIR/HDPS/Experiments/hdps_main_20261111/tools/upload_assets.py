import hashlib
import io
import json
from pathlib import Path
import tarfile
from remote_exec import run

CACHE = Path(r"C:\Users\noahx\.codex\visualizations\2026\11\04\01a1a703-ab56-79d2-9ef9-ab57d2c63a91\hdps_assets_20261111")
root = CACHE / "afhq_validation"
manifest = {}
buffer = io.BytesIO()
with tarfile.open(fileobj=buffer, mode="w") as archive:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        manifest[relative] = hashlib.sha256(data).hexdigest()
        item = tarfile.TarInfo(relative)
        item.size = len(data)
        archive.addfile(item, io.BytesIO(data))
    data = json.dumps({"files": manifest, "sources": json.loads((CACHE / "sources.json").read_text())}).encode()
    item = tarfile.TarInfo("__manifest__.json")
    item.size = len(data)
    archive.addfile(item, io.BytesIO(data))
assert len(manifest) == 1000
source = r'''
from pathlib import Path
import tarfile,sys,hashlib,json
root=Path('/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111/assets/afhq/val')
root.mkdir(parents=True,exist_ok=True)
manifest=None
received={}
with tarfile.open(fileobj=sys.stdin.buffer,mode='r|') as archive:
 for item in archive:
  assert item.isfile()
  if item.name=='__manifest__.json':
   manifest=json.loads(archive.extractfile(item).read());continue
  parts=Path(item.name).parts
  assert len(parts)==2 and parts[0] in ['cat','dog'] and '..' not in parts
  destination=root/item.name
  assert destination.resolve().is_relative_to(root.resolve())
  assert not any(p.is_symlink() for p in [destination,*destination.parents])
  data=archive.extractfile(item).read()
  destination.parent.mkdir(parents=True,exist_ok=True)
  if destination.exists():assert destination.read_bytes()==data
  else:
   with destination.open('xb') as f:f.write(data)
  received[item.name]=hashlib.sha256(data).hexdigest()
assert manifest is not None and manifest['files']==received
(root.parent/'sources.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'uploaded_afhq_validation':len(received),'bytes':sum(p.stat().st_size for p in root.rglob('*') if p.is_file())}))
'''
raise SystemExit(run(source, buffer.getvalue(), timeout=180))
