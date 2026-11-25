---
title: fill() fill_n() — 序列填充
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
  - fill
  - fill_n
  - fill()
  - fill_n()
  - 序列填充
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `fill()` & `fill_n()` — 序列填充

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/count()/count()|count() — 元素计数]] · 下一篇：[[CS Learning/C++ STL/Algorithms/find()/find()|find() — 查找元素]]
> 源码：[[CS Learning/C++ STL/Algorithms/fill() fill_n()/fill() fill_n().cpp|查看源码]]

> [!abstract] 本节概览
> `std::fill()` 和 `std::fill_n()` 定义在头文件 `#include <algorithm>` 中，用于将指定值批量写入一段序列：`fill()` 按==区间 `[first, last)`== 填充，`fill_n()` 按==起始位置与个数 `n`== 填充。两者时间复杂度均为 $O(n)$，按元素类型安全赋值，适用于任意可赋值类型。

## 核心语法与接口对比

| 函数 | 原型 | 填充范围 | 返回值 | 时间复杂度 |
| :--- | :--- | :--- | :--- | :---: |
| `std::fill` | `void fill(ForwardIt first, ForwardIt last, const T& val)` | 左闭右开区间 `[first, last)` | `void` | $O(n)$ |
| `std::fill_n` | `OutputIt fill_n(OutputIt first, Size count, const T& val)` | 从 `first` 起的连续 `count` 个位置 | 指向最后一个写入元素之后的迭代器（C++11） | $O(\text{count})$ |

参数含义：
- `first`：指向被填充区域起始位置的迭代器（包含）。
- `last`（仅 `fill`）：指向被填充区域结束位置的迭代器（不包含）。
- `count`（仅 `fill_n`）：要填充的元素个数（若 `count <= 0` 则不执行任何操作）。
- `val`：用于填充的新值。

## 典型用法与实战模式

### 1. 填充整个 `vector` 或普通数组

```cpp
#include <algorithm>
#include <vector>

std::vector<int> vec(5);                  // 必须先分配好空间
std::fill(vec.begin(), vec.end(), 9);     // 结果：{9, 9, 9, 9, 9}

int arr[10];
std::fill(arr, arr + 10, -1);             // 普通数组同样适用
std::fill_n(arr, 4, 42);                  // 仅将前 4 个元素改为 42
```

### 2. 对空容器使用 `fill_n()`（搭配插入迭代器）

当目标容器尚未预分配元素时，可以配合 `<iterator>` 中的 `std::back_inserter` 动态追加元素：

```cpp
#include <algorithm>
#include <iterator>
#include <vector>

std::vector<int> v;
std::fill_n(std::back_inserter(v), 5, 9); // 向空 vector 尾部追加 5 个 9
```

## 常见易错点与注意事项

> [!warning] `fill_n()` 不会自动扩容，越界写入会导致未定义行为
> 如果对空的 `vector<int> v;` 直接调用 `fill_n(v.begin(), 5, 9)`，会产生**内存越界（UB）**。使用 `fill()` / `fill_n()` 前，必须保证目标位置已存在足够元素（例如先 `vector<int> v(5)` 或 `v.resize(5)`），或者使用 `std::back_inserter(v)`。

> [!tip] 为什么优先用 `std::fill()` 替代 `memset()`？
> `memset()` 是按**字节（Byte）**填充内存的：
> - `memset(a, 0, sizeof(a))` 和 `memset(a, -1, sizeof(a))` 对 `int` 有效，但 `memset(a, 1, sizeof(a))` 会把每个 `int` 填成 `0x01010101`（即 `16843009`），且无法用于 `double`、`std::string` 或非平凡类对象。
> - `std::fill()` 按元素类型调用赋值运算符，==可安全填充任意整数、浮点数及自定义对象==。

## 完整源码

```cpp
/*
fill() 和 fill_n() 算法提供了一种为元素序列填入给定值的简单方式，fill() 会填充整个序列
fill_n() 则以给定的迭代器为起始位置，为指定个数的元素设置值。

语法:
fill(ForwardIterator first,ForwardIterator last,const T& val);
    first： 指向填充区域开始位置的迭代器（包含）。
    last：  指向填充区域结束位置的迭代器（不包含）。
    val：   用来填充的新值。
fill_n() 的参数分别是指向被修改序列的第一个元素的正向迭代器、被修改元素的个数以及要被设置的值。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
    vector<int> vec(5); // 创建一个包含 5 个元素的 vector
    // 将整个 vector 填充为 9
    fill(vec.begin(),vec.end(),9);
    for(int x : vec){
        cout<<x<<" ";
    }
    return 0;
}
```
