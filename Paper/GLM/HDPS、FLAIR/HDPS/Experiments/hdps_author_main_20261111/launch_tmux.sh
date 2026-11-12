#!/usr/bin/env bash
set -euo pipefail
ROOT=/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111
SESSION=hdps_author_main
if [ -n "${HDPS_GPU_UUID:-}" ]; then export CUDA_VISIBLE_DEVICES="$HDPS_GPU_UUID"; fi
: "${CUDA_VISIBLE_DEVICES:?GPU selection must be provided explicitly; no card is hardcoded}"
[[ "$CUDA_VISIBLE_DEVICES" =~ ^([0-9]+|GPU-[A-Za-z0-9._:-]+|MIG-[A-Za-z0-9._:/-]+)$ ]] || { printf 'Select one GPU\n'; exit 1; }
COMMAND="env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES bash $ROOT/worker.sh"
if tmux has-session -t "$SESSION" 2>/dev/null; then
  [ "$(tmux list-panes -t "$SESSION" -F '#{pane_dead}')" = 1 ] || { printf 'Session is active\n'; exit 1; }
  tmux respawn-pane -t "$SESSION:0.0" -c "$ROOT" "$COMMAND"
else
  tmux new-session -d -s "$SESSION" -c "$ROOT" "$COMMAND"
fi
tmux set-option -t "$SESSION" remain-on-exit on
printf 'Started %s\n' "$SESSION"
