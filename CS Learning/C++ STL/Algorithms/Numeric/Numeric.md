---
title: Numeric — 数值算法
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
  - Numeric
  - numeric
  - accumulate
  - iota
  - partial_sum
  - gcd
  - lcm
  - 数值算法
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `Numeric` — 数值算法

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/max() min() max_element() min_element()/max() min() max_element() min_element()|max() min() max_element() min_element() — 最值与最值位置]] · 下一篇：[[CS Learning/C++ STL/Algorithms/prev_permutation() next_permutation()/prev_permutation() next_permutation()|prev_permutation() next_permutation() — 字典序排列]]
> 源码：[[CS Learning/C++ STL/Algorithms/Numeric/Numeric.cpp|查看源码]]

> [!abstract] 本节概览
> 头文件 `#include <numeric>` 提供了一组面向迭代器区间的通用数值算法，覆盖**序列累加（`accumulate`）、内积（`inner_product`）、前缀和（`partial_sum`）、相邻差分（`adjacent_difference`）、连续递增填充（`iota`）**以及 C++17 新增的**最大公约数（`gcd`）与最小公倍数（`lcm`）**。

## 常用函数与复杂度速查

| 函数 | 常用原型 | 功能与典型用途 | 标准版本 | 时间复杂度 |
| :--- | :--- | :--- | :---: | :---: |
| `accumulate` | `T accumulate(first, last, T init [, op])` | 计算区间累加和（或自定义二元规约，如连乘） | C++98 | $O(n)$ |
| `inner_product` | `T inner_product(b1, e1, b2, T init [, op1, op2])` | 计算两序列内积 $\text{init} + \sum a_i b_i$（向量点积、加权求和） | C++98 | $O(n)$ |
| `partial_sum` | `OutIt partial_sum(first, last, d_first [, op])` | 计算前缀和数组（第 $k$ 项为前 $k$ 项之和），返回输出尾后迭代器 | C++98 | $O(n)$ |
| `adjacent_difference` | `OutIt adjacent_difference(first, last, d_first [, op])` | 计算差分数组（首项为 `a[0]`，其余为 `a[i] - a[i-1]`），返回输出尾后迭代器 | C++98 | $O(n)$ |
| `iota` | `void iota(first, last, T init)` | 用 `init, init+1, ...` 连续递增填充区间（如并查集/索引初始化） | C++11 | $O(n)$ |
| `gcd` | `common_type_t<M,N> gcd(M a, N b)` | 计算两个整数的最大公约数 $\gcd(a, b)$ | C++17 | $O(\log \min(a, b))$ |
| `lcm` | `common_type_t<M,N> lcm(M a, N b)` | 计算两个整数的最小公倍数 $\operatorname{lcm}(a, b)$ | C++17 | $O(\log \min(a, b))$ |

## 典型用法与示例拆解

### 1. 累加、自定义规约与向量内积

```cpp
#include <numeric>
#include <functional>
#include <vector>

std::vector<int> v = {1, 2, 3, 4, 5};
int sum = std::accumulate(v.begin(), v.end(), 0);                           // 15
long long prod = std::accumulate(v.begin(), v.end(), 1LL, std::multiplies<>()); // 120

std::vector<int> v1 = {1, 2, 3}, v2 = {4, 5, 6};
int dot = std::inner_product(v1.begin(), v1.end(), v2.begin(), 0);          // 1*4 + 2*5 + 3*6 = 32
```

### 2. 前缀和、差分与连续序列初始化

```cpp
std::vector<int> a = {1, 2, 3, 4};

// 前缀和：result0 = {1, 3, 6, 10}（也支持原地覆盖 partial_sum(a.begin(), a.end(), a.begin())）
std::vector<int> pre(a.size());
std::partial_sum(a.begin(), a.end(), pre.begin());

// 相邻差分：diff = {1, 1, 1, 1}（注意长度与原数组相同！）
std::vector<int> diff(a.size());
std::adjacent_difference(a.begin(), a.end(), diff.begin());

// 递增填充：idx = {1, 2, 3, 4, 5}
std::vector<int> idx(5);
std::iota(idx.begin(), idx.end(), 1);
```

### 3. 最大公约数与最小公倍数（C++17）

```cpp
int g = std::gcd(48, 18);  // 6
int l = std::lcm(48, 18);  // 144
```

## 常见易错点与注意事项

> [!warning] `adjacent_difference()` 输出长度等于原序列长度 $n$（而非 $n - 1$）
> `std::adjacent_difference(first, last, d_first)` 会依次写入 **$n$ 个元素**：
> - `d[0] = a[0]`（保留首元素，使差分与前缀和互为逆运算）
> - `d[i] = a[i] - a[i - 1]`（$1 \le i < n$）
>
> **源码细节提醒**：文末原源码中写了 `vector<int> result1(v4.size() - 1);`，目标缓冲区比实际写入少 1 个元素，会触发越界写入（未定义行为）。实战中目标容器必须至少分配 `v4.size()` 个元素（或使用 `std::back_inserter(result1)`）。

> [!warning] `accumulate()` 的累加类型完全由初始值 `init` 的类型决定
> 即使容器元素是 `long long` 或 `double`，若把初始值写成整型字面量 `0`，`std::accumulate` 也会按 `int` 累加，导致**整数溢出或小数截断**！
> - 对大整数求和务必写 `0LL`：`accumulate(v.begin(), v.end(), 0LL)`；
> - 对浮点数求和务必写 `0.0`：`accumulate(v.begin(), v.end(), 0.0)`。

> [!note] 原注释函数签名勘误
> 文末原始学习注释中的简写原型与标准库实际签名略有出入：
> - `std::gcd` 与 `std::lcm` 返回两个参数公共整型（非 `void`）；
> - `std::partial_sum` 与 `std::adjacent_difference` 返回输出区间的尾后迭代器（非 `void`）；
> - `std::inner_product` 至少需要 **4 个参数**（`b1, e1, b2, init`），其中第二个序列只需提供起始迭代器 `b2`（调用者需确保其长度不少于第一个序列）。

## 完整源码

```cpp
/*
<numeric> 头文件提供了一组用于数值计算的函数模板
这些函数可以对容器中的元素进行各种数值操作，如求和、乘积、最小值、最大值等。
这些函数模板非常强大，可以应用于任何类型的容器，包括数组、向量、列表等。

头文件 #include <numeric>

1.accumulate    函数
计算序列的累加和（可自定义二元操作）它接受三个参数：容器的开始迭代器、结束迭代器和初始值。
    int accumulate(iterator beg,iterator end,int init);
    可用于求数组总和、统计累计值

2.inner_product 函数
计算两个序列的内积（对应元素相乘后累加，可自定义操作） 它接受三个参数：容器的开始迭代器、结束迭代器和初始值。
    int inner_product(iter1 b1,iter1 e1,iter2 b2,int init);
    可用于向量点积、加权求和

3.partial_sum   函数
计算序列的前缀和（第n个结果=前n个元素的和，可自定义操作）
    void partial_sum(iter b,iter e,iter res);
    可用于生成前缀和数组、累积统计

4.adjacent_difference   函数
计算序列相邻元素的差值（第n个结果=elem[n]-elem[n-1]，可自定义操作）
    void adjacent_difference(iter b,iter e,iter res);
    可用于计算差分、检测序列变化量

5.gcd   函数
计算两个整数的最大公约数
    void gcd (int a,int b);

6.lcm   函数
计算两个整数的最小公倍数：
    void lcm (int a,int b);

7.iota  函数
用连续递增的值填充序列（从 init 开始，逐个+1）
    void iota(iter b,iter e,T init);
    可用于生成连续整数序列、初始化有序容器
*/
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
int main(){
    //accumulate
    vector<int> v0={1,2,3,4,5};
    int sum=accumulate(v0.begin(),v0.end(),0);
    cout<<"Sum: "<<sum<<endl; // 输出: Sum: 15
    //inner_product
    vector<int> v1={1,2,3};
    vector<int> v2={4,5,6};
    int product_sum=inner_product(v1.begin(),v1.end(),v2.begin(),0);
    cout<<"Product Sum: "<<product_sum<<endl; // 输出: Product Sum: 32
    //partial_sum
    vector<int> v3={1,2,3,4};
    vector<int> result0(v3.size());
    partial_sum(v3.begin(),v3.end(),result0.begin());
    for (int i:result0){
        cout<<i<<" "; // 输出: 1 3 6 10
    }
    cout<<endl;
    //adjacent_difference
    vector<int> v4={1,2,3,4};
    vector<int> result1(v4.size() - 1);
    adjacent_difference(v4.begin(),v4.end(),result1.begin());
    for (int i:result1){
        cout<<i<<" "; // 输出: 1 1 1
    }
    cout<<endl;
    //gcd、lcm
    int a=48;
    int b=18;
    int result2=gcd(a,b);  // 计算 48 和 18 的最大公约数
    cout<<"GCD: "<<result2<<endl;  // 输出 6
    int result3=lcm(a,b);  // 计算 48 和 18 的最小公倍数
    cout<<"LCM: "<<result3<<endl;
    //iota
    vector<int> v5(5); // 创建一个包含5个元素的向量
    // 使用 iota 填充向量，起始值为1
    iota(begin(v5),end(v5),1);
    // 输出填充后的向量
    for (int i:v5){
        cout<<i<<" ";
    }
    cout<<endl; // 输出: 1 2 3 4 5
    return 0;
}
```
