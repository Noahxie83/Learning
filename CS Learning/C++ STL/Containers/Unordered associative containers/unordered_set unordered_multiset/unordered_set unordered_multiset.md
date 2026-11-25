---
title: unordered_set unordered_multiset — 无序集合
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
  - unordered_set
  - unordered_multiset
  - STL 无序集合
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# unordered_set / unordered_multiset — 无序集合

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_map unordered_multimap/unordered_map unordered_multimap|unordered_map unordered_multimap — 无序键值映射]] · 下一篇：[[CS Learning/C++ STL/Containers/Utility/pair/pair|pair — 二元组]]
> 相关：[[CS Learning/C++ STL/Containers/Associative containers/set/set|set — 有序集合]]
> 源码：[[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_set unordered_multiset/unordered_set unordered_multiset.cpp|查看源码]]

> [!abstract] 本节概览
> `<unordered_set>` 提供基于==哈希表==的集合容器 **`std::unordered_set`**（元素唯一）与 **`std::unordered_multiset`**（允许重复元素）。二者放弃元素排序，提供平均 $O(1)$ 的存在性查询、插入与删除，适合高速去重与成员判重场景。

---

## 一、模板签名与核心参数

头文件：`#include <unordered_set>`（两者共用同一头文件）。

```cpp
template <
    class Key,
    class Hash = std::hash<Key>,
    class Pred = std::equal_to<Key>,
    class Alloc = std::allocator<Key>
> class unordered_set;
```

| 模板参数 | 含义 | 默认值 |
| --- | --- | --- |
| `Key` | 存储在集合中的元素类型（键即值，不可原地修改） | 必填 |
| `Hash` | 计算元素哈希值的函数对象 | `std::hash<Key>` |
| `Pred` | 判断两个元素是否相等的二元谓词 | `std::equal_to<Key>` |
| `Alloc` | 内存分配器类型 | `std::allocator<Key>` |

---

## 二、常用操作与复杂度

| 接口 | 说明 | 平均复杂度 | 最坏复杂度 |
| --- | --- | :---: | :---: |
| `insert(val)` / `emplace(val)` | 插入元素（`unordered_set` 重复插入无效） | $O(1)$ | $O(n)$ |
| `find(val)` | 查找元素，命中返回前向迭代器，否则返回 `end()` | $O(1)$ | $O(n)$ |
| `count(val)` | 统计 `val` 出现次数（`unordered_set` 为 0 或 1） | $O(1)$ | $O(n)$ |
| `erase(val)` / `erase(it)` | 删除值等于 `val` 的全部元素或单个迭代器指向元素 | $O(1)$ | $O(n)$ |
| `size()` / `empty()` / `clear()` | 查询元素数、判空、清空所有元素 | $O(1)$ / $O(n)$ | $O(1)$ / $O(n)$ |
| `reserve(n)` | 预分配至少容纳 `n` 个元素的桶空间 | $O(n)$ | $O(n)$ |

---

## 三、四大集合容器与集合三要素对比

| 集合性质 | 解释 | `set` | `multiset` | `unordered_set` | `unordered_multiset` |
| --- | --- | :---: | :---: | :---: | :---: |
| **确定性** | 元素要么在集合中，要么不在 | ✔ | ✔ | ✔ | ✔ |
| **互异性** | 元素至多出现一次 | ✔ | ❌（任意次） | ✔ | ❌（任意次） |
| **无序性** | 元素不按大小顺序存储 | ❌（升序） | ❌（升序） | ✔ | ✔ |
| **底层结构** | 实现机制 | 红黑树 | 红黑树 | 哈希表 | 哈希表 |
| **典型复杂度** | 查找 / 插入 / 删除 | $O(\log n)$ | $O(\log n)$ | 平均 $O(1)$ | 平均 $O(1)$ |

> [!tip] `unordered_multiset` 删除单个元素技巧
> 调用 `ums.erase(val)` 会**删除所有等于 `val` 的元素**；若只想删掉其中一个副本，应先 `auto it = ums.find(val); if (it != ums.end()) ums.erase(it);`。

---

## 完整源码

```cpp
/*
unordered_set的定义:
在C++中,<unordered_set> 是标准模板库(STL)的一部分,提供了一种基于哈希表的容器,用于存储唯一的元素集合。
与 set 不同,unordered_set 不保证元素的排序,但通常提供更快的查找、插入和删除操作。

unordered_set的声明:
头文件:#include <unordered_set>
    unordered_set<Key,Hash =hash<Key>,Pred=equal_to<Key>,Alloc=allocator<Key>>
    Key   是存储在unordered_set中的元素类型。
    Hash  是一个函数或函数对象,用于生成元素的哈希值,默认为 hash<Key>。
    Pred  是一个二元谓词,用于比较两个元素是否相等,  默认为 equal_to<Key>。
    Alloc 是分配器类型,用于管理内存分配,           默认为 allocator<Key>。

unordered_multiset:
unordered_multiset除了能存储相同值的元素外,它和 unordered_set 容器完全相同。
实现unordered_multiset容器的模板类并没有定义在以该容器名命名的文件中,而是和 unordered_set容器共用同一个<unordered_set>头文件
*/
#include <iostream>
#include <unordered_set>
using namespace std;
int main(){
    // 创建一个整数类型的 unordered_set
    unordered_set<int> uset;
    // 插入元素
    uset.insert(10);
    uset.insert(20);
    uset.insert(30);
    // 打印 unordered_set 中的元素
    cout<<"Elements in uset: ";
    for (int elem:uset){
        cout<<elem<<" ";
    }
    cout<<endl;
    // 查找元素
    auto it = uset.find(20);
    if (it != uset.end()){
        cout<<"Element 20 found in uset."<<endl;
    } else{
        cout<<"Element 20 not found in uset."<<endl;
    }
    // 删除元素
    uset.erase(20);
    cout<<"After erasing 20, elements in uset: ";
    for (int elem:uset){
        cout<<elem<<" ";
    }
    cout<<endl;
    // 检查大小和是否为空
    cout<<"Size of uset: "<<uset.size()<<endl;
    cout<<"Is uset empty? "<<(uset.empty()?"Yes":"No")<<endl;
    // 清空 unordered_set
    uset.clear();
    cout<<"After clearing, is uset empty? "<<(uset.empty()?"Yes":"No")<<endl;
    return 0;
}
/*
集合三要素	        解释	                    set	        multiset	    unordered_set       unordered_multiset
确定性	    一个元素要么在集合中,要么不在	       ✔	        ✔	            ✔                      ✔
互异性	    一个元素仅可以在集合中出现一次	       ✔	        ❌(任意次)	    ✔                      ❌(任意次)
无序性	    集合中的元素是没有顺序的	          ❌(从小到大)  ❌(从小到大)	   ✔                       ✔
*/
```
