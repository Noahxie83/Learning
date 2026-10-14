---
title: array — 可变长数组接口
date: '2026-09-12'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: 翁恺 C 语言
tags:
- 领域/计算机基础
- 类型/程序笔记
- 课程/翁恺_C_语言
cssclasses:
- learning-note
- subject-cs
- learning-code
---

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/README|C wengkai]]

# array — 可变长数组接口

[查看源码](./array.h) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 代码导读

本文件定义 Array 结构体，并声明创建、释放、查询大小、访问元素和扩容的接口；实现位于可变长数组练习中。

## 配套实现

该头文件随配套程序一起使用：[可变长数组与封装](../12-1%20可变长数组与封装/12-1-learning%20resizble%20array.md)。

## 完整源码

```c
#ifndef _ARRAY_H_
#define _ARRAY_H_
typedef struct{
    int *array;
    int size;
}Array;
Array array_create(int init_size);
void array_free(Array *a);
int array_size(const Array *a);
int* array_at(Array *a,int index);
void array_inflate(Array *a,int more_size);
#endif
```
