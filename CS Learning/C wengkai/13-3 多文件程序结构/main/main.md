# main — 多文件程序的入口

[查看源码](./main.c) · [返回 C wengkai 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 代码导读

本文件声明并调用 max 函数，传入 5 和 6，然后输出返回值；函数实现位于配套的 max.c。

## 多文件编译

配套文件：[max.c](../max/max.c)。在上一级 `13-3 多文件程序结构` 目录运行：

```powershell
gcc "main/main.c" "max/max.c" -o example.exe
```

## 完整源码

```c
#include <stdio.h>
int max(int a,int b);
int main(void){
    int a=5,b=6;
    printf("%d\n",max(a,b));
    return 0;
}
```
