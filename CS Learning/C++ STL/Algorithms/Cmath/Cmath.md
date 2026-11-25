---
title: Cmath — 数学函数
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
aliases:
  - Cmath
  - cmath
  - 数学函数
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `Cmath` — 数学函数

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/binary_search()/binary_search()|binary_search() — 二分查找]] · 下一篇：[[CS Learning/C++ STL/Algorithms/count()/count()|count() — 元素计数]]
> 源码：[[CS Learning/C++ STL/Algorithms/Cmath/Cmath.cpp|查看源码]]

> [!abstract] 本节概览
> 头文件 `#include <cmath>`（对应 C 语言 `<math.h>`）提供了丰富的标准数学运算函数，涵盖**基本运算、指数与对数、三角与双曲函数、取整与浮点拆分、以及浮点数特殊状态（`NaN`/`Inf`）检测**。绝大多数函数对 `float`、`double`、`long double` 均提供重载，单次调用时间复杂度为 $O(1)$。

## 常用函数分类速查

### 1. 基本数学函数

| 函数 | 功能说明 | 示例与返回值 |
| :--- | :--- | :--- |
| `abs(x)` | 计算 `x` 的绝对值（`<cmath>` 同时重载整数与浮点类型） | `abs(-5)` → `5`；`abs(-5.0)` → `5.0` |
| `fabs(x)` | 计算浮点数 `x` 的绝对值 | `fabs(-5.5)` → `5.5` |
| `fmod(x, y)` | 浮点取余（商向 $0$ 截断，$x - \text{trunc}(x/y)\cdot y$） | `fmod(5.3, 2)` → `1.3` |
| `remainder(x, y)` | IEEE 浮点取余（商向最近偶数取整，$x - n\cdot y$） | `remainder(5.5, 2)` → `-0.5` |
| `fmax(x, y)` | 返回 `x` 与 `y` 中的较大值（能正确忽略单个 `NaN`） | `fmax(3.5, 4.2)` → `4.2` |
| `fmin(x, y)` | 返回 `x` 与 `y` 中的较小值（能正确忽略单个 `NaN`） | `fmin(3.5, 4.2)` → `3.5` |
| `hypot(x, y)` | 计算 $\sqrt{x^2 + y^2}$（避免中间平方上溢/下溢） | `hypot(3, 4)` → `5` |

### 2. 指数与对数函数

| 函数 | 功能说明 | 示例与返回值 |
| :--- | :--- | :--- |
| `exp(x)` | 计算 $e^x$ | `exp(1)` → `2.71828...` |
| `log(x)` | 计算自然对数 $\ln x$（$x > 0$） | `log(2.71828)` → `≈ 1` |
| `log10(x)` | 计算常用对数 $\log_{10} x$（另有 `log2(x)` 计算 $\log_2 x$） | `log10(100)` → `2` |
| `pow(x, y)` | 计算幂 $x^y$ | `pow(2, 3)` → `8` |
| `sqrt(x)` | 计算平方根 $\sqrt{x}$（$x \ge 0$） | `sqrt(16)` → `4` |
| `cbrt(x)` | 计算立方根 $\sqrt[3]{x}$（支持负数） | `cbrt(27)` → `3` |
| `expm1(x)` | 计算 $e^x - 1$（$x$ 接近 $0$ 时精度更高） | `expm1(1)` → `1.71828...` |
| `log1p(x)` | 计算 $\ln(1 + x)$（适用于 $x$ 接近 $0$ 的情况，避免有效位损失） | `log1p(0.00001)` → `≈ 0.00001` |

### 3. 三角函数（参数与返回值均为弧度制）

| 函数 | 功能说明 | 示例与返回值 |
| :--- | :--- | :--- |
| `sin(x)` | 正弦 $\sin x$ | `sin(PI / 2)` → `1` |
| `cos(x)` | 余弦 $\cos x$ | `cos(PI)` → `-1` |
| `tan(x)` | 正切 $\tan x$ | `tan(0)` → `0` |
| `asin(x)` | 反正弦 $\arcsin x \in [-\pi/2, \pi/2]$（$x \in [-1, 1]$） | `asin(1)` → `≈ 1.5708`（$\pi/2$） |
| `acos(x)` | 反余弦 $\arccos x \in [0, \pi]$（$x \in [-1, 1]$） | `acos(-1)` → `≈ 3.14159`（$\pi$） |
| `atan(x)` | 反正切 $\arctan x \in (-\pi/2, \pi/2)$ | `atan(1)` → `≈ 0.7854`（$\pi/4$） |
| `atan2(y, x)` | 根据坐标 $(x, y)$ 计算极角 $\in [-\pi, \pi]$（可区分四象限且允许 $x = 0$） | `atan2(1, 1)` → `≈ 0.7854`（$\pi/4$） |

### 4. 双曲函数

| 函数 | 功能说明 | 示例与返回值 |
| :--- | :--- | :--- |
| `sinh(x)` | 双曲正弦 $\frac{e^x - e^{-x}}{2}$ | `sinh(0)` → `0` |
| `cosh(x)` | 双曲余弦 $\frac{e^x + e^{-x}}{2}$ | `cosh(0)` → `1` |
| `tanh(x)` | 双曲正切 $\frac{\sinh x}{\cosh x}$ | `tanh(1)` → `≈ 0.7616` |
| `asinh(x)` | 反双曲正弦 | `asinh(1)` → `≈ 0.8814` |
| `acosh(x)` | 反双曲余弦（定义域 $x \ge 1$） | `acosh(1)` → `0` |
| `atanh(x)` | 反双曲正切（定义域 $x \in (-1, 1)$） | `atanh(0.5)` → `≈ 0.5493` |

### 5. 取整与浮点数拆分

| 函数 | 功能说明 | 示例与返回值 |
| :--- | :--- | :--- |
| `ceil(x)` | 向上取整：返回不小于 `x` 的最小整数（浮点型） | `ceil(2.3)` → `3.0` |
| `floor(x)` | 向下取整：返回不大于 `x` 的最大整数（浮点型） | `floor(2.3)` → `2.0` |
| `trunc(x)` | 向零截断：直接舍去小数部分 | `trunc(2.8)` → `2.0`；`trunc(-2.8)` → `-2.0` |
| `round(x)` | 四舍五入到最接近整数（中点 `.5` 远离零舍入） | `round(2.5)` → `3.0` |
| `lround(x)` | 四舍五入并返回 `long` 整数 | `lround(2.5)` → `3L` |
| `llround(x)` | 四舍五入并返回 `long long` 整数 | `llround(2.5)` → `3LL` |
| `nearbyint(x)` | 按当前舍入模式取整（默认银行家舍入，不触发 `FE_INEXACT` 异常） | `nearbyint(2.5)` → `2.0` |
| `rint(x)` | 按当前舍入模式取整（可能触发 `FE_INEXACT` 浮点异常） | `rint(2.5)` → `2.0` |
| `modf(x, &intpart)` | 将 `x` 拆分为整数部分（写入 `intpart`）和小数部分（返回） | `modf(2.3, &ip)` → 返回 `0.3`，`ip = 2.0` |

### 6. 浮点数状态检查（C++11）

| 函数 | 功能说明 | 示例与返回值 |
| :--- | :--- | :--- |
| `isfinite(x)` | 检查 `x` 是否为有限数（既非 `Inf` 也非 `NaN`） | `isfinite(3.0)` → `true` |
| `isinf(x)` | 检查 `x` 是否为正/负无穷大 | `isinf(1.0 / 0.0)` → `true` |
| `isnan(x)` | 检查 `x` 是否为非数（`NaN`） | `isnan(0.0 / 0.0)` → `true` |
| `isnormal(x)` | 检查 `x` 是否为正常的非零有限浮点数（非 `0`、非次正规数、非 `Inf`/`NaN`） | `isnormal(1.0)` → `true` |
| `signbit(x)` | 检查 `x` 的符号位是否为负（包括 `-0.0`） | `signbit(-5.3)` → `true` |

## 常见易错点与注意事项

> [!note] 对原注释中两处细节的勘误说明
> 1. **`remainder(5.5, 2)` 的结果**：与 `fmod(5.5, 2) = 1.5` 不同，IEEE 标准的 `remainder` 将商 $5.5 / 2 = 2.75$ 四舍五入到最近整数 $3$，因此返回 $5.5 - 3 \times 2 = -0.5$（而非原表注释写的 `1.5`）。
> 2. **`rint(2.5)` 的结果**：`rint` 与 `nearbyint` 默认都采用 IEEE 754 的**向最近偶数舍入（Round-to-Nearest-Even）**，因此 `rint(2.5)` 默认返回 `2.0`；若希望 `.5` 始终向远离零方向四舍五入，应使用 `round(2.5)`（返回 `3.0`）。

> [!warning] 整数幂与 $\pi$ 常量的常见坑点
> - **慎用 `pow()` 计算大整数幂**：`pow(x, y)` 是浮点函数，对超过 $2^{53}$ 的 `long long` 会丢失精度，且有时出现 `pow(10, 2) = 99.999999` 强转 `int` 变 `99` 的误差。整数幂请手写循环或**快速幂**。
> - **$\pi$ 的标准写法**：`M_PI` 是 POSIX 扩展而非 ISO C++ 标准宏；C++11/17 中可定义 `const double PI = std::acos(-1.0);`，C++20 起可直接使用 `<numbers>` 中的 `std::numbers::pi`。
> - **角度与弧度转换**：所有三角函数均使用==弧度制==，角度转弧度公式为 $\text{rad} = \text{deg} \times \frac{\pi}{180}$。

## 完整源码

```cpp
/*
<cmath> 是一个包含数学函数的头文件,它提供了许多基本的数学运算和常数。
<cmath> 是 C++ 标准库中的一个头文件,它定义了一组数学函数,这些函数可以执行基本的数学运算,如幂运算、三角函数、对数、绝对值等。

头文件 #include <cmath>

1.基本数学函数
函数	            功能	                    示例
abs(x)	        计算整数 x 的绝对值	            abs(-5)             // 5
fabs(x)	        计算浮点数 x 的绝对值	        fabs(-5.5)          // 5.5
fmod(x,y)	    计算 x 除以 y 的余数	        fmod(5.3,2)        // 1.3
remainder(x,y)	计算 x 除以 y 的余数	        remainder(5.5,2)   // 1.5
fmax(x,y)	    返回 x 和 y 中的较大值	        fmax(3.5,4.2)      // 4.2
fmin(x,y)	    返回 x 和 y 中的较小值	        fmin(3.5,4.2)      // 3.5
hypot(x,y)	    计算 sqrt(x*x + y*y)	       hypot(3,4)         // 5

2. 指数和对数函数
函数	            功能	                    示例
exp(x)	        计算 e^x,e 为自然对数的底数     exp(1)              // 2.71828...
log(x)	        计算 x 的自然对数	            log(2.71828)        // 1
log10(x)	    计算 x 的以 10 为底的对数	    log10(100)          // 2
pow(x,y)	    计算 x 的 y 次方	            pow(2,3)           // 8
sqrt(x)	        计算 x 的平方根	                sqrt(16)           // 4
cbrt(x)	        计算 x 的立方根	                cbrt(27)           // 3
expm1(x)	    计算 e^x - 1	               expm1(1)           // 1.71828...
log1p(x)	    计算 log(1 + x),             log1p(0.00001)       // 0.00001
            (适用于 x 接近 0 的情况)

3. 三角函数
函数	            功能	                    示例
sin(x)	        计算 x 的正弦值,x 以弧度为单位	sin(3.14159/2)    // 1
cos(x)	        计算 x 的余弦值,x 以弧度为单位	cos(3.14159)        // -1
tan(x)	        计算 x 的正切值,x 以弧度为单位	tan(0)              // 0
asin(x)	        计算 x 的反正弦值,返回弧度	    asin(1)             // 3.14159/2
acos(x)	        计算 x 的反余弦值,返回弧度	    acos(-1)            // 3.14159
atan(x)	        计算 x 的反正切值,返回弧度	    atan(1)             // 3.14159/4
atan2(y,x)	    计算 y/x 的反正切值,返回弧度	atan2(1,1)          // 3.14159/4

4. 双曲函数
函数	            功能	                    示例
sinh(x)	        计算 x 的双曲正弦	            sinh(0)             // 0
cosh(x)	        计算 x 的双曲余弦	            cosh(0)             // 1
tanh(x)	        计算 x 的双曲正切	            tanh(1)             // 0.7616
asinh(x)	    计算 x 的反双曲正弦	            asinh(1)            // 0.8814
acosh(x)	    计算 x 的反双曲余弦,x ≥ 1	    acosh(1)            // 0
atanh(x)	    计算 x 的反双曲正切,x 在(-1,1)  atanh(0.5)          // 0.5493

5. 取整和浮点数操作
函数	            功能	                    示例
ceil(x)	        返回不小于 x 的最小整数	        ceil(2.3)           // 3
floor(x)	    返回不大于 x 的最大整数	        floor(2.3)          // 2
trunc(x)	    返回去除小数部分的整数值	    trunc(2.8)          // 2
round(x)	    返回四舍五入到最接近的整数	    round(2.5)          // 3
lround(x)	    返回四舍五入到 long 类型	    lround(2.5)         // 3
llround(x)	    返回四舍五入到 long long 类型	llround(2.5)        // 3
nearbyint(x)	返回舍入到最接近整数(无浮点异常) nearbyint(2.5)      // 2
rint(x)	        返回四舍五入到整数	            rint(2.5) // 3
modf(x,&intpart)将 x 的整数和小数部分分离	    modf(2.3,&intpart)

6. 浮点数检查
函数	            功能	                    示例
isfinite(x)	    检查 x 是否为有限值(非NaN)	    isfinite(3.0)        // true
isinf(x)	    检查 x 是否为无穷大	            isinf(1.0/0.0)     // true
isnan(x)	    检查 x 是否为 NaN	            isnan(0.0/0.0)    // true
isnormal(x)	    检查 x 是否为正常的非零浮点数	 isnormal(1.0)        // true
signbit(x)	    检查 x 的符号是否为负	        signbit(-5.3)        // true
*/
#include <iostream>
#include <cmath> // 包含 <cmath> 头文件
#define PI 3.14159
using namespace std;
int main(){
    double num = 9.0;
    double root = sqrt(num); // 计算平方根
    double sinValue = sin(PI/2); // 计算正弦值，M_PI 是 π 的近似值
    double absValue = abs(-5.0); // 计算绝对值
    cout<<"The square root of "<<num<<" is "<<root<<endl;
    cout<<"The sine of "<<PI/2<<" is "<<sinValue<<endl;
    cout<<"The absolute value of -5.0 is "<<absValue<<endl;
    // 基本数学运算
    cout<<"abs(-5) = "<<abs(-5)<<endl;
    cout<<"fmod(5.3, 2) = "<<fmod(5.3, 2)<<endl;
    // 指数和对数函数
    cout<<"exp(1) = "<<exp(1)<<endl;
    cout<<"log(2.71828) = "<<log(2.71828)<<endl;
    cout<<"pow(2, 3) = "<<pow(2, 3)<<endl;
    // 三角函数
    cout<<"sin(3.14159/2) = "<<sin(3.14159/2)<<endl;
    cout<<"cos(3.14159) = "<<cos(3.14159)<<endl;
    // 取整函数
    cout<<"ceil(2.3) = "<<ceil(2.3)<<endl;
    cout<<"floor(2.3) = "<<floor(2.3)<<endl;
    // 浮点数检查
    double x = 1.0/0.0;
    if (isinf(x)){
        cout<<"x is infinite"<<endl;
    }
    return 0;
}
```
