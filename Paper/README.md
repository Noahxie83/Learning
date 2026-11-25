<!-- learning-vault-navigation:v1 -->
<details>
<summary>笔记导航</summary>

目录：[学习导航](../README.md)

</details>

# 论文阅读与资料

本目录用于归档论文阅读笔记、原文 PDF 及相关实验配置，按**稳定的研究领域**组织目录，**阅读与复现状态**以各笔记 YAML 元数据与本页标注为准（资料归档不代表已完成阅读或复现）。新增、迁移或维护论文资料请遵循 [Paper/AGENTS.md](./AGENTS.md)。

> **当前主线**：[逆问题求解（HDPS / FLAIR / FlowDPS / FlowLPS）](./Generative-Models/Inverse-Problems/README.md)

## 目录结构

| 专题目录 | 范围说明 | 入口 |
| --- | --- | --- |
| `Foundations/` | 视觉、序列/语言与图神经网络 7 篇经典基础论文（均已归档三遍精读笔记与 PDF） | 见下表 |
| `Generative-Models/` | 生成模型总专题：含 GAN、扩散/分数模型与流匹配（4 篇精读 + 23 篇待读 PDF）、逆问题求解（4 篇精读 + 9 篇待读 PDF） | [生成模型资料导航](./Generative-Models/README.md) |

## 经典基础论文（Foundations）

| 论文 | 领域 | 阅读笔记 | 本地 PDF | 原文来源 | 阅读状态 |
| --- | --- | --- | --- | --- | --- |
| AlexNet | 视觉 / CNN | [阅读笔记](./Foundations/AlexNet/AlexNet.md) | [PDF](./Foundations/AlexNet/AlexNet_NIPS2012.pdf) | [NeurIPS 2012](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) | 待确认 |
| ResNet | 视觉 / CNN | [阅读笔记](./Foundations/ResNet/ResNet.md) | [PDF](./Foundations/ResNet/ResNet_1512.03385.pdf) | [arXiv](https://arxiv.org/abs/1512.03385) | 待确认 |
| Transformer（Attention Is All You Need） | 序列 / 通用架构 | [阅读笔记](./Foundations/Transformer/Transformer.md) | [PDF](./Foundations/Transformer/Transformer_NIPS2017.pdf) | [arXiv](https://arxiv.org/abs/1706.03762) | 待确认 |
| BERT | 语言预训练 | [阅读笔记](./Foundations/BERT/BERT.md) | [PDF](./Foundations/BERT/BERT_1810.04805.pdf) | [arXiv](https://arxiv.org/abs/1810.04805) | 待确认 |
| ViT（An Image is Worth 16x16 Words） | 视觉 / Transformer | [阅读笔记](./Foundations/ViT/ViT.md) | [PDF](./Foundations/ViT/ViT_2010.11929.pdf) | [arXiv](https://arxiv.org/abs/2010.11929) | 待确认 |
| MAE（Masked Autoencoders） | 视觉 / 自监督 | [阅读笔记](./Foundations/MAE/MAE.md) | [PDF](./Foundations/MAE/MAE_2111.06377.pdf) | [arXiv](https://arxiv.org/abs/2111.06377) | 待确认 |
| A Gentle Introduction to Graph Neural Networks（GNN） | 图神经网络（教学综述） | [阅读笔记](./Foundations/GNN/GNN.md) | [PDF](./Foundations/GNN/GNN_Distill2021.pdf) | [Distill](https://distill.pub/2021/gnn-intro/) | 待确认 |

以上 7 篇均已归档三遍精读笔记；GNN 为 Distill 教学型文章，同目录保留离线 HTML 与资源包。

## 生成模型专题（Generative-Models）

- [生成模型论文总览](./Generative-Models/README.md)：共归档 9 篇精读笔记（GAN、DDPM、Score-SDE、Flow Matching、Rectified Flow、HDPS、FLAIR、FlowDPS、FlowLPS）与 32 份专题待读/参考 PDF。
- [扩散、分数与流匹配（Diffusion-and-Flow）](./Generative-Models/README.md#%E6%89%A9%E6%95%A3%E5%88%86%E6%95%B0%E4%B8%8E%E6%B5%81%E5%8C%B9%E9%85%8Ddiffusion-and-flow)：Flow Matching 已确认完成阅读；其余阅读与复现阶段见各笔记元数据。
- [基于扩散/流的逆问题求解（Inverse-Problems）](./Generative-Models/Inverse-Problems/README.md)：当前学习主线（HDPS、FLAIR 阅读中，配套 FlowDPS、FlowLPS 及 9 篇逆问题 PDF）。

上级入口：[Learning](../README.md)。
