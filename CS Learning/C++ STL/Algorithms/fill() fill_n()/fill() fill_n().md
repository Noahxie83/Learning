# fill() fill\_n() — 序列填充

[查看源码](./fill%28%29%20fill_n%28%29.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

fill() 和 fill\_n() 算法提供了一种为元素序列填入给定值的简单方式，fill() 会填充整个序列

fill\_n() 则以给定的迭代器为起始位置，为指定个数的元素设置值。

### 语法

```cpp
fill(ForwardIterator first,ForwardIterator last,const T& val);
```

first： 指向填充区域开始位置的迭代器（包含）。

| 用法 / 项目 | 原笔记 |
| --- | --- |
| last： | 指向填充区域结束位置的迭代器（不包含）。 |
| val： | 用来填充的新值。 |

fill\_n() 的参数分别是指向被修改序列的第一个元素的正向迭代器、被修改元素的个数以及要被设置的值。

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 17 | ` vector<int> vec(5); ` | 创建一个包含 5 个元素的 vector |
| 18 | 独立注释 | 将整个 vector 填充为 9 |

## 完整源码

```cpp
/*
fill() 和 fill_n() 算法提供了一种为元素序列填入给定值的简单方式，fill() 会填充整个序列
fill_n() 则以给定的迭代器为起始位置，为指定个数的元素设置值。

语法:
fill(ForwardIterator first,ForwardIterator last,const T& val);
    first： 指向填充区域开始位置的迭代器（包含）。
    last：  指向填充区域结束位置的迭代器（不包含）。
    val：   用来填充的新值。
fill_n() 的参数分别是指向被修改序列的第一个元素的正向迭代器、被修改元素的个数以及要被设置的值。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
    vector<int> vec(5); // 创建一个包含 5 个元素的 vector
    // 将整个 vector 填充为 9
    fill(vec.begin(),vec.end(),9);
    for(int x : vec){
        cout<<x<<" ";
    }
    return 0;
}
```
