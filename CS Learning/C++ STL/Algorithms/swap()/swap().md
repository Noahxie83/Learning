---
title: swap() — 交换
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
  - swap
  - swap()
  - iter_swap
  - 交换
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `swap()` — 交换

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/sort()/sort()|sort() — 排序]] · 下一篇：[[CS Learning/C++ STL/Algorithms/unique()/unique()|unique() — 相邻去重]]
> 源码：[[CS Learning/C++ STL/Algorithms/swap()/swap().cpp|查看源码]]

> [!abstract] 本节概览
> `std::swap()` 用于交换两个同类型对象的值，C++11 起定义在头文件 `#include <utility>` 中（C++98 位于 `#include <algorithm>`，包含 `<algorithm>` 时通常也可使用）。C++11 后其默认实现基于==移动语义（`std::move`）==，对基本类型和大多数 STL 容器均为 $O(1)$ 常数时间。

## 核心语法与复杂度速查

```cpp
#include <utility>  // C++11 起推荐（C++98 为 <algorithm>）

template <class T>
void swap(T& a, T& b) noexcept(/* ... */);
```

| 交换对象类型 | 底层机制 | 时间复杂度 |
| :--- | :--- | :---: |
| 基本类型（`int`、`double`、指针） | 通过临时变量完成三次赋值 | $O(1)$ |
| 动态容器（`vector`、`string`、`map` 等） | 仅交换内部数据指针、大小与容量（**不逐个拷贝元素**） | $O(1)$ |
| 定长数组（`int a[N]`、`std::array<T, N>`） | 逐元素依次交换 | $O(N)$ |
| 自定义类对象 | 默认执行 1 次移动构造 + 2 次移动赋值（或调用定制 `swap`） | 取决于移动/定制实现 |

## 相关算法家族

`<algorithm>` 还提供了面向迭代器与区间的交换工具：

| 函数 | 功能说明 | 复杂度 |
| :--- | :--- | :---: |
| `std::swap(a, b)` | 交换两个变量 / 对象的值 | $O(1)$（容器）/ $O(N)$（定长数组） |
| `std::iter_swap(it1, it2)` | 交换两个迭代器**所指向元素**的值（等价于 `swap(*it1, *it2)`） | $O(1)$ |
| `std::swap_ranges(first1, last1, first2)` | 逐个交换区间 `[first1, last1)` 与从 `first2` 开始的等长区间 | $O(n)$ |

## 典型用法与自定义类定制 `swap`

### 1. 基础交换与容器 $O(1)$ 交换

```cpp
int x = 10, y = 20;
std::swap(x, y);      // x = 20, y = 10

std::vector<int> a(100000, 1), b(100000, 2);
std::swap(a, b);      // O(1) 指针交换，极快，且不会使指向内部元素的迭代器失效
```

### 2. 为自定义类提供高效定制 `swap`

虽然标准库为所有类型提供了通用的 `std::swap`，但如果自定义类管理了动态资源（如裸指针、句柄），应当为其提供 `noexcept` 的定制 `swap` 友元函数，并在泛型代码中采用 **ADL（参数依赖查找）惯用法**：

```cpp
class Buffer {
    int* data;
    std::size_t len;
public:
    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap;
        swap(a.data, b.data);
        swap(a.len, b.len);
    }
};

// 泛型代码中调用：优先匹配自定义 swap，找不到则回退到 std::swap
using std::swap;
swap(obj1, obj2);
```

## 常见易错点与注意事项

> [!tip] 交换两个变量无需再写位运算异或技巧
> 老旧教材中常见的 `a ^= b; b ^= a; a ^= b;` 存在**`a` 与 `b` 指向同一地址时会清零**的严重 Bug，且仅适用于整数，速度并不优于现代编译器优化后的 `std::swap(a, b)`。实战中应一律直接使用 `std::swap()`。

## 完整源码

```cpp
/*
swap的功能:交换两个变量的值，譬如参数A和参数B，把A的值赋给B，再把B的值赋给A参数
虽然标准库为所有类型提供了通用的swap，但对于你自己的类，如果它有更高效的交换方式，你应该为其提供定制版本。
 swap(_Tp& __a,_Tp& __b)
*/
#include <iostream>
#include <algorithm>
using namespace std;
int main(){
    int x=10;
    int y=20;
    cout<<"before swap: x:"<<x<<" y:"<<y<<endl;
    swap(x,y);
    cout<<"after swap: x:"<<x<<" y:"<<y<<endl;
}
```
