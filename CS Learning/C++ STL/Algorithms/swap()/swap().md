---
title: swap() — 交换
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
tags:
- 领域/计算机基础
- 类型/程序笔记
- 课程/Cpp_STL
cssclasses:
- learning-note
- subject-cs
- learning-code
---

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/README|C++ STL]]

# swap() — 交换

[查看源码](./swap%28%29.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

swap的功能:交换两个变量的值，譬如参数A和参数B，把A的值赋给B，再把B的值赋给A参数

虽然标准库为所有类型提供了通用的swap，但对于你自己的类，如果它有更高效的交换方式，你应该为其提供定制版本。

swap(\_Tp&amp; \_\_a,\_Tp&amp; \_\_b)

## 完整源码

```cpp
/*
swap的功能:交换两个变量的值，譬如参数A和参数B，把A的值赋给B，再把B的值赋给A参数
虽然标准库为所有类型提供了通用的swap，但对于你自己的类，如果它有更高效的交换方式，你应该为其提供定制版本。
 swap(_Tp& __a,_Tp& __b)
*/
#include <iostream>
#include <algorithm>
using namespace std;
int main(){
    int x=10;
    int y=20;
    cout<<"before swap: x:"<<x<<" y:"<<y<<endl;
    swap(x,y);
    cout<<"after swap: x:"<<x<<" y:"<<y<<endl;
}
```
