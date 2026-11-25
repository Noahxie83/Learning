---
title: "map — 有序键值映射"
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
aliases:
  - std::map
  - map
  - 有序键值映射
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# map — 有序键值映射

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/unique()/unique()|unique() — 相邻去重]] · 下一篇：[[CS Learning/C++ STL/Containers/Associative containers/multimap/multimap|multimap — 允许重复键的有序映射]]
> 相关：[[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_map unordered_multimap/unordered_map unordered_multimap|unordered_map unordered_multimap — 无序键值映射]]
> 源码：[[CS Learning/C++ STL/Containers/Associative containers/map/map.cpp|查看源码]]

> [!abstract] 本节概览
> `std::map` 定义于头文件 `<map>`，是 C++ STL 中的有序关联容器，底层通常基于==红黑树（自平衡二叉搜索树）==实现。容器以 `std::pair<const Key, T>` 形式存储键值对，所有元素按**键（key）严格有序排列**且**键唯一**。查找、插入和删除的时间复杂度均为 $O(\log n)$，提供双向迭代器；插入操作不会使任何现有迭代器失效，删除操作仅使指向被删节点的迭代器失效。

## 核心概念、底层结构与声明

### 1. 容器特点与与 `multimap` 的区别

- **底层结构**：基于平衡二叉树（红黑树），中序遍历即得按键升序排列的序列。
- **键值对元素**：每个节点存储一个 `pair<const Key, Value>`，可概念上理解为：

```cpp
// pair<T1, T2> 的结构等价示意
struct {
    T1 first;   // 关键字（在 map 中为 const Key，不可直接修改）
    T2 second;  // 映射值
};
```

- **与 [[CS Learning/C++ STL/Containers/Associative containers/multimap/multimap|multimap]] 的核心差异**：
  1. **键唯一性**：`map` 不允许关键字重复，因此 `insert()` 在键已存在时会插入失败（不覆盖旧值）。
  2. **支持下标访问**：`map` 支持 `mp[key]`，返回对应 `first == key` 元素的 `second` 引用；`multimap` 不支持 `[]`。
  3. **双向迭代器**：仅支持 `++`、`--`、`==`、`!=`，不支持随机偏移（如 `it + 2`）。

### 2. 声明与初始化

```cpp
#include <map>

map<key_type, value_type> myMap;                           // 默认按 less<key_type> 升序
map<string, int, greater<string>> descMap;                 // 自定义比较器（按 key 降序）
map<string, int> scores = {{"Alice", 90}, {"Bob", 85}};    // 初始化列表
```

## 常用接口与时间复杂度速查

| 成员函数 / 操作 | 说明 | 时间复杂度 |
| --- | --- | --- |
| `mp[key]` | 访问键 `key` 对应值的引用；==若键不存在，会默认插入 `{key, T()}`== | $O(\log n)$ |
| `mp.at(key)` | 访问键 `key` 对应值的引用；若键不存在则抛出 `std::out_of_range` | $O(\log n)$ |
| `mp.insert({k, v})` | 插入键值对，返回 `pair<iterator, bool>`（已存在时不覆盖，`second` 为 `false`） | $O(\log n)$ |
| `mp.emplace(k, v)` | 原地构造键值对并插入，减少临时对象拷贝 | $O(\log n)$ |
| `mp.find(key)` | 查找键为 `key` 的元素，找到返回其迭代器，否则返回 `mp.end()` | $O(\log n)$ |
| `mp.count(key)` | 统计键出现次数（在 `map` 中只可能返回 `0` 或 `1`） | $O(\log n)$ |
| `mp.contains(key)` | 判断键是否存在（C++20 起支持） | $O(\log n)$ |
| `mp.lower_bound(key)` | 返回首个键值 $\ge \text{key}$ 的元素迭代器 | $O(\log n)$ |
| `mp.upper_bound(key)` | 返回首个键值 $> \text{key}$ 的元素迭代器 | $O(\log n)$ |
| `mp.erase(key)` / `mp.erase(it)` | 按键删除（返回删除个数 0 或 1）或按迭代器删除（均摊 $O(1)$） | $O(\log n)$ / 均摊 $O(1)$ |
| `mp.size()` / `mp.empty()` | 返回元素个数 / 判断容器是否为空 | $O(1)$ |
| `mp.clear()` | 清空所有节点 | $O(n)$ |

## 典型用法解析

在源码示例中，演示了 `map<string, int>` 的增、查、遍历、删基本闭环：

```cpp
map<string, int> scores;
scores["Alice"] = 90;              // 通过下标插入或更新
scores["Bob"] = 85;
scores.insert({"Charlie", 92});    // 若 "Charlie" 已存在则插入失败

// 按键字典序遍历：Alice -> Bob -> Charlie
for (const auto& p : scores) {
    cout << p.first << " => " << p.second << endl;
}
// C++17 结构化绑定写法更简洁：
// for (const auto& [name, score] : scores) { ... }

auto it = scores.find("Bob");      // 查找：推荐用 find 而非直接 []
if (it != scores.end()) {
    cout << "Bob's score: " << it->second << endl;
}

scores.erase("Alice");             // 按键删除
```

## 常见易错点与迭代器失效规则

> [!warning] `operator[]` 的隐式插入陷阱
> 当 `key` 不存在于 `map` 中时，仅仅执行一次读取表达式（如 `if (scores["David"] == 0)` 或 `cout << scores["David"]`）就会**静默向容器中插入一个新条目 `{"David", 0}`**，导致 `size()` 增大并改变容器内容！
> - **只读查询或判断是否存在**时，请使用 `find(key) != end()`、`count(key)` 或 `at(key)`。
> - `const map` 对象上**不能调用 `operator[]`**，因为 `[]` 可能需要修改容器。

> [!tip] 键的不可变性与迭代器稳定性
> - **不可修改键**：`it->first` 是 `const Key` 类型，直接修改会破坏红黑树有序性，编译器会报错；若需改键，应先 `erase` 旧条目再插入新条目（C++17 起可用 `extract()` 无拷贝换键）。
> - **迭代器高度稳定**：`insert` / `emplace` 不会使任何现有迭代器、指针或引用失效；`erase(it)` 仅使指向被删元素的迭代器失效，其余节点迭代器均保持有效。遍历中安全删除的标准写法为 `it = mp.erase(it);`。

## 完整源码

```cpp
/*
map即映射(基于平衡二叉树)

map和multimap区别在于:
    不能有关键字重复的元素
    可以使用[]，下标为关键字，返回值为first和关键字相同的元素的secind
    插入可能失败

map的定义:
在 C++ 中，<map> 是标准模板库（STL）的一部分，它提供了一种关联容器，用用于存储键值对（key-value pairs）。
map容器中的元素是按照键的顺序自动排序的，这使得它非常适合需要快速查找和有序数据的场景。

map的声明:
头文件:#include <map>
map<key_type,value_type> myMap;
    key_type是键的类型。
    value_type是值的类型。
插入元素：myMap[key] = value;
访问元素：value = myMap[key];
map的特点:
键值对：map 存储的是键值对，其中每个键都是唯一的。
排序：map 中的元素按照键的顺序自动排序，通常是升序。
唯一性：每个键在 map 中只能出现一次。
双向迭代器：map 提供了双向迭代器，可以向前和向后遍历元素。
*/
#include <iostream>
#include <map>
#include <string>
using namespace std;
int main() {
    map<string,int>scores;
    // 插入
    scores["Alice"]=90;
    scores["Bob"]=85;
    scores.insert({"Charlie",92});
    // 遍历
    for (auto &p:scores){
        cout<<p.first<<" => "<<p.second<<endl;
    }
    // 查找
    auto it=scores.find("Bob");
    if (it!=scores.end()){
        cout<<"Bob's score: "<<it->second<<endl;
    }
    // 删除
    scores.erase("Alice");
    cout<<"Size: "<<scores.size()<<endl;
    return 0;
}
//PS:
/*
pair<T1,T2>等价于           e.g. pair<int,double>a;等价于
struct{                     struct{
T1 first;                          int first;
T2 second;                         double second;
};                          }a;
*/
```
