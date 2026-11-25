---
title: Random — 随机数
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
  - Random
  - random
  - mt19937
  - random_device
  - 随机数
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `Random` — 随机数

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/prev_permutation() next_permutation()/prev_permutation() next_permutation()|prev_permutation() next_permutation() — 字典序排列]] · 下一篇：[[CS Learning/C++ STL/Algorithms/reverse()/reverse()|reverse() — 反转序列]]
> 源码：[[CS Learning/C++ STL/Algorithms/Random/Random.cpp|查看源码]]

> [!abstract] 本节概览
> C++11 引入的头文件 `#include <random>` 将随机数生成拆分为==随机数引擎（Engine）==、==随机数分布（Distribution）==与==引擎适配器（Adaptor）==三大正交组件，全面替代了 C 语言时代周期短、均匀性差且范围受限的 `rand()` / `srand()`。

## 核心架构：种子 → 引擎 → 分布

```mermaid
flowchart LR
    Seed["随机种子 (random_device 或 steady_clock)"] --> Eng["伪随机数引擎 (如 mt19937)"]
    Eng --> Dist["概率分布 (如 uniform_int_distribution)"]
    Dist --> Val["目标区间随机数"]
```

- **伪随机数生成器（PRNG）**：基于确定性数学算法生成近似随机的序列；相同种子能完全复现结果，非常适合仿真实验与算法对拍。
- **真随机数生成器（TRNG）**：依赖物理熵源（热噪声等）；C++ 标准库提供 `std::random_device` 尝试访问系统熵源（主要用于为伪随机数引擎提供种子，不建议高频直接调用）。
- **引擎适配器**：包装底层引擎以调整输出特性（如 `discard_block_engine`、`shuffle_order_engine`）。

## 常用随机数引擎与分布速查

### 1. 标准随机数引擎

| 引擎名称 | 底层算法与特点 | 推荐场景 |
| :--- | :--- | :--- |
| `std::mt19937` | 32 位梅森旋转算法（Mersenne Twister），周期长达 $2^{19937}-1$，速度与质量兼优 | ==日常开发与算法竞赛首选== |
| `std::mt19937_64` | 64 位梅森旋转算法，直接输出 `uint64_t` | 需要 64 位大范围随机数、随机哈希 |
| `std::default_random_engine` | 实现定义的默认引擎（不同编译器底层不同） | 简单演示（跨平台复现性不如 `mt19937`） |
| `std::minstd_rand` | 线性同余引擎（LCG），状态极小、速度快 | 内存极度受限的轻量场景 |
| `std::ranlux24_base` | 简化减法进位引擎（Subtract-with-carry） | 配合适配器追求高统计质量 |
| `std::knuth_b` | 基于 `minstd_rand0` 的 Knuth Shuffle 适配器引擎 | 历史/特定统计仿真需求 |

### 2. 常用随机数分布

| 分布类 | 区间 / 参数含义 | 示例 |
| :--- | :--- | :--- |
| `std::uniform_int_distribution<int>(L, R)` | 离散均匀分布，**闭区间 `[L, R]`** | 模拟掷骰子 `(1, 6)` |
| `std::uniform_real_distribution<double>(L, R)` | 连续均匀分布，**左闭右开 `[L, R)`** | 生成 `[0.0, 1.0)` 随机概率 |
| `std::normal_distribution<double>(mu, sigma)` | 正态（高斯）分布 $\mathcal{N}(\mu, \sigma^2)$ | 噪声模拟与统计采样 |
| `std::bernoulli_distribution(p)` | 伯努利分布，以概率 `p` 返回 `true` | 随机事件触发 |

## 典型用法：标准三步写法

```cpp
#include <iostream>
#include <random>

int main() {
    // 1. 获取随机种子并初始化 32 位梅森旋转引擎
    std::random_device rd;
    std::mt19937 gen(rd());

    // 2. 定义目标分布（例如闭区间 [1, 100] 的均匀整数）
    std::uniform_int_distribution<int> dist(1, 100);

    // 3. 将引擎传入分布对象生成随机数
    for (int i = 0; i < 5; ++i) {
        std::cout << dist(gen) << ' ';
    }
}
```

## 常见易错点与注意事项

> [!warning] 不要用 `gen() % N` 替代分布类，且不要在循环内重复创建引擎
> - **取模偏差（Modulo Bias）**：直接写 `gen() % N` 在 $N$ 不能整除引擎值域时会导致较小数值出现概率偏高，应当使用 `std::uniform_int_distribution`。
> - **引擎只需初始化一次**：将 `mt19937 gen(...)` 放在循环外部（或声明为 `static`），在循环内部反复重新播种不仅极慢，还可能因种子相同导致每次生成一样的数。

> [!tip] 跨平台可靠播种与安全边界
> - **旧版 MinGW-GCC 的 `random_device` 陷阱**：部分旧版 Windows MinGW 中 `std::random_device` 可能退化为固定伪随机序列；若需稳定随时间变化的种子，可使用 `std::chrono::steady_clock::now().time_since_epoch().count()`。
> - **不可用于密码学安全场景**：`mt19937` 虽统计性质优秀，但观察 624 个连续输出即可反推内部状态，**严禁用于密钥、令牌等加密安全用途**。

## 完整源码

```cpp
/*
<random> 头文件提供了一组用于生成随机数的工具，涵盖了从简单的均匀分布到复杂的离散分布，
为需要随机数的应用程序提供了广泛的选择。这些工具对于模拟、游戏开发、加密算法等领域非常有用。
<random> 不仅支持生成伪随机数，还支持种子控制、各种概率分布等，使得开发者可以灵活地生成符合特定需求的随机数序列。

<random> 库由以下三个主要组件构成：
随机数引擎：生成伪随机数的核心，用于控制生成过程的可重复性和随机性。
随机数分布：控制生成的数值遵循的概率分布类型。
随机数适配器：允许调整引擎行为，如 discard_block 等适配器。

在 C++ 中，随机数生成器（Random Number Generator, RNG）可以分为两大类：
伪随机数生成器：它们使用确定性算法生成看似随机的数列。这些数列在理论上是可预测的，但通常对于大多数应用来说足够随机。
真随机数生成器：它们基于物理过程（如热噪声、放射性衰变等）生成随机数，但 C++ 标准库不直接提供这类生成器。

常用随机数引擎
引擎	                            描述
default_random_engine	默认随机数引擎，实现依赖于具体编译器。
minstd_rand	        线性同余引擎，产生均匀的伪随机数序列。
mt19937	            梅森旋转算法，适合通用随机数生成。
mt19937_64	            64位的梅森旋转算法。
ranlux24_base	        简化的减法进位引擎，用于高质量生成。
knuth_b	            Knuth shuffle 随机数生成器。

使用 <random> 库的基本步骤如下：
包含头文件 <random>。
创建一个随机数生成器对象。
使用分布类生成随机数。
*/
#include <iostream>
#include <random>
using namespace std;
int main() {
    // 使用随机设备创建一个随机种子
    random_device rd;
    // 使用随机种子初始化 Mersenne Twister 随机数生成器
    mt19937 generator(rd());
    // 生成一个随机数
    cout<<"Random number: "<<generator()<<endl;
    return 0;
}
```
