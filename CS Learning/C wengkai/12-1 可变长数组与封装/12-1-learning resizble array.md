# 12-1-learning resizble array — 可变长数组与封装

[查看源码](./12-1-learning%20resizble%20array.c) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

重要思想“封装”：外部代码不直接操作内部细节，而是通过各种函数来操作，

例如size、free函数的创建和main中at的使用

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 38 | ` *array_at(&a,0)=10; ` | &lt;=&gt;a.array\[0\]=10;,此处使用函数用以封装 |

## 文件依赖与编译

本文件使用 ` #include "array.h" `。整理后的头文件：[array.h](../array/array.h)；[头文件说明](../array/array.md)。

在当前笔记所在文件夹打开终端，可用以下 GCC 命令指定头文件搜索目录：

```powershell
gcc -I "../array" "12-1-learning resizble array.c" -o example.exe
```

## 完整源码

```c
#include "array.h"
#include <stdio.h>
#include <stdlib.h>
const int BLOCK_SIZE=20;
Array array_create(int init_size){
    Array a;
    a.size=init_size;
    a.array=(int*)malloc(sizeof(int)*a.size);
    return a;
}
void array_free(Array *a){
    free(a->array);
    a->size=0;
    a->array=NULL;
}
int array_size(const Array *a){
    return a->size;
}
int* array_at(Array *a,int index){
    if (index>=a->size){
        array_inflate(a,(index/BLOCK_SIZE+1)*BLOCK_SIZE-a->size);
    }
    return &(a->array[index]);
}
void array_inflate(Array *a,int more_size){
    int *p=(int*)malloc(sizeof(int)*(a->size+more_size));
    int i;
    for (i=0;i<a->size;i++){
        p[i]=a->array[i];
    }
    free(a->array);
    a->array=p;
    a->size+=more_size;
}
int main(int argc,char const *argv[]){
    Array a=array_create(100);
    printf("%d\n",array_size(&a));
    *array_at(&a,0)=10;//<=>a.array[0]=10;,此处使用函数用以封装
    printf("%d\n",*array_at(&a,0));
    int cnt=0,number=0;
    while (number!=-1){
        scanf("%d",&number);
        if (number!=-1){
        *array_at(&a,cnt++)=number;
        }
    }
    array_free(&a);
    return 0;
}
/*重要思想“封装”：外部代码不直接操作内部细节，而是通过各种函数来操作，
  例如size、free函数的创建和main中at的使用*/
```
