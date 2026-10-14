---
title: GitHub AI/CS 项目周记
date: '2026-10-12'
date_source: 文件修改日期
subject: 学习动态
note_type: 周记
tags:
- 领域/学习动态
- 类型/周记
cssclasses:
- learning-note
- subject-weekly
- learning-study
---

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[00 学习导航|学习导航]]
> 相关：[[ai-research-weekly|AI 研究与论文阅读周报]]

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
## 2026-W39（2026-09-21 至 2026-09-27）

本周按个人适配度、学习价值、仓库质量、热度、活跃度和成长性综合排序。选择覆盖循序渐进的 LLM 教程、现代 Transformer 训练实现，以及近期快速增长的轻量决策模型训练案例。

### 1. [Modern LLM Notebook](https://github.com/walkinglabs/modern-llm-notebook)

- **检索时约 star 数**：约 218；仓库活跃、未归档。最近一次提交为 2026-09-14；README 记载 2026-08 对推理部分 7 个 notebook 的重写，包括量化、推测解码、推理系统和评测。
- **核心功能**：中英双语、从零实现的 PyTorch LLM 学习课程，含 26 个英文 notebook，中文课程有 30 多个 notebook；沿 tokenizer、Transformer、训练、微调/对齐、推理、评测和部署逐步展开。
- **适合学习的知识点**：BPE、注意力和 Transformer 前向流程、训练损失、RoPE/RMSNorm/SwiGLU/MoE、LoRA/DPO、KV Cache、推测解码、基准测试。
- **为什么对我有用**：课程把直觉、小算例、实现和实验放在一起，能从 Python/NumPy/PyTorch 基础自然衔接到读论文和理解生产系统，且大部分 notebook 可在 CPU 上运行。
- **下一步**：从中文课程的 tokenizer notebook 开始，依次完成自注意力和 Mini-GPT；每节记下张量形状、关键公式和实验观察，再进入训练与推理部分。
- **限制/难点**：大型训练实验仍需要较多内存或 GPU；许可证为 CC BY-NC-SA 4.0，要求注明来源、非商业使用并采用相同许可。最近提交距本周开始约一周多，建议先确认课程内容和 notebook 环境仍匹配当前依赖。
- **分类与评分**：A — Learn Now；个人评分 **90/100**；适配度 **★★★★★**。

### 2. [LLM from Scratch（fangpin）](https://github.com/fangpin/llm-from-scratch)

- **检索时约 star 数**：约 131；MIT 许可，约 53 次提交、14 个 fork、2 个开放 issue；最近一次提交在 2026-09-25，本周仍有代码更新。
- **核心功能**：用 PyTorch 从头实现 decoder-only Transformer、BPE tokenizer、数据清洗与去重，并扩展到 Triton Flash Attention、DDP/分片优化器、SFT 和 GRPO 微调；提供中文 README、文档、benchmark 和测试。
- **适合学习的知识点**：Transformer 组件拆解、BPE、训练循环、梯度与优化器、数据准备、Flash Attention、分布式训练、微调和性能测量。
- **为什么对我有用**：中文材料降低入门成本，同时代码从基础模型延伸到训练系统，适合作为课程学习后的源码练习和科研/工程方向预备。
- **下一步**：先按 README_cn 跑 tokenizer 和小模型训练，阅读 `llm/transformer.py` 并用测试对照实现；掌握单卡流程后再看 `parallel/` 和 `kernel/`。
- **限制/难点**：分布式、Triton 和 Qwen 数学微调部分需要 CUDA/GPU 及更强的工程基础；仓库规模和社区仍小，benchmark 与效果应视作项目自测，不等同于独立复现或大规模验证。
- **分类与评分**：B — Stretch；个人评分 **86/100**；适配度 **★★★★☆**。

### 3. [Kev](https://github.com/jaredpalmer/kev)

- **检索时约 star 数**：约 7.3k；仓库创建于 2026-09-17，截至检索约 296 次提交、440 个 fork；最近更新于 2026-09-27，属于本周快速上升的新项目。
- **核心功能**：基于 Qwen 的小型判定模型，可对一段文本并行完成是/否、多选和评分任务；提供 LoRA 微调、校准概率、benchmark 和本地服务代码。仓库采用 Apache-2.0 许可。
- **适合学习的知识点**：预训练模型适配、LoRA、分类式输出头、交叉熵、数据集切分、温度校准、准确率与 Brier score、训练和评测的防泄漏做法。
- **为什么对我有用**：它展示了大模型不只用于自由文本生成，也能变成可评测的小型专用模型；训练记录和测试有助于学习如何用数据验证一项模型改进。
- **下一步**：先读 README 中的模型结构、训练和 benchmark 部分，复现一个小规模微调及留出集评测；重点检查训练集与测试集的来源差异、概率校准和失败案例。
- **限制/难点**：它是面向特定判定任务的近期实验项目，不代表通用 LLM 能力；本机环境要求 Python 3.12 或 3.13（如使用 Python 3.14，需另建兼容环境），较大模型需要 GPU，README 中的效果数据是项目作者报告且与 Jev 的比较并非完全受控。
- **分类与评分**：B — Stretch；个人评分 **83/100**；适配度 **★★★★☆**。

### 本周推荐顺序

**Modern LLM Notebook → LLM from Scratch（fangpin） → Kev**

本周总结：先通过双语 notebook 建好现代 LLM 的概念地图，再从源码练习训练与分布式组件，最后借 Kev 观察如何把微调、概率校准和严谨评测用于一个具体模型任务。

## 2026-W41（2026-10-05 至 2026-10-11）

检索日期：2026-10-05（Asia/Shanghai）。这是本周周初的新推荐快照，不代表整周趋势；本周仅记录一次。本次三个项目均未出现在已有周度记录中。

归档依据：只读查阅了与 `Noahxie83/Learning` 远程地址一致的本地 `D:\Learning`，包括根 README、AI learning/README.md、Practice/README.md、Paper/README.md、MLP 个人代码与 Transformer 笔记。近期相关记录为 [9 月 30 日 Transformer 笔记提交](https://github.com/Noahxie83/Learning/commit/2c986c6) 和 [10 月 4 日 D2L Notebook 运行记录](https://github.com/Noahxie83/Learning/commit/3880f05)；后者涉及 AlexNet、BatchNorm、ResNet 等教材 Notebook，不据此认定已独立实现或完成复现。当前能力仍按你明确确认的“能独立用 PyTorch 训练模型，正在学习 Transformer / LLM”判断，不按旧 README 降回入门阶段，也不把论文笔记等同于掌握。

本周按当前适配度、原理学习价值、代码/测试质量、维护情况和最小实验资源要求综合排序。评分是个人学习优先级判断，并非仓库客观排行榜；以下实验均为建议，未安装依赖、下载权重或在你的设备上实际运行。

### 1. [LLMs-from-scratch — 从注意力实现到小型 GPT](https://github.com/rasbt/LLMs-from-scratch)

- **分类与评分**：A — Learn Now；95/100；★★★★★（5/5）。与你的 Transformer 阅读目标直接衔接，逐步展开的实现和低资源组件练习最适合现在动手；不需要重新通读整套 Python/PyTorch 入门材料。
- **检索时约 star 数**：106.0k，检索于 2026-10-05。[仓库数据](https://api.github.com/repos/rasbt/LLMs-from-scratch)
- **维护证据**：默认分支最近提交为 2026-10-02（UTC）的 [cdbd33e：修正拼写](https://github.com/rasbt/LLMs-from-scratch/commit/cdbd33e6d57a71e20ea31434841095fac50cecd8)；10 月 1 日还有 Chainlit 上下文裁剪修复。证明仍在维护，但不将文档修正包装成新的模型算法。
- **核心功能与知识点**：用 PyTorch 逐步构建注意力、GPT、预训练与微调流程。本周只聚焦 Q/K/V 投影、缩放点积、多头拆分/拼接、因果掩码以及 Transformer block 的残差和归一化。[章节导航](https://github.com/rasbt/LLMs-from-scratch#readme)
- **与你的归档衔接**：[Transformer 笔记](Paper/Attention%20Is%20All%20You%20Need/Transformer.md) 已涉及注意力与掩码；[MLP 个人练习](AI%20learning/D2L-李沐/Practice/MLP.py) 已有手写参数和矩阵运算。这次把“公式和说明”转成你自己的可检查张量运算，而不是再次收集教程。
- **前置与缺口**：需要熟悉 `view/transpose`、广播、Softmax 的维度和自动求导；尚未确认你能独立写出多头注意力，因此从这一块验证，而非直接假定已掌握完整 GPT。
- **已核实入口**：[第 3 章 Notebook](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch03/01_main-chapter-code/ch03.ipynb) → [gpt.py 中的 MultiHeadAttention](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/01_main-chapter-code/gpt.py)。先实现注意力，暂不加载预训练模型。
- **最小练习与验收**：自行实现两头因果自注意力，输入取 `[B,T,D]=[2,6,8]`，写清 `[2,2,6,4]` 的 Q/K/V 与 `[2,2,6,6]` 的分数矩阵。固定随机种子，关闭 dropout，与仓库模块使用完全相同的权重；输出最大绝对误差目标小于 `1e-5`（CPU、float32 小输入）。再只改变第 6 个 token，前 5 个位置输出应不变；检查未来位置的注意力权重为零，并说明为什么。交付一份自己的实现及这两项测试结果，才算完成，而非仅运行原 Notebook。
- **资源、限制与难点**：该组件实验只需 CPU 和小张量；完整 GPT 训练不是同等成本。仓库主线依赖列出 PyTorch ≥2.2.2（Intel macOS 另有上限），但不是对任意 Python/CUDA 组合的兼容承诺。[依赖声明](https://github.com/rasbt/LLMs-from-scratch/blob/main/requirements.txt) 注意正确比较投影权重与输出投影，避免把随机初始化差异误判为公式错误；CPU 小实验的实际耗时未测。

### 2. [CS336 Assignment 1 — 用测试驱动的现代语言模型独立实现](https://github.com/stanford-cs336/assignment1-basics)

- **分类与评分**：B — Stretch；89/100；★★★★★（5/5）。官方作业的接口契约、测试和参考快照适合检验“能否自己写出来”；低频维护和较严格的环境要求扣分。建议只选模块练习，不把整门课程当作新的前置门槛。
- **检索时约 star 数**：2.9k，检索于 2026-10-05。[仓库数据](https://api.github.com/repos/stanford-cs336/assignment1-basics)
- **维护证据**：默认分支最新提交为 2026-04-07（UTC）的 [a158843：调整排行榜时间限制](https://github.com/stanford-cs336/assignment1-basics/commit/a158843b20107949f1a8d7df1b05cd33b9166712)，距检索约半年，不能称为近期高活跃。仍保留推荐是因为其明确的作业接口、模型测试和依赖锁定有学习价值，而不是因为页面近期被抓取；安装兼容性尚未实测。
- **核心功能与知识点**：围绕 tokenizer、Transformer 语言模型、优化器和训练工具组织独立实现任务。特别适合从原始 Transformer 过渡到 RMSNorm、RoPE、SwiGLU 与稳定训练。[作业说明与目录](https://github.com/stanford-cs336/assignment1-basics#readme)
- **与你的归档衔接**：接在 [Transformer 笔记](Paper/Attention%20Is%20All%20You%20Need/Transformer.md) 的位置编码/归一化之后，用现代组件练习检验理解；也延续 [MLP 个人练习](AI%20learning/D2L-李沐/Practice/MLP.py) 的手写思路。近期教材 BatchNorm 运行记录可作为比较归一化轴的线索，但不据此认定你已掌握 LayerNorm/RMSNorm。
- **前置与缺口**：补两点即可开始：RMSNorm 的均方根缩放与 LayerNorm 去均值的区别；RoPE 的二维旋转与位置索引。会读 pytest 断言和张量形状即可做模块子集，不必先掌握分布式训练。
- **已核实入口**：[tests/adapters.py](https://github.com/stanford-cs336/assignment1-basics/blob/main/tests/adapters.py) 的 `run_rmsnorm`、`run_rope` 接口，以及 [tests/test_model.py](https://github.com/stanford-cs336/assignment1-basics/blob/main/tests/test_model.py) 的对应测试。它是需要你补实现的作业骨架，不是开箱即有完整答案的训练项目；初始 `NotImplementedError` 是预期状态。
- **最小练习与验收**：在自己的模块实现 RMSNorm 和 RoPE，再通过 adapter 接入；只运行 `test_rmsnorm` 与 `test_rope` 两个测试。通过仓库各自的参考快照比较（源码绝对容差分别为 `1e-4`、`1e-5`）；另外检查 RoPE 旋转前后每个向量的二范数在浮点误差内一致，并解释位置 0 的旋转结果。记录公式、维度、测试命令与实际结果。通过这些测试只说明对应组件符合测试，不能声称完整模型正确或复现了论文。
- **资源、限制与难点**：所选测试使用小张量，可从 CPU 开始；整份作业的训练与排行榜是另一层计算需求，不在本周目标内。[pyproject.toml](https://github.com/stanford-cs336/assignment1-basics/blob/main/pyproject.toml) 明确要求 Python `>=3.12,<3.14`、`torch~=2.11.0`，因此不要直接塞入不匹配的既有环境；将来动手时单独准备匹配环境。尚未验证 Windows/WSL 下的实际安装；完整训练显存与时间取决于配置，这里不估成固定数值。

### 3. [MiniMind — 把现代 LLM 组件接到预训练与 SFT 数据流](https://github.com/jingyaogong/minimind)

- **分类与评分**：B — Stretch；86/100；★★★★☆（4/5）。中文说明、模型与训练源码便于追踪端到端数据流；但功能面较宽，完整训练资源未知，当前优先级低于前两项。只看 dense 模型与预训练/SFT，暂不启动 MoE、强化学习或 Agent 扩展。
- **检索时约 star 数**：63.2k，检索于 2026-10-05。[仓库数据](https://api.github.com/repos/jingyaogong/minimind)
- **维护证据**：默认分支最近提交为 2026-09-22 16:07 UTC（北京时间 9 月 23 日）的 [f659b55：修正剩余训练步的处理顺序](https://github.com/jingyaogong/minimind/commit/f659b55761b754d306bd140573493a6543cafd7f)，同日还有梯度累积末尾 checkpoint 相关合并。这里依据实际提交日期，不使用搜索抓取时间代替活跃度。
- **核心功能与知识点**：提供小语言模型定义、预训练、全量 SFT、LoRA 等流程；当前 README 的 MiniMind-3 dense 路线约 64M 参数，不能沿用旧版本“默认 26M”的说法。[项目说明](https://github.com/jingyaogong/minimind#readme) 本周重点是 next-token 标签位移、SFT 的监督位置、RMSNorm/RoPE/GQA 与训练损失如何接起来，而非追求聊天演示效果。
- **与你的归档衔接**：把 [Softmax 个人练习](AI%20learning/D2L-李沐/Practice/Softmax.py) 的分类交叉熵扩展为序列逐 token 交叉熵；把 [Dropout 练习](AI%20learning/D2L-李沐/Practice/Dropout.py) 中训练/评估模式的区别用于可复核比较；承接 [Transformer 笔记](Paper/Attention%20Is%20All%20You%20Need/Transformer.md) 的因果注意力。它为之后组织一个受控小训练实验提供入口，不等于现阶段必须训练完整模型。
- **前置与缺口**：先理解 causal LM 的输入/标签错位、`ignore_index=-100`、聊天模板边界；再补现代注意力组件。SFT 只在回答目标位置计算损失，不代表提示词不参与注意力或没有梯度传播。
- **已核实入口**：[dataset/lm_dataset.py](https://github.com/jingyaogong/minimind/blob/master/dataset/lm_dataset.py) 的 `SFTDataset.generate_labels` → [model/model_minimind.py](https://github.com/jingyaogong/minimind/blob/master/model/model_minimind.py) 的 `MiniMindForCausalLM.forward` → [trainer/train_full_sft.py](https://github.com/jingyaogong/minimind/blob/master/trainer/train_full_sft.py)。当前源码在模型内对齐 `logits[..., :-1, :]` 和 `labels[..., 1:]`，不要在数据端再重复位移一次。
- **最小练习与验收**：先不用模型权重，以一条固定问答和本地 tokenizer 展示“位置—token—下一个目标—是否参与 loss”，固定随机种子，避免数据预处理随机变化影响对照。随后对同一份随机 logits，分别用手动筛选有效目标的交叉熵、源码式 `ignore_index=-100` 计算 loss，误差目标小于 `1e-6`（CPU、float32 小样本）。仅扰动被忽略目标对应的 logits，loss 应不变；样本须保留至少一个有效回答目标，不能把全被截断的回答误判为测试成功。保存这张对照表及断言结果即可完成本次练习。
- **资源、限制与难点**：标签和损失核对可在 CPU 完成，不需要下载模型权重或全量语料。作者 README 的训练参考涉及 Ubuntu 20.04、Python 3.10.16、CUDA 12.2 和 RTX 3090；这是作者环境，不是最低配置或你的设备实测。“数小时/数元”等宣传受模型、数据、训练阶段和租用价格影响，本记录不作承诺。[requirements.txt](https://github.com/jingyaogong/minimind/blob/master/requirements.txt) 固定了多项依赖，PyTorch 行为注释示例；后续应单独核对兼容性。真正训练时另设训练/验证划分和 checkpoint；小样本过拟合只能验证训练链路，不能当作泛化效果或论文结论复现。

本周推荐顺序：**LLMs-from-scratch → CS336 Assignment 1 → MiniMind**。这是递进候选，不要求本周同时开三个项目。

最优先动手的一项任务：完成第 1 项的双头因果注意力，实现“相同权重下输出对齐”和“改变未来 token 不影响过去输出”两项测试；通过后再选第 2 项的 RMSNorm/RoPE。

本周总结：先让 Transformer 公式变成你亲手写出、能用断言验证的组件，再推进到可检查的小模型训练流程。

## 2026-W42（2026-10-12 至 2026-10-18）

检索日期：2026-10-12（Asia/Shanghai）。本期为周一推荐快照，并非对尚未结束的一周作趋势总结；三个项目均未出现在已有周榜中。本周只需启动一项任务，其余作为后续候选。

归档依据：只读核对了 `D:/Learning` 的远程地址为 `https://github.com/Noahxie83/Learning.git`，抽样查看根 README、`AI learning/README.md`、`AI learning/D2L-李沐/Practice/README.md`、`Paper/README.md`、MLP/Dropout 个人代码和 Transformer 阅读笔记。最新课程进展是 [2026-10-11 的 D2L 完成记录](https://github.com/Noahxie83/Learning/commit/06c65fa)，根 README 更新到 10 月 11 日；[10 月 8 日进度整理](https://github.com/Noahxie83/Learning/commit/6e97dcc) 与 [Transformer 笔记](Paper/Attention%20Is%20All%20You%20Need/Transformer.md) 也作为衔接依据。“已学完 D2L”是归档明确记载的课程状态；个人练习目录仍主要列线性回归、Softmax、MLP、Dropout，尚未看到独立 Transformer 实现或论文复现实验记录。因此继续采用你确认的“能独立用 PyTorch 训练模型，正在学习 Transformer / LLM”，增加机制验证和实验设计的比重，不推断已经掌握整套现代 LLM。

排序综合当前适配度、原理价值、源码与测试质量、维护证据、资源要求和最小实验可行性。分数是个人学习优先级。下述步骤均为建议，本次未安装依赖、下载模型/数据或发起训练；数值容差是建议验收标准，不是本机实测结果。

### 1. [LitGPT — 验证 KV Cache 与现代解码器的数据流](https://github.com/Lightning-AI/litgpt)

- **分类、评分与适配度**：B — Stretch；**91/100；★★★★★（5/5）**。单文件模型和具体缓存测试便于把论文概念落实到张量；与小语言模型训练主线直接相接。需要补缓存位置索引、RoPE/GQA，且完整工程依赖较多，因此从小模型验证开始。
- **检索时约 star 数**：**13.7k**，检索于 2026-10-12，依据 [GitHub 主页](https://github.com/Lightning-AI/litgpt)。本次该仓库 API 遇到限流，采用主页显示的约数。
- **维护活动证据**：只读查询默认分支指向 `18c931c`；GitHub 提交页和提交订阅记录的时间为 **2026-09-09 01:49 UTC**（北京时间 9 月 9 日）。该 [提交](https://github.com/Lightning-AI/litgpt/commit/18c931c15c2398621d35371a12d2b1785e855bb6) 修复 Thunder DDP 重复启动器覆盖；同日另有提示词 token、tokenizer 配置修复。距检索约一个月，不能说本周有新提交，也不把分布式修复当成缓存算法更新。
- **核心功能与知识点**：提供 decoder-only 模型实现、预训练/微调及生成流程。当前优先追踪 Embedding → Transformer block → logits，理解因果掩码、RoPE 位置、GQA 的 K/V 共享，以及 prefill 与逐 token decode 的区别。[源码入口](https://github.com/Lightning-AI/litgpt/blob/18c931c15c2398621d35371a12d2b1785e855bb6/litgpt/model.py)
- **与你的归档衔接**：[Transformer 笔记](Paper/Attention%20Is%20All%20You%20Need/Transformer.md) 已说明掩码、Q/K/V 和生成前缀；本项目把这些解释连接到缓存实现。[Softmax 练习](AI%20learning/D2L-李沐/Practice/Softmax.py) 的分类输出也可延伸到逐 token 预测。它补充上周组件练习之后的推理数据流，不要求重新通读入门教程。
- **前置与缺口**：能跟踪 `[B,T,D]` 与多头维度；补充“缓存保存哪些位置、下一 token 使用什么位置编号”。GQA 的 query 头数与 K/V 组数不同，不能默认三者头数相同。
- **已核实入口**：[Config](https://github.com/Lightning-AI/litgpt/blob/18c931c15c2398621d35371a12d2b1785e855bb6/litgpt/config.py) → `GPT.forward`、`set_kv_cache`、`clear_kv_cache`、`KVCache`；参照 [tests/test_model.py 的 test_kv_cache 与 test_kv_cache_buffer_shape](https://github.com/Lightning-AI/litgpt/blob/18c931c15c2398621d35371a12d2b1785e855bb6/tests/test_model.py)。后续再查看 [pretrain.py 的 fit/validate](https://github.com/Lightning-AI/litgpt/blob/18c931c15c2398621d35371a12d2b1785e855bb6/litgpt/pretrain.py)：训练端将输入与目标错开一个 token，模型 forward 本身返回 logits。
- **最小练习**：仅构造随机初始化的 CPU 模型：`block_size=32, vocab_size=32, padding_multiple=1, n_layer=2, n_head=4, n_embd=32, n_query_groups=2, rotary_percentage=1.0`，不加载预训练权重。固定种子，设 `eval()`，使用 float32 和推理模式。对同一段 8-token 输入，先整段计算 logits；再初始化缓存，以前 4 个 token 做 prefill、之后逐 token 输入并正确传入 `input_pos`。拼接两条路径对应位置的输出；每次新序列前清理并重新创建缓存。
- **完成标准**：两条路径均得到 `[1,8,32]` 的输出，使用建议容差 `atol=1e-5, rtol=1e-4` 比较全部位置；解释每层 K/V 缓存为何是 `[1,2,32,8]`，并记录位置索引和误差。通过表示这组配置的缓存计算与全序列计算相符，不能据此声称所有模型正确或缓存必然加速。
- **资源、限制与难点**：该小张量实验可从 CPU 起步；实际耗时未知。极小 CPU 输入可能因管理开销而没有速度收益。完整预训练、量化、FSDP/Thunder 是其他资源层级。[pyproject.toml](https://github.com/Lightning-AI/litgpt/blob/18c931c15c2398621d35371a12d2b1785e855bb6/pyproject.toml) 声明 Python ≥3.10、PyTorch ≥2.7、Lightning ≥2.6.1；可选编译组件有独立版本/平台约束。未验证你的 Windows 环境兼容性，不能把项目的“大模型训练配方”当作 CPU 训练承诺。

### 2. [PEFT — 用小型 MLP 看清 LoRA 的参数、梯度与合并](https://github.com/huggingface/peft)

- **分类、评分与适配度**：A — Learn Now（限定普通 LoRA 小模块）；**88/100；★★★★☆（4/5）**。可以直接利用已有 MLP 和训练经验，用少量参数验证低秩更新；实现、文档和测试齐全。完整库的适配器种类与框架封装较多，当前只学普通 LoRA，不同时推进 QLoRA、DoRA 或复杂后训练。
- **检索时约 star 数**：**21.8k**，检索于 2026-10-12，依据 [GitHub API](https://api.github.com/repos/huggingface/peft) 返回的 21,781 stars。
- **维护活动证据**：默认分支最近提交为 **2026-10-09 10:21 UTC** 的 [9db0f37](https://github.com/huggingface/peft/commit/9db0f37197c95ee7010fdcff107355d1cefb3f34)，修复 seq2seq prompt generation 方法恢复并补回归测试；同日还有 HRA 前向内存优化。说明近期维护活跃，但这两项并非新的 LoRA 论文结果。
- **核心功能与知识点**：提供参数高效微调方法；普通 LoRA 在线性层增加 `ΔW=(α/r)BA`，冻结基座权重并只学习低秩矩阵。重点学习参数量、初始化、梯度路径、目标模块选择和权重合并，原理对应 [LoRA 论文](https://arxiv.org/abs/2106.09685)。论文中的大模型资源收益是作者特定实验报告，不等于你的小模型实验结果。
- **与你的归档衔接**：[MLP.py](AI%20learning/D2L-李沐/Practice/MLP.py) 已有矩阵乘法和手写参数；可直接把一个 Linear 的完整更新换成低秩增量。[Dropout.py](AI%20learning/D2L-李沐/Practice/Dropout.py) 则衔接确定性比较时的训练/评估模式。完成后才考虑把 LoRA 放到小 Transformer 的注意力投影。
- **前置与缺口**：熟悉 `requires_grad`、优化器参数组与矩阵形状即可开始；补充 rank 的意义和“冻结基座权重仍需要通过该层反向传播”的区别。默认 B 零初始化时，第一步 A 的梯度可以为零，不能要求第一步 A/B 都发生非零更新。
- **已核实入口**：[src/peft/tuners/lora/layer.py](https://github.com/huggingface/peft/blob/9db0f37197c95ee7010fdcff107355d1cefb3f34/src/peft/tuners/lora/layer.py) 的 `Linear.forward`、初始化、`get_delta_weight` 和 `merge`；[tests/test_custom_models.py](https://github.com/huggingface/peft/blob/9db0f37197c95ee7010fdcff107355d1cefb3f34/tests/test_custom_models.py) 含原生 PyTorch MLP、适配器注入和合并测试。
- **最小练习**：采用测试中的 `10→20→2` MLP 结构，去掉 bias，只向第一个 `lin0` 注入普通 LoRA，配置 `r=2, lora_alpha=2, lora_dropout=0, bias="none"`。先按公式手写增量分支，再对照库实现。使用相同基座权重和输入，在 eval 模式核对默认初始化输出；之后用一小批合成样本做一次适配器更新，再比较合并前后的输出。这里是一项模块实验建议，不是对随机基座进行有实际用途的 LLM 微调。
- **完成标准**：第一个层的 A/B 形状为 `[2,10]` / `[20,2]`，仅有 **60** 个可训练参数；未合并前基座权重不随优化器更新。默认初始化输出与基座一致；取得非零增量后，手写与库实现、合并前后输出都在建议 `atol=1e-5, rtol=1e-4` 内相符。保存参数/梯度清单并解释首步 A 梯度；合并会把增量写入基座，此时不再要求合并后的权重等于原权重。
- **资源、限制与难点**：该 MLP 验证只需 CPU，不下载模型权重或数据集。真实 SFT 仍需要基座、分词与标签处理、验证集和显存预算；不能把这个合成实验当成 LoRA 效果复现。[setup.py](https://github.com/huggingface/peft/blob/9db0f37197c95ee7010fdcff107355d1cefb3f34/setup.py) 声明 Python ≥3.10、PyTorch ≥1.13，并依赖 Transformers/Accelerate 等；最低版本声明不保证任意新版组合兼容。普通 LoRA 的 `α/r` 不适用于所有变体，实验需明确关闭额外变体并固定版本。

### 3. [vit-pytorch — 从 CNN 阅读转到图像 token 与位置编码消融](https://github.com/lucidrains/vit-pytorch)

- **分类、评分与适配度**：B — Stretch；**85/100；★★★★☆（4/5）**。基础 ViT 实现集中，能将已有视觉学习与 Transformer 连起来；适合补一个小规模受控实验。它是视觉备选，不需要为了凑三个项目同时偏离 LLM 主线；仓库包含大量变体，应只选基础 ViT。
- **检索时约 star 数**：**25.5k**，检索于 2026-10-12，依据 [GitHub API](https://api.github.com/repos/lucidrains/vit-pytorch) 返回的 25,544 stars。
- **维护活动证据**：默认分支最近提交为 **2026-09-20 17:03 UTC**（北京时间 9 月 21 日）的 [c362297](https://github.com/lucidrains/vit-pytorch/commit/c3622978f68a114b5ae45c4322b54391b24f5c3d)，调整 LeJEPA 的 EMA 选项，并更新包版本到 1.26.7。距本次约三周；这是变体维护，不能说基础 ViT 本周增加了新结果。包元数据当前将项目主页/仓库地址指向 Codeberg，推荐和源码核查以这里的 GitHub 快照为准。
- **核心功能与知识点**：实现图像 patch embedding、可学习位置编码、CLS token、Transformer encoder 和分类头。对应 [ViT 论文](https://arxiv.org/abs/2010.11929) 的图像序列建模方法；该仓库是第三方 PyTorch 实现，不是论文作者的官方训练仓库。
- **与你的归档衔接**：承接 [ResNet 笔记](Paper/Deep%20Residual%20Learning%20for%20Image%20Recognition/ResNet.md)、[Transformer 笔记](Paper/Attention%20Is%20All%20You%20Need/Transformer.md) 和 D2L 的完成记录：比较卷积空间结构与图像 token 的位置表达。已有论文笔记仍只作为阅读依据，不标记你已复现 ResNet 或 ViT。
- **前置与缺口**：补图像分块顺序、`einops.rearrange`、CLS 汇聚及 encoder 双向自注意力。本项目没有语言生成的因果掩码；不能照搬 decoder-only 的 mask。小模型训练需要你自行组织数据划分、优化器、日志和 checkpoint。
- **已核实入口**：[vit_pytorch/vit.py](https://github.com/lucidrains/vit-pytorch/blob/c3622978f68a114b5ae45c4322b54391b24f5c3d/vit_pytorch/vit.py) 的 `ViT.to_patch_embedding`、`pos_embedding`、`Attention` 和 `forward`；[tests/test_vit.py](https://github.com/lucidrains/vit-pytorch/blob/c3622978f68a114b5ae45c4322b54391b24f5c3d/tests/test_vit.py) 主要验证输出形状，不能当作论文效果验证。
- **最小练习**：用灰度 `28×28` 输入、`patch_size=7, channels=1, dim=32, depth=2, heads=4, dim_head=8, mlp_dim=64, num_classes=10, pool="cls"`，关闭 dropout。先画出图像 → 16 个 49 维 patch → 16 个 32 维 token → 加 CLS 后 17 个 token → 分类 logits 的形状。然后在 eval 模式把位置编码置零，按固定排列重排完整 patch 并还原成图像，比较重排前后的 CLS 分类输出。
- **完成标准与后续消融**：输出形状为 `[B,10]`；位置编码置零、其他条件固定时，patch 重排前后 logits 在建议 `atol=1e-5, rtol=1e-4` 内相符，并解释“共享 patch 投影和自注意力的置换关系、CLS 输出不依赖 patch 排列”。若继续做训练，再在 Fashion-MNIST 训练集内部固定训练/验证划分，只比较“保留/去除位置编码”，固定初始化对应项、训练预算、增强、优化器，以至少 3 个种子记录验证准确率均值/标准差，测试集留到最终评估。完成的是这项小数据消融；不预设有位置编码一定更好，也不称为复现论文的大规模结论。
- **资源、限制与难点**：形状与置换验证可在 CPU 进行；训练耗时和显存未测，完整 ViT 预训练资源远高于上述练习。源码包含额外 LayerNorm 等实现选择，做论文对照需逐项记录差异。[pyproject.toml](https://github.com/lucidrains/vit-pytorch/blob/c3622978f68a114b5ae45c4322b54391b24f5c3d/pyproject.toml) 声明 Python ≥3.8、PyTorch ≥2.5、einops ≥0.8.2 和 torchvision；测试额外依赖固定 PyTorch 2.5.0/torchvision 0.20.0，因此不要把安装全部测试依赖当作任意环境的默认方案。Windows 实际安装情况未知。

本周推荐顺序：**LitGPT → PEFT → vit-pytorch**。先验证推理数据流，再理解低秩微调；视觉项目仅作为你选择论文实验方向时的备选。

最优先动手的一项任务：完成 LitGPT 的小随机模型 KV Cache 对照，提交一张维度/位置索引表和逐位置 logits 误差记录。如果上周的因果注意力练习还未完成，先完成该前置，再开始缓存实验。

本周总结：从课程阅读推进到可以复核的机制实验，用输出、梯度和受控消融判断自己的理解是否成立。
