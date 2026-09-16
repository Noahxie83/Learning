面向机器学习、深度学习与最优化的矩阵微积分学习笔记与速查表。

**阅读路线：** 基础求导见第 1–8 节；链式法则与常用损失见第 9–14 节；矩阵变量与反向传播见第 15–22 节；优化、维度检查与易错点见第 23–25 节；第 26 节是 Top 15 速查表，末尾附维度速检。

> Note: 全文使用实数、列向量梯度和“输出维度 × 输入维度”的 Jacobian。每节给出的维度适用于该节公式；局部重新声明的维度优先。除非特别说明，求导时其他参数均视为常量。

## 1. Notation and Conventions

### 1.1 基本记号

默认 $x\in\mathbb R^n$ 表示 $n\times1$ 列向量，$A\in\mathbb R^{m\times n}$ 表示矩阵。

| 概念 | 记号与定义 | 维度 / 条件 |
|---|---|---|
| Scalar，标量 | $c\in\mathbb R$ | 单个实数 |
| Vector，向量 | $x=[x_1,\ldots,x_n]^T$ | $n\times1$ |
| Matrix，矩阵 | $A=[A_{ij}]$ | $m\times n$ |
| Transpose，转置 | $(A^T)_{ij}=A_{ji}$ | $A^T\in\mathbb R^{n\times m}$ |
| Gradient，梯度 | $\nabla_x f$ | 标量函数对向量求导，$n\times1$ |
| Jacobian，雅可比矩阵 | $(J_f)_{ij}=\partial f_i/\partial x_j$ | $f:\mathbb R^n\to\mathbb R^m$ 时为 $m\times n$ |
| Hessian，海森矩阵 | $H_f=J_{\nabla f}=\nabla_x^2f$ | 标量函数的二阶导数，$n\times n$ |
| Trace，迹 | $\operatorname{tr}(A)=\sum_i A_{ii}$ | 方阵到标量 |
| Determinant，行列式 | $\det A$ | 方阵到标量；非零等价于可逆 |
| Frobenius norm | $\lVert A\rVert_F=\sqrt{\sum_{ij}A_{ij}^2}$ | 矩阵到非负标量 |
| Hadamard product，逐元素乘积 | $(A\odot B)_{ij}=A_{ij}B_{ij}$ | 默认 $A,B$ 形状相同，输出同形状 |
| Identity matrix，单位矩阵 | $I_nx=x$ | $I_n\in\mathbb R^{n\times n}$ |
| 对角矩阵 | $\operatorname{diag}(v)$ | $v\in\mathbb R^n$ 时输出 $n\times n$ |
| 全一向量 | $\mathbf1_n$ | $n\times1$ |
| Positive semidefinite，半正定 | $A\succeq0$：所有 $v$ 都有 $v^TAv\ge0$ | 本文要求 $A$ 为实对称方阵 |
| Positive definite，正定 | $A\succ0$：所有非零 $v$ 都有 $v^TAv>0$ | 本文要求 $A$ 为实对称方阵 |

转置会反转乘积次序：

$$
(AB)^T=B^TA^T.
$$

### 1.2 Gradient 与 Jacobian 的方向

对于 $f:\mathbb R^n\to\mathbb R$：

$$
\nabla_x f=
\begin{bmatrix}
\frac{\partial f}{\partial x_1}\\
\vdots\\
\frac{\partial f}{\partial x_n}
\end{bmatrix}
\in\mathbb R^{n\times1}.
$$

其 Jacobian 是一行：

$$
J_f=\frac{\partial f}{\partial x}
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1}&\cdots&
\frac{\partial f}{\partial x_n}
\end{bmatrix}
\in\mathbb R^{1\times n}.
$$

> **Key Formula**
>
> $$
> J_f=(\nabla_x f)^T.
> $$

直观上，梯度收集“每个输入坐标变化时，标量输出如何变化”；Jacobian 则对每个输出分别做这件事。

### 1.3 用微分统一记忆

对向量变量，标量微分满足：

$$
df=(\nabla_x f)^Tdx.
$$

对矩阵变量 $X\in\mathbb R^{r\times c}$：

$$
(\nabla_Xf)_{ij}=\frac{\partial f}{\partial X_{ij}},
\qquad
\nabla_Xf\in\mathbb R^{r\times c},
$$

$$
df=\langle\nabla_Xf,dX\rangle_F
=\operatorname{tr}\big((\nabla_Xf)^T dX\big).
$$

其中 $\langle U,V\rangle_F=\operatorname{tr}(U^TV)$ 为 Frobenius 内积。

> Warning: 本文的 $\partial L/\partial X$ 在标量损失对矩阵求导时表示与 $X$ 同形状的梯度。若先把 $X$ 展平再按 Jacobian 定义求导，得到的则是一行；不要混用这两种表示。

## 2. Basic Scalar Derivatives

以下均为标量输入、标量输出，导数也是标量。

| 函数 | 导数 | 条件 / 特殊情况 |
|---|---|---|
| $c$ | $\frac{d}{dx}c=0$ | $c$ 为常数 |
| $x^n$ | $\frac{d}{dx}x^n=nx^{n-1}$ | $n$ 为正整数时处处成立；常数函数 $x^0=1$ 的导数为 $0$ |
| $x^\alpha$ | $\alpha x^{\alpha-1}$ | 任意实数 $\alpha$ 时，在 $x>0$ 上成立 |
| $e^x$ | $\frac{d}{dx}e^x=e^x$ | $x\in\mathbb R$ |
| $\ln x$ | $\frac{d}{dx}\ln x=\frac1x$ | $x>0$ |
| $\sin x$ | $\frac{d}{dx}\sin x=\cos x$ | 角度按弧度计 |
| $\cos x$ | $\frac{d}{dx}\cos x=-\sin x$ | 角度按弧度计 |

设 $u(x),v(x)$ 可微：

| 法则 | 公式 | 条件 |
|---|---|---|
| Product rule，乘积法则 | $(uv)'=u'v+uv'$ | 两项都要求导 |
| Quotient rule，商法则 | $\left(\frac uv\right)'=\frac{u'v-uv'}{v^2}$ | $v(x)\ne0$ |
| Scalar chain rule，标量链式法则 | $\frac{d}{dx}f(g(x))=f'(g(x))g'(x)$ | 各层在相应点可微 |

**例：**

$$
\frac{d}{dx}\ln(1+e^x)
=\frac{e^x}{1+e^x}
=\sigma(x).
$$

> Note: 标量求导规则仍然适用于矩阵微积分，但矩阵乘积必须保留原有顺序。

## 3. Gradient: Scalar with Respect to Vector

### 3.1 Linear form

设 $a,x\in\mathbb R^n$，输出均为标量，梯度均为 $n\times1$：

| 函数 | 梯度 |
|---|---|
| $a^Tx$ | $\nabla_x(a^Tx)=a$ |
| $x^Ta$ | $\nabla_x(x^Ta)=a$ |
| $a^Tx+c$ | $a$ |

因为 $a^Tx=\sum_i a_ix_i$，每个分量的偏导数就是对应的 $a_i$。

### 3.2 Vector norm

设 $x\in\mathbb R^n$：

| 标量函数 | 梯度，$n\times1$ | 条件 |
|---|---|---|
| $x^Tx$ | $2x$ | 任意 $x$ |
| $\lVert x\rVert_2^2$ | $2x$ | 与上一行是同一函数 |
| $\frac12\lVert x\rVert_2^2$ | $x$ | 系数 $\frac12$ 抵消求导产生的 $2$ |
| $\lVert x\rVert_2$ | $x/\lVert x\rVert_2$ | 仅适用于 $x\ne0$ |

> Warning: $\lVert x\rVert_2$ 与 $\lVert x\rVert_2^2$ 的导数不同。前者在原点不可微，后者处处可微。

### 3.3 Bilinear form

本小节设 $x\in\mathbb R^m$、$y\in\mathbb R^n$、$A\in\mathbb R^{m\times n}$：

$$
f(x,y)=x^TAy\in\mathbb R.
$$

$$
\nabla_x f=Ay\in\mathbb R^m,
\qquad
\nabla_y f=A^Tx\in\mathbb R^n.
$$

对 $x$ 求导时，$Ay$ 是固定系数向量；对 $y$ 求导时，把函数写成 $(A^Tx)^Ty$ 即可。

> Warning: 两个变量在求偏导时相互独立。若 $y=x$，两个位置都依赖 $x$，必须把两条求导路径相加。

## 4. Quadratic Forms

本节设 $x,b\in\mathbb R^n$、$A\in\mathbb R^{n\times n}$、$c\in\mathbb R$。所有函数输出为标量，梯度为 $n\times1$。

### 4.1 一般矩阵与对称矩阵

> **Key Formula**
>
> $$
> \nabla_x(x^TAx)=(A+A^T)x.
> $$

用微分可以看出两项的来源：

$$
\begin{aligned}
d(x^TAx)
&=(dx)^TAx+x^TA\,dx\\
&=(Ax)^Tdx+(A^Tx)^Tdx\\
&=\big((A+A^T)x\big)^Tdx.
\end{aligned}
$$

| 函数 | 一般 $A$ 的梯度 | 当 $A=A^T$ |
|---|---|---|
| $x^TAx$ | $(A+A^T)x$ | $2Ax$ |
| $\frac12x^TAx$ | $\frac12(A+A^T)x$ | $Ax$ |
| $\frac12x^TAx+b^Tx+c$ | $\frac12(A+A^T)x+b$ | $Ax+b$ |

一般二次函数的 Hessian 为：

$$
\nabla_x^2f=\frac12(A+A^T)\in\mathbb R^{n\times n}.
$$

若 $A=A^T$，则：

$$
\nabla_xf=Ax+b,
\qquad
\nabla_x^2f=A.
$$

### 4.2 为什么对称矩阵重要

令 $S=(A+A^T)/2$，则：

$$
x^TAx=x^TSx.
$$

反对称部分不会影响二次型的值。因此，二次型的梯度、曲率和凸性都由对称部分决定。实对称矩阵的特征值为实数，可以直接用特征值符号判断曲率。

**例：** 对非对称矩阵

$$
A=
\begin{bmatrix}
1&2\\
0&3
\end{bmatrix},
\qquad
f(x)=x_1^2+2x_1x_2+3x_2^2,
$$

有：

$$
\nabla_xf=
\begin{bmatrix}
2x_1+2x_2\\
2x_1+6x_2
\end{bmatrix}
=(A+A^T)x.
$$

> Warning: 只有在 $A$ 对称时，才能直接写 $\nabla_x(x^TAx)=2Ax$。即使 $2Ax$ 的 shape 正确，公式也可能错误。

## 5. Least Squares and Linear Regression

### 5.1 最小二乘的完整推导

设：

$$
A\in\mathbb R^{m\times n},
\quad x\in\mathbb R^n,
\quad b\in\mathbb R^m,
\quad r=Ax-b\in\mathbb R^m.
$$

残差 $r$ 表示预测与目标的差。平方损失将所有残差的平方相加：

$$
\begin{aligned}
f(x)
&=\lVert Ax-b\rVert_2^2\\
&=(Ax-b)^T(Ax-b)\\
&=x^TA^TAx-2b^TAx+b^Tb.
\end{aligned}
$$

因为 $A^TA$ 对称：

$$
\nabla_xf
=2A^TAx-2A^Tb
=2A^T(Ax-b).
$$

对于带 $\frac12$ 的版本，也可以直接使用微分：

$$
d\left(\frac12r^Tr\right)
=r^Tdr
=r^TA\,dx
=(A^Tr)^Tdx.
$$

| 标量目标函数 | 梯度，$n\times1$ | Hessian，$n\times n$ |
|---|---|---|
| $\lVert Ax-b\rVert_2^2$ | $2A^T(Ax-b)$ | $2A^TA$ |
| $\frac12\lVert Ax-b\rVert_2^2$ | $A^T(Ax-b)$ | $A^TA$ |
| $\frac1{2m}\lVert Ax-b\rVert_2^2$ | $\frac1mA^T(Ax-b)$ | $\frac1mA^TA$ |

> Note: $A^T$ 将输出空间中 $m$ 维的残差信号传回 $n$ 维参数空间。$A^TA\succeq0$ 始终成立；当 $A$ 列满秩时，$A^TA\succ0$。

### 5.2 线性回归与正规方程

设 $N$ 个样本、$d$ 个特征：

$$
X\in\mathbb R^{N\times d},
\quad\theta\in\mathbb R^d,
\quad y\in\mathbb R^N.
$$

这里每一行是一个样本；截距可以通过在 $X$ 中添加全一列并入 $\theta$。

$$
J(\theta)=\frac12\lVert X\theta-y\rVert_2^2,
$$

$$
\nabla_\theta J=X^T(X\theta-y)\in\mathbb R^d.
$$

令梯度为零：

$$
X^TX\theta=X^Ty.
$$

若 $\operatorname{rank}(X)=d$，则 $X^TX$ 可逆，唯一最小二乘解为：

$$
\theta^*=(X^TX)^{-1}X^Ty.
$$

若 $X$ 不列满秩，最小二乘解不唯一；Moore–Penrose 伪逆给出其中欧氏范数最小的解：

$$
\theta^*=X^+y.
$$

> Warning: 正规方程始终是最小二乘解的条件，但逆矩阵表达式要求 $X^TX$ 可逆。数值计算通常直接使用最小二乘求解器、QR 或 SVD，避免显式求逆；构造 $X^TX$ 还可能放大病态问题。

> Note: 损失采用样本平均值时，梯度和 Hessian 都要乘相同的 $1/N$；这不会改变无正则项时的最优解。

## 6. Jacobian

### 6.1 定义

若 $f:\mathbb R^n\to\mathbb R^m$，则：

$$
J_f(x)=\frac{\partial f}{\partial x}
=
\begin{bmatrix}
\frac{\partial f_1}{\partial x_1}&\cdots&\frac{\partial f_1}{\partial x_n}\\
\vdots&\ddots&\vdots\\
\frac{\partial f_m}{\partial x_1}&\cdots&\frac{\partial f_m}{\partial x_n}
\end{bmatrix}
\in\mathbb R^{m\times n}.
$$

**每一行对应一个输出，每一列对应一个输入。** 第 $j$ 列描述只改变输入 $x_j$ 时，各输出如何变化。

### 6.2 常见 Jacobian

| 函数 | 输入 → 输出 | Jacobian | 条件 |
|---|---|---|---|
| $f(x)=x$ | $\mathbb R^n\to\mathbb R^n$ | $I_n$ | 恒等映射 |
| $f(x)=Ax+b$ | $\mathbb R^n\to\mathbb R^m$ | $A\in\mathbb R^{m\times n}$ | $A,b$ 为常量 |
| $f(x)=a^Tx$ | $\mathbb R^n\to\mathbb R$ | $a^T\in\mathbb R^{1\times n}$ | 不是列梯度 $a$ |
| $y_i=\phi(x_i)$ | $\mathbb R^n\to\mathbb R^n$ | $\operatorname{diag}(\phi'(x_1),\ldots,\phi'(x_n))$ | 各坐标独立且可微 |

### 6.3 二维例子

$$
f(x_1,x_2)=
\begin{bmatrix}
x_1^2+x_2\\
\sin x_2
\end{bmatrix}.
$$

$$
J_f(x)=
\begin{bmatrix}
2x_1&1\\
0&\cos x_2
\end{bmatrix}
\in\mathbb R^{2\times2}.
$$

在 $x=(1,0)^T$ 处，微小变化 $\Delta x=(\varepsilon,\delta)^T$ 约产生：

$$
\Delta f\approx J_f(x)\Delta x
=
\begin{bmatrix}
2\varepsilon+\delta\\
\delta
\end{bmatrix}.
$$

> Warning: 逐元素函数的 Jacobian 是对角矩阵；一般向量函数的 Jacobian 可能有非零的非对角元素。

## 7. Hessian

### 7.1 定义与常用公式

对二阶连续可微的标量函数 $f:\mathbb R^n\to\mathbb R$：

$$
H_f(x)=\nabla_x^2f=J_{\nabla f}(x)
=
\begin{bmatrix}
\frac{\partial^2f}{\partial x_1^2}&\cdots&
\frac{\partial^2f}{\partial x_1\partial x_n}\\
\vdots&\ddots&\vdots\\
\frac{\partial^2f}{\partial x_n\partial x_1}&\cdots&
\frac{\partial^2f}{\partial x_n^2}
\end{bmatrix}
\in\mathbb R^{n\times n}.
$$

连续的二阶偏导数保证混合偏导可交换，因此 $H_f=H_f^T$。

| 标量函数 | Hessian | 条件 |
|---|---|---|
| $x^TAx$ | $A+A^T$ | $A\in\mathbb R^{n\times n}$ |
| $x^TAx$ | $2A$ | $A=A^T$ |
| $\frac12x^TAx$ | $\frac12(A+A^T)$ | 一般方阵 $A$ |
| $\frac12x^TAx$ | $A$ | $A=A^T$ |
| $\frac12\lVert Ax-b\rVert_2^2$ | $A^TA$ | $A\in\mathbb R^{m\times n}$ |

### 7.2 曲率、正定性与凸性

沿固定方向 $v\in\mathbb R^n$：

$$
\left.\frac{d^2}{dt^2}f(x+tv)\right|_{t=0}
=v^TH_f(x)v.
$$

因此，Hessian 描述不同方向上的曲率：

| Hessian 的性质 | 含义 |
|---|---|
| $H(x)\succeq0$ | 在该点，所有方向的二阶曲率非负 |
| $H(x)\succ0$ | 在该点，所有非零方向的二阶曲率为正 |
| $H(x)$ 有正、负特征值 | 存在向上弯和向下弯的方向；若该点驻定，则为鞍点 |
| 某方向满足 $v^TH(x)v=0$ | 二阶项无法判断该方向的高阶行为 |

> **Key Formula**
>
> 在开凸域上，若 $f$ 二阶连续可微，则：
>
> $$
> f\text{ 为凸函数}
> \iff H_f(x)\succeq0\quad\text{对域内所有 }x.
> $$

在二阶连续可微的前提下，某点的 Hessian 正定会在足够小的邻域内保持正定，从而得到局部严格凸性。若该点还满足 $\nabla f=0$，则它是严格局部极小点。

> Warning: 一个点的 $H(x)\succeq0$ 不能证明整个函数凸。全域严格凸只能保证最优解“至多一个”，还需确认最优解存在；例如 $e^x$ 二阶导数处处为正，但在 $\mathbb R$ 上不取得最小值。

## 8. Taylor Expansion

设 $\Delta x\in\mathbb R^n$ 足够小。Taylor 展开把非线性函数在当前点附近近似为线性或二次函数。

### 8.1 标量函数的一阶展开

对可微的 $f:\mathbb R^n\to\mathbb R$：

$$
f(x+\Delta x)
\approx f(x)+\nabla f(x)^T\Delta x.
$$

维度为 $(1\times n)(n\times1)=1\times1$。严格余项为 $o(\lVert\Delta x\rVert_2)$。

### 8.2 向量函数的一阶展开

对可微的 $f:\mathbb R^n\to\mathbb R^m$：

$$
f(x+\Delta x)\approx f(x)+J_f(x)\Delta x.
$$

维度为 $(m\times n)(n\times1)=m\times1$，输出变化与 $f(x)$ 同形状。

### 8.3 标量函数的二阶展开

若 $f$ 在邻域内二阶连续可微：

$$
f(x+\Delta x)
\approx f(x)
+\nabla f(x)^T\Delta x
+\frac12\Delta x^TH_f(x)\Delta x.
$$

二次项是标量，严格余项为 $o(\lVert\Delta x\rVert_2^2)$。

| 对象 | 直觉 | 作用 |
|---|---|---|
| Gradient | Slope：各输入方向的斜率 | 给出一阶变化、最速上升方向 |
| Jacobian | Local linear transformation：局部线性映射 | 把输入扰动映射为输出扰动 |
| Hessian | Curvature：曲率 | 描述梯度如何变化，修正一阶近似 |

**例：** 对 $f(x)=\frac12x^TAx+b^Tx+c$ 且 $A=A^T$，二阶展开是精确等式，因为没有更高阶项。

> Note: “梯度是最速上升方向”使用的是欧氏距离衡量方向长度。

## 9. Chain Rule

链式法则把复杂模型拆成若干局部映射，再按依赖关系组合导数。

### 9.1 Scalar chain rule

对于标量链 $x\to u(x)\to y(u)$：

$$
\frac{dy}{dx}=\frac{dy}{du}\frac{du}{dx}.
$$

**例：** $y=(3x+1)^2$，则 $dy/dx=2(3x+1)\cdot3$。

### 9.2 Jacobian chain rule：沿前向顺序组合

设：

$$
x\in\mathbb R^n
\xrightarrow{g}
z\in\mathbb R^m
\xrightarrow{f}
y\in\mathbb R^p.
$$

微分满足：

$$
dz=J_g(x)\,dx,
\qquad
dy=J_f(z)\,dz.
$$

代入后：

> **Key Formula**
>
> $$
> J_{f\circ g}(x)=J_f(g(x))J_g(x).
> $$

shape 检查：

$$
\underbrace{J_f}_{p\times m}
\underbrace{J_g}_{m\times n}
\in\mathbb R^{p\times n}.
$$

右边的 $J_g$ 先作用于输入扰动，左边的 $J_f$ 再把中间扰动传到输出。

> Warning: 应在 $z=g(x)$ 处计算 $J_f$。一般不能交换 $J_fJ_g$ 的次序。

### 9.3 Gradient chain rule：把损失梯度传回输入

设 $z=g(x)\in\mathbb R^m$，$L=f(z)\in\mathbb R$。已知上游梯度 $\nabla_zL$：

$$
\begin{aligned}
dL
&=(\nabla_zL)^Tdz\\
&=(\nabla_zL)^TJ_g(x)\,dx\\
&=\big(J_g(x)^T\nabla_zL\big)^Tdx.
\end{aligned}
$$

所以：

> **Key Formula**
>
> $$
> \nabla_xL=J_g(x)^T\nabla_zL.
> $$

shape 检查：

$$
\underbrace{J_g^T}_{n\times m}
\underbrace{\nabla_zL}_{m\times1}
=
\underbrace{\nabla_xL}_{n\times1}.
$$

转置来自列梯度约定：前向扰动通过 $J_g$ 传播，反向梯度通过 $J_g^T$ 传播。

### 9.4 为什么这就是 backpropagation

对计算链 $x\to z_1\to z_2\to L$：

$$
\nabla_xL
=J_{z_1}(x)^T
J_{z_2}(z_1)^T
\nabla_{z_2}L.
$$

反向传播从标量损失开始，把上游梯度逐层传回去。每一层只需要实现“本层 Jacobian 的转置乘以上游梯度”，通常无需显式生成完整 Jacobian。

**例：**

$$
z=Ax+b,\qquad L=\frac12z^Tz.
$$

这里 $x\in\mathbb R^n$、$z,b\in\mathbb R^m$、$A\in\mathbb R^{m\times n}$。先有 $\nabla_zL=z$，再有：

$$
\nabla_xL=A^Tz=A^T(Ax+b).
$$

> Warning: 如果一个变量经多条路径影响损失，各条路径的梯度必须相加。反向传播既包含链式相乘，也包含分支汇合处的累加。

## 10. Common Activation Functions

### 10.1 标量激活函数

下表中的输入、输出、导数均为标量。

| 激活函数 | 定义 | 导数 | 条件 / 特点 |
|---|---|---|---|
| Sigmoid | $\sigma(x)=\frac1{1+e^{-x}}$ | $\sigma'(x)=\sigma(x)(1-\sigma(x))$ | 处处可微，输出在 $(0,1)$ |
| Tanh | $\tanh x$ | $1-\tanh^2x$ | 处处可微，输出在 $(-1,1)$ |
| ReLU | $\max(0,x)$ | 正半轴为 $1$，负半轴为 $0$ | $x=0$ 处不可微 |

ReLU 的导数写为：

$$
\operatorname{ReLU}'(x)=
\begin{cases}
1,&x>0,\\
0,&x<0.
\end{cases}
$$

### 10.2 元素级向量形式

设 $x,y\in\mathbb R^n$，激活函数逐元素作用。

| 映射 | Jacobian，$n\times n$ | 给定 $g=\nabla_yL$ 后的 $\nabla_xL$ |
|---|---|---|
| $y=\sigma(x)$ | $\operatorname{diag}(y\odot(\mathbf1_n-y))$ | $g\odot y\odot(\mathbf1_n-y)$ |
| $y=\tanh(x)$ | $\operatorname{diag}(\mathbf1_n-y\odot y)$ | $g\odot(\mathbf1_n-y\odot y)$ |
| $y=\operatorname{ReLU}(x)$ | $\operatorname{diag}(r)$ | $g\odot r$ |

其中 $r_i=1$ 当 $x_i>0$，$r_i=0$ 当 $x_i<0$。

> Note: ReLU 在零点的凸次梯度集合为 $[0,1]$。实现中需要选择一个约定值，常见选择为 $0$；这不表示零点存在普通导数。

> Warning: Sigmoid 和 Tanh 在饱和区的导数接近零，多层连乘可能造成梯度消失。

## 11. Softmax

### 11.1 定义

设 logits $z\in\mathbb R^K$：

$$
p_i=\frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}},
\qquad
p=\operatorname{softmax}(z)\in\mathbb R^K.
$$

对有限的 $z$，有 $p_i>0$ 且 $\sum_i p_i=1$。

### 11.2 Jacobian

记 $\delta_{ij}$ 为 Kronecker delta，即 $i=j$ 时为 $1$，否则为 $0$。用商法则：

$$
\frac{\partial p_i}{\partial z_j}
=p_i(\delta_{ij}-p_j)
=
\begin{cases}
p_i(1-p_i),&i=j,\\
-p_ip_j,&i\ne j.
\end{cases}
$$

> **Key Formula**
>
> $$
> J_{\mathrm{softmax}}(z)
>=\operatorname{diag}(p)-pp^T
>\in\mathbb R^{K\times K}.
> $$

提高一个 logit 会提高对应概率，同时降低其他类别的概率，因此这里存在非对角导数。

### 11.3 反向传播与数值稳定性

给定 $g=\nabla_pL\in\mathbb R^K$：

$$
\nabla_zL
=J_{\mathrm{softmax}}^Tg
=p\odot\big(g-(p^Tg)\mathbf1_K\big).
$$

无需显式构造 $K\times K$ 矩阵。

数值上可减去最大值：

$$
c=\max_i z_i,
\qquad
p_i=\frac{e^{z_i-c}}{\sum_j e^{z_j-c}}.
$$

> Note: Softmax 对整体平移不变：$\operatorname{softmax}(z+c\mathbf1_K)=\operatorname{softmax}(z)$。因此 $J_{\mathrm{softmax}}\mathbf1_K=0$；该 Jacobian 对称、半正定且奇异。

> Warning: Softmax 不是逐元素函数，不能只保留 $p_i(1-p_i)$ 并丢弃非对角项。

## 12. Log-Sum-Exp

设 $x\in\mathbb R^n$：

$$
f(x)=\log\sum_{i=1}^n e^{x_i}\in\mathbb R.
$$

### 12.1 梯度与 Hessian

$$
\frac{\partial f}{\partial x_i}
=\frac{e^{x_i}}{\sum_j e^{x_j}}
=p_i.
$$

因此：

$$
\nabla_xf=\operatorname{softmax}(x)=p\in\mathbb R^n,
$$

$$
H_f(x)=\operatorname{diag}(p)-pp^T
\in\mathbb R^{n\times n}.
$$

**关系：** Softmax 是 Log-Sum-Exp 的梯度；Softmax 的 Jacobian 是 Log-Sum-Exp 的 Hessian。

### 12.2 直觉与凸性

Log-Sum-Exp 是最大值的平滑近似：

$$
\max_i x_i
\le \log\sum_i e^{x_i}
\le \max_i x_i+\log n.
$$

对任意 $v\in\mathbb R^n$：

$$
v^TH_fv
=\sum_i p_iv_i^2-\left(\sum_i p_iv_i\right)^2
\ge0.
$$

右侧是以 $p$ 为权重的方差，因此 $f$ 为凸函数。

数值稳定形式为：

$$
f(x)=c+\log\sum_i e^{x_i-c},
\qquad c=\max_i x_i.
$$

> Note: 它在整个 $\mathbb R^n$ 上不是严格凸函数，因为 $f(x+t\mathbf1_n)=f(x)+t$，沿全一方向是线性的。

## 13. Logistic Regression

### 13.1 单样本定义

设 $x,w\in\mathbb R^d$，$b,z,p,L\in\mathbb R$，标签 $y\in[0,1]$：

$$
z=w^Tx+b,\qquad p=\sigma(z),
$$

$$
L=-y\log p-(1-y)\log(1-p).
$$

通常二分类硬标签为 $y\in\{0,1\}$，上述公式也适用于软标签。

### 13.2 推导 $p-y$

对 $0<p<1$：

$$
\frac{\partial L}{\partial p}
=-\frac yp+\frac{1-y}{1-p}
=\frac{p-y}{p(1-p)}.
$$

结合 Sigmoid 导数：

$$
\frac{\partial p}{\partial z}=p(1-p).
$$

所以：

> **Key Formula**
>
> $$
> \frac{\partial L}{\partial z}=p-y.
> $$

进一步：

| 被求导变量 | 导数 | Shape |
|---|---|---|
| $w$ | $\nabla_wL=(p-y)x$ | $d\times1$ |
| $b$ | $\partial L/\partial b=p-y$ | 标量 |
| $x$ | $\nabla_xL=(p-y)w$ | $d\times1$ |

预测比标签高时，$p-y>0$；梯度下降会沿降低 logit 的方向调整参数。

### 13.3 稳定计算与 batch

直接从 logit 写损失：

$$
L=\log(1+e^z)-yz
=\max(z,0)+\log(1+e^{-|z|})-yz.
$$

后一形式避免直接对接近 $0$ 或 $1$ 的概率取对数。

若 $X\in\mathbb R^{N\times d}$ 每行一个样本，$y,p\in\mathbb R^N$：

$$
p=\sigma(Xw+b\mathbf1_N),
\qquad
\bar L=\frac1N\sum_{i=1}^N L_i.
$$

$$
\nabla_w\bar L=\frac1N X^T(p-y),
\qquad
\frac{\partial\bar L}{\partial b}
=\frac1N\mathbf1_N^T(p-y).
$$

$$
\nabla_w^2\bar L
=\frac1N X^T
\operatorname{diag}\big(p\odot(\mathbf1_N-p)\big)X
\succeq0.
$$

> Warning: $p-y$ 是“Sigmoid 与 Binary Cross Entropy 组合后”对 logit 的导数，不是单独的 BCE 对概率 $p$ 的导数。

## 14. Softmax + Cross Entropy

### 14.1 定义与推导

设 $z,p,y\in\mathbb R^K$，标签满足：

$$
y_i\ge0,\qquad\sum_i y_i=1.
$$

既可使用 one-hot 标签，也可使用归一化的软标签。

$$
p=\operatorname{softmax}(z),
\qquad
L=-\sum_i y_i\log p_i.
$$

由 $\log p_i=z_i-\log\sum_j e^{z_j}$：

$$
L=-y^Tz+\log\sum_j e^{z_j}.
$$

分别求导：

> **Key Formula**
>
> $$
> \nabla_zL=p-y\in\mathbb R^K.
> $$

**例：** 若 $p=(0.2,0.7,0.1)^T$、$y=(0,1,0)^T$，则：

$$
\nabla_zL=(0.2,-0.3,0.1)^T.
$$

梯度下降会提高正确类别的 logit，并降低另外两类的 logit。

### 14.2 线性分类头

设：

$$
h\in\mathbb R^d,\quad
W\in\mathbb R^{K\times d},\quad
b\in\mathbb R^K,\quad
z=Wh+b.
$$

令 $\delta=p-y\in\mathbb R^K$：

| 梯度 | 公式 | Shape |
|---|---|---|
| 对权重 | $\nabla_WL=\delta h^T=(p-y)h^T$ | $(K\times1)(1\times d)=K\times d$ |
| 对偏置 | $\nabla_bL=\delta=p-y$ | $K\times1$ |
| 对特征 | $\nabla_hL=W^T\delta=W^T(p-y)$ | $(d\times K)(K\times1)=d\times1$ |

> Warning: 若标签总和为 $\alpha=\sum_i y_i$ 而不是 $1$，则一般公式为 $\nabla_zL=\alpha p-y$。类别加权、样本加权以及求和 / 求平均也会改变相应系数。

> Note: 用 $L=\operatorname{LogSumExp}(z)-y^Tz$ 或稳定的 log-softmax 形式计算损失，可避免先求概率再取对数带来的数值问题。

## 15. Matrix Variable Derivatives

### 15.1 矩阵梯度的含义

对于标量函数 $f(X)$，$\nabla_Xf$ 收集对每个矩阵元素的偏导数，与 $X$ 同形状。求导时可用：

$$
df=\operatorname{tr}\big((\nabla_Xf)^T dX\big).
$$

### 15.2 Frobenius norm

设 $X\in\mathbb R^{r\times c}$：

$$
\lVert X\rVert_F^2
=\sum_{i,j}X_{ij}^2
=\operatorname{tr}(X^TX).
$$

$$
\nabla_X\lVert X\rVert_F^2=2X,
\qquad
\nabla_X\frac12\lVert X\rVert_F^2=X.
$$

输出均为标量，梯度均为 $r\times c$。这类公式直接用于权重的平方范数正则化。

### 15.3 Linear matrix form

设 $a\in\mathbb R^r$、$b\in\mathbb R^c$、$X\in\mathbb R^{r\times c}$：

$$
f(X)=a^TXb=\sum_{i,j}a_iX_{ij}b_j\in\mathbb R.
$$

$$
\nabla_Xf=ab^T\in\mathbb R^{r\times c}.
$$

这就是外积形式：第 $(i,j)$ 个元素为 $a_ib_j$。

### 15.4 Matrix least squares

以下 $A,B$ 均为常量，函数输出均为标量。

| 目标函数 | 维度约定 | 对 $X$ 的梯度 |
|---|---|---|
| $\lVert AX-B\rVert_F^2$ | $A:m\times n$，$X:n\times k$，$B:m\times k$ | $2A^T(AX-B)\in\mathbb R^{n\times k}$ |
| $\frac12\lVert AX-B\rVert_F^2$ | 同上 | $A^T(AX-B)\in\mathbb R^{n\times k}$ |
| $\lVert XA-B\rVert_F^2$ | $X:m\times n$，$A:n\times k$，$B:m\times k$ | $2(XA-B)A^T\in\mathbb R^{m\times n}$ |
| $\frac12\lVert XA-B\rVert_F^2$ | 同上 | $(XA-B)A^T\in\mathbb R^{m\times n}$ |

**直觉：** 参数 $X$ 在乘积中位于哪一侧，反向传播时就从对应一侧乘上另一个因子的转置。

> Warning: 本节按矩阵各元素独立变化求梯度。若用少量参数表示对称矩阵、低秩矩阵等，仍需对该参数化应用链式法则。

## 16. Trace Tricks

Trace 技巧把矩阵表达式改写成可识别的标量内积，便于提取梯度。

### 16.1 基本恒等式

若 $A\in\mathbb R^{m\times n}$、$B\in\mathbb R^{n\times m}$：

$$
\operatorname{tr}(AB)=\operatorname{tr}(BA).
$$

若 $A\in\mathbb R^{r\times s}$、$B\in\mathbb R^{s\times t}$、$C\in\mathbb R^{t\times r}$：

$$
\operatorname{tr}(ABC)
=\operatorname{tr}(BCA)
=\operatorname{tr}(CAB).
$$

还常用：

$$
\operatorname{tr}(M)=\operatorname{tr}(M^T),
\qquad
a^TXb=\operatorname{tr}(ba^TX).
$$

> Warning: Trace 内只能循环移动因子，不能随意交换顺序。一般 $\operatorname{tr}(ABC)\ne\operatorname{tr}(ACB)$。循环后的方阵大小可以不同，但每个乘积都必须有定义。

### 16.2 常用 Trace 导数

下列函数输出均为标量。

| 函数 | 梯度 | 维度与条件 |
|---|---|---|
| $\operatorname{tr}(A^TX)$ | $A$ | $A,X\in\mathbb R^{r\times c}$ |
| $\operatorname{tr}(X)$ | $I_n$ | $X\in\mathbb R^{n\times n}$ |
| $\operatorname{tr}(X^TAX)$ | $(A+A^T)X$ | $X\in\mathbb R^{n\times k}$，$A\in\mathbb R^{n\times n}$ |
| $\operatorname{tr}(X^TAX)$ | $2AX$ | 上一行且 $A=A^T$ |
| $\operatorname{tr}(X^TAXB)$ | $AXB+A^TXB^T$ | $X:n\times k$，$A:n\times n$，$B:k\times k$ |
| $\operatorname{tr}(X^TAXB)$ | $2AXB$ | 上一行且 $A,B$ 均对称 |

### 16.3 用微分提取梯度

对 $f(X)=\operatorname{tr}(X^TAXB)$：

$$
\begin{aligned}
df
&=\operatorname{tr}\big((dX)^TAXB\big)
+\operatorname{tr}\big(X^TA(dX)B\big)\\
&=\operatorname{tr}\big((AXB)^T dX\big)
+\operatorname{tr}\big((A^TXB^T)^T dX\big)\\
&=\operatorname{tr}\big((AXB+A^TXB^T)^T dX\big).
\end{aligned}
$$

与梯度定义比较即可读出结果。

> Note: 如果整理得到 $df=\operatorname{tr}(M\,dX)$，那么梯度是 $M^T$，不是 $M$。

## 17. Matrix Inverse and Determinant

本节 $X\in\mathbb R^{n\times n}$。逆矩阵输出为 $n\times n$；行列式及对数行列式输出为标量，矩阵梯度为 $n\times n$。

### 17.1 逆矩阵的微分

若 $X$ 可逆，由 $XX^{-1}=I_n$：

$$
(dX)X^{-1}+X\,d(X^{-1})=0.
$$

因此：

> **Key Formula**
>
> $$
> d(X^{-1})=-X^{-1}(dX)X^{-1}.
> $$

若 $X=X(t)$ 对标量 $t$ 可微且在所考虑点可逆：

$$
\frac{dX^{-1}}{dt}
=-X^{-1}\frac{dX}{dt}X^{-1}.
$$

> Warning: $d(X^{-1})$ 描述矩阵扰动对应的输出扰动，不是标量函数的矩阵梯度。一般不能把右边改成 $-X^{-2}dX$，因为矩阵未必可交换。

### 17.2 Determinant

当 $X$ 可逆：

$$
d(\det X)=\det(X)\operatorname{tr}(X^{-1}dX),
$$

$$
\nabla_X\det X=\det(X)X^{-T},
\qquad X^{-T}:=(X^{-1})^T.
$$

在奇异矩阵处，行列式依然可微，但上述含逆矩阵的表达式不能直接使用。一般公式是：

$$
\nabla_X\det X=\operatorname{adj}(X)^T,
$$

其中 $\operatorname{adj}(X)$ 是伴随矩阵，即代数余子式矩阵的转置。

### 17.3 Log determinant

实数函数 $\log\det X$ 的定义域要求 $\det X>0$：

$$
d(\log\det X)=\operatorname{tr}(X^{-1}dX),
$$

$$
\nabla_X\log\det X=X^{-T}.
$$

若进一步 $X=X^T$，则：

$$
\nabla_X\log\det X=X^{-1}.
$$

| 表达式 | 梯度 | 条件 |
|---|---|---|
| $\det X$ | $\det(X)X^{-T}$ | 此表达式要求 $X$ 可逆 |
| $\log\det X$ | $X^{-T}$ | $\det X>0$ |
| $\log\det X$ | $X^{-1}$ | $X=X^T$ 且 $\det X>0$；常用充分条件为 $X\succ0$ |
| $\log\lvert\det X\rvert$ | $X^{-T}$ | $\det X\ne0$ |

这些公式常见于 Gaussian models、协方差矩阵、概率机器学习及带 log-det 项的优化。

> Warning: 对称并不自动保证 $\log\det X$ 有定义。协方差场景通常要求严格正定；奇异的半正定矩阵有 $\det X=0$，不能直接代入 $\log\det X$。

## 18. Computational Graph and Backpropagation

### 18.1 前向计算图

设：

$$
x\in\mathbb R^n,\quad
W\in\mathbb R^{m\times n},\quad
b\in\mathbb R^m.
$$

$$
x
\xrightarrow{z=Wx+b}
z\in\mathbb R^m
\xrightarrow{a=\sigma(z)}
a\in\mathbb R^m
\xrightarrow{L=L(a)}
L\in\mathbb R.
$$

这里 Sigmoid 逐元素作用，$L$ 是可微标量损失。

### 18.2 从损失向前一层传播

已知上游梯度 $g_a=\nabla_aL\in\mathbb R^m$。激活层的 Jacobian 是对角矩阵，因此：

$$
g_z=\nabla_zL
=g_a\odot\sigma'(z)
=g_a\odot a\odot(\mathbf1_m-a).
$$

仿射层的微分为：

$$
dz=(dW)x+W\,dx+db.
$$

代入 $dL=g_z^Tdz$，分别收集 $dW$、$dx$、$db$ 的系数：

| 目标 | 反向公式 | Shape |
|---|---|---|
| 输入梯度 | $\nabla_xL=W^Tg_z$ | $n\times1$ |
| 权重梯度 | $\nabla_WL=g_zx^T$ | $m\times n$ |
| 偏置梯度 | $\nabla_bL=g_z$ | $m\times1$ |

对于权重的每个元素：

$$
\frac{\partial L}{\partial W_{ij}}
=\frac{\partial L}{\partial z_i}x_j.
$$

这解释了为什么权重梯度是“输出误差信号 × 输入”的外积。

> Note: Backpropagation 本质上是链式法则在计算图上的反向执行。前向阶段保存局部求导需要的值，反向阶段传播并累加梯度。

> Warning: 若损失还直接依赖 $x$ 或 $W$，例如额外加入正则项，则必须再加上直接依赖产生的梯度。

## 19. Matrix Multiplication Backward

### 19.1 定义与推导

设：

$$
Y=WX,\quad
W\in\mathbb R^{m\times d},\quad
X\in\mathbb R^{d\times N},\quad
Y\in\mathbb R^{m\times N}.
$$

本节采用 **batch 中每一列是一个样本** 的约定。已知标量损失对输出的梯度：

$$
G=\frac{\partial L}{\partial Y}
=\nabla_YL\in\mathbb R^{m\times N}.
$$

由：

$$
dY=(dW)X+W(dX),
$$

$$
\begin{aligned}
dL
&=\operatorname{tr}(G^TdY)\\
&=\operatorname{tr}\big((GX^T)^T dW\big)
+\operatorname{tr}\big((W^TG)^T dX\big),
\end{aligned}
$$

可得：

> **Key Formula**
>
> $$
> \frac{\partial L}{\partial W}=GX^T,
> \qquad
> \frac{\partial L}{\partial X}=W^TG.
> $$

### 19.2 Shape 检查与 bias

$$
\underbrace{G}_{m\times N}
\underbrace{X^T}_{N\times d}
=
\underbrace{\nabla_WL}_{m\times d},
$$

$$
\underbrace{W^T}_{d\times m}
\underbrace{G}_{m\times N}
=
\underbrace{\nabla_XL}_{d\times N}.
$$

若还有广播偏置 $b\in\mathbb R^m$：

$$
Y=WX+b\mathbf1_N^T,
\qquad
\nabla_bL=G\mathbf1_N\in\mathbb R^m.
$$

这表示对 batch 维求和。权重梯度也隐含样本贡献的累加：

$$
GX^T=\sum_{i=1}^N g_i x_i^T,
$$

其中 $g_i,x_i$ 分别为 $G,X$ 的第 $i$ 列。

> Warning: 若 $G$ 已经来自平均损失，其中已经包含 $1/N$，不要再次除以 $N$。若样本按行存储，前向公式和反向公式都应按新的布局重写。

## 20. Hadamard Product Backward

设 $x,y,z\in\mathbb R^n$，且没有广播：

$$
z=x\odot y,
\qquad z_i=x_iy_i.
$$

其局部 Jacobian 为：

$$
J_x=\operatorname{diag}(y),
\qquad
J_y=\operatorname{diag}(x).
$$

给定 $g=\nabla_zL\in\mathbb R^n$：

$$
\nabla_xL=g\odot y,
\qquad
\nabla_yL=g\odot x.
$$

输出梯度与各自变量均为 $n\times1$；同形状矩阵的逐元素乘法也使用相同规则。

**例：** $x=(2,3)^T$、$y=(4,5)^T$、$g=(1,2)^T$，则：

$$
\nabla_xL=(4,10)^T,
\qquad
\nabla_yL=(2,6)^T.
$$

> Warning: 若一个输入被广播，先按逐元素规则求贡献，再沿被广播的轴求和。例如 $z=sx$、$s$ 为标量时，$\partial L/\partial s=g^Tx$，结果必须是标量。

## 21. Addition Backward

### 21.1 相同形状的加法

若 $x,y,z\in\mathbb R^n$：

$$
z=x+y.
$$

因为两个局部 Jacobian 都是 $I_n$：

$$
\nabla_xL=\nabla_zL,
\qquad
\nabla_yL=\nabla_zL.
$$

同形状矩阵加法也如此：上游梯度原样传给每一个独立输入。

### 21.2 广播与重复使用

设 $Z=X+b\mathbf1_N^T$，其中 $X,Z,G\in\mathbb R^{m\times N}$、$b\in\mathbb R^m$，$G=\nabla_ZL$：

$$
\nabla_XL=G,
\qquad
\nabla_bL=G\mathbf1_N.
$$

偏置被使用了 $N$ 次，所以需要把这 $N$ 次贡献相加。

> Warning: 若 $z=x+x$，两个输入实际是同一个变量，则 $\nabla_xL=2\nabla_zL$。不能只保留其中一条路径。

## 22. JVP, VJP and HVP

这些乘积直接计算导数对某个向量的作用，常可避免存储巨大的 Jacobian 或 Hessian。

### 22.1 JVP：Jacobian-vector product

设 $f:\mathbb R^n\to\mathbb R^m$，$J_f(x)\in\mathbb R^{m\times n}$，输入方向 $v\in\mathbb R^n$：

$$
J_f(x)v\in\mathbb R^m.
$$

$$
J_f(x)v
=\left.\frac{d}{dt}f(x+tv)\right|_{t=0}.
$$

它回答：“输入沿 $v$ 变化时，输出的一阶变化是什么？”

**Forward-mode automatic differentiation** 沿前向计算传播方向扰动，直接计算 JVP。

### 22.2 VJP：Vector-Jacobian product

对输出侧向量 $u\in\mathbb R^m$：

$$
u^TJ_f(x)\in\mathbb R^{1\times n}.
$$

这就是常写作 $v^TJ$ 的 VJP；这里改用 $u$，是为了与 JVP 的输入方向区分。采用列梯度表示时，同一运算写为：

$$
J_f(x)^Tu\in\mathbb R^n.
$$

若 $u=\nabla_yL$、$y=f(x)$，则：

$$
\nabla_xL=J_f(x)^Tu.
$$

**Reverse-mode automatic differentiation / backpropagation** 通常实际计算的就是 VJP，并不显式构造完整 Jacobian。对标量损失，以 $\partial L/\partial L=1$ 为起点即可得到全部输入梯度。

### 22.3 HVP：Hessian-vector product

对二阶连续可微的标量函数 $f:\mathbb R^n\to\mathbb R$，设 $v\in\mathbb R^n$ 为与 $x$ 无关的固定向量：

$$
H_f(x)v\in\mathbb R^n.
$$

> **Key Formula**
>
> $$
> H_f(x)v
>=\nabla_x\left(\nabla_xf(x)^Tv\right).
> $$

因为 $H_f$ 对称，上式把 HVP 转为对一个标量内积再次求梯度。也可看作梯度函数的 JVP：

$$
H_f(x)v
=\left.\frac{d}{dt}\nabla_xf(x+tv)\right|_{t=0}.
$$

Newton-CG 等方法只需反复计算 $Hv$，即可近似求解 Newton 线性系统，无需存储 $n\times n$ 的完整 Hessian。

| 运算 | 输入侧向量 | 输出形状 | 常见用途 |
|---|---|---|---|
| JVP：$Jv$ | $v:n\times1$ | $m\times1$ | 前向自动微分、方向导数 |
| VJP：$u^TJ$ | $u:m\times1$ | $1\times n$；列形式为 $J^Tu$ | 反向传播 |
| HVP：$Hv$ | $v:n\times1$ | $n\times1$ | 二阶优化、曲率分析 |

> Warning: HVP 的内积求导公式要求 $v$ 对 $x$ 固定。若 $v=v(x)$，求导会多出 $J_v(x)^T\nabla f(x)$。

## 23. Convexity and Optimization

### 23.1 驻点、极小点与全局最优

考虑开域内可微的无约束问题：

$$
\min_x f(x).
$$

内点局部极小点必须满足一阶驻点条件：

$$
\nabla f(x^*)=0.
$$

| 条件 | 可以得出的结论 |
|---|---|
| $\nabla f(x^*)=0$ | 仅说明驻点，可能是极小点、极大点或鞍点 |
| $f$ 在开凸域上二阶连续可微，且所有点 $H(x)\succeq0$ | $f$ 为凸函数 |
| $f$ 凸且 $\nabla f(x^*)=0$ | $x^*$ 为全局最小点 |
| $\nabla f(x^*)=0$ 且 $H(x^*)\succ0$，并且邻域内二阶连续可微 | $x^*$ 为严格局部极小点 |
| $f$ 严格凸且最优解存在 | 全局最优解唯一 |

> Warning: 驻点处仅有 $H(x^*)\succeq0$ 还不够。例如 $f(x)=-x^4$ 在 $0$ 处梯度和 Hessian 都为零，却是严格局部极大点。反过来，$x^4$ 在 $0$ 处是严格极小点，但 Hessian 并不正定。

> Note: 边界最优点或约束优化问题通常不能直接要求 $\nabla f=0$，需考虑可行方向或约束最优性条件。

### 23.2 Gradient descent

设 $g_k=\nabla f(x_k)\in\mathbb R^n$：

$$
x_{k+1}=x_k-\eta_k g_k,
\qquad \eta_k>0.
$$

负梯度是欧氏意义下的最速下降方向。学习率 $\eta_k$ 控制步长；步长过大仍可能使损失上升。

### 23.3 Newton's method

Newton 方法最小化局部二次近似：

$$
f(x_k+s)\approx f(x_k)+g_k^Ts+\frac12s^TH_ks,
\qquad H_k=H_f(x_k).
$$

令该近似对 $s$ 的梯度为零：

$$
H_ks=-g_k.
$$

若 $H_k$ 可逆：

$$
x_{k+1}=x_k-H_k^{-1}g_k.
$$

实际实现求解线性系统 $H_ks=-g_k$，然后令 $x_{k+1}=x_k+s$，通常不显式计算逆矩阵。

> Warning: 若 $H_k$ 不正定，Newton 方向未必是下降方向；即使正定，完整步长也可能需要调整。非凸优化中常结合阻尼、线搜索或信赖域。

## 24. Dimension Checking

Shape 检查是发现漏转置、乘法次序和 batch 错误最快的方法之一。

### 24.1 先写目标形状

| 求导对象 | 必须得到的形状 |
|---|---|
| 标量 $f$ 对 $x\in\mathbb R^n$ 的梯度 | $n\times1$ |
| $f:\mathbb R^n\to\mathbb R^m$ 的 Jacobian | $m\times n$ |
| 标量 $f$ 对 $x\in\mathbb R^n$ 的 Hessian | $n\times n$ |
| 标量 $L$ 对 $W\in\mathbb R^{m\times n}$ 的梯度 | $m\times n$ |

### 24.2 最小二乘例子

设 $A\in\mathbb R^{m\times n}$、$x\in\mathbb R^n$、$b\in\mathbb R^m$：

$$
f(x)=\frac12\lVert Ax-b\rVert_2^2.
$$

先计算中间量：

$$
r=Ax-b\in\mathbb R^{m\times1}.
$$

目标是 $\nabla_xf\in\mathbb R^{n\times1}$，因此正确公式的 shape 为：

$$
\underbrace{A^T}_{n\times m}
\underbrace{(Ax-b)}_{m\times1}
=
\underbrace{\nabla_xf}_{n\times1}.
$$

若误写成 $A(Ax-b)$，当 $m\ne n$ 时，内维 $n$ 和 $m$ 不匹配，立即暴露错误。

### 24.3 矩阵乘法 backward 例子

设：

$$
W\in\mathbb R^{4\times3},
\quad X\in\mathbb R^{3\times8},
\quad Y=WX\in\mathbb R^{4\times8},
\quad G=\nabla_YL\in\mathbb R^{4\times8}.
$$

对权重：

$$
\nabla_WL=GX^T:
\qquad (4\times8)(8\times3)=4\times3.
$$

对输入：

$$
\nabla_XL=W^TG:
\qquad (3\times4)(4\times8)=3\times8.
$$

对偏置 $b\in\mathbb R^4$：

$$
\nabla_bL=G\mathbf1_8:
\qquad (4\times8)(8\times1)=4\times1.
$$

### 24.4 外积、内积与逐元素乘积

设 $u\in\mathbb R^m$、$v\in\mathbb R^n$：

| 表达式 | 输出形状 | 说明 |
|---|---|---|
| $uv^T$ | $m\times n$ | 外积，常用于权重梯度 |
| $u^Tv$ | 标量 | 要求 $m=n$，是内积 |
| $u\odot v$ | $n\times1$ | 无广播时要求 $m=n$ |

> Warning: Shape 正确只是必要条件。例如 $A$ 为方阵时，$Ax$ 与 $A^Tx$ 的形状完全相同；维度无法检查对称性、正负号、系数 $2$ 或遗漏的梯度路径。

## 25. Common Mistakes

| 常见错误 | 正确检查方式 |
|---|---|
| 1. 混淆 Gradient 和 Jacobian | 标量函数的 $J_f=(\nabla f)^T$；前者一行，后者一列 |
| 2. 忘记转置 | 梯度链式法则为 $J^Tg$；同时核对输入、输出维度 |
| 3. 随意交换矩阵乘法顺序 | 一般 $AB\ne BA$；Trace 也只能循环移动 |
| 4. 没有条件就默认 $A$ 对称 | 先用一般公式，再依据 $A=A^T$ 化简 |
| 5. 混淆逐元素乘法与矩阵乘法 | $\odot$ 逐元素作用；相邻书写的矩阵乘积需要收缩内维 |
| 6. 忽略 batch 维或广播 | 明确样本按行还是按列存储；广播变量的梯度需要沿扩展轴求和 |
| 7. 不检查最终梯度 shape | 标量损失对变量的梯度必须与变量同形状 |
| 8. 混用 numerator / denominator layout | 阅读教材时先看 $J_{ij}$ 的定义；不同布局可能使 Jacobian 整体转置 |
| 9. 显式构造巨大 Jacobian | 先判断是否只需要 JVP 或 VJP |
| 10. 对非对称 $A$ 使用 $2Ax$ | $\nabla_x(x^TAx)=(A+A^T)x$ |
| 11. 漏掉或重复使用平均因子 | 区分损失的 sum 与 mean；上游梯度可能已经包含 $1/N$ |
| 12. 把 $p-y$ 当成任何交叉熵的导数 | 先确认求导变量是 logits、标签归一化，以及是否加权 |
| 13. 在不可逆或无定义处套用公式 | 检查逆矩阵、$\log\det X$、$\ln x$ 等的使用条件 |
| 14. HVP 求导时让方向向量参与变化 | $\nabla_x(\nabla f^Tv)=Hv$ 要求 $v$ 对 $x$ 固定 |
| 15. 分支或共享参数只算一次梯度 | 对所有使用位置的梯度贡献求和 |

> Note: 数学列向量与代码中的一维数组不完全相同。许多数值库中，一维数组转置后 shape 不变；需要显式区分行、列时，应使用二维形状。

## 26. Machine Learning Formula Cheat Sheet — 最常用公式 Top 15

下表中未被求导的量均为常量。除 Jacobian 项外，函数或损失均为标量。

| # | 场景 | 核心公式 | 输入条件 → 导数形状 |
|---|---|---|---|
| 1 | 线性形式 | $\nabla_x(a^Tx)=a$ | $a,x\in\mathbb R^n$ → $n\times1$ |
| 2 | 平方范数 | $\nabla_x(x^Tx)=2x$ | $x\in\mathbb R^n$ → $n\times1$ |
| 3 | 一般二次型 | $\nabla_x(x^TAx)=(A+A^T)x$ | $A:n\times n$，$x:n\times1$ → $n\times1$ |
| 4 | 对称二次型 | $\nabla_x\frac12x^TAx=Ax$ | $A=A^T\in\mathbb R^{n\times n}$ → $n\times1$ |
| 5 | 最小二乘梯度 | $\nabla_x\frac12\lVert Ax-b\rVert_2^2=A^T(Ax-b)$ | $A:m\times n$，$x:n\times1$，$b:m\times1$ → $n\times1$ |
| 6 | 最小二乘 Hessian | $\nabla_x^2\frac12\lVert Ax-b\rVert_2^2=A^TA$ | 同上 → $n\times n$ |
| 7 | 仿射 Jacobian | $J_{Ax+b}=A$ | $\mathbb R^n\to\mathbb R^m$ → $m\times n$ |
| 8 | Jacobian 链式法则 | $J_{f\circ g}(x)=J_f(g(x))J_g(x)$ | $g:\mathbb R^n\to\mathbb R^m$，$f:\mathbb R^m\to\mathbb R^p$ → $p\times n$ |
| 9 | 梯度反向传播 | $\nabla_xL=J^T\nabla_yL$ | $y=g(x)$，$J=J_g(x):m\times n$ → $n\times1$ |
| 10 | Sigmoid | $\sigma'(x)=\sigma(x)(1-\sigma(x))$ | 标量输入 → 标量导数 |
| 11 | Softmax Jacobian | $J_{\mathrm{softmax}}=\operatorname{diag}(p)-pp^T$ | $p=\operatorname{softmax}(z)$，$z\in\mathbb R^K$ → $K\times K$ |
| 12 | Softmax + CE | $\nabla_zL=p-y$ | $p,y\in\mathbb R^K$，$y_i\ge0$，$\sum_i y_i=1$ → $K\times1$ |
| 13 | 矩阵平方范数 | $\nabla_X\frac12\lVert X\rVert_F^2=X$ | $X:r\times c$ → $r\times c$ |
| 14 | Trace 线性形式 | $\nabla_X\operatorname{tr}(A^TX)=A$ | $A,X:r\times c$ → $r\times c$ |
| 15 | Log determinant | $\nabla_X\log\det X=X^{-T}$ | $X:n\times n$，$\det X>0$ → $n\times n$；若 $X=X^T$，结果为 $X^{-1}$ |

## 附录：维度检查法 — 30 秒速检

遇到一个矩阵求导结果，按以下顺序检查：

1. **圈出被求导变量。** 对标量损失求梯度时，先写下变量的 shape，这就是最终答案必须具有的 shape。
2. **写出每个中间量的 shape。** 特别标清残差、logits、batch 轴和上游梯度。
3. **沿乘法逐项检查内维。** 转置交换行列；矩阵乘法满足 $(a\times b)(b\times c)=a\times c$。
4. **核对广播与累加。** 变量在哪个轴被重复使用，梯度就要沿该轴把贡献相加，最后恢复变量形状。
5. **最后检查公式条件。** Shape 无法替代对称性、可逆性、归一化条件、系数和正负号的检查。

记住三条最常用的形状路径：

$$
\underbrace{A^T}_{n\times m}
\underbrace{(Ax-b)}_{m\times1}
\longrightarrow
\underbrace{\nabla_xL}_{n\times1},
$$

$$
\underbrace{G}_{m\times N}
\underbrace{X^T}_{N\times d}
\longrightarrow
\underbrace{\nabla_WL}_{m\times d},
$$

$$
\underbrace{W^T}_{d\times m}
\underbrace{G}_{m\times N}
\longrightarrow
\underbrace{\nabla_XL}_{d\times N}.
$$

> **最终检查：梯度与变量同形状；Jacobian 是输出维度 × 输入维度；维度正确后，再确认数学条件。**
