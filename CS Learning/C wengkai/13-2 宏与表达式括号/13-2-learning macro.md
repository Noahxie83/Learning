# 13-2-learning macro — 宏与表达式括号

[查看源码](./13-2-learning%20macro.c) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记（原注释）

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 1 | ` #include <stdio.h> ` | \#语句是编译预处理语句 |
| 2 | ` #define PI 3.14159 ` | 等效于const double PI=3.14159;这里定义的PI就是宏(macro) |
| 9 | ` #define radtodeg2(x) (x)*57.29578 ` | 注意一切都要有括号 |
| 11 | 独立注释 | printf(FORMAT,PI2\*3.0); |
| 12 | 独立注释 | PRT; |
| 13 | 独立注释 | int i; |
| 14 | 独立注释 | scanf("%d",&amp;i); |
| 15 | 独立注释 | printf("%d\\n",cube(i+2)); |

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
