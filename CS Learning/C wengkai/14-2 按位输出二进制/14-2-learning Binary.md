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
aliases:
  - 14-2
  - 14-2-learning Binary
  - 按位输出二进制
  - C 语言位运算
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# 14-2-learning Binary — 按位输出二进制

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/14-1 格式化输入输出与文件操作/14-1-learning format|14-1-learning format — 格式化输入输出与文件操作]] · 下一篇：[[CS Learning/C wengkai/array/array|array — 可变长数组接口]]
> 源码：[[CS Learning/C wengkai/14-2 按位输出二进制/14-2-learning Binary.c|查看源码]]

> [!abstract] 本节概览
> 使用**无符号位掩码（Bitmask）**逐位提取并打印 32 位整数在内存中的完整二进制补码表示（如 `0x55555555` 输出交替的 `0101...`），深刻理解无符号右移（逻辑右移）与有符号右移（算术右移）的关键差异。

---

## 核心知识点与位运算原理

1. **构造最高位掩码**：`unsigned mask = 1u << 31;`
   - 字面量后加 `u` 指定为 `unsigned int`，避免有符号 `1 << 31` 溢出符号位触发未定义行为；
   - `mask` 二进制为 `10000000 00000000 00000000 00000000`。
2. **逻辑右移逐位扫描**：`for (; mask; mask >>= 1)`
   - 因为 `mask` 是**无符号整数**，每次 `mask >>= 1` 左侧必定补 `0`（逻辑右移），循环精确执行 32 次直至 `mask == 0` 退出；
   - `num & mask ? 1 : 0` 判断 `num` 在该位是否为 `1`（可直接观测负数在计算机中的**二进制补码**表示，例如 `-1` 输出 32 个 `1`）。

> [!warning] 如果把 `mask` 误声明为有符号 `int` 会怎样？
> 有符号负数右移在主流平台执行**算术右移（高位补符号位 `1`）**，导致 `mask` 永远不会变为 `0`，陷入**死循环**！因此位掩码务必声明为 `unsigned`。

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
