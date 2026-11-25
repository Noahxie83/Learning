---
title: pair — 二元组
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
  - std::pair
  - make_pair
  - STL 二元组
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# pair — 二元组

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Unordered associative containers/unordered_set unordered_multiset/unordered_set unordered_multiset|unordered_set unordered_multiset — 无序集合]] · 下一篇：[[CS Learning/C++ STL/Containers/Utility/tuple/tuple|tuple — 多元组]]
> 相关：[[CS Learning/C++ STL/Containers/Utility/tuple/tuple|tuple — 多元组]]
> 源码：[[CS Learning/C++ STL/Containers/Utility/pair/pair.cpp|查看源码]]

> [!abstract] 本节概览
> `std::pair<T1, T2>` 定义在 `<utility>` 头文件中，用于将**两个（可不同类型）的值**打包成单一结构体对象，通过公开成员 `.first` 与 `.second` 直接访问。它既是 `map` / `unordered_map` 的底层元素载体，也是函数返回双值与坐标/边权排序的常用轻量工具。

---

## 一、本质结构与三种构造方式

从语义上，`pair<T1, T2>` 等价于一个自带默认比较运算的二元模板结构体：

```cpp
template <class T1, class T2>
struct pair {
    T1 first;
    T2 second;
};
```

### 常见初始化方式对比

| 方式 | 写法示例 | 特点与适用版本 |
| --- | --- | --- |
| **直接构造** | `pair<int, string> s1(101, "Alice");` | 显式指明类型，兼容所有 C++ 版本 |
| **列表初始化（C++11）** | `pair<int, string> s1 = {101, "Alice"};` | 写法最简洁，适合函数 `return {a, b};` |
| **`make_pair` 工厂函数** | `auto s2 = make_pair(102, "Bob");` | 自动推导类型（注意字面量 `"Bob"` 推导为 `const char*` 而非 `string`） |
| **类模板参数推导 CTAD（C++17）** | `pair s3(103, "Charlie");` | 无需写尖括号与 `make_pair`，现代 C++ 推荐 |

---

## 二、字典序比较与结构化绑定

1. **内置字典序比较（`<`, `<=`, `>`, `>=`, `==`, `!=`）**：==先比较 `.first`，仅当 `.first` 相等时再比较 `.second`==。因此 `vector<pair<int, int>>` 或 `priority_queue<pair<int, int>>` 可直接排序或建堆，无需手写比较器。
2. **结构化绑定（C++17）**：
   ```cpp
   auto [id, name] = student1; // 直接解包 first 与 second，语义比 .first/.second 更清晰
   ```

> [!tip] 超过两个字段时如何选择？
> - 临时组合 3 个及以上异构值：使用 [[CS Learning/C++ STL/Containers/Utility/tuple/tuple|std::tuple]]；
> - 需要清晰业务字段名（如 `x, y, weight`）：自定义 `struct` 的可读性远胜嵌套 `pair<int, pair<int, int>>`。

---

## 完整源码

```cpp
/*
pair的定义:
pair是utility库中最常用的组件,用于将两个值组合成一个单一对象。

pair的声明:
#include <utility>
// 创建 pair 对象的基本方式
pair<类型1,类型2> 变量名(值1,值2);

pair<T1,T2>等价于           e.g. pair<int,double>a;等价于
struct{                     struct{
T1 first;                          int first;
T2 second;                         double second;
};                          }a;

make_pair 是一个模板函数,可以自动推导类型,简化 pair 的创建过程。
*/
#include <iostream>
#include <utility>
#include <string>
using namespace std;
int main() {
    // 方式1：直接初始化
    pair<int,string> student1(101,"Alice");
    // 方式2：使用 make_pair 函数（推荐）
    auto student2=make_pair(102,"Bob");
    // 方式3：C++17 起支持的推导指引
    pair student3(103,"Charlie");
    // 访问 pair 的成员
    cout<<"学号: "<<student1.first<<",姓名: "<<student1.second<<endl;
    return 0;
}
```
