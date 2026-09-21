# 每周最有用的 GitHub AI/CS 项目 Top 3

> 唯一周度记录文件。每周追加一个自然周区块，不覆盖历史内容，不为周榜创建其他文件。

## 2026-W37（2026-09-07 至 2026-09-13）

本周基于 9 月 9 日至 11 日的新增推荐，结合当前学习阶段、可运行性、学习价值和后续路线，选出以下 3 个项目。

### 1. [Hugging Face smol-course](https://github.com/huggingface/smol-course)

- 选择理由：低硬件门槛，能把 PyTorch 基础直接连接到指令微调、评测和 DPO。
- 适合学习：SFT、数据集、chat template、模型评测、偏好对齐。
- 个人评分：88/100；分类：A — Learn Now；适配度：★★★★★
- 建议动作：完成 instruction tuning 单元，并用一个小型自定义数据集复现练习。

### 2. [tinygrad](https://github.com/tinygrad/tinygrad)

- 选择理由：适合从已经接触的 micrograd 继续理解张量、自动求导、计算图和算子融合。
- 适合学习：Tensor、反向传播、lazy evaluation、kernel fusion、硬件后端。
- 个人评分：86/100；分类：A/B — Learn Now → Stretch；适配度：★★★★★
- 建议动作：阅读 `Tensor`、`UOp` 和一个 reduction 算子，尝试添加简单算子。

### 3. [Mamba Minimal](https://github.com/johnma2006/mamba-minimal)

- 选择理由：用单文件 PyTorch 实现 Mamba，代码短且能帮助理解 Transformer 之外的序列建模路线。
- 适合学习：状态空间模型、Selective State Space、线性时间序列建模。
- 个人评分：87/100；分类：A/B — Learn Now → Stretch；适配度：★★★★★
- 建议动作：阅读 `model.py`，比较 Mamba 与 self-attention 的计算复杂度和状态更新方式。

### 本周建议顺序

`smol-course → tinygrad → mamba-minimal`
## 2026-W38（2026-09-14 至 2026-09-20）

本周按个人适配度、学习价值、仓库质量、活跃度和可运行性综合排序，选出 3 个项目。整体路线是：先学会可靠评测与数据准备，再进入 LLM 推理系统底层。

### 1. [OpenCompass](https://github.com/open-compass/opencompass)

- **检索时约 star 数**：约 7.5k；仓库约 1,230 次提交、290 个 issue、115 个 PR，近期仍有 PR 活动；README 记录了 2026-08-25 的 VLMEvalKit 集成更新。
- **核心功能**：面向大语言模型与多模态模型的开放、可复现评测平台，支持多种模型接口、数据集、零样本/少样本/CoT 评测、分布式运行和结果管理。
- **适合学习的知识点**：评测指标与数据集设计、批量推理、实验配置、可复现实验、模型接口抽象、结果汇总与误差分析。
- **为什么对我有用**：它把“跑模型”连接到论文研究中的“公平比较、实验复现和结果解释”，适合建立以后做论文复现和科研实验的工作流。
- **下一步**：先阅读 README 和 `configs/`，用一个 Hugging Face 模型跑通最小评测，再追踪一个 dataset evaluator 的调用链。
- **限制/难点**：完整评测会消耗较多 GPU、磁盘和下载时间；不同模型与数据集的环境依赖较多，不能把一次跑通简单等同于评测结论可靠。
- **分类与评分**：B — Stretch；个人评分 **87/100**；适配度 **★★★★★**。

### 2. [NVIDIA NeMo Curator](https://github.com/NVIDIA-NeMo/Curator)

- **检索时约 star 数**：约 1.8k；项目近期仍在更新并接受贡献，定位清晰，README 提供了数据处理和运行入口。
- **核心功能**：面向 LLM 训练数据的数据整理工具，覆盖数据下载/读取、清洗、去重、语义去重、质量过滤和 GPU 加速的数据准备流程。
- **适合学习的知识点**：训练数据管线、数据质量、MinHash/语义去重、批处理与并行计算、数据规模对模型训练的影响。
- **为什么对我有用**：高质量数据是大模型训练的基础；这个项目能补上从 PyTorch/模型代码走向“数据—训练—评测”完整链路时最容易忽略的数据工程部分。
- **下一步**：先用小规模文本数据跑通清洗和去重示例，记录输入样本数、过滤原因、输出规模和耗时，再阅读一个 stage 的实现。
- **限制/难点**：大规模场景更依赖 GPU、存储和分布式环境；部分优化对初学者不够直观，建议先用 CPU/小数据理解流程。
- **分类与评分**：B — Stretch；个人评分 **81/100**；适配度 **★★★★☆**。

### 3. [FlashInfer](https://github.com/flashinfer-ai/flashinfer)

- **检索时约 star 数**：约 6.5k；仓库约 3,157 次提交、328 个 issue、621 个 PR，页面显示 2026-09-19 仍有更新。
- **核心功能**：面向 LLM serving 的高性能 kernel library，提供 CUDA/C++/Python 实现，重点优化 attention、prefill/decode、分页 KV cache 和量化等推理路径。
- **适合学习的知识点**：GPU kernel、CUDA 内存与并行、attention 推理、KV cache、量化、算子融合、Python 与 C++/CUDA 扩展的边界。
- **为什么对我有用**：它把 Transformer 推理中的抽象算子与真实 GPU 性能联系起来，适合作为以后进入 AI 系统、推理优化或大厂基础设施方向的进阶材料。
- **下一步**：先阅读一个 Python API 到 CUDA kernel 的最小调用链，再用官方 benchmark 比较一个 attention 配置，记录显存、吞吐和延迟。
- **限制/难点**：明显偏 Advanced，需要 NVIDIA GPU、CUDA 工具链和一定的 C++/GPU 基础；不适合作为当前阶段的第一本深度学习教材。
- **分类与评分**：C — Advanced；个人评分 **77/100**；适配度 **★★★☆☆**。

### 本周推荐顺序

**OpenCompass → NVIDIA NeMo Curator → FlashInfer**

本周总结：先用 OpenCompass 建立可复现评测习惯，再用 NeMo Curator 补齐训练数据管线，最后把 FlashInfer 作为 CUDA/LLM 推理系统的进阶阅读目标。
