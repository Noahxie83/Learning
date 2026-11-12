#!/usr/bin/env bash
set -euo pipefail
ROOT=/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111
ENV=/data2/cy/xzn/envs/hdps_repro
mkdir -p "$ROOT/logs" "$ROOT/checkpoints" /data2/cy/xzn/.cache/torch
if [[ ! -x "$ENV/bin/python" ]]; then
  /home/cy/.conda/envs/flair/bin/python -m venv --system-site-packages "$ENV"
fi
export PIP_DISABLE_PIP_VERSION_CHECK=1
"$ENV/bin/python" -m pip install --no-cache-dir \
  diffusers==0.30.1 transformers==4.46.3 accelerate==1.0.1 \
  lpips==0.1.4 pytorch-msssim==1.0.0
"$ENV/bin/python" -c 'import torch,diffusers,transformers,lpips,pytorch_msssim; print("HDPS environment imports OK", torch.__version__, diffusers.__version__, transformers.__version__)'
