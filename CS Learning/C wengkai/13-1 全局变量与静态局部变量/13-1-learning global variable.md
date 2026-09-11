# 13-1-learning global variable — 全局变量与静态局部变量

[查看源码](./13-1-learning%20global%20variable.c) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记（原注释）

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 3 | ` int gAll=12; ` | 全局变量默认初始化为0 |
| 4 | 独立注释 | int g2=gAll;//只能用已知值初始化全局变量 |
| 6 | 独立注释 | printf("in %s gAll=%d\\n",\_\_func\_\_,gAll); |
| 7 | ` f(); ` | f();f(); |
| 8 | 独立注释 | printf("agn in %s gAll=%d\\n",\_\_func\_\_,gAll); |
| 12 | 独立注释 | int gAll=1;//局部变量覆盖全局变量 |
| 13 | ` int k=1; ` | 普通本地变量执行三次f为1 3;1 3;1 3 |
| 14 | ` static int all=1; ` | 静态本地变量执行三次f为1 3;3 5;5 7 |
| 15 | ` printf("&gAll=%p\n",&gAll); ` | &amp;gAll=00007FF736D53000 |
| 16 | ` printf("&all =%p\n",&all); ` | &amp;all =00007FF736D53004  静态本地变量本质上是全局变量，生存期都是全局，区别是作用域 |
| 17 | ` printf("&k   =%p\n",&k); ` | &amp;k   =0000009D25FFF69C |
| 19 | 独立注释 | gAll+=2; |

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
