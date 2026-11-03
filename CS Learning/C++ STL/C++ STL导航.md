---
title: "C++ STL导航"
date: 2026-10-23
date_source: 导航拆分日期，不代表学习或完成日期
note_type: 导航
navigation_for: Obsidian
tags:
  - 类型/导航
cssclasses:
  - learning-index
---

# C++ STL

C++ 标准模板库（STL）学习与示例代码。

学习状态：本专题已学完。

参考入口：[cppreference — C++ 标准库](https://en.cppreference.com/cpp/standard_library)。本模块是独立学习专题，尚未指定统一课程；此链接是参考文档，不是课程官网。

## Markdown 笔记目录

本目录的 35 个 C++ 源文件已整理为同名主题目录：每个目录内包含原源码和一篇 Markdown 笔记，原有 STL 分类与文件名保留。

Markdown 将原注释整理为正文、用法表格、输入输出样例及带行号的注释索引，文末附完整源码。笔记保留学习时的记录，未进行逐项知识校订。

例如 ` Containers/Sequence containers/vector.cpp ` 现整理为：

```text
Containers/Sequence containers/vector/
├── vector.cpp
└── vector.md
```

下面的链接可直接打开对应笔记。

### Adapters

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| priority\_queue.cpp | 优先队列 | [[CS Learning/C++ STL/Adapters/priority_queue/priority_queue\|阅读笔记]] | [[CS Learning/C++ STL/Adapters/priority_queue/priority_queue.cpp\|查看源码]] |
| queue.cpp | 队列 | [[CS Learning/C++ STL/Adapters/queue/queue\|阅读笔记]] | [[CS Learning/C++ STL/Adapters/queue/queue.cpp\|查看源码]] |
| stack.cpp | 栈 | [[CS Learning/C++ STL/Adapters/stack/stack\|阅读笔记]] | [[CS Learning/C++ STL/Adapters/stack/stack.cpp\|查看源码]] |

### Algorithms

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| Algorithms.cpp | 标准算法概览 | [[CS Learning/C++ STL/Algorithms/Algorithms/Algorithms\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/Algorithms/Algorithms.cpp\|查看源码]] |
| binary\_search().cpp | 二分查找 | [[CS Learning/C++ STL/Algorithms/binary_search()/binary_search()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/binary_search()/binary_search().cpp\|查看源码]] |
| Cmath.cpp | 数学函数 | [[CS Learning/C++ STL/Algorithms/Cmath/Cmath\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/Cmath/Cmath.cpp\|查看源码]] |
| count().cpp | 元素计数 | [[CS Learning/C++ STL/Algorithms/count()/count()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/count()/count().cpp\|查看源码]] |
| fill() fill\_n().cpp | 序列填充 | [[CS Learning/C++ STL/Algorithms/fill() fill_n()/fill() fill_n()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/fill() fill_n()/fill() fill_n().cpp\|查看源码]] |
| find().cpp | 查找元素 | [[CS Learning/C++ STL/Algorithms/find()/find()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/find()/find().cpp\|查看源码]] |
| lower\_bound() upper\_nound().cpp | 上下界查找 | [[CS Learning/C++ STL/Algorithms/lower_bound() upper_nound()/lower_bound() upper_nound()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/lower_bound() upper_nound()/lower_bound() upper_nound().cpp\|查看源码]] |
| max() min() max\_element() min\_element().cpp | 最值与最值位置 | [[CS Learning/C++ STL/Algorithms/max() min() max_element() min_element()/max() min() max_element() min_element()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/max() min() max_element() min_element()/max() min() max_element() min_element().cpp\|查看源码]] |
| Numeric.cpp | 数值算法 | [[CS Learning/C++ STL/Algorithms/Numeric/Numeric\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/Numeric/Numeric.cpp\|查看源码]] |
| prev\_permutation() next\_permutation().cpp | 字典序排列 | [[CS Learning/C++ STL/Algorithms/prev_permutation() next_permutation()/prev_permutation() next_permutation()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/prev_permutation() next_permutation()/prev_permutation() next_permutation().cpp\|查看源码]] |
| Random.cpp | 随机数 | [[CS Learning/C++ STL/Algorithms/Random/Random\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/Random/Random.cpp\|查看源码]] |
| reverse().cpp | 反转序列 | [[CS Learning/C++ STL/Algorithms/reverse()/reverse()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/reverse()/reverse().cpp\|查看源码]] |
| shuffle().cpp | 随机打乱 | [[CS Learning/C++ STL/Algorithms/shuffle()/shuffle()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/shuffle()/shuffle().cpp\|查看源码]] |
| sort().cpp | 排序 | [[CS Learning/C++ STL/Algorithms/sort()/sort()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/sort()/sort().cpp\|查看源码]] |
| swap().cpp | 交换 | [[CS Learning/C++ STL/Algorithms/swap()/swap()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/swap()/swap().cpp\|查看源码]] |
| unique().cpp | 相邻去重 | [[CS Learning/C++ STL/Algorithms/unique()/unique()\|阅读笔记]] | [[CS Learning/C++ STL/Algorithms/unique()/unique().cpp\|查看源码]] |

### Containers / Associative containers

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| map.cpp | 有序键值映射 | [[CS Learning/C++ STL/Containers/Associative containers/map/map\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Associative containers/map/map.cpp\|查看源码]] |
| multimap.cpp | 允许重复键的有序映射 | [[CS Learning/C++ STL/Containers/Associative containers/multimap/multimap\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Associative containers/multimap/multimap.cpp\|查看源码]] |
| multiset.cpp | 允许重复元素的有序集合 | [[CS Learning/C++ STL/Containers/Associative containers/multiset/multiset\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Associative containers/multiset/multiset.cpp\|查看源码]] |
| set.cpp | 有序集合 | [[CS Learning/C++ STL/Containers/Associative containers/set/set\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Associative containers/set/set.cpp\|查看源码]] |

### Containers / Sequence containers

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| array.cpp | 定长数组容器 | [[CS Learning/C++ STL/Containers/Sequence containers/array/array\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Sequence containers/array/array.cpp\|查看源码]] |
| deque.cpp | 双端队列容器 | [[CS Learning/C++ STL/Containers/Sequence containers/deque/deque\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Sequence containers/deque/deque.cpp\|查看源码]] |
| forward\_list.cpp | 单向链表容器 | [[CS Learning/C++ STL/Containers/Sequence containers/forward_list/forward_list\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Sequence containers/forward_list/forward_list.cpp\|查看源码]] |
| list.cpp | 双向链表容器 | [[CS Learning/C++ STL/Containers/Sequence containers/list/list\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Sequence containers/list/list.cpp\|查看源码]] |
| string.cpp | string 字符串容器 | [[CS Learning/C++ STL/Containers/Sequence containers/string/string\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Sequence containers/string/string.cpp\|查看源码]] |
| vector.cpp | 动态数组容器 | [[CS Learning/C++ STL/Containers/Sequence containers/vector/vector\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Sequence containers/vector/vector.cpp\|查看源码]] |

### Containers / Unordered associative containers

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| unordered\_map unordered\_multimap.cpp | 无序键值映射 | [[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_map unordered_multimap/unordered_map unordered_multimap\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_map unordered_multimap/unordered_map unordered_multimap.cpp\|查看源码]] |
| unordered\_set unordered\_multiset.cpp | 无序集合 | [[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_set unordered_multiset/unordered_set unordered_multiset\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_set unordered_multiset/unordered_set unordered_multiset.cpp\|查看源码]] |

### Containers / Utility

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| pair.cpp | 二元组 | [[CS Learning/C++ STL/Containers/Utility/pair/pair\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Utility/pair/pair.cpp\|查看源码]] |
| tuple.cpp | 多元组 | [[CS Learning/C++ STL/Containers/Utility/tuple/tuple\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Utility/tuple/tuple.cpp\|查看源码]] |
| Utility.cpp | utility 工具 | [[CS Learning/C++ STL/Containers/Utility/Utility/Utility\|阅读笔记]] | [[CS Learning/C++ STL/Containers/Utility/Utility/Utility.cpp\|查看源码]] |

### Iterators

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| Iterators.cpp | 迭代器 | [[CS Learning/C++ STL/Iterators/Iterators/Iterators\|阅读笔记]] | [[CS Learning/C++ STL/Iterators/Iterators/Iterators.cpp\|查看源码]] |

## 目录导航

| 目录 | 内容 |
| --- | --- |
| [Containers](./Containers/) | 序列容器、关联容器、无序关联容器和工具类容器 |
| [Iterators](./Iterators/) | 迭代器及其使用方式 |
| [Algorithms](./Algorithms/) | STL 算法及其典型用法 |
| [Adapters](./Adapters/) | 容器适配器和相关接口 |

## 学习重点

- 容器的元素组织方式和适用场景。
- 迭代器与算法之间的配合。
- `vector`、`list`、`deque` 等序列容器。
- `set`、`map` 及其无序版本。
- 排序、查找、遍历和变换等通用算法。
- 容器适配器提供的受限接口。

建议先学习容器和迭代器，再结合算法目录中的示例进行练习。

上级入口：[[CS Learning/计算机基础导航|CS Learning/README.md]]。

---

[[CS Learning/计算机基础导航|返回上级导航]]
