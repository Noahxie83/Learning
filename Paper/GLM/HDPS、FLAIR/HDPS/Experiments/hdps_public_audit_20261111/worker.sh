#!/usr/bin/env bash
set -euo pipefail
ROOT=/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_public_audit_20261111
export CUDA_VISIBLE_DEVICES=GPU-51dfeb46-24e7-8fd8-992d-ff14f7e32902
export TORCH_HOME=/data2/cy/xzn/.cache/torch
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8
cd /data2/cy/xzn/Code/HDPS
exec >> "$ROOT/console.log" 2>&1
exec /data2/cy/xzn/envs/hdps_repro/bin/python -u "$ROOT/benchmark_public.py"
