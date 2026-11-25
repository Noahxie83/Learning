---
title: 13-1-learning global variable — 全局变量与静态局部变量
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: 翁恺 C 语言
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/翁恺_C_语言
aliases:
  - 13-1
  - 13-1-learning global variable
  - 全局变量与静态局部变量
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# 13-1-learning global variable — 全局变量与静态局部变量

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/12-2 单链表的增删查与释放/12-2-learning linked-list|12-2-learning linked-list — 单链表的增删查与释放]] · 下一篇：[[CS Learning/C wengkai/13-2 宏与表达式括号/13-2-learning macro|13-2-learning macro — 宏与表达式括号]]
> 源码：[[CS Learning/C wengkai/13-1 全局变量与静态局部变量/13-1-learning global variable.c|查看源码]]

> [!abstract] 本节概览
> 通过实测变量内存地址与多次函数调用的数值演变，深入区分 C 语言中的三类变量：**全局变量**、**静态局部变量（`static`）**与**普通局部变量（自动变量）**在**生存期（Lifetime）**、**作用域（Scope）**、默认初始化及内存分区上的本质差异。

---

## 核心知识点与实测对比

### 1. 三类变量全景对比

| 特性 | 全局变量 (`int gAll = 12;`) | 静态局部变量 (`static int all = 1;`) | 普通局部变量 (`int k = 1;`) |
| --- | --- | --- | --- |
| **存储分区** | 全局/静态数据区（Data / BSS） | 全局/静态数据区（与全局变量紧邻！） | 栈区（Stack） |
| **生存期** | 全局（程序启动到结束） | **全局**（程序启动到结束，跨调用保值） | 局部（函数返回即销毁） |
| **作用域** | 文件/跨文件全局可见 | **仅限当前函数/代码块内** | 仅限当前函数/代码块内 |
| **默认初值** | 自动初始化为 `0` | 自动初始化为 `0` | **未定义垃圾值** |
| **连续调 3 次 `f()` 输出** | 持续累加 | `1 -> 3`、`3 -> 5`、`5 -> 7` | 每次重置为 `1 -> 3` |

### 2. 原实测地址证据（保留原运行记录）

源码注释记录了一次 64 位 Windows 下的真实地址输出：
- `&gAll = 00007FF736D53000`（数据区）
- `&all  = 00007FF736D53004`（与 `gAll` 仅差 4 字节，紧挨在静态数据区！）
- `&k    = 0000009D25FFF69C`（位于完全不同的高位栈区地址）

==静态本地变量本质上就是「作用域受限于函数内部的全局变量」：生存期都是全局，区别仅在于可见范围。==

> [!warning] 两个经典语法规则
> 1. **编译期常量初始化**：在 C 语言中，全局变量与 `static` 变量的初始化表达式必须是**编译期常量**，不能用另一个非常量全局变量初始化（因此 `int g2 = gAll;` 在 C 中编译报错）。
> 2. **同名遮蔽（Shadowing）**：若函数内部定义了与全局变量同名的局部变量（如注释中的 `int gAll = 1;`），则在函数体内局部变量会遮蔽全局变量；利用 `__func__` 预定义标识符可在调试打印中直接输出当前函数名。

## 完整源码

```c
#include <stdio.h>
int f(void);
int gAll=12;//全局变量默认初始化为0
//int g2=gAll;//只能用已知值初始化全局变量
int main(int argc,char const *argv[]){
    //printf("in %s gAll=%d\n",__func__,gAll);
    f();//f();f();
    //printf("agn in %s gAll=%d\n",__func__,gAll);
    return 0;
}
int f(void){
    //int gAll=1;//局部变量覆盖全局变量
    int k=1;//普通本地变量执行三次f为1 3;1 3;1 3
    static int all=1;//静态本地变量执行三次f为1 3;3 5;5 7
    printf("&gAll=%p\n",&gAll);//&gAll=00007FF736D53000
    printf("&all =%p\n",&all); //&all =00007FF736D53004  静态本地变量本质上是全局变量，生存期都是全局，区别是作用域
    printf("&k   =%p\n",&k);   //&k   =0000009D25FFF69C
    printf("in %s all=%d\n",__func__,all);
    //gAll+=2;
    all+=2;
    printf("agn in %s all=%d\n",__func__,all);
    return all;
}
```
