# count() — 元素计数

[查看源码](./count%28%29.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

count是C++标准模板库(STL)中的一个算法函数，用于统计某个指定值在容器或指定范围内出现的次数。它包含在 &lt;algorithm&gt; 头文件中。

### 语法

```cpp
count(first,last,value);
```

first：指向范围起始位置的迭代器（包含该位置）。

last：指向范围结束位置的迭代器（不包含该位置）。

value：要查找和统计的目标值。

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 16 | 独立注释 | 统计数字 2 出现的次数 |
| 18 | ` cout<<"数字 2 出现的次数为: "<<count_2<<endl; ` | 输出 3 |

## 完整源码

```cpp
/*
count是C++标准模板库(STL)中的一个算法函数，用于统计某个指定值在容器或指定范围内出现的次数。它包含在 <algorithm> 头文件中。

语法:
count(first,last,value);
    first：指向范围起始位置的迭代器（包含该位置）。
    last：指向范围结束位置的迭代器（不包含该位置）。
    value：要查找和统计的目标值。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    vector<int> nums={1,2,3,2,4,2};
    // 统计数字 2 出现的次数
    int count_2=count(nums.begin(),nums.end(),2);
    cout<<"数字 2 出现的次数为: "<<count_2<<endl; // 输出 3
    return 0;
}
```
