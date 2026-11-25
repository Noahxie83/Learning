---
title: 13-2-learning macro — 宏与表达式括号
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
  - 13-2
  - 13-2-learning macro
  - 宏与表达式括号
  - C 语言预处理器宏
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# 13-2-learning macro — 宏与表达式括号

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/13-1 全局变量与静态局部变量/13-1-learning global variable|13-1-learning global variable — 全局变量与静态局部变量]] · 下一篇：[[CS Learning/C wengkai/13-3 多文件程序结构/main/main|main — 多文件程序的入口]]
> 源码：[[CS Learning/C wengkai/13-2 宏与表达式括号/13-2-learning macro.c|查看源码]]

> [!abstract] 本节概览
> 学习 C 语言编译预处理指令 `#define`（对象宏、多行宏、带参数宏），重点通过 `radtodeg1` 与 `radtodeg2` 的对比实验，理解宏在预处理阶段执行**纯粹文本替换**所带来的运算符优先级陷阱——==写带参宏时，每个参数与整个表达式外层都必须加括号==。

---

## 核心知识点与宏展开陷阱

### 1. 预处理指令与常见宏形式

- 以 `#` 开头的语句（`#include`、`#define` 等）由**预处理器**在编译前处理，**行尾不要加分号**；
- 宏定义若跨行，行尾用反斜杠 `\` 续行（如源码中的 `PRT`）；
- 带参数宏（如 `#define cube(x) ((x)*(x)*(x))`）在调用处直接展开文本，没有函数调用栈帧开销，但也不做类型检查。

### 2. 括号缺失的灾难对比（源码实测剖析）

| 宏定义 | 调用表达式 | 预处理文本展开结果 | 问题分析 |
| --- | --- | --- | --- |
| `radtodeg1(x) (x*57.29578)` | `radtodeg1(5+2)` | `(5+2*57.29578)` = `119.59` | **参数未加括号**：`*` 优先级高于 `+`，漏算 `5*57.29578`！ |
| `radtodeg2(x) (x)*57.29578` | `180/radtodeg2(1)` | `180/(1)*57.29578` = `10313.24` | **整体未加括号**：`/` 与 `*` 同级左结合，变成先除后乘！ |
| 正确写法 `((x)*57.29578)` | 任意调用 | `180/((1)*57.29578)` = `3.14159` | ==参数和整体双层加括号==，彻底隔离外部优先级干扰 |

> [!warning] 宏的隐藏副作用与现代替代
> - 即使写成 `((x)*(x)*(x))`，调用 `cube(i++)` 仍会展开为 `((i++)*(i++)*(i++))`，导致 `i` 被重复自增三次且触发未定义行为！
> - 现代 C/C++ 中，定义常量优先使用 `const` / `enum`，定义简短计算优先使用 `static inline` 函数而非复杂带参宏。

## 完整源码

```c
#include <stdio.h>//#语句是编译预处理语句
#define PI 3.14159//等效于const double PI=3.14159;这里定义的PI就是宏(macro)
#define FORMAT "%f\n"
#define PI2 2*PI
#define PRT printf(FORMAT,PI);\
            printf(FORMAT,PI2)
#define cube(x) ((x)*(x)*(x))
#define radtodeg1(x) (x*57.29578)
#define radtodeg2(x) (x)*57.29578//注意一切都要有括号
int main(){
    //printf(FORMAT,PI2*3.0);
    //PRT;
    //int i;
    //scanf("%d",&i);
    //printf("%d\n",cube(i+2));
    printf(FORMAT,radtodeg1(5+2));
    printf(FORMAT,radtodeg1(7));
    printf(FORMAT,radtodeg2(5+2));
    printf(FORMAT,radtodeg2(7));
    printf(FORMAT,180/radtodeg1(1));
    printf(FORMAT,180/radtodeg2(1));
    return 0;
}
```
