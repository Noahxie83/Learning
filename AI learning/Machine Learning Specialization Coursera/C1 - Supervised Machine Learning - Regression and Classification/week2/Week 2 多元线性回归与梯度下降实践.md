---
title: C1 Week 2：多元线性回归与梯度下降实践
date: '2026-09-19'
date_source: 文件修改日期
subject: 人工智能
note_type: 课程笔记
course: Machine Learning Specialization C1
tags:
  - 领域/人工智能
  - 类型/课程笔记
  - 课程/Machine_Learning_Specialization
aliases:
  - C1 Week 2
  - 多元线性回归与梯度下降实践
cssclasses:
  - learning-note
  - subject-ai
  - learning-study
---

# C1 Week 2：多元线性回归与梯度下降实践

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/机器学习C1监督学习导航|机器学习 C1 监督学习导航]]
> 上一章：[[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week1/Week 1 监督学习与单变量线性回归|C1 Week 1：监督学习与单变量线性回归]] · 下一章：[[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week3/Week 3 逻辑回归分类与正则化|C1 Week 3：逻辑回归分类与正则化]]

> [!abstract] 本周学习概览与原始资料
> 本周将单变量线性回归推广至真实世界的**多特征场景**，核心掌握四大工程支柱：基于 NumPy 的 ==向量化计算（Vectorization）==、==特征缩放（Feature Scaling）== 与学习率收敛诊断、突破直线局限的 ==特征工程与多项式回归（Feature Engineering & Polynomial Regression）==，以及工业界工具库 **Scikit-learn**（`SGDRegressor` 与闭式解析解 `LinearRegression`），并完成了 **C1W2A1 餐厅特许经营利润预测** 编程作业。
> - 本周索引：[[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/机器学习C1第2周导航|机器学习 C1 第 2 周导航]]
> - 配套测验：
>   - [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Practice quiz - Multiple linear regression/C1W2多元线性回归测验导航|Practice Quiz: Multiple Linear Regression]]
>   - [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Practice quiz - Gradient descent in practice/C1W2梯度下降实践测验导航|Practice Quiz: Gradient Descent in Practice]]
> - 编程作业：[[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/C1W2A1/C1_W2_Linear_Regression.ipynb|C1W2A1: Linear Regression (Restaurant Profit)]]

---

## 1. 多元线性回归与向量化加速

### 1.1 多特征矩阵表示与模型公式

真实房价不仅取决于面积，还涉及卧室数、楼层数、房龄等 $n$ 个特征（如 Lab02 的 4 特征房价表：`size(sqft), bedrooms, floors, age`）。全部 $m$ 个样本组织为 $(m, n)$ 维设计矩阵 $\mathbf{X}$：

$$
\mathbf{X} = \begin{pmatrix}
x^{(0)}_0 & x^{(0)}_1 & \cdots & x^{(0)}_{n-1} \\
x^{(1)}_0 & x^{(1)}_1 & \cdots & x^{(1)}_{n-1} \\
\vdots & \vdots & \ddots & \vdots \\
x^{(m-1)}_0 & x^{(m-1)}_1 & \cdots & x^{(m-1)}_{n-1}
\end{pmatrix}, \quad
\mathbf{w} = \begin{pmatrix} w_0 \\ w_1 \\ \vdots \\ w_{n-1} \end{pmatrix}
$$

- **多元线性回归假设函数**写成简洁的向量点积形式：
$$
f_{\mathbf{w}, b}(\mathbf{x}^{(i)}) = w_0 x^{(i)}_0 + w_1 x^{(i)}_1 + \cdots + w_{n-1} x^{(i)}_{n-1} + b = \mathbf{w} \cdot \mathbf{x}^{(i)} + b
$$
- **多元代价函数**：
$$
J(\mathbf{w}, b) = \frac{1}{2m} \sum_{i=0}^{m-1} \left( \mathbf{w} \cdot \mathbf{x}^{(i)} + b - y^{(i)} \right)^2
$$
- **多元梯度下降更新（对 $j=0, \dots, n-1$ 与 $b$ 同步更新）**：
$$
\begin{aligned}
\frac{\partial J(\mathbf{w}, b)}{\partial w_j} &= \frac{1}{m} \sum_{i=0}^{m-1} \left( f_{\mathbf{w}, b}(\mathbf{x}^{(i)}) - y^{(i)} \right) x^{(i)}_j \\
\frac{\partial J(\mathbf{w}, b)}{\partial b} &= \frac{1}{m} \sum_{i=0}^{m-1} \left( f_{\mathbf{w}, b}(\mathbf{x}^{(i)}) - y^{(i)} \right)
\end{aligned}
$$

### 1.2 为什么必须使用向量化（NumPy `np.dot`）？

在 [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab01_Python_Numpy_Vectorization_Soln.ipynb|Lab01: Python, NumPy & Vectorization]] 中，对长度为 $10^7$ 的两个随机向量计算点积的实测对比极其震撼：

- **Python `for` 循环 (`my_dot`)**：耗时 **2137.48 ms**；
- **NumPy 向量化 (`np.dot`)**：耗时 **29.93 ms**（提速约 **71 倍**！）。

> [!tip] 向量化加速的底层硬件原理
> 现代 CPU 与 GPU 支持 **SIMD（Single Instruction, Multiple Data，单指令多数据）** 并行流水线。`np.dot(a, b)` 将运算交给底层 C/BLAS 高度优化的并行硬件指令批量完成，避免 Python 解释器的逐次循环开销。
>
> **形状对齐关键习惯（Lab01 重点）**：
> - `X_train` 形状为 `(m, n)`，切片单行 `X_train[i]`（等价于 `X_train[i, :]`）返回 **1-D 向量 `(n,)`**；
> - 参数 `w` 形状为 `(n,)`，`np.dot(X_train[i], w)` 返回标量（shape `()`）；
> - `np.arange(6).reshape(-1, 2)` 中的 `-1` 让 NumPy 自动推断行数。

---

## 2. 特征缩放（Feature Scaling）与学习率诊断

### 2.1 为什么特征尺度悬殊会拖垮梯度下降？

在 [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab02_Multiple_Variable_Soln.ipynb|Lab02]] 和 [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab03_Feature_Scaling_and_Learning_Rate_Soln.ipynb|Lab03]] 的 Ames 房价数据中，`size(sqft)` 量级在 $1000$–$2500$（峰峰值 $2410$），而 `bedrooms` 仅在 $1$–$5$（峰峰值 $4$）：

1. **梯度更新严重失衡**：所有参数共享同一个学习率 $\alpha$，但 `dj_dw[j]` 乘以了 $x_j$，导致 `w_0` 的梯度比 `w_1` 大数百倍；
2. **狭长椭圆等高线**：未缩放时，代价等高线在 $(w_0, w_1)$ 平面被压成极度扁长的峡谷，迫使 $\alpha$ 只能取极小值（如 `9e-7`），即使跑数小时，`w_1, w_2, w_3` 依然进展蜗速；
3. **缩放后效果立竿见影**：Z-score 归一化后各特征峰峰值收敛至 $2$–$6$ 左右，等高线趋近同心圆，学习率可大胆提升 **10 万倍**至 $\alpha = 0.1$，仅 **200–300 步**梯度即趋近于零，迅速收敛到最优解！

### 2.2 三种常用特征缩放方法对比

| 缩放方法 | 公式 | 缩放后范围/统计特征 | 适用说明 |
| :--- | :--- | :--- | :--- |
| **最大值缩放 / Min-Max** | $x_j \leftarrow \dfrac{x_j}{\max(x_j)}$ 或 $\dfrac{x_j - \min}{\max - \min}$ | $[0, 1]$（含负值时 $[-1, 1]$） | 简单直观，适合无极端离群点的有界特征 |
| **均值归一化（Mean Normalization）** | $x_j \leftarrow \dfrac{x_j - \mu_j}{\max - \min}$ | 均值 $0$，大致落在 $[-1, 1]$ | 兼具零中心化与尺度压缩 |
| **Z-score 标准化（最常用）** | $x^{(i)}_j \leftarrow \dfrac{x^{(i)}_j - \mu_j}{\sigma_j}$ | **均值 $\mu=0$，标准差 $\sigma=1$**，大多数样本在 $[-3, 3]$ | 课程与 `sklearn.preprocessing.StandardScaler` 首选方案 |

其中：

$$
\mu_j = \frac{1}{m} \sum_{i=0}^{m-1} x^{(i)}_j, \qquad \sigma_j = \sqrt{\frac{1}{m} \sum_{i=0}^{m-1} \left(x^{(i)}_j - \mu_j\right)^2}
$$

> [!warning] 预测新样本时的致命易错点！
> 用归一化后的特征训练得到 $(w_{\text{norm}}, b_{\text{norm}})$ 后，对新样本 `x_house = [1200, 3, 1, 40]` 做预测时，==必须先用**训练集保存下来的均值 `X_mu` 和标准差 `X_sigma`** 对新样本做完全相同的归一化==，再代入点积计算：
> ```python
> x_house_norm = (x_house - X_mu) / X_sigma
> pred_price = np.dot(x_house_norm, w_norm) + b_norm  # -> $318,709
> ```
> 切忌把原始未缩放特征直接喂给归一化模型，也不能用单条测试样本重新算均值方差。

### 2.3 学习率 $\alpha$ 调试与收敛判断（Lab03 实测）

在 Lab03 未缩放房价数据上测试 3 组学习率，清晰展示了诊断学习率曲线的实战方法：
- `alpha = 9.9e-7`：Cost 从 `9.56e4` 飙升到 `2.31e5`，参数反复过冲（Overshoot） $\to$ **过大，发散**；
- `alpha = 9e-7`：`w_0` 虽在极小值两侧震荡，但幅度逐渐衰减、Cost 单调下降 $\to$ **接近临界上限，能收敛**；
- `alpha = 1e-7`：无震荡单调逼近，但步子更小、收敛更慢。

**工程调参推荐阶梯**：按约 3 倍步进尝试 $\alpha \in \{0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1\}$，找到“既不发散又下降最快”的区间；结合绘制 **Learning Curve（$J(\mathbf{w}, b)$ vs. iterations）** 与设定自动收敛阈值（如单步代价下降 $< \epsilon = 10^{-3}$）判断收敛。

---

## 3. 特征工程与多项式回归（Feature Engineering & Polynomial Regression）

原生线性回归只能拟合超平面，如何用同一套线性回归工具拟合非线性曲线（例如房屋面积过大或过小时价格呈现弯曲走势，或拟合 $y = 1 + x^2$、$y = \cos(x/2)$）？

答案是 ==特征工程（Feature Engineering）==：运用领域直觉对原始特征做变换或组合（例如土地长宽 `frontage × depth = area`），或构造**多项式特征（Polynomial Features）**如 $x, x^2, x^3, \sqrt{x}$。

```mermaid
flowchart LR
    RAW["原始特征 x"] --> FE["特征工程: np.c_[x, x**2, x**3]"]
    FE --> SC["特征缩放: Z-score 标准化 (必做!)"]
    SC --> LR["多元线性回归 + 梯度下降"]
    LR --> CURVE["对原始 x 呈现出高度非线性拟合曲线"]
```

### Lab04 关键实验发现（[[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab04_FeatEng_PolyReg_Soln.ipynb|Lab04]]）
1. **将非线性问题转化为新特征空间的线性问题**：对于真实规律 $y = x^2$，如果构造 $X = [x, x^2, x^3]$，画散点图会发现 $y$ 与新特征 $x^2$ 呈完美的**线性关系**；
2. **梯度下降自带“特征权重筛选”效果**：在标准化后的 `[x, x^2, x^3]` 上以 $\alpha = 0.1$ 跑 100,000 步，得到 `w = [5.27e-05, 113.0, 8.43e-05]`，算法自动把无关的 $x$ 与 $x^3$ 权重压到几乎为 $0$，突出真正的 $x^2$ 项；
3. **多项式特征必须配合特征缩放！** 当 $x \in [0, 19]$ 时，原始峰峰值差距极其悬殊：`[19, 361, 6859]`；Z-score 标准化后压缩至 `[3.30, 3.18, 3.28]`，从而能用高至 13 次多项式成功逼近复杂周期函数 $y = \cos(x/2)$。

---

## 4. 求解线性回归的两条路线：梯度下降 vs. 正规方程（Scikit-learn 实战）

在 [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab05_Sklearn_GD_Soln.ipynb|Lab05: Sklearn GD]] 与 [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab06_Sklearn_Normal_Soln.ipynb|Lab06: Sklearn Normal Equation]] 中，课程展示了 Scikit-learn 的两种实现：

| 对比维度 | 梯度下降 (`SGDRegressor`) | 正规方程闭式解 (`LinearRegression`) |
| :--- | :--- | :--- |
| **数学原理** | 沿负梯度方向迭代更新参数 | 直接解 $\nabla J = 0$ 的解析方程 $\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^T \mathbf{y}$ |
| **是否需要特征缩放** | **强烈需要**（配合 `StandardScaler().fit_transform(X)`） | **不需要**（直接拟合原始 `X_train` 即可） |
| **是否需要调学习率 $\alpha$** | 需要（或由库内置调度策略控制） | **不需要**，无迭代过程 |
| **大特征规模效率（如 $n > 10,000$）** | **高效**，可扩展到超大规模数据集与所有深度学习模型 | 矩阵求逆/分解复杂度高达 $O(n^3)$，特征极多时很慢 |
| **适用算法范围** | 通用（线性回归、逻辑回归、神经网络等） | **仅限线性回归** |
| **Lab05 / Lab06 实测结果** | 111 轮迭代收敛：`w=[109.95, -20.97, -32.35, -38.07], b=363.15`（归一化空间） | 瞬间求解原始空间参数 `w=[0.27, -32.62, -67.25, -1.47], b=220.42`；两者对 1200 sqft 房屋预测完全一致（`$318,709`） |

```python
# 1) Scikit-learn 梯度下降标准流水线 (Lab05)
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor

scaler = StandardScaler()
X_norm = scaler.fit_transform(X_train)
sgdr = SGDRegressor(max_iter=1000)
sgdr.fit(X_norm, y_train)
w_norm, b_norm = sgdr.coef_, sgdr.intercept_

# 2) Scikit-learn 闭式解析解 (Lab06，注意 1D 特征需 reshape(-1, 1))
from sklearn.linear_model import LinearRegression

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
w, b = linear_model.coef_, linear_model.intercept_
```

---

## 5. 编程作业复盘：C1W2A1 餐厅特许经营利润预测

在 [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/C1W2A1/C1_W2_Linear_Regression.ipynb|C1_W2_Linear_Regression.ipynb]] 中，基于 `ex1data1.txt`（$m = 97$ 个城市的人口规模与餐厅月利润数据，单位均为 $10,000$）亲手完成了单变量线性回归的完整训练与预测，全部单元测试通过（`All tests passed!`）：

1. **Exercise 1 (`compute_cost`)**：遍历 97 个城市累加平方误差并除以 $2m$。测试初值 `w=2, b=1` 得 `Cost = 75.203`。
2. **Exercise 2 (`compute_gradient`)**：同步累积 `dj_db` 与 `dj_dw` 并求均值。测试初值 `w=0, b=0` 得 `dj_dw = -65.3288, dj_db = -5.8391`；测试 `w=0.2, b=0.2` 得 `dj_dw = -47.4161, dj_db = -4.0072`。
3. **Batch Gradient Descent 训练结果**（`alpha = 0.01`, `iterations = 1500`）：
   - 代价从第 0 步的 `6.74` 平滑收敛至第 1350 步的 `4.49`；
   - 最终拟合直线参数：$w = 1.1664, \; b = -3.6303$。
4. **商业选址预测**：
   - 人口 35,000（$x = 3.5$）城市预测月利润：**\$4,519.77**；
   - 人口 70,000（$x = 7.0$）城市预测月利润：**\$45,342.45**。

---

## 6. Optional Labs 索引与自测清单

| 实验文件 | 核心主题 |
| :--- | :--- |
| [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab01_Python_Numpy_Vectorization_Soln.ipynb\|Lab01: NumPy Vectorization]] | 向量/矩阵创建、切片、`reshape(-1, k)` 及 `np.dot` 相比循环 70× 加速基准测试 |
| [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab02_Multiple_Variable_Soln.ipynb\|Lab02: Multiple Variable Regression]] | 将预测、代价与梯度函数扩展为多特征矩阵输入（3 样本 × 4 特征） |
| [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab03_Feature_Scaling_and_Learning_Rate_Soln.ipynb\|Lab03: Feature Scaling & Learning Rate]] | Ames 房价数据上对比 `9.9e-7 / 9e-7 / 1e-7` 学习率，实现 Z-score 归一化并将 $\alpha$ 提速至 `0.1` |
| [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab04_FeatEng_PolyReg_Soln.ipynb\|Lab04: Feature Engineering & PolyReg]] | 构造 `x, x^2, x^3` 及 13 次多项式拟合 $x^2$ 与 $\cos(x/2)$，验证特征缩放在高阶多项式中的必要性 |
| [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab05_Sklearn_GD_Soln.ipynb\|Lab05: Sklearn SGDRegressor]] | 使用 `StandardScaler` + `SGDRegressor` 实现标准化梯度下降回归 |
| [[AI learning/Machine Learning Specialization Coursera/C1 - Supervised Machine Learning - Regression and Classification/week2/Optional Labs/C1_W2_Lab06_Sklearn_Normal_Soln.ipynb\|Lab06: Sklearn Normal Equation]] | 使用 `LinearRegression` 闭式解析解直接拟合，对比无须归一化的便捷性与计算复杂度局限 |

> [!question]- Week 2 核心自检清单
> 1. **在多元回归中，为何特征缩放能让等高线更接近圆形？**
>    - 当特征 $x_0$ 与 $x_1$ 数值范围接近时，参数 $w_0$ 与 $w_1$ 的最优量级接近、偏导量级均衡，损失曲面在各参数轴上曲率相近，梯度方向几乎直指碗底而非来回之字形震荡。
> 2. **为什么多项式回归仍被称为“线性回归”？**
>    - 尽管模型关于原始输入 $x$ 是非线性的（含 $x^2, x^3$），但关于**待学习参数 $\mathbf{w}, b$ 仍是线性的**，因此代价函数依然是凸函数，完全沿用线性回归的梯度下降或闭式解 machinery。
> 3. **什么时候优先选梯度下降而不是正规方程？**
>    - 当特征维度 $n$ 很大（例如 $n > 10,000$），或模型不是线性回归（如逻辑回归、神经网络）时，正规方程要么计算不可行要么根本不存在闭式解，必须使用梯度下降。
