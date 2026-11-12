# 环境与恢复适配

上游sd3_sampler.py、solve.py及脚本保持原样。prepare_runtime.py只生成运行副本：替换模型/正则文件路径，补Tiny VAE的shift_factor=0，冻结预训练VAE，移除三种solver均未使用的PIQ对象，以及加入断点观察钩子。

生成时删除观察钩子并还原正则文件路径后，逐个比较HDPS、FlowDPS、FLAIR完整类AST，必须与上游一致。原始loss、步长、循环次数、CFG、时间格和提前停止均保留。

批处理使用一份模型、文本预编码、逐图原子保存和指标缓存；不修改算法更新。首个HDPS高斯输出额外核对已完成作者基准的PNG哈希，不一致时停止而不继续全量。
