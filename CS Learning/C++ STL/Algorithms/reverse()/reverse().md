---
title: reverse() — 反转序列
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
  - reverse
  - reverse()
  - reverse_copy
  - 反转序列
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `reverse()` — 反转序列

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/Random/Random|Random — 随机数]] · 下一篇：[[CS Learning/C++ STL/Algorithms/shuffle()/shuffle()|shuffle() — 随机打乱]]
> 源码：[[CS Learning/C++ STL/Algorithms/reverse()/reverse().cpp|查看源码]]

> [!abstract] 本节概览
> `std::reverse()` 定义在头文件 `#include <algorithm>` 中，用于将左闭右开区间 `[first, last)` 内的元素==原地反转==。它通过首尾双指针向中间逐对交换实现，时间复杂度为 $O(n)$（精确执行 $\lfloor n / 2 \rfloor$ 次交换），额外空间复杂度为 $O(1)$。

## 核心语法与迭代器要求

```cpp
#include <algorithm>

void reverse(BidirectionalIt first, BidirectionalIt last);
```

| 项目 | 说明 |
| :--- | :--- |
| **作用范围** | 左闭右开区间 `[first, last)`，原地修改原序列 |
| **迭代器要求** | 至少支持**双向迭代器（BidirectionalIterator）** |
| **支持的容器 / 类型** | `vector`、`string`、`deque`、`array`、`list`、C 风格普通数组 |
| **不支持的容器** | `forward_list`（单向链表，需用成员函数 `fl.reverse()`）、`set`/`map`（键有序不可逆转） |
| **复杂度** | 时间 $O(n)$，额外空间 $O(1)$ |

## 典型用法与实战模式

### 1. 整体反转与局部子区间反转

```cpp
#include <algorithm>
#include <string>
#include <vector>

std::vector<int> v = {1, 2, 3, 4, 5};
std::reverse(v.begin(), v.end());          // 整体反转：{5, 4, 3, 2, 1}
std::reverse(v.begin() + 1, v.begin() + 4); // 局部反转下标 [1, 4)：{5, 2, 3, 4, 1}

std::string s = "algorithm";
std::reverse(s.begin(), s.end());          // "mhtirogla"
```

### 2. 三次反转实现循环左移 $k$ 位

将序列 `[0, n)` 循环左移 $k$ 位（等价于 `std::rotate(v.begin(), v.begin() + k, v.end())`），只需对前 $k$ 个、后 $n - k$ 个以及整体各做一次 `reverse()`，时间 $O(n)$、空间 $O(1)$：

```cpp
k %= n;
std::reverse(v.begin(), v.begin() + k);
std::reverse(v.begin() + k, v.end());
std::reverse(v.begin(), v.end());
```

### 3. 不修改原序列：`std::reverse_copy()`

若需保留原序列并将反转结果写入新容器，可使用 `std::reverse_copy(first, last, d_first)`。

## 常见易错点与注意事项

> [!warning] 注意 `forward_list` 与 `list` 的差异
> - `std::forward_list` 仅提供前向迭代器，无法调用 `std::reverse()`，必须调用其成员函数 `fl.reverse()`。
> - `std::list` 虽可调用 `std::reverse()`（交换元素值），但其成员函数 `lst.reverse()` 仅重连节点指针，对大型对象更高效。

> [!tip] 反转 C 风格字符串不要把结束符 `\0` 算进去
> 对 `char str[] = "hello";` 反转时，应传 `reverse(str, str + strlen(str))`，而不要传 `str + sizeof(str)`，否则会把末尾的 `'\0'` 换到下标 `0` 导致字符串被截断为空。

## 完整源码

```cpp
/*
C++STL的 reverse 函数用来反转（颠倒）指定范围内的元素顺序。它包含在 <algorithm> 头文件中。
功能：将区间 [first,last) 内的元素原地反转。
迭代器要求：容器必须支持双向迭代器，例如 vector、string、list、普通数组等。不支持单向迭代器
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
    vector<int> v = {1,2,3,4,5};
    reverse(v.begin(),v.end()); // 反转整个 vector
    for (int x:v) cout<<x<<" "; // 输出: 5 4 3 2 1
}
```
