<!-- learning-vault-navigation:v1 -->
<details>
<summary>笔记导航</summary>

目录：[人工智能 · 课程总览](../README.md)

</details>

# 动手学深度学习（李沐 · PyTorch）

李沐《动手学深度学习》的课程与教材学习归档，使用中文版 PyTorch 材料，结合概念、数学推导与 Notebook 实践学习深度学习。

- [课程网站](https://courses.d2l.ai/zh-v2/)
- [官方在线教材](https://zh.d2l.ai/)

## 学习状态

按本人学习记录，李沐《动手学深度学习》（PyTorch）课程已学完。吴恩达 Machine Learning Specialization 的 C1 已学完，C2/C3 暂缓。下方教材、PDF、Notebook 和配图是课程学习资料归档。

概率论、随机过程与离散数学基础见 [Math Learning](../../Math%20Learning/README.md)，相关课程按各自的学习记录维护进度。

## 材料入口

- [中文版 PyTorch 教材 PDF](./d2l-zh-pytorch.pdf)
- [Notebook 总目录](./pytorch/index.ipynb)
- [安装说明](./pytorch/chapter_installation/index.ipynb)
- [术语表](./pytorch/TERMINOLOGY.ipynb)
- [深度学习基础课件归档（20 份 PDF）](./PPT/Part0_%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%9F%BA%E7%A1%80/)：沿用现有文件分类，课件的具体出处待补充，不以目录名推断作者或已学习进度。

## 章节导航

以下为已归档材料的入口；已确认的学习进度见上方“学习状态”，不由资料是否归档推断。

| 章节 | 章节笔记 | Notebook 入口 |
| --- | --- | --- |
| 前言 | — | [阅读](./pytorch/chapter_preface/index.ipynb) |
| 符号 | — | [阅读](./pytorch/chapter_notation/index.ipynb) |
| 01. 引言 | [笔记](./笔记/01.%20引言.md) | [阅读](./pytorch/chapter_introduction/index.ipynb) |
| 02. 预备知识 | [笔记](./笔记/02.%20预备知识.md) | [阅读](./pytorch/chapter_preliminaries/index.ipynb) |
| 03. 线性神经网络 | [笔记](./笔记/03.%20线性神经网络.md) | [阅读](./pytorch/chapter_linear-networks/index.ipynb) |
| 04. 多层感知机 | [笔记](./笔记/04.%20多层感知机.md) | [阅读](./pytorch/chapter_multilayer-perceptrons/index.ipynb) |
| 05. 深度学习计算 | [笔记](./笔记/05.%20深度学习计算.md) | [阅读](./pytorch/chapter_deep-learning-computation/index.ipynb) |
| 06. 卷积神经网络 | [笔记](./笔记/06.%20卷积神经网络.md) | [阅读](./pytorch/chapter_convolutional-neural-networks/index.ipynb) |
| 07. 现代卷积神经网络 | [笔记](./笔记/07.%20现代卷积神经网络.md) | [阅读](./pytorch/chapter_convolutional-modern/index.ipynb) |
| 08. 循环神经网络 | [笔记](./笔记/08.%20循环神经网络.md) | [阅读](./pytorch/chapter_recurrent-neural-networks/index.ipynb) |
| 09. 现代循环神经网络 | [笔记](./笔记/09.%20现代循环神经网络.md) | [阅读](./pytorch/chapter_recurrent-modern/index.ipynb) |
| 10. 注意力机制 | [笔记](./笔记/10.%20注意力机制.md) | [阅读](./pytorch/chapter_attention-mechanisms/index.ipynb) |
| 11. 优化算法 | [笔记](./笔记/11.%20优化算法.md) | [阅读](./pytorch/chapter_optimization/index.ipynb) |
| 12. 计算性能 | [笔记](./笔记/12.%20计算性能.md) | [阅读](./pytorch/chapter_computational-performance/index.ipynb) |
| 13. 计算机视觉 | [笔记](./笔记/13.%20计算机视觉.md) | [阅读](./pytorch/chapter_computer-vision/index.ipynb) |
| 14. 自然语言处理：预训练 | [笔记](./笔记/14.%20自然语言处理：预训练.md) | [阅读](./pytorch/chapter_natural-language-processing-pretraining/index.ipynb) |
| 15. 自然语言处理：应用 | [笔记](./笔记/15.%20自然语言处理：应用.md) | [阅读](./pytorch/chapter_natural-language-processing-applications/index.ipynb) |
| 附录：深度学习工具 | — | [阅读](./pytorch/chapter_appendix-tools-for-deep-learning/index.ipynb) |
| 参考文献 | — | [阅读](./pytorch/chapter_references/zreferences.ipynb) |

多层感知机相关 Notebook：

| 主题 | Notebook |
| --- | --- |
| 暂退法（Dropout） | [阅读](./pytorch/chapter_multilayer-perceptrons/dropout.ipynb) |
| 房价预测示例 | [阅读](./pytorch/chapter_multilayer-perceptrons/kaggle-house-price.ipynb) |

## 个人练习

以下是与本课程配套的个人代码练习，文件存在不表示已经完成对应章节：

- [个人练习总览](./Practice/README.md)
- [Linear Regression.py](./Practice/Linear%20Regression.py)
- [Softmax.py](./Practice/Softmax.py)
- [MLP.py](./Practice/MLP.py)
- [Dropout.py](./Practice/Dropout.py)

## 配套数据

- [house_tiny.csv](./pytorch/data/house_tiny.csv)：预备知识中“数据预处理”示例使用的小型 CSV 数据集。
- House Prices 示例数据：[训练集](./pytorch/data/kaggle_house_pred_train.csv) · [测试集](./pytorch/data/kaggle_house_pred_test.csv)。文件来自 D2L 房价预测示例；关联数据集为 [Kaggle House Prices](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)。
- [图像分类数据集 Notebook](./pytorch/chapter_linear-networks/image-classification-dataset.ipynb)运行时会按需下载 FashionMNIST。

## 资料来源

教材、配套 Notebook 和图片归原作者所有；本目录用于学习归档，原有示例输出不作为个人实验成果。配套示例的安装与依赖说明见上方教材入口。

上级入口：[AI Learning](../README.md) · [Learning](../../README.md)。
