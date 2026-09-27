# 动手学深度学习（李沐 · PyTorch）

李沐《动手学深度学习》的课程与教材学习归档，使用中文版 PyTorch 材料，结合概念、数学推导与 Notebook 实践学习深度学习。

- [课程网站](https://courses.d2l.ai/zh-v2/)
- [官方在线教材](https://zh.d2l.ai/)

## 学习状态

吴恩达 Machine Learning Specialization 的 C1 已学完，C2/C3 暂缓；当前学习重点为本课程。本课程已学完第一章，整门课程尚未学完。已归档的 PDF、Notebook 和配图是课程参考材料，不能据此推断其他章节已经完成。

数学基础需要时再查阅 [Mathematics for Machine Learning and Data Science](../Mathematics%20for%20Machine%20Learning%20and%20Data%20Science%20Specialization/README.md)。

## 材料入口

- [中文版 PyTorch 教材 PDF](./d2l-zh-pytorch.pdf)
- [Notebook 总目录](./pytorch/index.ipynb)
- [安装说明](./pytorch/chapter_installation/index.ipynb)
- [术语表](./pytorch/TERMINOLOGY.ipynb)
- [深度学习基础课件归档（20 份 PDF）](./PPT/Part0_深度学习基础/)：沿用现有文件分类，课件的具体出处待补充，不以目录名推断作者或已学习进度。

## 章节导航

以下为已归档材料的入口；已确认的学习进度见上方“学习状态”，不由资料是否归档推断。

| 章节 | Notebook 入口 |
| --- | --- |
| 前言 | [阅读](./pytorch/chapter_preface/index.ipynb) |
| 符号 | [阅读](./pytorch/chapter_notation/index.ipynb) |
| 引言 | [阅读](./pytorch/chapter_introduction/index.ipynb) |
| 预备知识 | [阅读](./pytorch/chapter_preliminaries/index.ipynb) |
| 线性神经网络 | [阅读](./pytorch/chapter_linear-networks/index.ipynb) |
| 多层感知机 | [阅读](./pytorch/chapter_multilayer-perceptrons/index.ipynb) |
| 深度学习计算 | [阅读](./pytorch/chapter_deep-learning-computation/index.ipynb) |
| 卷积神经网络 | [阅读](./pytorch/chapter_convolutional-neural-networks/index.ipynb) |
| 现代卷积神经网络 | [阅读](./pytorch/chapter_convolutional-modern/index.ipynb) |
| 循环神经网络 | [阅读](./pytorch/chapter_recurrent-neural-networks/index.ipynb) |
| 现代循环神经网络 | [阅读](./pytorch/chapter_recurrent-modern/index.ipynb) |
| 注意力机制 | [阅读](./pytorch/chapter_attention-mechanisms/index.ipynb) |
| 优化算法 | [阅读](./pytorch/chapter_optimization/index.ipynb) |
| 计算性能 | [阅读](./pytorch/chapter_computational-performance/index.ipynb) |
| 计算机视觉 | [阅读](./pytorch/chapter_computer-vision/index.ipynb) |
| 自然语言处理：预训练 | [阅读](./pytorch/chapter_natural-language-processing-pretraining/index.ipynb) |
| 自然语言处理：应用 | [阅读](./pytorch/chapter_natural-language-processing-applications/index.ipynb) |
| 附录：深度学习工具 | [阅读](./pytorch/chapter_appendix-tools-for-deep-learning/index.ipynb) |
| 参考文献 | [阅读](./pytorch/chapter_references/zreferences.ipynb) |

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

## 配套数据

- [house_tiny.csv](./pytorch/data/house_tiny.csv)：预备知识中“数据预处理”示例使用的小型 CSV 数据集。
- House Prices 示例数据：[训练集](./pytorch/data/kaggle_house_pred_train.csv) · [测试集](./pytorch/data/kaggle_house_pred_test.csv)。文件来自 D2L 房价预测示例；关联数据集为 [Kaggle House Prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)。
- [图像分类数据集 Notebook](./pytorch/chapter_linear-networks/image-classification-dataset.ipynb)运行时会按需下载 FashionMNIST。

## 资料来源

教材、配套 Notebook 和图片归原作者所有；本目录用于学习归档，原有示例输出不作为个人实验成果。配套示例的安装与依赖说明见上方教材入口。

上级入口：[AI Learning](../README.md) · [Learning](../../README.md)。
