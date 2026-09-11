# pair — 二元组

[查看源码](./pair.cpp) · [返回 C++ STL 笔记目录](../../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### pair的定义

pair是utility库中最常用的组件,用于将两个值组合成一个单一对象。

### pair的声明

```cpp
#include <utility>
// 创建 pair 对象的基本方式
pair<类型1,类型2> 变量名(值1,值2);

pair<T1,T2>等价于           e.g. pair<int,double>a;等价于
struct{                     struct{
T1 first;                          int first;
T2 second;                         double second;
};                          }a;
```

make\_pair 是一个模板函数,可以自动推导类型,简化 pair 的创建过程。

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 23 | 独立注释 | 方式1：直接初始化 |
| 25 | 独立注释 | 方式2：使用 make\_pair 函数（推荐） |
| 27 | 独立注释 | 方式3：C++17 起支持的推导指引 |
| 29 | 独立注释 | 访问 pair 的成员 |

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
