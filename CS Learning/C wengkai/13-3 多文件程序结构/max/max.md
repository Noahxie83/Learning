---
title: max — 多文件程序的 max 函数
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

# max — 多文件程序的 max 函数

[查看源码](./max.c) · [返回 C wengkai 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 代码导读

本文件通过条件表达式比较两个整数，返回较大者；它是 main.c 的配套实现文件。

## 多文件编译

配套文件：[main.c](../main/main.c)。在上一级 `13-3 多文件程序结构` 目录运行：

```powershell
gcc "main/main.c" "max/max.c" -o example.exe
```

## 完整源码

```c
int max(int a,int b){
    return a>b?a:b;
}
```
