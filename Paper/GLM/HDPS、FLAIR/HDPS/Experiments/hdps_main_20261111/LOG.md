# 运行记录

2026-11-11：收到用户明确指令，以论文原文重启并删除前一轮结果。重新读取 Eq6–12、Sec5.1、Appendix B、Table1。

本轮使用 paper_equations_v1，旧结果/断点/日志删除后从零开始。实时状态、完成数和失败原因以远程 status.json、logs/console.log 和 logs/monitor.log 为准。

02:04 核验：运行至首图第 16/50 外循环，断点 next_step=15，GPU2 显存约 21GB。论文公式/恢复相关 5 项测试通过。监控 app 78 项 TypeScript 测试通过；只读探针 38 项测试通过（3 项依赖 Linux 的检查跳过），GPU 探针 19 项通过。已有一个旧的 T1/mock 边界测试因 mock 源码中出现 wsl 字符串失败，属于本轮修改范围外；未改写该测试或 mock。

02:17—02:26：逐项核对最新作者提交1105b54，本地54份非缓存文件全部Git blob一致。偏离版本保存FLAIR step6断点暂停，保留已完成HDPS与FlowDPS两个样本。独立tmux hdps_public_audit_gpu2运行作者HDPS两次，19.6341/19.0729秒、801次解码，输出哈希一致；四种VAE/精度微基准完成。报告位于相邻hdps_public_audit_20261111目录。
