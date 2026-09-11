# scanf &amp; cin special usage — 读入状态与循环输入

[查看源码](./scanf%20%26%20cin%20special%20usage.cpp) · [返回 C++ PKU 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

```cpp
while ((scanf("%d%d",&n,&m))!=EOF){
        printf("%d\n",n+m);
    }
```

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 4 | 独立注释 | 注意scanf的返回值为int类型,故当值为EOF时输入结束 |
| 5 | 独立注释 | 而cin表达式的值在成功读入所有变量时为true,否则为flase |
| 13 | 独立注释 | 以上两种都可用于无结束标记的数据输入情况 |

## 完整源码

```cpp
#include <iostream>
using namespace std;
int main(){
    //注意scanf的返回值为int类型,故当值为EOF时输入结束
    //而cin表达式的值在成功读入所有变量时为true,否则为flase
    int n,m;
    /*while ((scanf("%d%d",&n,&m))!=EOF){
        printf("%d\n",n+m);
    }*/
    while (cin>>n>>m){
        printf("%d\n",n+m);
    }
    //以上两种都可用于无结束标记的数据输入情况
    return 0;
}
```
