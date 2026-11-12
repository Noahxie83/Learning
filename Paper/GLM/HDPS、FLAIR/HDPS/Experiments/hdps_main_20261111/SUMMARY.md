# HDPS 实验（已暂停核对）

当前状态：已保存断点并暂停。公开仓库核对与小样本测速已完成，详见 ../hdps_public_audit_20261111/AUDIT_REPORT.md。

此前按用户要求重新开始。上一轮混合配置的结果、断点和运行日志已删除；这轮从零运行 HDPS、FlowDPS、FLAIR 的 Table 1 主实验。

目标为 3 个数据集 × 5 个任务 × 3 种方法，共 42,000 次重建、45 组均值、135 项论文指标。HDPS 依 Eq. (6)–(12) 实现；全部方法共用 SD3 Medium 原始 VAE、数据和成对观测。运行状态以远程 status.json 为准。

论文未报告 eta_x、eta_z、精确子集编号及完整指标实现。已将所选常数与约定固定在 config.json，详见 COMPARABILITY_REPORT.md。结果和论文目标逐组对照，完成运行后再判断数值复现程度。

实际启动核验：GPU2 / tmux `hdps_main_gpu2`，PID 1457344。第 15 步断点已验证，潜变量 float32，形状 [1,16,96,96]，Python/NumPy/Torch/CUDA RNG 齐全。监控器已确认 running、累计进度、本轮进度及当前 Step。完整样本尚在计算中。

2026-11-11 公开代码核对：这轮 paper_equations_v1 增加了完整 VAE FP32、Armijo 回溯及其他更新差异，偏离作者基线，暂停用于诊断。首张 HDPS 采样 1125.80 秒；同图同 GPU 的作者算法两次为 19.63/19.07 秒。当前保留 2 个完成结果，以及 FLAIR 首图第 6 步断点，不作为主实验表值复现结论。
