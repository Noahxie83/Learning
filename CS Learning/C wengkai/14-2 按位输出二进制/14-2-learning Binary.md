---
title: 14-2-learning Binary — 按位输出二进制
date: '2026-09-11'
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

# 14-2-learning Binary — 按位输出二进制

[查看源码](./14-2-learning%20Binary.c) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记（原注释）

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 5 | 独立注释 | num=0x55555555; |

## 完整源码

```c
#include <stdio.h>
int main(){
    int num;
    scanf("%d",&num);
    //num=0x55555555;
    unsigned mask=1u<<31;
    for (;mask;mask>>=1){
        printf("%d",num&mask?1:0);
    }
    printf("\n");
    return 0;
}
```
