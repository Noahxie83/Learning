---
title: tuple — 多元组
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
  - std::tuple
  - make_tuple
  - std::tie
  - STL 多元组
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# tuple — 多元组

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Utility/pair/pair|pair — 二元组]] · 下一篇：[[CS Learning/C++ STL/Containers/Utility/Utility/Utility|Utility — utility 工具]]
> 相关：[[CS Learning/C++ STL/Containers/Utility/pair/pair|pair — 二元组]]
> 源码：[[CS Learning/C++ STL/Containers/Utility/tuple/tuple.cpp|查看源码]]

> [!abstract] 本节概览
> `std::tuple`（头文件 `<tuple>`）是 [[CS Learning/C++ STL/Containers/Utility/pair/pair|std::pair]] 的泛化升级版，用于将**固定数量、任意类型的多个对象**捆绑为单一对象。支持编译期索引访问 `std::get<I>`、多变量解包 `std::tie`、C++17 结构化绑定以及多元组拼接 `std::tuple_cat`。

---

## 一、常用工具与元编程接口

| 工具 / 接口 | 作用说明 | 典型用法 |
| --- | --- | --- |
| `make_tuple(a, b, ...)` | 自动推导类型创建 `tuple` | `auto t = make_tuple(11, 22.0, "3aa");` |
| `get<I>(t)` / `get<T>(t)` | 按**编译期常量索引**（或唯一类型，C++14）访问元素引用 | `auto v = get<0>(t);` |
| `tie(a, b, ...)` | 生成左值引用 `tuple`，用于解包赋值或简化结构体 `<` 比较 | `tie(a, b, s) = t;`（可用 `std::ignore` 占位忽略某项） |
| `forward_as_tuple(...)` | 构造保存参数原始引用类别（左值/右值引用）的 `tuple` | 多用于转发参数给 `emplace` |
| `tuple_cat(t1, t2, ...)` | 将多个 `tuple` 拼接为一个新的 `tuple` | `auto t3 = tuple_cat(t1, t2);` |
| `tuple_size<Tuple>::value` | 编译期查询 `tuple` 元素个数 | `tuple_size_v<decltype(t)>` (C++17) |
| `tuple_element<I, Tuple>::type` | 编译期获取第 `I` 个元素的类型 | `tuple_element_t<1, decltype(t)>` |

---

## 二、解包方式对比与常见陷阱

```cpp
// 1. std::get<I>：索引 I 必须是编译期常量（不能写运行时循环变量 i）
int oa = get<0>(mtuple);

// 2. std::tie：解包到已声明的变量
int a; double b; string s;
tie(a, b, s) = make_tuple(111, 222.0, "3aaa");

// 3. C++17 结构化绑定（最简洁）
auto [intVal, doubleVal, strVal] = mtuple2;
```

> [!warning] `forward_as_tuple` 的悬空引用风险
> 源码第 30 行 `auto mtuple3 = forward_as_tuple(1111, 2222.0, "3aaaa");` 内部存储的是**对临时右值的引用**——语句结束时临时字面量即销毁，继续读写 `mtuple3`（包括对其做结构化绑定）会触发**未定义行为（悬空引用）**！`forward_as_tuple` 应仅作为**当前完整表达式内的临时转发参数**使用（例如 `mp.emplace(piecewise_construct, forward_as_tuple(k), forward_as_tuple(v))`），不要存为具名变量长期复用。

---

## 完整源码

```cpp
/*
tuple的定义:(pair的升级版)
C++中的tuple是一个标准库类模板，用于存储固定数量的异类对象。
允许将多个对象捆绑成一个单一的对象，并且可以轻松地从中提取值或者通过结构化绑定将其解构到不同的变量中。
tuple提供了一个通用的数据结构，可以保存不同类型的元素，并通过下标或者get函数来访问其中的值。

常用函数
tuple_size      返回 tuple 中元素的数量
tuple_element   返回 tuple 中指定索引的元素类型
get             通过索引访问 tuple 的元素
tie             将 tuple 的元素绑定到指定的变量
make_tuple      创建 tuple
forward_as_tuple创建 tuple，保留变量的类型(包括引用)
tuple_cat       连接两个或多个 tuple
*/
#include <iostream>
#include <tuple>
#include <string>
using namespace std;
int main(){
    // 直接初始化：
    tuple<int,double,string> mtuple(1,2.0,"3a");
    // 使用`make_tuple`函数进行初始化：
    auto mtuple2=make_tuple(11,22.0,"3aa");
    // 使用`tie`进行结构化绑定的初始化：
    int a;
    double b;
    string s;
    tie(a,b,s)=make_tuple(111,222.0,"3aaa");
    // 使用`forward_as_tuple`进行创建和初始化：
    auto mtuple3=forward_as_tuple(1111,2222.0,"3aaaa");
    // 使用 `get` 函数按索引访问元素：
    cout<<"使用 `get` 函数按索引访问元素："<<endl;
    int oa=get<0>(mtuple);
    double ob=get<1>(mtuple);
    string os=get<2>(mtuple);
    cout<<"oa="<<oa<<",ob="<<ob<<",os="<<os<<endl;
    cout<<"使用 tie 进行结构化绑定，将 tuple 成员绑定到指定的变量："<<endl;
    cout<<"a="<<a<<",b="<<b<<",s="<<s<<endl;
    cout<<"使用结构化绑定(C++17):"<<endl;
    // 注意，forward_as_tuple的初始化方式是无法使用结构化绑定访问元素的。
    auto [intVal,doubleVal,strVal]=mtuple2;
    cout<<"intVal="<<intVal<<",doubleVal="<<doubleVal<<",strVal="<<strVal<<endl;
    return 0;
}
```
