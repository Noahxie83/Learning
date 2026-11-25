---
title: find() — 查找元素
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
aliases:
  - find
  - find()
  - find_if
  - 查找元素
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `find()` — 查找元素

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/fill() fill_n()/fill() fill_n()|fill() fill_n() — 序列填充]] · 下一篇：[[CS Learning/C++ STL/Algorithms/lower_bound() upper_nound()/lower_bound() upper_nound()|lower_bound() upper_nound() — 上下界查找]]
> 相关：[[CS Learning/C++ STL/Algorithms/count()/count()|count() — 元素计数]]
> 源码：[[CS Learning/C++ STL/Algorithms/find()/find().cpp|查看源码]]

> [!abstract] 本节概览
> `std::find()` 定义在头文件 `#include <algorithm>` 中，是在未排序区间 `[first, last)` 内进行**线性查找**的基础算法。它从前往后逐个用 `==` 运算符比对元素，返回指向==第一个匹配元素==的迭代器；若未找到，则返回尾后迭代器 `last`，时间复杂度为 $O(n)$。

## 核心语法与返回值约定

```cpp
#include <algorithm>

InputIterator find(InputIterator first, InputIterator last, const T& val);
```

| 组成部分 | 说明 |
| :--- | :--- |
| `[first, last)` | 输入迭代器指定的左闭右开查找区间，既可用于 STL 序列容器，也可用于普通数组 |
| `val` | 要查找的目标值；区间内元素必须支持 `==` 运算符 |
| **查找成功** | 返回指向区间内**第一个**等于 `val` 的元素的迭代器（对普通数组则为指向该元素的指针） |
| **查找失败** | 返回与 `last` 相同的迭代器，**严禁直接解引用** |

## 典型用法与示例解析

### 1. 作用于普通数组（含 C 风格字符串）

在文末源码中，对 `char stl[] = "hello c++";` 调用 `find(stl, stl + strlen(stl), 'c')`：
- 返回的 `char* p` 指向字符 `'c'` 的位置；
- 校验 `p != stl + strlen(stl)` 后执行 `cout << p`，会输出从 `'c'` 开始直至 `\0` 的子串 `c++`。

### 2. 作用于 `vector` 等容器并获取下标

```cpp
std::vector<int> v = {10, 20, 30, 40, 50};
auto it = std::find(v.begin(), v.end(), 30);
if (it != v.end()) {
    std::cout << "找到元素：" << *it << "，下标：" << (it - v.begin()) << '\n';
}
```

### 3. 按条件查找：`std::find_if()`

若需查找第一个满足某种谓词条件的元素（例如第一个大于 `25` 的数），可使用 `std::find_if()`：

```cpp
auto it = std::find_if(v.begin(), v.end(), [](int x) { return x > 25; });
```

## 常见易错点与注意事项

> [!warning] 解引用前必须判断 `it != last`
> 当查找失败时，`find()` 返回的 `last` 指向尾后哨兵位置（不对应有效元素）。如果不加判断直接写 `*find(...)`，会触发**未定义行为（越界读取/崩溃）**。

> [!tip] 不同容器与场景的查找方式选择
> - **自定义结构体**：使用 `std::find()` 前需为结构体实现 `operator==`，否则改用 `std::find_if()`。
> - **有序序列**：优先用 [[CS Learning/C++ STL/Algorithms/binary_search()/binary_search()|binary_search()]] 或 [[CS Learning/C++ STL/Algorithms/lower_bound() upper_nound()/lower_bound() upper_nound()|lower_bound() / upper_bound()]]（$O(\log n)$）。
> - **`set` / `map` / `unordered_map` / `string`**：优先调用容器自带的成员函数 `.find()`，效率远高于全局线性扫描 `std::find()`。

## 完整源码

```cpp
/*
find 是标准模板库（STL）中一个基础且常用的查找算法,定义在头文件 <algorithm> 中

语法：
InputIterator find (InputIterator first,InputIterator last,const T& val);
    其中,first 和 last 为输入迭代器,[first,last)用于指定该函数的查找范围；val 为要查找的目标元素。
    该函数会返回一个输入迭代器,当 find()函数查找成功时,其指向的是在[first,last)区域内查找到的第一个目标元素；
    如果查找失败,则该迭代器的指向和 last 相同。
注意:
find()函数的底层实现,其实就是用"=="运算符将 val 和[first,last)区域内的元素逐个进行比对。这也就意味着,[first,last)区域内的元素必须支持"=="运算符。
find()函数除了可以作用于序列式容器，还可以作用于普通数组。
*/
#include <iostream>
#include <algorithm>
#include <cstring>
#include <vector>
using namespace std;
int main(){
    //find() 函数作用于普通数组
    char stl[] ="hello c++";
    //调用 find() 查找第一个字符 'c'
    char *p=find(stl,stl+strlen(stl),'c');
    //判断是否查找成功
    if (p!=stl+strlen(stl)){
        cout<<p<<endl;
    }
    //find() 函数作用于容器
    vector<int> myvector{10,20,30,40,50};
    vector<int>::iterator it;
    it=find(myvector.begin(),myvector.end(),30);
    if (it!=myvector.end())
        cout<<"查找成功："<<*it;
    else
        cout<<"查找失败";
    return 0;
}
```
