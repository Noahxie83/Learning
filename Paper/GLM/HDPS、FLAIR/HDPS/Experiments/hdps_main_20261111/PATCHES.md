# 实现说明

第三方 Code 目录保持原样；prepare_runtime.py 从原 sampler 生成运行副本。

- 完整 SD3 VAE，float32 解码与求导；冻结权重。encoder 使用 mode，潜变量 float32。
- HDPS 方法由 paper_hdps.py 实现；基线 DC 参数按 Appendix B.2。
- 三种方法保存外循环断点；保留 RNG 和 FLAIR SGD 状态。
- driver 保存固定范围 PNG、双 LPIPS、严格逐文件配对与指标汇总。
- monitor_bridge.py 提供专用日志和带 PID/startTicks/boot ID 的状态文件；当前步与实际外循环对应。

数学与公开代码差异详见 COMPARABILITY_REPORT.md。monitoring app 的只读 probe 补充身份字段白名单，以便其已有基线校验逻辑接收状态文件。
