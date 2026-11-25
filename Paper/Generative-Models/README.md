<!-- learning-vault-navigation:v1 -->
<details>
<summary>笔记导航</summary>

目录：[论文阅读 · 索引](../README.md)

</details>

# Generative-Models：生成模型论文资料

> **当前主线**：[基于扩散/流模型的逆问题求解（HDPS / FLAIR）](./Inverse-Problems/README.md)

本目录按研究脉络归档生成模型相关论文、精读笔记与实验配置，分为**生成基础（Foundations）**、**扩散/分数与流匹配（Diffusion-and-Flow）**、**逆问题求解（Inverse-Problems）**三个子专题。具体阅读与复现状态以各笔记 YAML 元数据为准；资料归档不等于已读完或已完成复现。

## 一、精读笔记总览（9 篇）

### 生成模型基础（Foundations）

| 论文 | 阅读笔记 | 本地 PDF | 原文来源 | 阅读状态 | 复现状态 |
| --- | --- | --- | --- | --- | --- |
| Generative Adversarial Nets（GAN） | [阅读笔记](./Foundations/GAN/GAN.md) | [PDF](./Foundations/GAN/GAN_1406.2661.pdf) | [arXiv](https://arxiv.org/abs/1406.2661) | 待确认 | 未复现 |

### 扩散、分数与流匹配（Diffusion-and-Flow）

| 论文 | 阅读笔记 | 本地 PDF | 配套资料 | 阅读状态 | 复现状态 |
| --- | --- | --- | --- | --- | --- |
| Denoising Diffusion Probabilistic Models（DDPM） | [阅读笔记](./Diffusion-and-Flow/DDPM/DDPM.md) | [PDF](./Diffusion-and-Flow/DDPM/DDPM_2006.11239.pdf) | — | 待确认 | 未复现 |
| Score-Based Generative Modeling through SDEs（Score-SDE） | [阅读笔记](./Diffusion-and-Flow/Score-SDE/Score-SDE.md) | [PDF](./Diffusion-and-Flow/Score-SDE/Score-SDE_2011.13456.pdf) | [CIFAR-10 训练配置](./Diffusion-and-Flow/Score-SDE/CIFAR10_Score_SDE_Training_Config.md) | 待确认 | 待确认 |
| Flow Matching for Generative Modeling | [阅读笔记](./Diffusion-and-Flow/Flow-Matching/Flow-Matching.md) | [论文 PDF](./Diffusion-and-Flow/Flow-Matching/Flow-Matching_2210.02747.pdf) · [Guide & Code PDF](./Diffusion-and-Flow/Flow-Matching/Flow-Matching-Guide-and-Code_2412.06264.pdf) | [OT-CFM 训练配置](./Diffusion-and-Flow/Flow-Matching/CIFAR10_OTCFM_Training_Config.md) | 已完成（2026-11-03 确认） | 待确认 |
| Flow Straight and Fast with Rectified Flow | [阅读笔记](./Diffusion-and-Flow/Rectified-Flow/Rectified-Flow.md) | [PDF](./Diffusion-and-Flow/Rectified-Flow/Rectified-Flow_2209.03003.pdf) | [Rectified Flow 训练配置](./Diffusion-and-Flow/Rectified-Flow/CIFAR10_Rectified_Flow_Training_Config.md) | 待确认 | 待确认 |

### 基于扩散/流的逆问题求解（Inverse-Problems）

详见子专题入口：[逆问题求解总览](./Inverse-Problems/README.md)。

| 论文 | 阅读笔记 | 本地 PDF | 配套资料 | 阅读状态 | 复现状态 |
| --- | --- | --- | --- | --- | --- |
| Hybrid-Domain Posterior Sampling（HDPS） | [阅读笔记](./Inverse-Problems/HDPS/HDPS.md) | [PDF](./Inverse-Problems/HDPS/HDPS_2608.00537.pdf) | [作者代码库](https://github.com/74587887/HDPS) | 阅读中（当前主线） | 待确认 |
| Solving Inverse Problems with FLAIR | [阅读笔记](./Inverse-Problems/FLAIR/FLAIR.md) | [PDF](./Inverse-Problems/FLAIR/FLAIR_2506.02680.pdf) | — | 阅读中（当前主线） | 未复现 |
| FlowDPS: Flow-Driven Posterior Sampling | [阅读笔记](./Inverse-Problems/FlowDPS/FlowDPS.md) | [PDF](./Inverse-Problems/FlowDPS/FlowDPS_2503.08136.pdf) | — | 待确认 | 未复现 |
| FlowLPS: Langevin-Proximal Sampling | [阅读笔记](./Inverse-Problems/FlowLPS/FlowLPS.md) | [PDF](./Inverse-Problems/FlowLPS/FlowLPS_2512.07150.pdf) | — | 待确认 | 未复现 |

## 二、扩散与流待读/参考 PDF（按子方向分组，共 23 篇）

> 物理文件统一存放于 `Diffusion-and-Flow/PDFs/`；决定精读时按 [Paper/AGENTS.md](../AGENTS.md) 升格为独立短名目录。

### 1. 扩散与 Score 基础理论（6 篇）

| 论文 | 本地 PDF |
| --- | --- |
| Deep Unsupervised Learning using Nonequilibrium Thermodynamics | [PDF](./Diffusion-and-Flow/PDFs/Deep_Unsupervised_Learning_using_Nonequilibrium_Thermodynamics.pdf) |
| Estimation of Non-Normalized Statistical Models by Score Matching | [PDF](./Diffusion-and-Flow/PDFs/Estimation_of_Non-Normalized_Statistical_Models_by_Score_Matching.pdf) |
| A Connection Between Score Matching and Denoising Autoencoders | [PDF](./Diffusion-and-Flow/PDFs/A_Connection_Between_Score_Matching_and_Denoising_Autoencoders.pdf) |
| Generative Modeling by Estimating Gradients of the Data Distribution（NCSN） | [PDF](./Diffusion-and-Flow/PDFs/Generative_Modeling_by_Estimating_Gradients_of_the_Data_Distribution.pdf) |
| Understanding Diffusion Models: A Unified Perspective | [PDF](./Diffusion-and-Flow/PDFs/Understanding_Diffusion_Models_A_Unified_Perspective.pdf) |
| Elucidating the Design Space of Diffusion-Based Generative Models（EDM） | [PDF](./Diffusion-and-Flow/PDFs/Elucidating_the_Design_Space_of_Diffusion-Based_Generative_Models.pdf) |

### 2. 连续流 / ODE / 随机插值统一框架（4 篇）

| 论文 | 本地 PDF |
| --- | --- |
| Neural Ordinary Differential Equations | [PDF](./Diffusion-and-Flow/PDFs/Neural_Ordinary_Differential_Equations.pdf) |
| Building Normalizing Flows with Stochastic Interpolants | [PDF](./Diffusion-and-Flow/PDFs/Building_Normalizing_Flows_with_Stochastic_Interpolants.pdf) |
| Stochastic Interpolants: A Unifying Framework for Flows and Diffusions | [PDF](./Diffusion-and-Flow/PDFs/Stochastic_Interpolants_A_Unifying_Framework_for_Flows_and_Diffusions.pdf) |
| Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport（OT-CFM） | [PDF](./Diffusion-and-Flow/PDFs/Improving_and_generalizing_flow-based_generative_models_with_minibatch_optimal_transport.pdf) |

### 3. 加速采样 / 蒸馏 / 少步与一步生成（9 篇）

| 论文 | 本地 PDF |
| --- | --- |
| Denoising Diffusion Implicit Models（DDIM） | [PDF](./Diffusion-and-Flow/PDFs/Denoising_Diffusion_Implicit_Models.pdf) |
| DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps | [PDF](./Diffusion-and-Flow/PDFs/DPM-Solver_A_Fast_ODE_Solver_for_Diffusion_Probabilistic_Model_Sampling_in_Around_10_Steps.pdf) |
| Progressive Distillation for Fast Sampling of Diffusion Models | [PDF](./Diffusion-and-Flow/PDFs/Progressive_Distillation_for_Fast_Sampling_of_Diffusion_Models.pdf) |
| Consistency Models | [PDF](./Diffusion-and-Flow/PDFs/Consistency_Models.pdf) |
| Consistency Flow Matching: Defining Straight Flows with Velocity Consistency | [PDF](./Diffusion-and-Flow/PDFs/Consistency_Flow_Matching_Defining_Straight_Flows_with_Velocity_Consistency.pdf) |
| Isokinetic Flow Matching for Pathwise Straightening of Generative Flows | [PDF](./Diffusion-and-Flow/PDFs/Isokinetic_Flow_Matching_for_Pathwise_Straightening_of_Generative_Flows.pdf) |
| Mean Flows for One-step Generative Modeling | [PDF](./Diffusion-and-Flow/PDFs/Mean_Flows_for_One-step_Generative_Modeling.pdf) |
| One Step Diffusion via Shortcut Models | [PDF](./Diffusion-and-Flow/PDFs/One_Step_Diffusion_via_Shortcut_Models.pdf) |
| PeRFlow: Piecewise Rectified Flow as Universal Plug-and-Play Accelerator | [PDF](./Diffusion-and-Flow/PDFs/PeRFlow_Piecewise_Rectified_Flow_as_Universal_Plug-and-Play_Accelerator.pdf) |

### 4. 条件引导与规模化主干架构（4 篇）

| 论文 | 本地 PDF |
| --- | --- |
| Classifier-Free Diffusion Guidance（CFG） | [PDF](./Diffusion-and-Flow/PDFs/Classifier-Free_Diffusion_Guidance.pdf) |
| High-Resolution Image Synthesis with Latent Diffusion Models（LDM） | [PDF](./Diffusion-and-Flow/PDFs/High-Resolution_Image_Synthesis_with_Latent_Diffusion_Models.pdf) |
| Scalable Diffusion Models with Transformers（DiT） | [PDF](./Diffusion-and-Flow/PDFs/Scalable_Diffusion_Models_with_Transformers.pdf) |
| FLUX（`FLUX_2506.15742v2`） | [arXiv:2506.15742](https://arxiv.org/abs/2506.15742)（本地归档，未公开分发 PDF） |

## 三、逆问题求解待读/参考 PDF（9 篇）

详见 [逆问题求解总览](./Inverse-Problems/README.md)（含 DPS、RED-Diff、PSLD、MPGD、DAPS、PnP-Flow、FLOWER、Posterior-Transport-View、CLIMB-Flow）。

## 资料来源

论文标题按现有文件和原文标注；作者、出版信息及许可说明以原始材料为准，归档不改变原作者权利。

上级入口：[论文总览](../README.md) · [Learning](../../README.md)。
