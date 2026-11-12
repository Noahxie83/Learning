# 与论文的对应关系

本轮以所附 PDF 为协议依据，执行 Table 1 中 HDPS / FlowDPS / FLAIR 的 135 个指标目标。HDPS 数学步骤单独实现，原始第三方源码保留。

| 项目 | 本轮设置与依据 |
|---|---|
| 图像、退化、噪声与提示词 | Sec. 5.1、Appendix B；成对输入 |
| HDPS | Eq. (6)–(12)，Nx=20、Nz=15、50 外循环、t0=.8 |
| 模型 | SD3 Medium 完整原始 VAE；公开 sampler 用 Tiny VAE，此处依论文 backbone 描述采用完整模型 |
| FlowDPS / FLAIR | B.2 预算；公开 baseline 算法与正则权重 |
| CFG | HDPS 字面 Eq.6 lambda2→通常 scale3；基线 B.2 通常 scale2。论文记号与公开实现存在歧义 |
| 缺省步长 | 原文未给；eta_x 取公开代码值，eta_z=.01+平方目标回溯，统一固定 |
| 数据与预处理 | 指定数量；FFHQ/AFHQ 精确 ID 未发表；AFHQ 猫狗组成由提示词推断。预处理沿公开 Resize+CenterCrop |
| 算子 | 沿公开离散化；HDPS 像素梯度用真实前向的 autograd 伴随。高斯 SVD 截断、运动边界与 A†实现未在论文详列 |
| 输出与 LPIPS | 固定物理范围映射；双 LPIPS 口径。论文未报告 resize/归一化，公开 eval.py 采用 VGG224 [0,1] |

这些未报告细节会影响数值对齐，固定后与论文表值比较。没有按测试指标调整协议。单个样本结果用于确认运行；45 组完整均值用于评估复现程度。
