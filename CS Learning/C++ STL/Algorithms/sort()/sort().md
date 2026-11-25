---
title: sort() — 排序
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
  - sort
  - sort()
  - stable_sort
  - 排序
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `sort()` — 排序

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/shuffle()/shuffle()|shuffle() — 随机打乱]] · 下一篇：[[CS Learning/C++ STL/Algorithms/swap()/swap()|swap() — 交换]]
> 相关：[[CS Learning/C++ STL/Algorithms/binary_search()/binary_search()|binary_search() — 二分查找]]
> 源码：[[CS Learning/C++ STL/Algorithms/sort()/sort().cpp|查看源码]]

> [!abstract] 本节概览
> `std::sort()` 定义在头文件 `#include <algorithm>` 中，用于对左闭右开区间 `[first, last)` 进行原地排序。C++11 标准保证其平均与最坏时间复杂度均为 $O(n \log n)$（主流标准库采用**内省排序 Introsort** = 快速排序 + 堆排序兜底 + 小区间插入排序），要求容器支持**随机访问迭代器**，且为**不稳定排序**。

## 核心用法与三种排序方式

| 排序方式 | 数组写法（范围 `[n1, n2)`） | 容器写法 | 说明 |
| :--- | :--- | :--- | :--- |
| **1. 默认升序** | `sort(a + n1, a + n2);` | `sort(v.begin(), v.end());` | 要求元素类型支持 `<` 运算符 |
| **2. 标准降序** | `sort(a + n1, a + n2, greater<T>());` | `sort(v.begin(), v.end(), greater<T>());` | `greater<T>()` 来自 `<functional>` |
| **3. 自定义规则** | `sort(a + n1, a + n2, Rule());` | `sort(v.begin(), v.end(), cmp);` | 支持仿函数对象、普通函数指针或 Lambda |

### 自定义比较器的三种写法

比较函数表达的语义统一为：**若 `a1` 应当排在 `a2` 前面，返回 `true`；否则返回 `false`**。

```cpp
#include <algorithm>
#include <functional>

// 方式 A：仿函数结构体（源码中的写法，调用时需加括号构造临时对象 Rule2()）
struct Rule2 {
    bool operator()(const int& a1, const int& a2) const {
        return a1 % 10 < a2 % 10;  // 按个位数从小到大
    }
};
std::sort(a, a + n, Rule2());

// 方式 B：Lambda 表达式（C++11 起最简洁）
std::sort(a, a + n, [](int a1, int a2) {
    return a1 % 10 < a2 % 10;
});

// 方式 C：普通比较函数
bool cmp(int a1, int a2) { return a1 > a2; }
std::sort(a, a + n, cmp);
```

### 源码示例运行结果

原数组 `a[] = {12, 45, 3, 98, 21, 7}`（长度 `6`）：
1. 按 `Rule1`（降序）排序输出：`98,45,21,12,7,3,`
2. 按 `Rule2`（个位数升序）排序输出：`21,12,3,45,7,98,`

## 常见易错点与注意事项

> [!warning] 比较器必须满足严格弱序（严禁使用 `<=` 或 `>=`）
> 自定义比较器在两元素等价时**必须返回 `false`**（即 `comp(x, x) == false`）。如果误写成 `return a1 <= a2` 或 `return a1 >= a2`，破坏了严格弱序，在 `libstdc++` 的 Introsort 分区循环中会导致**迭代器越界并直接崩溃（段错误）**！

> [!warning] 其他高频易错点
> - **仿函数传对象而非类型名**：原注释中 `sort(a+n1, a+n2, 排序规则结构名)` 容易漏掉括号，正确写法必须带括号实例化临时对象：`Rule1()`。
> - **注意区间右边界不要越界**：`sort(a, a + n)` 排序的是 `[0, n)` 共 `n` 个元素；原源码注释行 `//sort(a,a+7,greater<int>());` 若取消注释会越界（数组 `a` 仅有 6 个元素），应当使用 `a + sizeof(a) / sizeof(int)` 或 `std::end(a)`。
> - **`std::list` 不能用 `std::sort()`**：链表仅支持双向迭代器，需调用成员函数 `lst.sort()`。

> [!tip] 需要保持相等元素相对顺序时改用 `std::stable_sort()`
> `std::sort()` 不保证相等元素的原有相对顺序（例如按个位数排 `15` 和 `25` 顺序可能互换）。若需要**稳定排序**，可直接使用 `std::stable_sort(first, last, comp)`（底层多为归并排序，时间复杂度通常为 $O(n \log n)$）。

## 完整源码

```cpp
/*
sort()即排序算法,时间复杂度nlogn
(一)对基本类型的数组从小到大:
    sort(数组名+n1,数组名+n2)
    sort(arr.begin(),arr.end());
    n1、n2为int类型,可以包含变量
    排序范围是[n1,n2)
(二)对类型为T的基本类型数组从大到小:
    sort(数组名+n1,数组名+n2,greater<T>());
    sort(arr.begin(),arr.end(),greater<T>());
(三)用自定义的排序规则,对任何类型T的数组排序
    sort(数组名+n1,数组名+n2,排序规则结构名);
    sort(arr.begin(),arr.end(),排序规则结构名<T>());
    排序规则结构定义方式:
    struct 结构名{
    bool operator()(const T &a1,const T &a2)const{
        //若a1应该在a2前面,返回true
        //否则返回false
        }
    }
*/
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;
struct Rule1{//从大到小
    bool operator()(const int &a1,const int &a2)const{
        return a1>a2;
        }
    };
struct Rule2{//按个位数从小到大
    bool operator()(const int &a1,const int &a2)const{
        return a1%10<a2%10;
        }
    };
void Print(int a[],int size){
    for (int i=0;i<size;++i){
        cout<<a[i]<<",";
    }
    cout<<endl;
}
int main(){
    int a[]={12,45,3,98,21,7};
    //sort(a+2,a+6);
    //sort(a,a+7,greater<int>());
    sort(a,a+sizeof(a)/sizeof(int),Rule1());
    Print(a,sizeof(a)/sizeof(int));
    sort(a,a+sizeof(a)/sizeof(int),Rule2());
    Print(a,sizeof(a)/sizeof(int));
}
```
