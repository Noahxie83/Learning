# pointer — void 指针与内存操作

[查看源码](./pointer.cpp) · [返回 C++ PKU 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

与C语言不同,在C++中,对于Void\* 指针类型的指针p

sizeof(void)没有定义,\*p、++p、p+=n、p+n等均无定义

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 11 | ` memset(szName,'a',10); ` | void\*的用途之一,memset(void\* dest,int ch,int n)即把从dest开始的n个字节都设置成ch,返回dest,ch只有第一个字节起作用 |
| 12 | ` cout<<szName<<endl; ` | 输出了10个a，memset可用于初始化字符串数组 |
| 14 | ` cout<<a<<endl; ` | 输出20个0,体现出void\* 可以用于memset函数中让第一个参数可以是任何类型的指针 |
| 17 | ` memcpy(a2,a1,10*sizeof(int)); ` | memcpy(void\* dest,void\* src,int n)把地址scr开始的n个字节拷贝到地址dest,返回dest |

## 完整源码

```cpp
/*
与C语言不同,在C++中,对于Void* 指针类型的指针p
sizeof(void)没有定义,*p、++p、p+=n、p+n等均无定义
*/
#include <iostream>
#include <cstring>
using namespace std;
int main(){
    char szName[200]="";
    int a[20];
    memset(szName,'a',10);//void*的用途之一,memset(void* dest,int ch,int n)即把从dest开始的n个字节都设置成ch,返回dest,ch只有第一个字节起作用
    cout<<szName<<endl;//输出了10个a，memset可用于初始化字符串数组
    memset(a,'0',sizeof(a));
    cout<<a<<endl;//输出20个0,体现出void* 可以用于memset函数中让第一个参数可以是任何类型的指针
    return 0;
    int a1[10],a2[10];
    memcpy(a2,a1,10*sizeof(int));//memcpy(void* dest,void* src,int n)把地址scr开始的n个字节拷贝到地址dest,返回dest
}
```
