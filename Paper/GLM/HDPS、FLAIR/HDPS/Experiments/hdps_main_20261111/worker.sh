#!/usr/bin/env bash
set -euo pipefail
ROOT=/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111
ENV=/data2/cy/xzn/envs/hdps_repro
export CUDA_VISIBLE_DEVICES=GPU-51dfeb46-24e7-8fd8-992d-ff14f7e32902
export TORCH_HOME=/data2/cy/xzn/.cache/torch
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
export PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
export CUBLAS_WORKSPACE_CONFIG=:4096:8
cd "$ROOT"
mkdir -p logs checkpoints
exec >> logs/console.log 2>&1
printf '%s Starting or resuming HDPS main experiment on physical GPU2\n' "$(date -Is)"
exec "$ENV/bin/python" -u "$ROOT/run_experiments.py" "$@"
