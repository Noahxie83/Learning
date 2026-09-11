# tuple — 多元组

[查看源码](./tuple.cpp) · [返回 C++ STL 笔记目录](../../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### tuple的定义:(pair的升级版)

C++中的tuple是一个标准库类模板，用于存储固定数量的异类对象。

允许将多个对象捆绑成一个单一的对象，并且可以轻松地从中提取值或者通过结构化绑定将其解构到不同的变量中。

tuple提供了一个通用的数据结构，可以保存不同类型的元素，并通过下标或者get函数来访问其中的值。

### 常用函数

| 用法 / 项目 | 原笔记 |
| --- | --- |
| tuple\_size | 返回 tuple 中元素的数量 |
| tuple\_element | 返回 tuple 中指定索引的元素类型 |
| get | 通过索引访问 tuple 的元素 |
| tie | 将 tuple 的元素绑定到指定的变量 |
| make\_tuple | 创建 tuple |

forward\_as\_tuple创建 tuple，保留变量的类型(包括引用)

tuple\_cat       连接两个或多个 tuple

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 21 | 独立注释 | 直接初始化： |
| 23 | 独立注释 | 使用\`make\_tuple\`函数进行初始化： |
| 25 | 独立注释 | 使用\`tie\`进行结构化绑定的初始化： |
| 30 | 独立注释 | 使用\`forward\_as\_tuple\`进行创建和初始化： |
| 32 | 独立注释 | 使用 \`get\` 函数按索引访问元素： |
| 41 | 独立注释 | 注意，forward\_as\_tuple的初始化方式是无法使用结构化绑定访问元素的。 |

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
