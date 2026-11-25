---
title: count() — 元素计数
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
  - count
  - count()
  - count_if
  - 元素计数
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `count()` — 元素计数

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/Cmath/Cmath|Cmath — 数学函数]] · 下一篇：[[CS Learning/C++ STL/Algorithms/fill() fill_n()/fill() fill_n()|fill() fill_n() — 序列填充]]
> 相关：[[CS Learning/C++ STL/Algorithms/find()/find()|find() — 查找元素]]
> 源码：[[CS Learning/C++ STL/Algorithms/count()/count().cpp|查看源码]]

> [!abstract] 本节概览
> `std::count()` 定义在头文件 `#include <algorithm>` 中，用于线性统计指定值 `value` 在左闭右开区间 `[first, last)` 内出现的次数。底层逐个使用 `==` 比较元素，时间复杂度为 $O(n)$。

## 核心语法与参数说明

```cpp
#include <algorithm>

auto cnt = std::count(first, last, value);
```

| 参数 | 含义 | 说明 |
| :--- | :--- | :--- |
| `first` | 范围起始迭代器（包含） | 只需满足输入迭代器（InputIterator）要求 |
| `last` | 范围结束迭代器（不包含） | 与 `first` 共同构成左闭右开区间 `[first, last)` |
| `value` | 待统计的目标值 | 区间元素必须支持与 `value` 进行 `==` 比较 |

**返回值**：区间中与 `value` 相等的元素个数（返回类型为迭代器的 `difference_type`，通常可赋值给 `int` 或 `long long`）。

## 典型用法与扩展：`count_if()`

### 1. 基础值统计（源码示例）

在 `vector<int> nums = {1, 2, 3, 2, 4, 2}` 中调用 `count(nums.begin(), nums.end(), 2)`，逐一比对后返回 `3`。

### 2. 按条件统计：`std::count_if()`

如果需要统计满足特定条件（而非等于某个定值）的元素个数，可搭配 Lambda 表达式使用 `std::count_if()`：

```cpp
// 统计 vector 中偶数的个数
int even_cnt = std::count_if(nums.begin(), nums.end(), [](int x) {
    return x % 2 == 0;
});
```

## 常见易错点与性能对比

| 场景 | 推荐做法 | 时间复杂度 |
| :--- | :--- | :---: |
| 无序数组 / `vector` / `string` | `std::count(first, last, val)` | $O(n)$ |
| **已排序**数组 / `vector` | `upper_bound(...) - lower_bound(...)` | $O(\log n)$ |
| `set` / `multiset` / `map` | 成员函数 `c.count(key)` | $O(\log n + k)$ |
| `unordered_set` / `unordered_map` | 成员函数 `c.count(key)` | 平均 $O(1 + k)$ |

> [!tip] 避免对关联容器调用全局 `std::count()`
> 对 `set`、`multiset` 或 `unordered_set` 调用全局 `std::count(s.begin(), s.end(), x)` 会退化为 $O(n)$ 全表扫描；应直接调用容器自带的成员函数 `s.count(x)`。

## 完整源码

```cpp
/*
count是C++标准模板库(STL)中的一个算法函数，用于统计某个指定值在容器或指定范围内出现的次数。它包含在 <algorithm> 头文件中。

语法:
count(first,last,value);
    first：指向范围起始位置的迭代器（包含该位置）。
    last：指向范围结束位置的迭代器（不包含该位置）。
    value：要查找和统计的目标值。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    vector<int> nums={1,2,3,2,4,2};
    // 统计数字 2 出现的次数
    int count_2=count(nums.begin(),nums.end(),2);
    cout<<"数字 2 出现的次数为: "<<count_2<<endl; // 输出 3
    return 0;
}
```
