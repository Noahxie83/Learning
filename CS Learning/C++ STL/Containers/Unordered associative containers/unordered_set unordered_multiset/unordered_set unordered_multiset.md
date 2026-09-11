# unordered\_set unordered\_multiset — 无序集合

[查看源码](./unordered_set%20unordered_multiset.cpp) · [返回 C++ STL 笔记目录](../../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### 原注释 1（源码第 1–17 行）

#### unordered\_set的定义

在C++中,&lt;unordered\_set&gt; 是标准模板库(STL)的一部分,提供了一种基于哈希表的容器,用于存储唯一的元素集合。

与 set 不同,unordered\_set 不保证元素的排序,但通常提供更快的查找、插入和删除操作。

#### unordered\_set的声明

头文件:\#include &lt;unordered\_set&gt;

unordered\_set&lt;Key,Hash =hash&lt;Key&gt;,Pred=equal\_to&lt;Key&gt;,Alloc=allocator&lt;Key&gt;&gt;

| 用法 / 项目 | 原笔记 | 补充 1 |
| --- | --- | --- |
| Key | 是存储在unordered\_set中的元素类型。 |  |
| Hash | 是一个函数或函数对象,用于生成元素的哈希值,默认为 hash&lt;Key&gt;。 |  |
| Pred | 是一个二元谓词,用于比较两个元素是否相等, | 默认为 equal\_to&lt;Key&gt;。 |
| Alloc 是分配器类型,用于管理内存分配, | 默认为 allocator&lt;Key&gt;。 |  |

unordered\_multiset:

unordered\_multiset除了能存储相同值的元素外,它和 unordered\_set 容器完全相同。

实现unordered\_multiset容器的模板类并没有定义在以该容器名命名的文件中,而是和 unordered\_set容器共用同一个&lt;unordered\_set&gt;头文件

### 原注释 2（源码第 56–61 行）

| 集合三要素 | 解释 | set | multiset | unordered\_set | unordered\_multiset |
| --- | --- | --- | --- | --- | --- |
| 确定性 | 一个元素要么在集合中,要么不在 | ✔ | ✔ | ✔ | ✔ |
| 互异性 | 一个元素仅可以在集合中出现一次 | ✔ | ❌(任意次) | ✔ | ❌(任意次) |
| 无序性 | 集合中的元素是没有顺序的 | ❌(从小到大) | ❌(从小到大) | ✔ | ✔ |

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 22 | 独立注释 | 创建一个整数类型的 unordered\_set |
| 24 | 独立注释 | 插入元素 |
| 28 | 独立注释 | 打印 unordered\_set 中的元素 |
| 34 | 独立注释 | 查找元素 |
| 41 | 独立注释 | 删除元素 |
| 48 | 独立注释 | 检查大小和是否为空 |
| 51 | 独立注释 | 清空 unordered\_set |

## 完整源码

```cpp
/*
unordered_set的定义:
在C++中,<unordered_set> 是标准模板库(STL)的一部分,提供了一种基于哈希表的容器,用于存储唯一的元素集合。
与 set 不同,unordered_set 不保证元素的排序,但通常提供更快的查找、插入和删除操作。

unordered_set的声明:
头文件:#include <unordered_set>
    unordered_set<Key,Hash =hash<Key>,Pred=equal_to<Key>,Alloc=allocator<Key>>
    Key   是存储在unordered_set中的元素类型。
    Hash  是一个函数或函数对象,用于生成元素的哈希值,默认为 hash<Key>。
    Pred  是一个二元谓词,用于比较两个元素是否相等,  默认为 equal_to<Key>。
    Alloc 是分配器类型,用于管理内存分配,           默认为 allocator<Key>。

unordered_multiset:
unordered_multiset除了能存储相同值的元素外,它和 unordered_set 容器完全相同。
实现unordered_multiset容器的模板类并没有定义在以该容器名命名的文件中,而是和 unordered_set容器共用同一个<unordered_set>头文件
*/
#include <iostream>
#include <unordered_set>
using namespace std;
int main(){
    // 创建一个整数类型的 unordered_set
    unordered_set<int> uset;
    // 插入元素
    uset.insert(10);
    uset.insert(20);
    uset.insert(30);
    // 打印 unordered_set 中的元素
    cout<<"Elements in uset: ";
    for (int elem:uset){
        cout<<elem<<" ";
    }
    cout<<endl;
    // 查找元素
    auto it = uset.find(20);
    if (it != uset.end()){
        cout<<"Element 20 found in uset."<<endl;
    } else{
        cout<<"Element 20 not found in uset."<<endl;
    }
    // 删除元素
    uset.erase(20);
    cout<<"After erasing 20, elements in uset: ";
    for (int elem:uset){
        cout<<elem<<" ";
    }
    cout<<endl;
    // 检查大小和是否为空
    cout<<"Size of uset: "<<uset.size()<<endl;
    cout<<"Is uset empty? "<<(uset.empty()?"Yes":"No")<<endl;
    // 清空 unordered_set
    uset.clear();
    cout<<"After clearing, is uset empty? "<<(uset.empty()?"Yes":"No")<<endl;
    return 0;
}
/*
集合三要素	        解释	                    set	        multiset	    unordered_set       unordered_multiset
确定性	    一个元素要么在集合中,要么不在	       ✔	        ✔	            ✔                      ✔
互异性	    一个元素仅可以在集合中出现一次	       ✔	        ❌(任意次)	    ✔                      ❌(任意次)
无序性	    集合中的元素是没有顺序的	          ❌(从小到大)  ❌(从小到大)	   ✔                       ✔
*/
```
