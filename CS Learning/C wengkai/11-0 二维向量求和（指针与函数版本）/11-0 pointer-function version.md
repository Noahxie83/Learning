---
title: 11-0 pointer-function version — 二维向量求和（指针与函数版本）
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
  - 11-0 pointer-function version
  - 二维向量求和（指针与函数版本）
  - 结构体指针与输出参数
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# 11-0 pointer-function version — 二维向量求和（指针与函数版本）

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/10-5 查找子串的所有位置/10-5|10-5 — 查找子串的所有位置]] · 下一篇：[[CS Learning/C wengkai/11-0 二维向量求和/11-0|11-0 — 二维向量求和]]
> 源码：[[CS Learning/C wengkai/11-0 二维向量求和（指针与函数版本）/11-0 pointer-function version.c|查看源码]]

> [!abstract] 本题概览
> 使用结构体 `struct vector` 表示二维平面向量，并通过==结构体指针传参 + 箭头运算符 `->` + 输出参数模式==封装向量加法函数 `add()`，同时处理 IEEE 754 浮点数四舍五入输出 `-0.0` 的经典边界陷阱。对照直接计算版本见 [[CS Learning/C wengkai/11-0 二维向量求和/11-0|11-0 — 二维向量求和]]。

---

## 题目描述

本题要求编写程序，计算两个二维平面向量的和向量。

### 输入格式

输入在一行中按照 `x1 y1 x2 y2` 的格式给出两个二维平面向量 $V_1 = (x_1, y_1)$ 和 $V_2 = (x_2, y_2)$ 的分量。

### 输出格式

在一行中按照 `(x, y)` 的格式输出和向量，坐标输出小数点后 1 位（注意不能输出 `-0.0`）。

### 输入样例

```text
3.5 -2.7 -13.9 8.7
```

### 输出样例

```text
(-10.4, 6.0)
```

---

## 解题思路与核心知识点

### 1. 结构体指针传参与 `->` 运算符

```c
struct vector {
    double x;
    double y;
};

void add(struct vector *v1, struct vector *v2, struct vector *ret) {
    ret->x = v1->x + v2->x;
    ret->y = v1->y + v2->y;
}
```

| 传参方式 | 成员访问语法 | 内存开销 | 能否直接修改调用方对象 |
| --- | :---: | --- | :---: |
| 值传递 `struct vector v` | `v.x` | 拷贝整个结构体（16 字节） | 否（仅修改局部副本） |
| 指针传递 `struct vector *p` | `p->x`（等价于 `(*p).x`） | 仅传递单个指针（8 字节） | ==是（可通过 `ret` 回写结果）== |

> [!tip] 工程最佳实践：只读输入加 `const`
> 在 `add()` 函数中，`v1` 和 `v2` 仅用于读取而不应被修改，工程上推荐写为：
> `void add(const struct vector *v1, const struct vector *v2, struct vector *ret)`，借助编译器在编译期杜绝误修改入参。

### 2. 原始学习注释与 `-0.0` 浮点陷阱

| 源码行号 | 对应代码 | 原注释 |
| :---: | --- | --- |
| 32 | `}` | 确保不输出 `-0.0` |

> [!warning] 为什么会出现 `-0.0`？
> IEEE 754 浮点数带有独立的符号位，存在 `+0.0` 与 `-0.0` 两种零值。当实际结果落在区间 $(-0.05,\; 0)$ 内（例如 `-0.01` 或 `-0.04`）时，用 `%.1f` 四舍五入保留 1 位小数，数值归零但**负号位仍被保留**，从而打印出 `-0.0`！
>
> **解决办法**：利用判断 `if (ret.x > -0.05 && ret.x < 0.05) ret.x = 0.0;`（或者 `fabs(ret.x) < 0.05`）将接近零的值显式归一为正零 `0.0`。
>
> **格式复核提示**：题目输出样例为 `(-10.4, 6.0)`（逗号后有一个空格），而源码第 33 行为 `printf("(%.1f,%.1f)", ret.x, ret.y);`（逗号后无空格）；提交严格判题平台时务必核对逗号后的空格要求！

- **时间复杂度**：$O(1)$；**空间复杂度**：$O(1)$。

## 完整源码

```c
/*
本题要求编写程序，计算两个二维平面向量的和向量。
输入格式：
输入在一行中按照“x1 y1 x2 y2”的格式给出两个二维平面向量V1=(x1, y1)和V2=(x2, y2)的分量。
输出格式：
在一行中按照“(x, y)”的格式输出和向量，坐标输出小数点后1位（注意不能输出-0.0）。
输入样例：
3.5 -2.7 -13.9 8.7
输出样例：
(-10.4, 6.0)
*/
#include <stdio.h>
#include <string.h>
struct vector{
    double x;
    double y;
};
void add(struct vector *v1,struct vector *v2,struct vector *ret){
    ret->x=v1->x+v2->x;
    ret->y=v1->y+v2->y;
}
int main(){
    struct vector v1,v2,ret;
    scanf("%lf %lf %lf %lf",
        &v1.x,&v1.y,&v2.x,&v2.y);
    add(&v1,&v2,&ret);
    if(ret.x>-0.05&&ret.x<0.05){
        ret.x=0.0;
    }
    if(ret.y>-0.05&&ret.y<0.05){
        ret.y=0.0;
    }       //确保不输出-0.0
    printf("(%.1f,%.1f)",ret.x,ret.y);
    return 0;
}
```
