# node — 链表节点定义

[查看源码](./node.h) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 代码导读

本文件定义 Node 节点：value 保存整数，next 指向下一个节点；由链表练习使用。

## 配套实现

该头文件随配套程序一起使用：[单链表的增删查与释放](../12-2%20单链表的增删查与释放/12-2-learning%20linked-list.md)。

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
