---
title: shuffle() — 随机打乱
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
tags:
- 领域/计算机基础
- 类型/程序笔记
- 课程/Cpp_STL
cssclasses:
- learning-note
- subject-cs
- learning-code
---

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/README|C++ STL]]

# shuffle() — 随机打乱

[查看源码](./shuffle%28%29.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

shuffle 是用于将指定范围内的元素随机打乱顺序(即洗牌)。

头文件&lt;algorithm&gt; 和 &lt;random&gt;

### 语法

```cpp
shuffle(RandomIt first,RandomIt last,URBG&& g);
```

first / last：双向或随机访问迭代器，指定要打乱的区间 \[first, last)。

g：随机数引擎对象(如 std::default\_random\_engine)

## 完整源码

```cpp
/*
shuffle 是用于将指定范围内的元素随机打乱顺序(即洗牌)。
头文件<algorithm> 和 <random>
语法
shuffle(RandomIt first,RandomIt last,URBG&& g);
first / last：双向或随机访问迭代器，指定要打乱的区间 [first, last)。
g：随机数引擎对象(如 std::default_random_engine)
*/
#include <iostream>
#include <random>
#include <algorithm>
#include <vector>
using namespace std;
template <typename T>
void PrintVector(const vector<T>& vector){
    for_each(vector.begin(),vector.end(),[](T x) {
        cout<<x<<" ";
        });
    cout<<endl;
}
int main(){
    for (int i=0; i<5;i++){
        vector<int> vec={1,2,3,4,5,6,7,8,9,10};
        random_device rd;
        shuffle(vec.begin(),vec.end(),default_random_engine(rd()));
        PrintVector(vec);
    }
    return 0;
}
```
