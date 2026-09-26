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
| priority\_queue.cpp | 优先队列 | [阅读笔记](Adapters/priority_queue/priority_queue.md) | [查看源码](Adapters/priority_queue/priority_queue.cpp) |
| queue.cpp | 队列 | [阅读笔记](Adapters/queue/queue.md) | [查看源码](Adapters/queue/queue.cpp) |
| stack.cpp | 栈 | [阅读笔记](Adapters/stack/stack.md) | [查看源码](Adapters/stack/stack.cpp) |

### Algorithms

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| Algorithms.cpp | 标准算法概览 | [阅读笔记](Algorithms/Algorithms/Algorithms.md) | [查看源码](Algorithms/Algorithms/Algorithms.cpp) |
| binary\_search().cpp | 二分查找 | [阅读笔记](Algorithms/binary_search%28%29/binary_search%28%29.md) | [查看源码](Algorithms/binary_search%28%29/binary_search%28%29.cpp) |
| Cmath.cpp | 数学函数 | [阅读笔记](Algorithms/Cmath/Cmath.md) | [查看源码](Algorithms/Cmath/Cmath.cpp) |
| count().cpp | 元素计数 | [阅读笔记](Algorithms/count%28%29/count%28%29.md) | [查看源码](Algorithms/count%28%29/count%28%29.cpp) |
| fill() fill\_n().cpp | 序列填充 | [阅读笔记](Algorithms/fill%28%29%20fill_n%28%29/fill%28%29%20fill_n%28%29.md) | [查看源码](Algorithms/fill%28%29%20fill_n%28%29/fill%28%29%20fill_n%28%29.cpp) |
| find().cpp | 查找元素 | [阅读笔记](Algorithms/find%28%29/find%28%29.md) | [查看源码](Algorithms/find%28%29/find%28%29.cpp) |
| lower\_bound() upper\_nound().cpp | 上下界查找 | [阅读笔记](Algorithms/lower_bound%28%29%20upper_nound%28%29/lower_bound%28%29%20upper_nound%28%29.md) | [查看源码](Algorithms/lower_bound%28%29%20upper_nound%28%29/lower_bound%28%29%20upper_nound%28%29.cpp) |
| max() min() max\_element() min\_element().cpp | 最值与最值位置 | [阅读笔记](Algorithms/max%28%29%20min%28%29%20max_element%28%29%20min_element%28%29/max%28%29%20min%28%29%20max_element%28%29%20min_element%28%29.md) | [查看源码](Algorithms/max%28%29%20min%28%29%20max_element%28%29%20min_element%28%29/max%28%29%20min%28%29%20max_element%28%29%20min_element%28%29.cpp) |
| Numeric.cpp | 数值算法 | [阅读笔记](Algorithms/Numeric/Numeric.md) | [查看源码](Algorithms/Numeric/Numeric.cpp) |
| prev\_permutation() next\_permutation().cpp | 字典序排列 | [阅读笔记](Algorithms/prev_permutation%28%29%20next_permutation%28%29/prev_permutation%28%29%20next_permutation%28%29.md) | [查看源码](Algorithms/prev_permutation%28%29%20next_permutation%28%29/prev_permutation%28%29%20next_permutation%28%29.cpp) |
| Random.cpp | 随机数 | [阅读笔记](Algorithms/Random/Random.md) | [查看源码](Algorithms/Random/Random.cpp) |
| reverse().cpp | 反转序列 | [阅读笔记](Algorithms/reverse%28%29/reverse%28%29.md) | [查看源码](Algorithms/reverse%28%29/reverse%28%29.cpp) |
| shuffle().cpp | 随机打乱 | [阅读笔记](Algorithms/shuffle%28%29/shuffle%28%29.md) | [查看源码](Algorithms/shuffle%28%29/shuffle%28%29.cpp) |
| sort().cpp | 排序 | [阅读笔记](Algorithms/sort%28%29/sort%28%29.md) | [查看源码](Algorithms/sort%28%29/sort%28%29.cpp) |
| swap().cpp | 交换 | [阅读笔记](Algorithms/swap%28%29/swap%28%29.md) | [查看源码](Algorithms/swap%28%29/swap%28%29.cpp) |
| unique().cpp | 相邻去重 | [阅读笔记](Algorithms/unique%28%29/unique%28%29.md) | [查看源码](Algorithms/unique%28%29/unique%28%29.cpp) |

### Containers / Associative containers

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| map.cpp | 有序键值映射 | [阅读笔记](Containers/Associative%20containers/map/map.md) | [查看源码](Containers/Associative%20containers/map/map.cpp) |
| multimap.cpp | 允许重复键的有序映射 | [阅读笔记](Containers/Associative%20containers/multimap/multimap.md) | [查看源码](Containers/Associative%20containers/multimap/multimap.cpp) |
| multiset.cpp | 允许重复元素的有序集合 | [阅读笔记](Containers/Associative%20containers/multiset/multiset.md) | [查看源码](Containers/Associative%20containers/multiset/multiset.cpp) |
| set.cpp | 有序集合 | [阅读笔记](Containers/Associative%20containers/set/set.md) | [查看源码](Containers/Associative%20containers/set/set.cpp) |

### Containers / Sequence containers

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| array.cpp | 定长数组容器 | [阅读笔记](Containers/Sequence%20containers/array/array.md) | [查看源码](Containers/Sequence%20containers/array/array.cpp) |
| deque.cpp | 双端队列容器 | [阅读笔记](Containers/Sequence%20containers/deque/deque.md) | [查看源码](Containers/Sequence%20containers/deque/deque.cpp) |
| forward\_list.cpp | 单向链表容器 | [阅读笔记](Containers/Sequence%20containers/forward_list/forward_list.md) | [查看源码](Containers/Sequence%20containers/forward_list/forward_list.cpp) |
| list.cpp | 双向链表容器 | [阅读笔记](Containers/Sequence%20containers/list/list.md) | [查看源码](Containers/Sequence%20containers/list/list.cpp) |
| string.cpp | string 字符串容器 | [阅读笔记](Containers/Sequence%20containers/string/string.md) | [查看源码](Containers/Sequence%20containers/string/string.cpp) |
| vector.cpp | 动态数组容器 | [阅读笔记](Containers/Sequence%20containers/vector/vector.md) | [查看源码](Containers/Sequence%20containers/vector/vector.cpp) |

### Containers / Unordered associative containers

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| unordered\_map unordered\_multimap.cpp | 无序键值映射 | [阅读笔记](Containers/Unordered%20associative%20containers/unordered_map%20unordered_multimap/unordered_map%20unordered_multimap.md) | [查看源码](Containers/Unordered%20associative%20containers/unordered_map%20unordered_multimap/unordered_map%20unordered_multimap.cpp) |
| unordered\_set unordered\_multiset.cpp | 无序集合 | [阅读笔记](Containers/Unordered%20associative%20containers/unordered_set%20unordered_multiset/unordered_set%20unordered_multiset.md) | [查看源码](Containers/Unordered%20associative%20containers/unordered_set%20unordered_multiset/unordered_set%20unordered_multiset.cpp) |

### Containers / Utility

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| pair.cpp | 二元组 | [阅读笔记](Containers/Utility/pair/pair.md) | [查看源码](Containers/Utility/pair/pair.cpp) |
| tuple.cpp | 多元组 | [阅读笔记](Containers/Utility/tuple/tuple.md) | [查看源码](Containers/Utility/tuple/tuple.cpp) |
| Utility.cpp | utility 工具 | [阅读笔记](Containers/Utility/Utility/Utility.md) | [查看源码](Containers/Utility/Utility/Utility.cpp) |

### Iterators

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| Iterators.cpp | 迭代器 | [阅读笔记](Iterators/Iterators/Iterators.md) | [查看源码](Iterators/Iterators/Iterators.cpp) |

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

上级入口：[CS Learning/README.md](../README.md)。
