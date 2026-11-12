# 本轮科学设置

2026-11-11 按用户要求清除上一轮结果，从零执行论文协议。

HDPS 使用独立的 paper_hdps.py：Eq8 正确噪声与 tau；Eq9 平方 L2；完整 50 步与从 .8 到 0 的时间格；Eq6 lambda2；Eq11/12 噪声混合。共用原始 SD3 VAE，替换上一轮 Tiny VAE。未报告的步长和离散化选择列于 config.json。

FlowDPS 依 B.2 使用 3 次 DC；FLAIR 每步执行 15 次 DC。所有方法使用固定输出范围映射。指标同时保留作者口径和标准 LPIPS。

恢复、监控与路径适配不改变数学更新；原作者 sd3_sampler.py、solve.py 未编辑。
