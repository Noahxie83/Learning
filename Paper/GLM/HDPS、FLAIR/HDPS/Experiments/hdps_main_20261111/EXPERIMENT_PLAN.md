# HDPS 主实验设计

研究目标：复现所附 PDF 的 Table 1 中 HDPS、FlowDPS、FLAIR 三行，覆盖五种线性逆问题和三个数据集。

## 数据与共同设置

- FFHQ 1000、AFHQ 验证集猫/狗各 500、DIV2K 训练集 800。先校验数量和逐文件清单。作者未公开 FFHQ/AFHQ 精确子集编号。
- 768×768。沿公开 solve.py 使用短边缩放、中心裁剪；三种方法处理同一幅参考图。
- 高斯模糊：核 61，标准差 3；运动模糊：核 61，强度 0.5；SR：bicubic ×12、avgpool ×12；随机修复：30%–70% 像素缺失。
- 测量加性高斯噪声标准差 0.03；图像使用 [-1,1]。固定种子 42，按数据集、任务、文件生成稳定种子，每种方法使用相同观测和随机退化。
- SD3 Medium 原始 AutoencoderKL；VAE float32、transformer float16、潜变量 float32，冻结模型权重。E 采用后验 mode。DAPE 描述按文件名关联。

## HDPS 原文实现

- Algorithm 1：50 个外循环，从 t0=0.8 均匀反向到 0。
- Eq. (6)：lambda=2，速度为 3 v_cond - 2 v_uncond。
- Eq. (7)(8)：sigma_y=0.03，tau_t²=sigma_t²/(1+sigma_t²)，20 次 Langevin；似然梯度通过真实前向算子自动求导获得其伴随，不以 MotionBlurOperator.At 的占位恒等映射替代。循环内不裁剪像素。
- Eq. (9)：从预测 clean latent 开始，15 次平方 L2（sum）梯度下降；无额外 sigma 因子。eta_z 初值 0.01，以该目标的 Armijo 回溯确保数值下降。
- Eq. (11)：alpha=1-sigma，混合独立高斯端点；最后返回 D(z_hat_0)。z1|t 采用 Eq. (3) 线性路径的 z+(1-sigma)v。
- Eq. (12)：混合噪声与 E(A†y)。有 SVD 伪逆接口时采用其截断伪逆；其他算子按公开适配使用 At 初始化。精确初始化离散化列入差异记录。

## 论文未指定的常数

eta_x 沿已公开代码：SR/高斯 1e-4，运动/随机修复 1e-5；每步固定。eta_z=0.01，最多回溯 12 次。这些设置不读取真值或 PSNR/SSIM/LPIPS，不按测试集分数调参。

## 对照方法

FlowDPS：NFE=50，3 次 DC，步长 15。保留公开算法的时间调度和再噪声。
FLAIR：NFE=50，每步 15 次 DC，SR 步长 12，其他 0.1；公开正则权重。移除公开实现的 DC 提前终止，执行论文 B.2 所列预算。
两者采用 B.2 通常意义的 guidance_scale=2。HDPS 按 Eq. (6) 字面 lambda=2，对应通常 scale=3。此记号歧义在比较报告保留。

## 指标与输出

- 固定 [-1,1]→[0,1] 后裁剪并保存 PNG；不按单张极值重新拉伸。
- RGB PSNR、pytorch_msssim SSIM。LPIPS 同时报作者 eval.py 的 VGG224/[0,1] 口径，以及标准 VGG768/[-1,1] 口径，列名明确分开。
- 按数据集/任务/方法汇总均值、样本数、论文值和差值；分配的样本必须完整，错误立即停止，不静默跳过。
- 记录原图/结果 SHA256、配置与代码指纹、随机种子、耗时、显存、实际外循环数。HDPS 另记录每次对齐的误差下降和接受步长。

## 运行和恢复

GPU2 UUID 固定，tmux hdps_main_gpu2。每 5 个外循环原子保存潜变量、优化器及 Python/NumPy/Torch/CUDA RNG。已完整且哈希一致的结果跳过；恢复时拒绝配置/代码/输入不匹配。后续可停机后按样本分片扩展多卡。

监控器读 logs/monitor.log 和 monitor_status.json。当前 Step 为累计外循环；每行另显示图像数、任务和该图的 step/50。累计计数含初始化 step0，因此总 exclusive index 为 2,100,001；实际采样迭代为 2,100,000。监控语义不改变推理预算。
