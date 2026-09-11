# unordered\_map unordered\_multimap — 无序键值映射

[查看源码](./unordered_map%20unordered_multimap.cpp) · [返回 C++ STL 笔记目录](../../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### 原注释 1（源码第 1–18 行）

#### unordered\_map的定义

在 C++ 中,&lt;unordered\_map&gt; 是标准模板库(STL)的一部分,提供了一种基于哈希表的键值对容器。

与 map 不同,unordered\_map 不保证元素的排序,但通常提供更快的查找速度。

unordered\_map 是一个关联容器,它存储了键值对(key-value pairs),其中每个键(key)都是唯一的。

unordered\_map 使用哈希表来存储元素,这使得它在查找、插入和删除操作中具有平均常数时间复杂度。

#### unordered\_map的声明

头文件\#include &lt;unordered\_map&gt;

```cpp
unordered_map<key_type,value_type> map_name;
```

key\_type 是键的类型。

value\_type 是值的类型。

unordered\_multimap:

和 unordered\_map 容器一样,unordered\_multimap 容器也以键值对的形式存储数据,且底层也采用哈希表结构存储各个键值对。

两者唯一的不同之处在于,unordered\_multimap容器可以存储多个键相等的键值对,而unordered\_map 容器不行。

STL标准库中实现unordered\_multimap容器的模板类并没有定义在以自己名称命名的头文件中,而是和unordered\_map容器一样,定义在&lt;unordered\_map&gt;

### 原注释 2（源码第 23–32 行）

以下是初始化示例

```cpp
    // 默认构造
    unordered_map<int,string> myMap;
    // 构造并初始化
    unordered_map<int,string> myMap={{1,"one"},{2,"two"}};
    // 构造并指定初始容量
    unordered_map<int,string> myMap(10);
    // 构造并复制另一个 unordered_map
    unordered_map<int,string> anotherMap=myMap;
```

### 原注释 3（源码第 55–59 行）

| 性质 | 解释 | map | multimap | unordered\_map | unordered\_multimap |
| --- | --- | --- | --- | --- | --- |
| 互异性 | 一个键仅可以在映射中出现一次 | ✔ | ❌(任意次) | ✔ | ❌(任意次) |
| 无序性 | 键是没有顺序的 | ❌(从小到大) | ❌(从小到大) | ✔ | ✔ |

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 34 | 独立注释 | 创建一个 unordered\_map,键为 int,值为 string |
| 36 | 独立注释 | 插入一些键值对 |
| 40 | 独立注释 | 打印所有元素 |
| 44 | 独立注释 | 访问特定键的值 |
| 46 | 独立注释 | 删除键为1的元素 |
| 48 | 独立注释 | 再次打印所有元素 |

## 完整源码

```cpp
/*
unordered_map的定义:
在 C++ 中,<unordered_map> 是标准模板库(STL)的一部分,提供了一种基于哈希表的键值对容器。
与 map 不同,unordered_map 不保证元素的排序,但通常提供更快的查找速度。
unordered_map 是一个关联容器,它存储了键值对(key-value pairs),其中每个键(key)都是唯一的。
unordered_map 使用哈希表来存储元素,这使得它在查找、插入和删除操作中具有平均常数时间复杂度。

unordered_map的声明:
头文件#include <unordered_map>
unordered_map<key_type,value_type> map_name;
    key_type 是键的类型。
    value_type 是值的类型。

unordered_multimap:
和 unordered_map 容器一样,unordered_multimap 容器也以键值对的形式存储数据,且底层也采用哈希表结构存储各个键值对。
两者唯一的不同之处在于,unordered_multimap容器可以存储多个键相等的键值对,而unordered_map 容器不行。
STL标准库中实现unordered_multimap容器的模板类并没有定义在以自己名称命名的头文件中,而是和unordered_map容器一样,定义在<unordered_map>
*/
#include <iostream>
#include <unordered_map>
using namespace std;
int main(){
    /*以下是初始化示例
    // 默认构造
    unordered_map<int,string> myMap;
    // 构造并初始化
    unordered_map<int,string> myMap={{1,"one"},{2,"two"}};
    // 构造并指定初始容量
    unordered_map<int,string> myMap(10);
    // 构造并复制另一个 unordered_map
    unordered_map<int,string> anotherMap=myMap;
    */

    // 创建一个 unordered_map,键为 int,值为 string
    unordered_map<int,string> myMap;
    // 插入一些键值对
    myMap[1]="one";
    myMap[2]="two";
    myMap[3]="three";
    // 打印所有元素
    for (const auto& pair:myMap){
        cout<<"Key: "<<pair.first<<",Value: "<<pair.second<<endl;
    }
    // 访问特定键的值
    cout<<"Value for key 2: "<<myMap[2]<<endl;
    // 删除键为1的元素
    myMap.erase(1);
    // 再次打印所有元素
    cout<<"After erasing key 1:"<<endl;
    for (const auto& pair:myMap){
        cout<<"Key: "<<pair.first<<",Value: "<<pair.second<<endl;
    }
    return 0;
}
/*
性质	    解释	                 map	        multimap	unordered_map       unordered_multimap
互异性	一个键仅可以在映射中出现一次	✔	          ❌(任意次)	      ✔                    ❌(任意次)
无序性	键是没有顺序的	              ❌(从小到大)	❌(从小到大)	     ✔                    ✔
*/
```
