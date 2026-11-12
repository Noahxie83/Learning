# 比较协议

当前以作者公开实现为基线，逐组对照论文Table1。其与论文文字的差异保留：FlowDPS源码16次DC（论文B.2写3次）；HDPS的任务特定Nx和SR提前停止、像素梯度尺度及潜空间norm目标，均按发布代码运行。完整差异见相邻hdps_public_audit_20261111/AUDIT_REPORT.md。

768²短边Resize+CenterCrop；固定提示词/DAPE文本；sigma_n=.03；CFG=2；命令NFE=50。HDPS SR保留源码43次完成的校正循环并返回。原始保存normalize=True同时用于重建图和参考图；RGB PSNR、pytorch_msssim SSIM、VGG224/[0,1] LPIPS按作者口径汇总。另列标准VGG768/[-1,1] LPIPS，列名与作者口径分开。

三方法共用同一dataset/task退化对象。为独立恢复与成对观测，退化对象及图像噪声采用稳定派生种子，区别于官方solve.py从全局seed42顺序消费的随机流；每幅输入、提示词、种子与输出SHA均记录。作者未公布FFHQ/AFHQ精确子集编号，沿用已核验的1000张集合；AFHQ为验证集猫狗各500，DIV2K为训练集800。

后续以45个完整分组均值比较135项目标；单图19秒测速仅证明作者算法的运行量级。当前无卡，本入口尚未进行新的GPU采样。
