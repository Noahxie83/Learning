# 12-2-learning linked-list — 单链表的增删查与释放

[查看源码](./12-2-learning%20linked-list.c) · [返回 C wengkai 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记（原注释）

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 18 | ` }while (number!=-1); ` | 建立链表 |
| 19 | ` print(&list); ` | 输出链表 |
| 32 | ` } ` | 查找 |
| 45 | ` } ` | 删除 |
| 49 | ` } ` | 释放 |
| 66 | ` } ` | 链表的添加 |
| 73 | ` } ` | 链表的输出 |

## 文件依赖与编译

本文件使用 ` #include "node.h" `。整理后的头文件：[node.h](../node/node.h)；[头文件说明](../node/node.md)。

在当前笔记所在文件夹打开终端，可用以下 GCC 命令指定头文件搜索目录：

```powershell
gcc -I "../node" "12-2-learning linked-list.c" -o example.exe
```

## 完整源码

```c
#include "node.h"
#include <stdio.h>
#include <stdlib.h>
typedef struct _list{
    Node* head;
}List;
void add(List*pList,int number);
void print(List *pList);
int main(int argc,char const *argv[]){
    List list;
    int number;
    list.head=NULL;
    do {
        scanf("%d",&number);
        if (number!=-1){
            add(&list,number);
        }
    }while (number!=-1);//建立链表
    print(&list);//输出链表
    scanf("%d",&number);
    Node *p;
    int isFound=0;
    for (p=list.head;p;p=p->next){
        if (p->value==number){
            printf("Find it\n");
            isFound=1;
            break;
        }
    }
    if (!isFound){
        printf("Not Found\n");
    }//查找
    Node *q;
    for (q=NULL,p=list.head;p;q=p,p=p->next){
        if (p->value==number){
            if (q){
                q->next=p->next;
            }
            else {
                list.head=p->next;
            }
            free(p);
            break;
        }
    }//删除
    for (p=list.head;p;p=q){
        q=p->next;
        free(p);
    }//释放
    return 0;
}
void add(List*pList,int number){
    Node *p=(Node*)malloc(sizeof(Node));
    p->value=number;
    p->next=NULL;
    Node *last=pList->head;
    if (last){
        while (last->next){
        last=last->next;
        }
        last->next=p;
    }
    else {
        pList->head=p;
    }
}//链表的添加
void print(List *pList){
        Node *p;
    for (p=pList->head;p;p=p->next){
        printf("%d\t",p->value);
    }
    printf("\n");
}//链表的输出
```
