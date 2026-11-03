# Flow Matching (OT-CFM) CIFAR-10 训练参数与配置说明文档

本文档记录了在实验室 8×RTX 4090 共享集群环境下，针对 **Flow Matching for Generative Modeling (Lipman et al., ICLR 2023)** 中 **OT-CFM (Optimal Transport Conditional Flow Matching)** 算法的训练参数调整方案与实操运行指南。

---

## 一、 实验基本信息

* **算法类型**：OT-CFM（最优传输条件流匹配，Exact Optimal Transport Conditional Flow Matcher）
* **数据集**：CIFAR-10（32×32×3，无条件图像生成）
* **基础代码库**：`torchcfm`（基于 `examples/images/cifar10/train_cifar10_ddp.py`）
* **硬件环境**：2 × NVIDIA GeForce RTX 4090（24GB 显存，指定物理卡号 **GPU 0** 与 **GPU 3**）
* **分布式框架**：PyTorch DistributedDataParallel (DDP)

---

## 二、 参数调整对照表与设计考量

| 参数名称         | 命令行参数           |  脚本默认值   |  4090 双卡调整值  | 调参原因与设计考量                                                                                            |
| :----------- | :-------------- | :------: | :----------: | :--------------------------------------------------------------------------------------------------- |
| **模型结构**     | `--model`       | `otcfm`  | **`otcfm`**  | **保持最优配置**。OT-CFM 通过构造线性插值速度场使样本轨迹尽量接近直线，在所有变体中收敛最快、采样 NFE 最低。                                       |
| **并行模式**     | `--parallel`    | `False`  |  **`True`**  | 启用 PyTorch DDP 多卡分布式训练模式，配合双卡算力。                                                                     |
| **总批次大小**    | `--batch_size`  |  `128`   |  **`128`**   | DDP 模式下总批次 128 会平分给 2 张显卡（**单卡 batch_size = 64**）。每张卡显存仅占用约 6~7 GB，留足安全冗余，杜绝 OOM。                    |
| **总迭代步数**    | `--total_steps` | `400001` | **`100000`** | 默认 40 万步针对完整论文复现（单卡需跑一整天）；在双卡 4090 上训练 **10 万步**（处理 1280 万张图片次）时，模型已高度收敛，足够支撑汇报与效果展示。                |
| **保存/采样步频**  | `--save_step`   | `20000`  |  **`5000`**  | **核心调优项**。默认 2 万步间隔过长（约需等 2 小时才存一次）。改成每 5000 步（双卡下约 35~40 分钟）自动生成 64 张采样网格图并存 Checkpoint，便于随时监控收敛质量。 |
| **基础学习率**    | `--lr`          |  `2e-4`  |  **`2e-4`**  | 配合 Adam 优化器，保持平稳收敛。                                                                                  |
| **学习率预热步数**  | `--warmup`      |  `5000`  |  **`5000`**  | 线性预热 5000 步，避免训练初期速度场梯度剧烈震荡。                                                                         |
| **梯度裁剪**     | `--grad_clip`   |  `1.0`   |  **`1.0`**   | 防止梯度爆炸，提高数值积分稳定性。                                                                                    |
| **EMA 衰减系数** | `--ema_decay`   | `0.9999` | **`0.9999`** | 指数移动平均（EMA）权重。用于最终高质量图像生成（EMA 采样的图片质量显著高于普通权重）。                                                      |
| **通信端口**     | `--master_port` | `12355`  | **`29505`**  | **服务器防冲突项**。默认 12355 端口常被实验室其他人占用，指定 29505 保证 DDP 通信正常建立。                                            |
| **数据加载线程**   | `--num_workers` |   `4`    |   **`4`**    | 双卡总计 8 个数据加载进程，能够充分利用 CPU，确保 GPU 计算无等待停滞。                                                            |

---

## 三、 启动命令速查

### 1. 双卡 DDP 加速模式（推荐，用时约 1.2 小时）
```bash
# 激活环境并进入目录
conda activate flow_matching
cd /data2/cy/xzn/Code/Flow_Matching/torchcfm/examples/images/cifar10

# 绑定 GPU 0 与 GPU 3，启动双卡并行
CUDA_VISIBLE_DEVICES=0,3 torchrun --nproc_per_node=2 train_cifar10_ddp.py \
  --model otcfm \
  --parallel=True \
  --batch_size 128 \
  --save_step 5000 \
  --total_steps 100000 \
  --master_port 29505 \
  --output_dir ./results/ > train.log 2>&1 &
```

### 2. 单卡降级备用模式（若临时只有一张卡可用，用时约 2.5 小时）
```bash
# 绑定单张空闲卡（如 GPU 0）
CUDA_VISIBLE_DEVICES=0 python train_cifar10.py \
  --model otcfm \
  --batch_size 128 \
  --save_step 5000 \
  --total_steps 100000 \
  --output_dir ./results/ > train.log 2>&1 &
```

---

## 四、 训练过程监控与预期产物

### 1. 监控指标变化规律
* **初始阶段 (0 ~ 1,000 步)**：`loss` 迅速从初始值 ~0.8 下降至 0.2 左右。
* **中期平稳阶段 (5,000 ~ 50,000 步)**：`loss` 缓慢且稳定下降至 0.08 ~ 0.12 区间，此时生成的采样图轮廓已清晰可辨。
* **收敛阶段 (50,000 ~ 100,000 步)**：`loss` 维持在 0.04 ~ 0.06，生成图像纹理细节丰富。

### 2. 输出文件分布（保存在 `./results/otcfm/`）
* **采样预览图片**：
  * `otcfm_cifar10_step_{step}_normal.png`：普通权重生成的 8×8 采样预览图。
  * `otcfm_cifar10_step_{step}_ema.png`：**重点查看此图**，EMA 权重生成的高质量效果图。
* **模型权重文件**：
  * `otcfm_cifar10_weights_step_{step}.pt`：包含网络权重、优化器状态及训练步数，可直接用于下游评估或继续微调。

---

## 五、 常用运维命令

```bash
# 查看训练实时日志
tail -f train.log

# 检查双卡占用状态与算力利用率
watch -n 1 nvidia-smi

# 杀死进程（若需紧急停止训练）
pkill -f train_cifar10_ddp.py
```
