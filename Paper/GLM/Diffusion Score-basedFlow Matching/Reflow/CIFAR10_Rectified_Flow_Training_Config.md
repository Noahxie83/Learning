# Rectified Flow (1-RF & 2-Reflow) CIFAR-10 训练参数与两阶段配置说明文档

本文档记录了在本地 RTX 5080 与学校 8×RTX 4090 服务器环境下，针对 **Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow (Liu et al., ICLR 2023)** 中 **1-Rectified Flow (基础生成)** 与 **2-Reflow (轨迹拉直 / 蒸馏)** 两阶段算法的调参方案、断点机制与实操运行指南。

---

## 一、 算法核心与两阶段逻辑

Rectified Flow 将扩散生成过程建模为常微分方程（ODE）的最短流线传输：
1. **第一阶段 (1-Rectified Flow)**：
   * **原理**：从标准高斯噪声 $X_0 \sim \mathcal{N}(0, I)$ 到真实图片 $X_1 \sim \text{CIFAR-10}$，通过直线插值 $X_t = t X_1 + (1-t) X_0$ 学习速度场 $v_\theta(X_t, t)$。
   * **特点**：单阶段训练后即可进行高质量生成，但流线之间可能存在微弱交叉。
2. **第二阶段 (Reflow / 2-RF 或在线蒸馏)**：
   * **原理**：利用第一阶段训练好的模型权重，以随机噪声 $Z_0$ 为初值积分推演生成终点图像 $Z_1$，构造强耦合对 $(Z_0, Z_1)$ 进行二次对齐（Reflow）。
   * **特点**：流线几乎变为完美直线，可实现 **1~2 步（NFE=1~2）极速高清生成**。
   * **衔接机制**：**支持在第一阶段任意阶段性检查点（如 20,000~30,000 步）随时中断，直接载入该权重进入第二阶段**。

---

## 二、 基础运行信息

* **骨干网络**：`NCSN++`（参数量约 61.8M，BigGAN 残差块，位置/傅里叶时间嵌入）
* **数据集**：CIFAR-10（32×32×3，无条件图像生成）
* **代码库路径**：
  * 本地路径：`D:\Learning\Paper\GLM\Reflow\RectifiedFlow\ImageGeneration` (WSL: `/mnt/d/Learning/Paper/GLM/Reflow/RectifiedFlow/ImageGeneration`)
  * 服务器路径：`/data2/cy/xzn/Code/Reflow/RectifiedFlow/ImageGeneration`
* **运行环境**：
  * 本地：WSL2 Ubuntu 26.04 + RTX 5080 (16GB 显存) + Conda 环境 `d2l` (PyTorch 2.14.0+cu130)
  * 服务器：Linux + 8×RTX 4090 (24GB 显存) + Conda 环境 `flow_matching` (PyTorch 2.6.0+cu124)

---

## 三、 第一阶段 (1-RF) 参数对照表与调优设计

| 参数名称 | 命令行 / 配置文件配置项 | 原始默认值 | 调参优化值 | 调整原因与设计考量 |
| :--- | :--- | :---: | :---: | :--- |
| **运行模式** | `--mode` | `train` | **`train`** | 1-RF 基础速度场训练。 |
| **配置文件** | `--config` | - | **`configs/rectified_flow/cifar10_rf_gaussian_ddpmpp.py`** | CIFAR-10 最优高斯先验 DDPM++ 骨干网络配置。 |
| **工作目录** | `--workdir` | - | **`./workdir_1rf`** | 第一阶段权重与图片独立隔离。 |
| **总迭代步数** | `config.training.n_iters` | `1300000` | **`100000`** | 原论文 130 万步旨在刷极低 FID；实测在 **20,000 ~ 30,000 步**（约 20~25 分钟）时物体轮廓即已清晰，即可中断转入第二阶段。 |
| **批次大小** | `config.training.batch_size` | `128` | **`128`** | 单卡 batch_size=128，在 16G 显存下占用约 7GB，速度稳定在 15~20 it/s。 |
| **采样/保存步频** | `config.training.snapshot_freq` | `100000` | **`5000`** | 默认 10 万步才存一次图，修改为每 5,000 步保存 Checkpoint 并用 ODE 求解器生成采样网格图。 |
| **容灾保存步频** | `config.training.snapshot_freq_for_preemption` | `10000` | **`5000`** | 周期性保存最新 `checkpoints-meta/checkpoint.pth`。 |
| **评估频率** | `config.training.eval_freq` | `100` | **`100`** | 每 100 步评估一次测试 Loss。 |
| **日志记录频率** | `config.training.log_freq` | `50` | **`50`** | 每 50 步输出终端日志与 TensorBoard 标量。 |
| **学习率与预热** | `config.optim.lr` / `warmup` | `2e-4` / `5000` | **`2e-4` / `5000`** | 保持 Adam 稳定收敛。 |

---

## 四、 代码稳定性增强与工程改进（已应用）

1. **显存彻底隔离**：
   - 在 `main.py` 入口主动调用 `tf.config.set_visible_devices([], 'GPU')`，使 TensorFlow 数据预取完全运行在 CPU/RAM 上，**100% 显存（16GB / 24GB）专供 PyTorch**，杜绝 CUDA 上下文冲突。
2. **PyTorch 2.6+ 序列化全覆盖修复**：
   - 在 `utils.py` 及第二阶段核心脚本 `run_lib_reflow.py:73` 中的 `torch.load` 均增加 `weights_only=False`，确保加载跨阶段权重时稳定无报错。
3. **两阶段统一的终端可视化 (tqdm) 与优雅中断**：
   - 第一阶段（`1-RectifiedFlow`）与第二阶段（`2-Reflow`）均已封装 `tqdm` 动态进度条，支持实时显式 Loss。
   - 均已内置 `KeyboardInterrupt` 异常拦截器：按下 `Ctrl+C` 自动将当前精确步数保存到 `checkpoints-meta/checkpoint.pth`。
4. **断点无缝自动恢复**：
   - 自动检测并载入已有 Checkpoint，重新执行命令即可自适应接力。

---

## 五、 实操运行命令指南

### 步骤 1：启动第一阶段 (1-RF) 基础训练
```bash
# 激活环境并进入工作目录
conda activate d2l
cd "/mnt/d/Learning/Paper/GLM/Reflow/RectifiedFlow/ImageGeneration"

# 启动 1-RF（随时可 Ctrl+C 中断，下次运行自动接力）
python main.py \
  --config=configs/rectified_flow/cifar10_rf_gaussian_ddpmpp.py \
  --workdir=./workdir_1rf \
  --mode=train \
  --config.training.n_iters=100000 \
  --config.training.snapshot_freq=5000 \
  --config.training.snapshot_freq_for_preemption=5000
```

### 步骤 2：中断第一阶段并进入第二阶段 (Reflow)
当第一阶段在 `workdir_1rf/samples/` 中的采样图已经清晰（建议跑至 20,000 ~ 30,000 步左右），在终端直接按 `Ctrl+C` 暂停，然后启动第二阶段在线 Reflow：

```bash
cd "/mnt/d/Learning/Paper/GLM/Reflow/RectifiedFlow/ImageGeneration"

# 载入第一阶段保存的最新断点，启动在线 Reflow 二次对齐
python main.py \
  --config=configs/rectified_flow/cifar10_rf_gaussian_reflow_train_online.py \
  --workdir=./workdir_2reflow \
  --mode=reflow \
  --config.reflow.last_flow_ckpt=./workdir_1rf/checkpoints/checkpoint_20.pth \
  --config.training.n_iters=50000 \
  --config.training.snapshot_freq=1000 \
  --config.training.snapshot_freq_for_preemption=1000 \
  --config.training.snapshot_at_start=True
```

---

## 六、 输出文件结构说明

```
ImageGeneration/
├── workdir_1rf/                        # 第一阶段输出
│   ├── samples/iter_5000/sample.png    # 阶段性 ODE 采样图片
│   ├── checkpoints/checkpoint_1.pth    # 阶段性权重 (对应步数 = x * 5000)
│   ├── checkpoints-meta/checkpoint.pth # 第一阶段最新断点 (供接力或转入第二阶段)
│   └── stdout.txt                      # 完整运行日志
└── workdir_2reflow/                    # 第二阶段输出
    ├── samples/iter_0/sample.png       # 第二阶段初始模型的采样图
    ├── samples/iter_1000/sample.png    # 每 1000 步生成采样图，同时保存 sample.np
    ├── checkpoints/checkpoint_0.pth   # 第二阶段尚未更新的模型状态
    ├── checkpoints/checkpoint_1.pth   # 完成 1000 次更新后的模型状态
    └── checkpoints-meta/checkpoint.pth # 第二阶段断点
```

---

## 七、2026-10-18 第二阶段输出周期调整与重新运行

本次调整仅针对在线第二阶段配置 `configs/rectified_flow/cifar10_rf_gaussian_reflow_train_online.py`，第一阶段每 5000 步保存的设置保持不变。

| 设置 | 之前实际运行值 | 本次运行值 | 作用 |
| :--- | :---: | :---: | :--- |
| `training.n_iters` | 50000 | 50000 | 第二阶段总更新次数，不缩短训练预算。 |
| `training.snapshot_freq` | 5000 | **1000** | 每 1000 次更新保存一个历史 checkpoint 并生成采样图。 |
| `training.snapshot_freq_for_preemption` | 5000 | **1000** | 每 1000 次更新保存最新恢复断点。 |
| `training.snapshot_at_start` | 无 | **True** | 新实验在第一次更新前保存第 0 步模型和采样图。 |
| `training.snapshot_sampling` | True | True | 同时生成 `sample.png` 与 `sample.np`。 |
| `training.log_freq` / `training.eval_freq` | 50 / 100 | 50 / 100 | 训练与验证 loss 的记录频率保持不变。 |
| `training.batch_size` / `optim.lr` | 128 / 2e-4 | 128 / 2e-4 | 批量与学习率保持不变。 |
| `sampling.use_ode_sampler` | rk45 | rk45 | 仍采用原 ODE 采样方法，没有改成一两步蒸馏。 |

旧版配置文件的 `snapshot_freq` 原始默认值为 20000；此前运行通过命令行覆盖为 5000。本次将配置文件默认值和运行命令统一为 1000，避免遗漏覆盖参数。

### 保存与恢复机制

- 新实验保存 `checkpoint_0.pth` 与 `samples/iter_0/`。这里的“第 0 步”指第二阶段尚未更新、已载入第一阶段模型的状态，不是随机初始化网络，也不是初始高斯噪声图片。
- 之后的 `checkpoint_1.pth`、`checkpoint_2.pth` 分别对应完成 1000、2000 次更新；后续依此类推。本次修正了旧循环中保存标签与实际更新次数差一位的问题。
- checkpoint 包含模型、EMA、优化器与已完成更新次数；最新断点保存到 `checkpoints-meta/checkpoint.pth`。采样前先保存 checkpoint，并在终端打印 `[CHECKPOINT]`、`[SAMPLING]`、`[SAMPLES]`，方便区分保存完成与正在积分采样。
- 采样中断时先恢复训练模型参数，再保存最新断点，避免误将临时 EMA 参数当成训练权重。训练退出时刷新 TensorBoard 日志。
- 使用同一输出目录再次运行会继续断点，不会自动补出先前未保存的历史节点。旧断点没有完整随机数状态，恢复训练不保证逐位复现原随机轨迹。

### 本次实验与耗时

为重新获取 1000、2000 步的真实历史节点，本次将旧 `workdir_2reflow` 目录移入同级 `workdir_2reflow_before_1000_时间戳` 留档，再用干净的 `workdir_2reflow` 从第二阶段第 0 步开始。第一阶段的模型、采样图、loss 日志全部保留。新旧实验的记录应分别展示。

本次留档目录为 `ImageGeneration/workdir_2reflow_before_1000_20261018_134119`，包含旧实验第 2841 步的中断断点及原 TensorBoard 记录。教师模型固定使用第一阶段最终历史文件 `workdir_1rf/checkpoints/checkpoint_20.pth`，避免引用后续可能被覆盖的最新断点。该文件对应旧日志标签 100000 步，内部计数为 100001，属于原第一阶段循环从 0 开始且包含终点的计数差异；本次没有修改或重写第一阶段文件。

按此前约 2.8 秒/步估算，1000 步约需 47 分钟；实际间隔还包含验证、写盘和采样时间。缩短输出周期不改变每步训练计算量，增加的写盘与采样次数会使总耗时略增，不能理解为整体训练提速。

全程将保留第 0 步和 50 个千步节点。后期每个完整 checkpoint 约 1 GB，历史 checkpoint 加最新断点预计占用约 50 GB，另有采样图和日志。第 0 步因优化器尚无完整状态，文件可能更小。

本地后台运行日志为 `workdir_2reflow/training.log`，进程号记录在 `workdir_2reflow/training.pid`；查看日志可使用：

```bash
tail -f "/mnt/d/Learning/Paper/GLM/Reflow/RectifiedFlow/ImageGeneration/workdir_2reflow/training.log"
```

本次已通过 3 项 CPU 回归测试：初始模型与图片保存、千步历史模型与最新断点保存、采样中断后的训练参数恢复。2026-10-18 13:42（北京时间）已启动新训练，并确认第 0 步 checkpoint、`sample.png` 与 `sample.np` 均已生成，随后进入实际训练更新。
