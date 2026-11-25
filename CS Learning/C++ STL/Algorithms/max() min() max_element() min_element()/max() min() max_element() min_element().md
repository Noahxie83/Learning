---
title: max() min() max_element() min_element() — 最值与最值位置
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
  - max
  - min
  - max_element
  - min_element
  - minmax_element
  - 最值与最值位置
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `max()` / `min()` 与 `max_element()` / `min_element()` — 最值与最值位置

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/lower_bound() upper_nound()/lower_bound() upper_nound()|lower_bound() upper_nound() — 上下界查找]] · 下一篇：[[CS Learning/C++ STL/Algorithms/Numeric/Numeric|Numeric — 数值算法]]
> 源码：[[CS Learning/C++ STL/Algorithms/max() min() max_element() min_element()/max() min() max_element() min_element().cpp|查看源码]]

> [!abstract] 本节概览
> 头文件 `#include <algorithm>` 提供了两类最值算法：`std::max()` / `std::min()` 直接返回**两个或多个值中的最值本身**（$O(1)$ 或 $O(k)$）；`std::max_element()` / `std::min_element()` 在左闭右开区间 `[first, last)` 内线性扫描（$O(n)$），返回指向==最值元素的迭代器==。

## 常用函数与接口速查

| 函数形式 | 功能说明 | 返回值类型 | 时间复杂度 |
| :--- | :--- | :--- | :---: |
| `max(a, b)` / `min(a, b)` | 比较两个同类型值，返回较大 / 较小者 | `const T&` | $O(1)$ |
| `max({a, b, c, ...})` / `min({...})` | 通过初始化列表比较多个值（C++11） | `T`（值返回） | $O(k)$ |
| `max(a, b, comp)` / `min(a, b, comp)` | 按自定义比较规则返回最值 | `const T&` | $O(1)$ |
| `max_element(first, last [, comp])` | 在 `[first, last)` 中寻找最大元素 | `ForwardIt`（迭代器） | $O(n)$ |
| `min_element(first, last [, comp])` | 在 `[first, last)` 中寻找最小元素 | `ForwardIt`（迭代器） | $O(n)$ |
| `minmax_element(first, last [, comp])` | 一次遍历同时找出最小值和最大值位置（C++11） | `pair<ForwardIt, ForwardIt>` | $O(n)$ |

## 典型用法与实战模式

### 1. 直接比较两值与多值

```cpp
#include <algorithm>

int a = std::max(10, 20);              // 20
int b = std::max({2, 9, 2, 5});        // 9（花括号初始化列表）
int c = std::min({2, 9, 2, 5});        // 2
```

### 2. 在数组或容器中取最值及下标

`max_element` / `min_element` 返回的是**迭代器（数组则为指针）**，取数值需解引用 `*`，取下标则减去起始迭代器：

```cpp
int n[] = {1, 4, 22, 3, 8, 5};
int len = sizeof(n) / sizeof(int);

int* pmax = std::max_element(n, n + len);
int* pmin = std::min_element(n, n + len);
// 最大值：*pmax = 22，下标：pmax - n = 2
// 最小值：*pmin = 1，下标：pmin - n = 0
```

## 常见易错点与注意事项

> [!warning] `max(a, b)` 要求两个参数类型严格一致
> `std::max` 是函数模板 `template<class T> const T& max(const T& a, const T& b)`，不会自动进行隐式类型转换。例如 `std::max(vec.size(), 10)` 会因 `size_t` 与 `int` 类型不匹配而**编译报错**，需要显式指定模板参数 `std::max<int>(vec.size(), 10)` 或强制类型转换。

> [!warning] 空区间不可解引用 `*_element()`
> 若区间 `[first, last)` 为空（`first == last`），`max_element()` 和 `min_element()` 会返回 `last`。在解引用 `*max_element(...)` 前，务必确认容器非空。

> [!tip] 存在多个相同最值时的返回位置
> 当区间中存在多个相同的最大值或最小值时，`max_element()` 与 `min_element()` 均返回**最先出现（下标最小）**的那个元素的迭代器。

## 完整源码

```cpp
/*
max/min是一个定义在 <algorithm> 头文件中的函数模板，用于返回两个或多个值中的较大/小者。
两者类似，以下以max为例

常用形式：
比较两个值：max(a,b)
比较多个值（初始化列表）：max({a,b,c,d})
自定义比较规则：max(a,b,comp)

max_element/max_element 是用来在指定范围内查找最大/小元素的标准库算法函数
max_element(v.begin(),v.end())
返回值：返回一个迭代器（指向最大元素），如果想获取具体数值，需要使用解引用操作符 *。
查找区间：左闭右开区间 [first,last)
*/
#include <iostream>
#include <algorithm>
using namespace std;
int main() {
    int x=10,y=20;
    cout<<max(x,y)<<endl;         // 输出 20
    cout<<max({2,9,2,5})<<endl; // 输出 9 (多值比较)
	int n[]={1,4,22,3,8,5};
	int len=sizeof(n)/sizeof(int);
	cout<<*max_element(n,n+len)<<endl;
	cout<<*min_element(n,n+len)<<endl;
    return 0;
}
```
