# max() min() max\_element() min\_element() — 最值与最值位置

[查看源码](./max%28%29%20min%28%29%20max_element%28%29%20min_element%28%29.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

max/min是一个定义在 &lt;algorithm&gt; 头文件中的函数模板，用于返回两个或多个值中的较大/小者。

两者类似，以下以max为例

常用形式：

比较两个值：max(a,b)

比较多个值（初始化列表）：max({a,b,c,d})

自定义比较规则：max(a,b,comp)

max\_element/max\_element 是用来在指定范围内查找最大/小元素的标准库算法函数

max\_element(v.begin(),v.end())

返回值：返回一个迭代器（指向最大元素），如果想获取具体数值，需要使用解引用操作符 \*。

查找区间：左闭右开区间 \[first,last)

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 20 | ` cout<<max(x,y)<<endl; ` | 输出 20 |
| 21 | ` cout<<max({2,9,2,5})<<endl; ` | 输出 9 (多值比较) |

## 完整源码

```cpp
/*
max/min是一个定义在 <algorithm> 头文件中的函数模板，用于返回两个或多个值中的较大/小者。
两者类似，以下以max为例

常用形式：
比较两个值：max(a,b)
比较多个值（初始化列表）：max({a,b,c,d})
自定义比较规则：max(a,b,comp)

max_element/max_element 是用来在指定范围内查找最大/小元素的标准库算法函数
max_element(v.begin(),v.end())
返回值：返回一个迭代器（指向最大元素），如果想获取具体数值，需要使用解引用操作符 *。
查找区间：左闭右开区间 [first,last)
*/
#include <iostream>
#include <algorithm>
using namespace std;
int main() {
    int x=10,y=20;
    cout<<max(x,y)<<endl;         // 输出 20
    cout<<max({2,9,2,5})<<endl; // 输出 9 (多值比较)
	int n[]={1,4,22,3,8,5};
	int len=sizeof(n)/sizeof(int);
	cout<<*max_element(n,n+len)<<endl;
	cout<<*min_element(n,n+len)<<endl;
    return 0;
}
```
