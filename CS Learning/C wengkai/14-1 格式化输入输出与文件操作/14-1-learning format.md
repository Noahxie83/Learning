# 14-1-learning format — 格式化输入输出与文件操作

[查看源码](./14-1-learning%20format.c) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### 原注释 1（源码第 1–28 行）

%\[flags\]\[width\]\[.prec\]\[hIL\]type

| Flag | 含义 | width或prec | 含义 |
| --- | --- | --- | --- |
| - | 左对齐 | number | 最小字符数(包括小数点) |
| + | 在前面放+或-(强制输出+) | \* | 下一个参数是字符数 |
| (space) 正数留空 | .number | 小数点后的位数 |  |
| 0 | 0填充 | .\* | 下一个参数是小数点后的位数 |

| hlL指代类型修饰 | type | 用于 | type | 用于 | 补充 |
| --- | --- | --- | --- | --- | --- |
| hh | 单个字节 | i/d | int | g/G | float |
| h | short | u | unsigned int | a/A | 十六进制浮点 |
| l | long | o | 八进制 | c | char |
| ll | long long | x | 十六进制 | s | 字符串 |
| L | long double | X | 字母大写的十六进制 | p | 指针 |
| f/F | float | n | 读入/写出的个数 |  |  |
| e/E | 指数 |  |  |  |  |

对于scanf的情况:%\[flag\]type

| Flag | 含义 | 补充 | 补充 |
| --- | --- | --- | --- |
| \* | 跳过 | l | long double |
| number | 最大字符数 | ll | long long |
| hh | char | L | long double |
| h | short |  |  |
| type | 用于 |  |  |
| d | int | a/e/f/g | float |
| i | 整数可能为十六或八进制 | c | char |
| u | unsigned int | s | 字符串 |
| o | 八进制 | \[...\] | 所允许的字符 |
| x | 十六进制 | p | 指针 |

### 原注释 2（源码第 46–59 行）

FILE结构:

```c
FILE*fopen(const char *restrict path,const char *restrict mode);
int fclose(FILE *stream);
fscanf(FILE*,...);
fprintf(FILE*,...);

FILE* fp=fopen("file","r");         r打开只读
    if (fp){                        r+打开读写,从文件头开始
```

| 用法 / 项目 | 原笔记 |
| --- | --- |
| fscnf(fp,...); | w打开只写。如果不存在则新建,如果存在则清空 |
| fclose(fp); | w+打开读写。如果不存在则新建,如果存在则清空 |
| } | a打卡追加。如果不存在则新建,如果存在则从文件尾开始 |

```c
    else {...}                      ...x只新建，如果文件已存在则不能打开
```

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 32 | 独立注释 | printf("%9d\\n",123); |
| 33 | 独立注释 | printf("%-9d\\n",123); |
| 34 | 独立注释 | printf("%+9d\\n",123); |
| 35 | 独立注释 | printf("%09d\\n",123); |
| 36 | 独立注释 | printf("%\*d\\n",6,123); |
| 37 | 独立注释 | printf("%9.2f\\n",123.0); |
| 38 | 独立注释 | printf("%hhd\\n",12345); |
| 39 | 独立注释 | printf("%d%n\\n",12345, &amp;num); |
| 40 | 独立注释 | printf("%d\\n",num);//%n是一个比较特殊、实际开发中也较少主动使用的格式符 |
| 41 | 独立注释 | Microsoft的CRT出于安全原因,默认禁用了printf中的%n |
| 42 | 独立注释 | scanf("%\*d%d",&amp;num); |
| 43 | 独立注释 | printf("%d",num); |

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
