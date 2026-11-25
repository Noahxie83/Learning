# Score-based SDE (VP-SDE / DDPM++) CIFAR-10 训练参数与配置说明文档

本文档记录了在本地 RTX 5080 与学校 8×RTX 4090 服务器环境下，针对 **Score-based Generative Modeling through Stochastic Differential Equations (Song et al., ICLR 2021)** 中 **VP-SDE (Variance Preserving SDE / Continuous DDPM++)** 算法的调参方案、断点机制与实操运行指南。

---

## 一、 实验基本信息

* **算法类型**：VP-SDE（连续时间方差保持随机微分方程，Continuous-time Variance Preserving SDE）
* **骨干网络**：`NCSN++`（深层 U-Net 结构，参数量约 61.8M，包含 BigGAN 残差块、Swish 激活函数与 16×16 分辨率自注意力机制）
* **数据集**：CIFAR-10（32×32×3，无条件图像生成，TFDS 本地高速缓存加载）
* **代码库路径**：
  * 本地路径：`D:\Learning\Paper\GLM\Score-Based\score_sde_pytorch` (WSL: `/mnt/d/Learning/Paper/GLM/Score-Based/score_sde_pytorch`)
  * 服务器路径：`/data2/cy/xzn/Code/Score-Based/score_sde_pytorch`
* **运行环境**：
  * 本地：WSL2 Ubuntu 26.04 + RTX 5080 (16GB 显存) + Conda 环境 `d2l` (PyTorch 2.14.0+cu130)
  * 服务器：Linux + 8×RTX 4090 (24GB 显存) + Conda 环境 `flow_matching` (PyTorch 2.6.0+cu124)

---

## 二、 关键参数调整对照表与设计考量

| 参数名称 | 命令行 / 配置文件配置项 | 原始默认值 | 调参优化值 | 调整原因与设计考量 |
| :--- | :--- | :---: | :---: | :--- |
| **运行模式** | `--mode` | `train` | **`train`** | 训练生成模型模式。 |
| **配置文件** | `--config` | - | **`configs/vp/cifar10_ddpmpp_continuous.py`** | 选用官方在 CIFAR-10 上最优的连续时间 VP-SDE DDPM++ 模型配置。 |
| **工作目录** | `--workdir` | - | **`./workdir_vp`** | 权重、日志、采样图片独立输出文件夹。 |
| **总迭代步数** | `config.training.n_iters` | `1300000` | **`100000`** | 原论文 130 万步旨在刷榜验证，单卡需连续跑多天；调整为 **10 万步**（在 **2~3 万步** 时即可观察到清晰成型的图像），大幅节省时间。 |
| **批次大小** | `config.training.batch_size` | `128` | **`128`** | 单卡 batch_size=128 在 5080 (16G) 和 4090 (24G) 上显存占用约为 7~8 GB，速度与显存利用率达到最佳平衡。 |
| **采样/保存步频** | `config.training.snapshot_freq` | `50000` | **`5000`** | **核心调优项**。默认 5 万步间隔太长，调整为每 5,000 步保存一次 Checkpoint 并调用 Predictor-Corrector 采样器生成 64 张采样网格图，便于实时监测模型质量。 |
| **容灾保存步频** | `config.training.snapshot_freq_for_preemption` | `10000` | **`5000`** | 周期性刷新保存 `checkpoints-meta/checkpoint.pth`，保障随时中断随时恢复。 |
| **评估频率** | `config.training.eval_freq` | `100` | **`100`** | 每 100 步计算一次验证集 loss。 |
| **日志记录频率** | `config.training.log_freq` | `50` | **`50`** | 每 50 步向终端及 TensorBoard 记录一次训练 Loss。 |
| **学习率与预热** | `config.optim.lr` / `warmup` | `2e-4` / `5000` | **`2e-4` / `5000`** | 保持 Adam 初始平稳收敛。 |
| **EMA 衰减系数** | `config.model.ema_rate` | `0.9999` | **`0.9999`** | 采样时启用 EMA 权重，生成画质显著优于未平滑权重。 |

---

## 三、 代码稳定性增强与工程改进（已应用）

1. **PyTorch 2.6+ 权重反序列化修复**：
   - 在 `utils.py` 中将 `torch.load` 补全 `weights_only=False`，彻底根除 PyTorch 新版本反序列化 `ml_collections` 配置字典时的崩溃问题。
2. **终端实时可视化 (tqdm + stdout 绑定)**：
   - 在 `main.py` 中加入标准输出流处理器（`sys_handler`），在 `run_lib.py` 中包装 `tqdm` 动态进度条，直观展示实时步数、速度（it/s）与实时 Loss。
3. **优雅中断保护（Graceful Ctrl+C Handler）**：
   - 增加捕获 `KeyboardInterrupt` 异常处理逻辑。用户在任何时候按下 `Ctrl+C`，系统均会完整捕获并将当前精确步数与所有优化器状态刷入 `workdir_vp/checkpoints-meta/checkpoint.pth`，杜绝文件损坏。
4. **断点无缝自动接力（Seamless Checkpoint Resume）**：
   - 重新运行同一条命令时，脚本自动检测最新检查点并从中断步数（如第 20,294 步）无缝继续训练。
5. **采样状态友好提醒**：
   - 在触发 5,000 步采样验证时，控制台明确提示“正在进行数值采样，耗时约 1~2 分钟”，消除误判“程序卡死”的疑虑。

---

## 四、 启动与接力运行命令

### 1. 本地 RTX 5080 启动 / 断点继续命令
```bash
# 激活环境并进入工作目录
conda activate d2l
cd "/mnt/d/Learning/Paper/GLM/Score-Based/score_sde_pytorch"

# 启动训练（如已有中断检查点，会自动无缝接力）
python main.py \
  --config=configs/vp/cifar10_ddpmpp_continuous.py \
  --workdir=./workdir_vp \
  --mode=train \
  --config.training.n_iters=100000 \
  --config.training.snapshot_freq=5000 \
  --config.training.snapshot_freq_for_preemption=5000
```

### 2. 服务器 4090 运行命令（单卡或指定空闲卡）
```bash
conda activate flow_matching
cd "/data2/cy/xzn/Code/Score-Based/score_sde_pytorch"

# 假设指定空闲的 GPU 1 运行
CUDA_VISIBLE_DEVICES=1 python main.py \
  --config=configs/vp/cifar10_ddpmpp_continuous.py \
  --workdir=./workdir_vp \
  --mode=train \
  --config.training.n_iters=100000 \
  --config.training.snapshot_freq=5000 \
  --config.training.snapshot_freq_for_preemption=5000
```

---

## 五、 输出文件说明

* **采样图片**：`workdir_vp/samples/iter_xxxx/sample.png`（包含 64 张生成图片的网格图）
* **模型权重**：`workdir_vp/checkpoints/checkpoint_x.pth`（阶段性权重，步数对应 x × 5000）
* **断点元数据**：`workdir_vp/checkpoints-meta/checkpoint.pth`（最新保存点，支持中断恢复）
* **完整日志**：`workdir_vp/stdout.txt`
* **TensorBoard**：`workdir_vp/tensorboard/`（可通过 `tensorboard --logdir=./workdir_vp/tensorboard` 启动看板）