---
title: 14-1-learning format — 格式化输入输出与文件操作
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
  - 14-1
  - 14-1-learning format
  - 格式化输入输出与文件操作
  - printf scanf 格式说明符
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# 14-1-learning format — 格式化输入输出与文件操作

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/13-3 多文件程序结构/max/max|max — 多文件程序的 max 函数]] · 下一篇：[[CS Learning/C wengkai/14-2 按位输出二进制/14-2-learning Binary|14-2-learning Binary — 按位输出二进制]]
> 源码：[[CS Learning/C wengkai/14-1 格式化输入输出与文件操作/14-1-learning format.c|查看源码]]

> [!abstract] 本节概览
> 系统梳理 C 语言标准输入输出库 `<stdio.h>` 的两大核心板块：**`printf` / `scanf` 完整格式化控制串语法**（标志位、宽度、精度、长度修饰符、类型转换符），以及基于 **`FILE*`** 指针的文本/标准文件读写模式（`fopen` / `fscanf` / `fprintf` / `fclose`）。

---

## 一、`printf` 格式化语法：`%[flags][width][.prec][hlL]type`

### 1. 标志位（Flags）与宽度/精度（Width & Precision）

| Flag | 含义 | Width / Prec | 含义 |
| :---: | --- | :---: | --- |
| `-` | 左对齐（默认右对齐） | `number` | 最小输出字符宽度（含小数点与符号） |
| `+` | 强制输出正负号（正数前加 `+`） | `*` | 宽度由下一个 `int` 实参动态指定（如 `printf("%*d", 6, 123)`） |
| `(space)` | 正数前留一个空格（与负号对齐） | `.number` | 小数点后保留位数（对 `%s` 表示最大输出字符数） |
| `0` | 宽度不足时用 `0` 左侧填充 | `.*` | 精度由下一个 `int` 实参动态指定 |

### 2. 长度修饰符（Length）与转换类型（Type）

| 长度修饰 | 对应类型 | Type | 含义 | Type | 含义 |
| :---: | --- | :---: | --- | :---: | --- |
| `hh` | `signed/unsigned char`（单字节） | `d` / `i` | 有符号十进制整数 `int` | `f` / `F` | 定点浮点数 |
| `h` | `short` | `u` | 无符号十进制 `unsigned int` | `e` / `E` | 科学计数法指数 |
| `l` | `long` | `o` | 八进制无符号整数 | `g` / `G` | 自动选择较短的 `%f` 或 `%e` |
| `ll` | `long long` | `x` / `X` | 小写 / 大写十六进制 | `a` / `A` | 十六进制浮点数 |
| `L` | `long double` | `c` / `s` | 单字符 / 字符串 | `p` / `n` | 指针地址 / 已输出字符数写入指针 |

> [!warning] `%n` 安全限制提示（保留原笔记记录）
> `%n` 会将此前已输出的字符数写回对应的 `int*` 实参，极易被格式化字符串漏洞利用；**Microsoft CRT 出于安全原因默认禁用 `printf` 中的 `%n`**。

---

## 二、`scanf` 格式化语法：`%[flag]type`

| Flag / 修饰 | 含义 | Type | 含义 |
| :---: | --- | :---: | --- |
| `*` | **赋值抑制（跳过该字段不存入变量）**，如 `scanf("%*d%d", &num)` | `d` / `i` | 十进制整数 / 自动识别十、八(`0`)、十六(`0x`)进制 |
| `number` | 最多读取的字符宽度（防缓冲区溢出） | `u` / `o` / `x` | 无符号十进制 / 八进制 / 十六进制 |
| `hh` / `h` | `char` / `short` | `a`/`e`/`f`/`g` | 浮点数（注意：`double` 必须写 `%lf`） |
| `l` / `ll` / `L` | `long` 或 `double` / `long long` / `long double` | `c` / `s` / `[...]` / `p` | 字符 / 字符串 / 扫描集合 / 指针 |

> [!note] 原笔记细节勘误
> 原注释表将 `scanf` 的 `l` 写为 `long double`；严格来说在 `scanf` 中 `%lf` 对应 `double`，`%ld` 对应 `long`，而 `%Lf` 才对应 `long double`。

---

## 三、标准文件操作（`FILE*`）

```c
FILE *fp = fopen("file", "r");
if (fp) {
    fscanf(fp, ...);
    fclose(fp);
} else {
    // 打开失败处理
}
```

| 打开模式 | 行为说明（文件存在 vs. 不存在） |
| :---: | --- |
| `"r"` | 只读打开；文件必须存在，否则返回 `NULL` |
| `"r+"` | 读写打开，从文件头开始；文件必须存在 |
| `"w"` | 只写打开；不存在则新建，**已存在则清空原内容** |
| `"w+"` | 读写打开；不存在则新建，**已存在则清空原内容** |
| `"a"` | 追加写入；不存在则新建，已存在则从文件末尾写入 |
| `"...x"` (C11) | 独占新建模式（如 `"wx"`），若文件已存在则打开失败，防止误覆盖 |

> [!tip] 跨课程关联
> C++ 中利用 `freopen` 重定向标准流以及 `cin`/`cout` 的对比用法，可参阅 [[CS Learning/C++ PKU/freopen/freopen|freopen — 输入输出重定向]]。

## 完整源码

```c
/*%[flags][width][.prec][hIL]type
Flag    含义                    width或prec     含义
-       左对齐                  number          最小字符数(包括小数点)
+       在前面放+或-(强制输出+)  *               下一个参数是字符数
(space) 正数留空                .number         小数点后的位数
0       0填充                   .*              下一个参数是小数点后的位数

hlL指代类型修饰                 type            用于              type          用于
hh      单个字节                i/d             int              g/G           float
h       short                   u              unsigned int     a/A           十六进制浮点
l       long                    o              八进制             c            char
ll      long long               x              十六进制           s            字符串
L       long double             X              字母大写的十六进制  p            指针
                                f/F            float             n            读入/写出的个数
                                e/E            指数
对于scanf的情况:%[flag]type
Flag    含义
*       跳过                    l               long double
number  最大字符数              ll              long long
hh      char                    L               long double
h       short
type    用于
d       int                   a/e/f/g          float
i       整数可能为十六或八进制  c                char
u       unsigned int          s                字符串
o       八进制                [...]             所允许的字符
x       十六进制              p                 指针
*/
#include <stdio.h>
int main(){
    int num;
    //printf("%9d\n",123);
    //printf("%-9d\n",123);
    //printf("%+9d\n",123);
    //printf("%09d\n",123);
    //printf("%*d\n",6,123);
    //printf("%9.2f\n",123.0);
    //printf("%hhd\n",12345);
    //printf("%d%n\n",12345, &num);
    //printf("%d\n",num);//%n是一个比较特殊、实际开发中也较少主动使用的格式符
                       //Microsoft的CRT出于安全原因,默认禁用了printf中的%n
    //scanf("%*d%d",&num);
    //printf("%d",num);
    return 0;
}
/*
FILE结构:
FILE*fopen(const char *restrict path,const char *restrict mode);
int fclose(FILE *stream);
fscanf(FILE*,...);
fprintf(FILE*,...);

FILE* fp=fopen("file","r");         r打开只读
    if (fp){                        r+打开读写,从文件头开始
        fscnf(fp,...);              w打开只写。如果不存在则新建,如果存在则清空
        fclose(fp);                 w+打开读写。如果不存在则新建,如果存在则清空
    }                               a打卡追加。如果不存在则新建,如果存在则从文件尾开始
    else {...}                      ...x只新建，如果文件已存在则不能打开
*/
```
