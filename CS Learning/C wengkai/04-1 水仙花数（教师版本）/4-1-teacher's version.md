---
title: 4-1-teacher's version — 水仙花数（教师版本）
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
  - 4-1-teacher's version
  - 水仙花数（教师版本）
  - 多层循环枚举与幂运算
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# 4-1-teacher's version — 水仙花数（教师版本）

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/03-4 百分制成绩转换/3-4|3-4 — 百分制成绩转换]] · 下一篇：[[CS Learning/C wengkai/04-1 水仙花数/4-1|4-1 — 水仙花数]]
> 源码：[[CS Learning/C wengkai/04-1 水仙花数（教师版本）/4-1-teacher's version.c|查看源码]]

> [!abstract] 本题概览
> 翁恺老师课堂示范版：给定位数 $N$（$3 \le N \le 7$），按递增顺序输出所有 $N$ 位水仙花数。采用**三层嵌套循环**——外层枚举所有 $N$ 位数、中层拆解各位数字、内层连乘计算 $d^N$；可与预计算优化版本 [[CS Learning/C wengkai/04-1 水仙花数/4-1|4-1 — 水仙花数]] 对照阅读。

---

## 题目描述

水仙花数是指一个 $N$ 位正整数（$N \ge 3$），它的每个位上的数字的 $N$ 次幂之和等于它本身。

例如：$153 = 1^3 + 5^3 + 3^3$。本题要求编写程序，计算所有 $N$ 位水仙花数。

### 输入格式

输入在一行中给出一个正整数 $N$（$3 \le N \le 7$）。

### 输出格式

按递增顺序输出所有 $N$ 位水仙花数，每个数字占一行。

### 输入样例

```text
3
```

### 输出样例

```text
153
370
371
407
```

---

## 解题思路与核心知识点

1. **动态确定枚举区间**：因为 $N$ 在运行时才输入，先用循环计算下界 `first = 10^{N-1}`，枚举范围即为 `[first, first * 10 - 1]`。
2. **拆位并累加 $N$ 次幂**：
   - 必须用临时变量 `t = i` 参与拆位（`d = t % 10; t /= 10;`），**切忌直接修改外层循环控制变量 `i`**；
   - 对每一位数字 `d`，再用内层 `while` 循环连乘 $N$ 次得到 $p = d^N$ 并累加到 `sum`。
3. **复杂度与优化方向**：
   - **时间复杂度**：外层 $9 \times 10^{N-1}$ 个数 $\times$ 每数 $N$ 位 $\times$ 每位 $N$ 次乘法，约 $O(N^2 \cdot 10^{N-1})$。当 $N = 7$ 时，内层乘法执行次数高达数亿次，在严格限时评测中容易超时（TLE）。
   - **对比优化**：由于数字 `d` 只可能取 `0`–`9`，提前算好 $0^N \dots 9^N$ 存表即可省去最内层循环——详见自主优化版本 [[CS Learning/C wengkai/04-1 水仙花数/4-1|4-1 — 水仙花数]]。

## 完整源码

```c
/*
水仙花数是指一个N位正整数（N>=3），它的每个位上的数字的N次幂之和等于它本身。
例如：153 = 1^3 + 5^3+ 3^3。本题要求编写程序,计算所有N位水仙花数。
输入格式：    输入在一行中给出一个正整数N（3<=N<=7）。
输出格式：    按递增顺序输出所有N位水仙花数，每个数字占一行。
输入样例：    3
输出样例：
153
370
371
407
*/
#include <stdio.h>
int main(){
    int n;
    scanf("%d", &n);
    int first =1;
    int i =1;
    while (i<n){
        first *=10;
        i++;
    }
    i =first;
    while (i< first*10){
        int t = i;
        int sum = 0;
        do {
            int d = t%10;
            t/=10;
            int p =1;
            int j =0;
            while (j<n){
                p*=d ;
                j++;
            }
            sum += p;
        }while (t>0);
        if (sum==i){
            printf("%d\n",i);
        }
        i++;
}
return 0;
}
```
