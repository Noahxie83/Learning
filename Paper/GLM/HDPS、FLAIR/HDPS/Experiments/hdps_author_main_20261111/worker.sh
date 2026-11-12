#!/usr/bin/env bash
set -euo pipefail
ROOT=/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111
if [ -n "${HDPS_GPU_UUID:-}" ]; then export CUDA_VISIBLE_DEVICES="$HDPS_GPU_UUID"; fi
: "${CUDA_VISIBLE_DEVICES:?Set the GPU selected by your monitor or an explicit free GPU}"
export TORCH_HOME=/data2/cy/xzn/.cache/torch
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8
cd "$ROOT"
mkdir -p logs checkpoints
exec >> "$ROOT/logs/console.log" 2>&1
printf '%s Starting author-code HDPS campaign\n' "$(date -Is)"
exec /data2/cy/xzn/envs/hdps_repro/bin/python -u "$ROOT/start.py" "$@"
