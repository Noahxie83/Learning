---
title: binary_search() — 二分查找
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
  - binary_search
  - binary_search()
  - 二分查找
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `binary_search()` — 二分查找

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/Algorithms/Algorithms|Algorithms — 标准算法概览]] · 下一篇：[[CS Learning/C++ STL/Algorithms/Cmath/Cmath|Cmath — 数学函数]]
> 相关：[[CS Learning/C++ STL/Algorithms/sort()/sort()|sort() — 排序]]
> 源码：[[CS Learning/C++ STL/Algorithms/binary_search()/binary_search().cpp|查看源码]]

> [!abstract] 本节概览
> `std::binary_search()` 定义在头文件 `#include <algorithm>` 中，用于在**已排序**的左闭右开区间 `[first, last)` 内快速判断目标值是否存在。对于随机访问迭代器（如 `vector`、普通数组），其时间复杂度为 $O(\log n)$；函数返回 `bool` 值（存在返回 `true`，否则返回 `false`）。

## 核心语法与两种重载形式

| 用法 | 函数原型 | 适用前提 | 返回值 | 时间复杂度 |
| :--- | :--- | :--- | :--- | :---: |
| **默认升序版** | `binary_search(first, last, val)` | 区间 `[first, last)` 已按 `<` 升序排列 | `bool` | $O(\log n)$ |
| **自定义规则版** | `binary_search(first, last, val, comp)` | 区间已按同一比较器 `comp` 排好序 | `bool` | $O(\log n)$ |

常见调用方式（同时支持普通数组与 STL 容器）：

```cpp
#include <algorithm>

// 1. 默认升序：在 [n1, n2) 范围内查找 val
bool ok1 = std::binary_search(a + n1, a + n2, val);
bool ok2 = std::binary_search(vec.begin(), vec.end(), val);

// 2. 自定义排序规则：comp 必须与 sort() 时使用的规则完全一致
bool ok3 = std::binary_search(a, a + n, val, Rule());
bool ok4 = std::binary_search(vec.begin(), vec.end(), val, Rule());
```

## 关键机制：“等价”而非 `==`

`std::binary_search()` 在判断区间中是否存在“等于” `val` 的元素时，==并不是直接调用 `==` 运算符==，而是基于严格弱序比较器来定义**等价（Equivalence）**：

- **默认版本**：$a$ 与 $b$ 等价 $\iff \neg(a < b) \land \neg(b < a)$。
- **自定义规则版本**：$a$ 与 $b$ 等价 $\iff \neg\text{comp}(a, b) \land \neg\text{comp}(b, a)$，即“既不满足 $a$ 必须排在 $b$ 前面，也不满足 $b$ 必须排在 $a$ 前面”。

### 源码示例运行追踪

文末源码中，数组 `a[] = {12, 45, 3, 98, 21, 7}` 先后进行了两次排序与查找：

1. **按默认 `<` 升序排序**后数组变为 `{3, 7, 12, 21, 45, 98}`：
   - `result1`：查找 `12` → `1`（`true`）
   - `result2`：查找 `77` → `0`（`false`）
2. **按自定义规则 `Rule`（按个位数 `a % 10` 升序）排序**后数组变为 `{21, 12, 3, 45, 7, 98}`：
   - `result3`：`binary_search(a, a + 6, 7)` 未传入 `Rule()`，数组未按 `<` 有序，**调用结果不可靠**（此处恰好输出 `0`）。
   - `result4`：`binary_search(a, a + 6, 8, Rule())` 输出 `1`（`true`）！尽管数组中没有 `8`，但 `98 % 10 == 8 % 10`，使得 `Rule()(98, 8)` 和 `Rule()(8, 98)` 均为 `false`，因此 `98` 与 `8` 在 `Rule` 规则下**等价**。

## 常见易错点与注意事项

> [!warning] 排序规则与查找规则必须严格一致
> 使用 `binary_search()` 前区间必须处于有序状态（至少针对目标值已划分），且**查找时传入的比较器必须与 `sort()` 时完全一致**。对未排序或排序规则不匹配的区间调用 `binary_search()` 会得到错误结果甚至触发未定义行为。

> [!tip] 需要知道元素位置时请改用 `lower_bound()` / `upper_bound()`
> `binary_search()` 仅返回“找没找到”（`bool`），无法得知元素下标或出现次数。如果需要定位元素的具体迭代器或统计出现次数，请使用 [[CS Learning/C++ STL/Algorithms/lower_bound() upper_nound()/lower_bound() upper_nound()|lower_bound() / upper_bound()]]。

## 完整源码

```cpp
/*
STL提供在【排好序】的数组上进行二分查找的算法
用binary_search进行二分查找(用法一)
    在从小到大排好序的基本类型数组上进行二分查找
    binary_search(数组名+n1,数组名+n2,值)
    binary_search(arr.begin(),arr.end(),值)
    n1、n2都是int,查找范围为[n1,n2),在该区间内查找"等于""值"的元素
    【等于】的含义:a等于b<=>a<b和a>b都不成立;【不是"=="】
    找到返回true,没找到返回false
用binary_search进行二分查找(用法二)
    在用自定义排序规则排好序的、元素为任意的T类型的数组中进行二分查找
    binary_search(数组名+n1,数组名+n2,值,排序规则结构名())
    binary_search(arr.begin(),arr.end(),值,排序规则结构名())
    【注意】查找时的排序规则,必须和排序时的规则一致！
    【等于】的含义:a等于b<=><a必须在b前面>和<b必须在a前面>都不成立;
*/
#include <iostream>
#include <cstring>
#include <algorithm>
#define NUM 7
using namespace std;
struct Rule{//按个位数从小到大排
    bool operator()(const int &a1, const int &a2) const{
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
    sort(a,a+6);
    Print(a,6);
    cout<<"result1:"<<binary_search(a,a+6,12)<<endl;
    cout<<"result2:"<<binary_search(a,a+6,77)<<endl;
    sort(a,a+6,Rule());
    Print(a,6);
    cout<<"result3:"<<binary_search(a,a+6,7)<<endl;//没有按从小到大排
    cout<<"result4:"<<binary_search(a,a+6,8,Rule())<<endl;
    //【等于】的含义:a等于b<=><a必须在b前面>和<b必须在a前面>都不成立;98与8刚好满足这里的"等于"的要求
}
```
