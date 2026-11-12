#!/usr/bin/env bash
set -euo pipefail
ROOT=/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111
SESSION=hdps_main_gpu2
if tmux has-session -t "$SESSION" 2>/dev/null; then
  printf 'Existing session: %s\n' "$SESSION"
  exit 1
fi
/usr/bin/python3 - <<'PY'
import subprocess,csv
uuid='GPU-51dfeb46-24e7-8fd8-992d-ff14f7e32902'
r=subprocess.check_output(['nvidia-smi','--query-gpu=index,uuid,memory.free,utilization.gpu','--format=csv,noheader,nounits'],text=True)
row=next(x for x in csv.reader(r.splitlines(),skipinitialspace=True) if x[1]==uuid)
assert row[0]=='2' and int(row[2])>22500 and int(row[3])<5, 'GPU2 is no longer sufficiently idle: '+str(row)
p=subprocess.check_output(['nvidia-smi','--query-compute-apps=gpu_uuid,pid','--format=csv,noheader,nounits'],text=True)
assert not any(line.startswith(uuid) for line in p.splitlines()),'GPU2 has another compute process'
PY
tmux new-session -d -s "$SESSION" -c "$ROOT" "bash $ROOT/worker.sh"
tmux set-option -t "$SESSION" remain-on-exit on
printf 'Started tmux session: %s\n' "$SESSION"
