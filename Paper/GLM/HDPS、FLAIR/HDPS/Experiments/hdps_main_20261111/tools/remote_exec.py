"""Run reviewed Python on lab-campus; no repository code is executed implicitly."""
import argparse
import base64
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
       "-o", "StrictHostKeyChecking=yes", "lab-campus"]
REMOTE = "/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111"


def run(source, payload=None, timeout=120):
    encoded = base64.b64encode(source.encode()).decode()
    command = 'python3 -c "import base64;exec(base64.b64decode(\'' + encoded + '\'))"'
    result = subprocess.run(SSH + [command], input=payload, capture_output=True,
                            timeout=timeout)
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    return result.returncode


def upload(directory):
    root = Path(directory).resolve()
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(root).as_posix()
            data = path.read_bytes()
            item = tarfile.TarInfo(relative)
            item.size = len(data)
            item.mode = 0o755 if path.suffix == ".sh" else 0o644
            archive.addfile(item, io.BytesIO(data))
    source = '''
import io,tarfile,pathlib,sys,hashlib,json
root=pathlib.Path(REMOTE_TARGET)
root.mkdir(parents=True,exist_ok=True)
assert not any(p.is_symlink() for p in [root,*root.parents])
count=0
with tarfile.open(fileobj=sys.stdin.buffer,mode="r|") as archive:
 for item in archive:
  path=pathlib.PurePosixPath(item.name)
  assert item.isfile() and not path.is_absolute() and ".." not in path.parts
  destination=root.joinpath(*path.parts)
  assert destination.resolve().is_relative_to(root.resolve())
  data=archive.extractfile(item).read()
  if destination.exists():
   assert destination.read_bytes()==data, "Refusing to overwrite changed file: "+str(destination)
  else:
   destination.parent.mkdir(parents=True,exist_ok=True)
   with destination.open("xb") as f:f.write(data)
   destination.chmod(item.mode)
  assert destination.read_bytes()==data
  count+=1
print(json.dumps({"uploaded":count,"directory":str(root)}))
'''.replace("REMOTE_TARGET", repr(REMOTE))
    return run(source, buffer.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["exec", "upload"])
    parser.add_argument("path")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.mode == "upload":
        raise SystemExit(upload(args.path))
    raise SystemExit(run(Path(args.path).read_text(encoding="utf-8"),
                         timeout=args.timeout))
