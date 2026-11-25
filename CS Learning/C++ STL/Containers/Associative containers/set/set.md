---
title: "set — 有序集合"
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
aliases:
  - std::set
  - set
  - 有序集合
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# set — 有序集合

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Associative containers/multiset/multiset|multiset — 允许重复元素的有序集合]] · 下一篇：[[CS Learning/C++ STL/Containers/Sequence containers/array/array|array — 定长数组容器]]
> 相关：[[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_set unordered_multiset/unordered_set unordered_multiset|unordered_set unordered_multiset — 无序集合]]
> 源码：[[CS Learning/C++ STL/Containers/Associative containers/set/set.cpp|查看源码]]

> [!abstract] 本节概览
> `std::set` 定义于头文件 `<set>`，是基于==红黑树（平衡二叉搜索树）==实现的有序集合容器。与 `multiset` 相比，`set` 保证所有元素**严格唯一**且**自动排序**，查找、插入、删除操作的时间复杂度均为 $O(\log n)$。它提供只读的双向迭代器（元素本身即为键，不可原地修改）；插入不使现有迭代器失效，删除仅使指向被删元素的迭代器失效。

## 核心概念、底层结构与声明

### 1. 容器特性与元素要求

- **底层结构**：红黑树，保证最坏情况下增删查复杂度均为 $O(\log n)$，遍历天然有序。
- **唯一性与等价判定**：`set` 不允许重复元素。元素 $a$ 与 $b$ 被视为重复，当且仅当比较器下**互不严格排在对方前面**（`!comp(a, b) && !comp(b, a)`）。因此向 `set` 插入已存在等价元素时，==插入会失败==。
- **对元素类型 `T` 的要求**：
  1. 必须支持比较大小（提供 `operator<` 或自定义比较器）。
  2. 必须可复制/移动构造（放入节点内存管理）。

### 2. 声明与自定义比较器

```cpp
#include <set>

set<int> mySet;                      // 默认使用 less<int> 升序排列
set<int, greater<int>> descSet;      // 使用 greater<int> 降序排列
set<int> initSet = {30, 10, 20, 10}; // 初始化后自动去重排序 -> {10, 20, 30}
```

## 常用接口与时间复杂度速查

| 成员函数 | 说明 | 时间复杂度 |
| --- | --- | --- |
| `st.insert(val)` | 插入元素，返回 `pair<iterator, bool>`（`second` 表示是否成功插入） | $O(\log n)$ |
| `st.emplace(args...)` | 原地构造并插入元素，返回值同 `insert` | $O(\log n)$ |
| `st.erase(val)` / `st.erase(it)` | 按值删除（返回 0 或 1）或按迭代器删除 | $O(\log n)$ / 均摊 $O(1)$ |
| `st.find(val)` | 查找元素，找到返回其迭代器，否则返回 `st.end()` | $O(\log n)$ |
| `st.count(val)` | 判断元素出现次数（在 `set` 中仅返回 `0` 或 `1`） | $O(\log n)$ |
| `st.contains(val)` | 检查元素是否存在（C++20 起支持） | $O(\log n)$ |
| `st.lower_bound(val)` | 返回首个 $\ge \text{val}$ 的元素迭代器 | $O(\log n)$ |
| `st.upper_bound(val)` | 返回首个 $> \text{val}$ 的元素迭代器 | $O(\log n)$ |
| `st.size()` / `st.empty()` | 返回元素个数 / 检查集合是否为空 | $O(1)$ |
| `st.clear()` | 清空集合中的所有元素 | $O(n)$ |

## 典型用法与选型对比

### 1. 检查 `insert()` 是否插入成功

在去重统计或查重逻辑中，可直接利用 `insert()` 的返回值避免先 `find` 再 `insert` 的两次树查找：

```cpp
auto [it, inserted] = mySet.insert(20); // C++17 结构化绑定
if (!inserted) {
    cout << "20 already exists!" << endl;
}
```

### 2. `set` / `multiset` / `unordered_set` 选型对比

| 特性 | `set` | `multiset` | `unordered_set` |
| --- | --- | --- | --- |
| 底层实现 | 红黑树 | 红黑树 | 哈希表（拉链法） |
| 允许重复元素 | 否 | 是 | 否 |
| 元素有序性 | 自动有序 | 自动有序 | 无序 |
| 增删查时间复杂度 | $O(\log n)$ 稳定 | $O(\log n)$ 稳定 | 平均 $O(1)$，最坏 $O(n)$ |
| 是否支持前驱/后继查询 | 支持（`lower_bound`/`--`） | 支持 | 不支持 |

## 常见易错点与迭代器失效规则

> [!warning] 禁止通过迭代器直接修改 `set` 中的元素
> `set` 中的元素值本身就是红黑树的排序键，因此 `set<T>::iterator` 解引用后通常为 `const T&`（不可修改）。若需修改某个元素，必须先 `erase` 旧值，再 `insert` 新值。

> [!tip] 迭代器失效规则与常用习惯
> - 插入新元素不会使任何现有迭代器失效；删除元素仅使指向被删元素的迭代器失效。
> - `set` 仅支持双向迭代器，因此不能使用 `it + 1`，前进/后退一步请用 `++it`、`--it` 或 `std::next(it)` / `std::prev(it)`；查找最小/最大元素可直接取 `*st.begin()` 与 `*st.rbegin()`（前提是 `!st.empty()`）。

## 完整源码

```cpp
/*
set即集合(基于平衡二叉树)

set和multiset区别在于:
    set和multiset的区别在于容器里不能有重复元素
    a和b重复<=><a必须在b前面>和<b必须在a前面>都不成立;
    set插入元素可能不成功

set的定义:
C++ 标准库中的 <set> 是一个关联容器，它存储了一组唯一的元素，并按照一定的顺序进行排序。
<set> 提供了高效的元素查找、插入和删除操作。它是基于红黑树实现的，因此具有对数时间复杂度的查找、插入和删除性能。
<set> 容器中存储的元素类型必须满足以下条件：
    元素类型必须可以比较大小。
    元素类型必须可以被复制和赋值。

set的声明:
头文件#include <set>
set<类型,比较器> st;
类型：要储存的数据类型
比较器：比较大小使用的比较器，默认为 less<类型>，可自定义

以下是常用成员函数
insert(元素):          插入一个元素。
erase(元素):           删除一个元素。
find(元素):            查找一个元素。
size():                返回容器中元素的数量。
empty():               检查容器是否为空。
*/
#include <iostream>
#include <set>
using namespace std;
int main() {
    // 声明一个整型 set 容器
    set<int> mySet;
    // 插入元素
    mySet.insert(10);
    mySet.insert(20);
    mySet.insert(30);
    mySet.insert(40);
    // 输出 set 中的元素
    cout<<"Set contains: ";
    for (int num:mySet){
        cout<<num<<" ";
    }
    cout<<endl;
    // 查找元素
    if (mySet.find(20)!=mySet.end()){
        cout<<"20 is in the set."<<endl;
    }else{
        cout<<"20 is not in the set."<<endl;
    }
    // 删除元素
    mySet.erase(20);
    // 再次输出 set 中的元素
    cout<<"After erasing 20, set contains: ";
    for (int num:mySet){
        cout<<num<<" ";
    }
    cout<<endl;
    // 检查 set 是否为空
    if (mySet.empty()){
        cout<<"The set is empty."<<endl;
    }else{
        cout<<"The set is not empty."<<endl;
    }
    // 输出 set 中元素的数量
    cout<<"The set contains "<<mySet.size()<<" elements."<<endl;
    return 0;
}
```
