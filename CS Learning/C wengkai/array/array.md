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
aliases:
  - array.h
  - 可变长数组接口
  - 头文件防卫
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# array — 可变长数组接口

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/14-2 按位输出二进制/14-2-learning Binary|14-2-learning Binary — 按位输出二进制]] · 下一篇：[[CS Learning/C wengkai/node/node|node — 链表节点定义]]
> 源码：[[CS Learning/C wengkai/array/array.h|查看源码]]

> [!abstract] 本节概览
> 可变长数组模块的公共头文件 `array.h`：利用**头文件保护宏（Include Guard）**防止重复包含，定义 `Array` 结构体类型并对外声明创建、释放、查容量、安全访问与扩容五个抽象接口。

---

## 核心知识点

- **头文件保护（`#ifndef _ARRAY_H_` / `#define _ARRAY_H_` / `#endif`）**：当同一编译单元通过多条依赖链多次 `#include "array.h"` 时，防止 `Array` 结构体被重复定义而报错。
- **接口与实现分离**：头文件只放类型定义与函数原型声明，不放函数实现体和全局变量定义，具体实现见 [[CS Learning/C wengkai/12-1 可变长数组与封装/12-1-learning resizble array|12-1 — 可变长数组与封装]]。
- **命名规范小贴士**：C 标准保留以下划线加大写字母（如 `_ARRAY_H_`）开头的标识符供标准库/编译器使用，现代工程中推荐写成 `ARRAY_H` 以避免潜在冲突。

---

## 配套实现

- 配套实现源码与详细解析：[[CS Learning/C wengkai/12-1 可变长数组与封装/12-1-learning resizble array|12-1-learning resizble array — 可变长数组与封装]]

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
