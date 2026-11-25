---
title: node — 链表节点定义
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
  - node.h
  - 链表节点定义
  - 自引用结构体
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# node — 链表节点定义

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/array/array|array — 可变长数组接口]]
> 源码：[[CS Learning/C wengkai/node/node.h|查看源码]]

> [!abstract] 本节概览
> 单链表模块的公共节点头文件 `node.h`：通过**自引用结构体（Self-Referential Struct）**定义链表节点 `Node`（数据域 `value` + 指向下一节点的指针域 `next`），并配合头文件保护宏供链表实现文件引用。

---

## 核心知识点

- **为什么结构体内部必须写 `struct _node *next;` 而不是 `Node *next;`？**
  - 在结构体体内部解析 `next` 成员时，`typedef` 别名 `Node` 尚未定义完成，因此必须使用结构体标签名 `struct _node` 来声明指向自身类型的指针！
- **为什么成员只能是指针而非结构体本身？**
  - 结构体不能直接包含自身实例（会导致大小无限递归），但指向自身的指针大小固定（32 位系统 4B / 64 位系统 8B），因此合法。

---

## 配套实现

- 配套链表实现与完整操作解析：[[CS Learning/C wengkai/12-2 单链表的增删查与释放/12-2-learning linked-list|12-2-learning linked-list — 单链表的增删查与释放]]

## 完整源码

```c
#ifndef _NODE_H_
#define _NODE_H_
typedef struct _node{
    int value;
    struct _node *next;
}Node;
#endif
```
