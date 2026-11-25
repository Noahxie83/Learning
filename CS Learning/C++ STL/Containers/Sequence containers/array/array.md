---
title: "array — 定长数组容器"
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
aliases:
  - std::array
  - array
  - 定长数组容器
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# array — 定长数组容器

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Associative containers/set/set|set — 有序集合]] · 下一篇：[[CS Learning/C++ STL/Containers/Sequence containers/deque/deque|deque — 双端队列容器]]
> 源码：[[CS Learning/C++ STL/Containers/Sequence containers/array/array.cpp|查看源码]]

> [!abstract] 本节概览
> `std::array`（C++11 引入）定义于头文件 `<array>`，是对 C 风格定长数组的**零开销（zero-overhead）容器封装**。其底层为==编译期确定大小的连续内存数组==（局部变量分配在栈上，无需堆分配），同时兼容 STL 迭代器与标准算法接口。随机访问复杂度为 $O(1)$，不支持动态扩容或增删元素，因此迭代器在对象生命周期内几乎不会失效（但注意 `swap` 为 $O(N)$ 逐元素交换）。

## 核心概念、底层结构与声明

### 1. 声明与初始化

```cpp
#include <array>

array<int, 5> arr1;                     // 默认初始化：局部变量元素值未定义（垃圾值）
array<int, 5> arr2{};                   // 值初始化：全部元素初始化为 0
array<int, 5> arr3 = {10, 20, 30, 40, 50}; // 聚合初始化
array<int, 5> arr4 = {1, 2};            // 前两项为 1, 2，其余自动补 0
```

其中模板参数 `T` 为元素类型，`N` 必须为**编译期非负整型常量表达式（`constexpr size_t`）**，运行期无法改变。

### 2. 相比 C 风格数组 `T[N]` 的优势

| 对比维度 | C 风格数组 `int a[5]` | `std::array<int, 5>` |
| --- | --- | --- |
| 传参退化 | 传给函数时自动退化为指针 `int*`，丢失长度 | ==不退化==，完整保留类型与长度信息 |
| 获取长度 | 需借助 `sizeof(a) / sizeof(a[0])` | 直接调用 `arr.size()` |
| 整体赋值与比较 | 不支持 `a = b`、`a == b` | 原生支持 `=`、`==`、`<` 等字典序比较 |
| 边界检查 | 仅支持 `[]`（越界未定义行为） | 额外提供带异常检查的 `.at(pos)` |
| 性能与内存开销 | 栈上连续存储，零额外开销 | **与原生数组完全等价**，`sizeof(array<T, N>) == sizeof(T) * N` |

## 常用接口与时间复杂度速查

| 成员函数 / 操作 | 说明 | 时间复杂度 |
| --- | --- | --- |
| `arr[pos]` | 访问下标 `pos` 处元素，不做边界检查 | $O(1)$ |
| `arr.at(pos)` | 访问下标 `pos` 处元素，越界抛出 `std::out_of_range` | $O(1)$ |
| `arr.front()` / `arr.back()` | 返回首个 / 最后一个元素的引用 | $O(1)$ |
| `arr.data()` | 返回指向底层连续数组首元素的原生指针 `T*`（兼容 C API） | $O(1)$ |
| `arr.size()` / `arr.max_size()` | 返回固定长度 $N$（`constexpr`） | $O(1)$ |
| `arr.empty()` | 判断 $N == 0$ 是否成立 | $O(1)$ |
| `arr.fill(val)` | 将数组中所有元素统一赋值为 `val` | $O(N)$ |
| `arr.swap(other)` | 与同类型、同长度的另一 `array` 逐元素交换内容 | ==$O(N)$== |
| `arr.begin()` / `arr.end()` | 返回随机访问起始 / 尾后迭代器（亦支持 `rbegin()`/`rend()`） | $O(1)$ |

## 典型用法与现代特性

源码展示了 `array` 的初始化、下标与范围 `for` 遍历、`front()`/`back()` 访问、`fill(100)` 批量填充以及 `swap()` 交换两个同尺寸数组：

```cpp
array<int, 5> arr = {10, 20, 30, 40, 50};
arr.fill(100); // 所有元素变为 100

array<int, 3> arr1 = {1, 2, 3};
array<int, 3> arr2 = {4, 5, 6};
arr1.swap(arr2); // arr1 -> {4, 5, 6}, arr2 -> {1, 2, 3}

// C++17 结构化绑定解包
auto [x, y, z] = arr1;
```

## 常见易错点与迭代器稳定性

> [!warning] 容易忽略的 3 个坑
> 1. **`array::swap` 是 $O(N)$ 而非 $O(1)$**：`vector` 只需交换内部指针，而 `array` 的元素直接内嵌在对象栈空间中，交换必须逐个搬移元素；且**只有类型和长度 `N` 完全相同的 `array` 才能互相 `swap` 或赋值**。
> 2. **局部 `array<int, N> a;` 不会自动清零**：对内置类型而言，不带 `{}` 的局部声明会保留栈上随机内存值，养成写 `array<int, N> a{};` 的习惯。
> 3. **栈溢出风险**：局部 `array` 分配在栈上，若 `N` 极大（如 `1e7`）会导致栈溢出（Stack Overflow），大数组应改为 `std::vector` 或静态/全局存储。

> [!tip] 迭代器失效规则
> 由于 `std::array` 永远不会扩容或重新分配内存，除对象销毁外，**普通读写与 `fill` 均不会导致迭代器或引用失效**；`swap` 后原迭代器仍指向原 `array` 对象对应下标位置，但位置上的元素值已被交换。

## 完整源码

```cpp
/*
<array> 头文件，提供了一种固定大小的数组容器，与C语言中的数组相比，具有更好的类型安全和内存管理特性。
array是C++标准库中的一个模板类，它定义在 <array> 头文件中。
array模板类提供了一个固定大小的数组，其大小在编译时确定，并且不允许动态改变。
基本用法:T为元素类型，N为数组大小(必须为非负整数)
#include <array>
array<T,N> array_name;
<array> 需要在编译时确定大小，不能动态改变。

特点:
 类型安全：array 强制类型检查，避免了 C 语言数组的类型不安全问题。
 固定大小：数组的大小在编译时确定，不能在运行时改变。
 内存连续：array 的元素在内存中是连续存储的，这使得它可以高效地访问元素。
 标准容器：array 提供了与 vector 类似的接口，如 size(),at(),front(),back() 等。
以下是常用成员函数
at(size_t pos)	        返回指定位置的元素，带边界检查
operator[]	            返回指定位置的元素，不带边界检查
front()	                返回数组的第一个元素
back()	                返回数组的最后一个元素
data()	                返回指向数组数据的指针
size()	                返回数组大小（固定不变）
fill(const T& value)	将数组所有元素设置为指定值
swap(array& other)	    交换两个数组的内容
begin() / end()	        返回数组的起始/结束迭代器
*/
#include <iostream>
#include <array>
using namespace std;
int main(){
    array<int,5> arr={10,20,30,40,50};
    cout<<"Array elements: ";
    for (int i=0;i<arr.size();i++) {
        cout<<arr[i]<<" ";
    }
    cout<<endl;
    cout<<"First element:"<<arr.front()<<endl;
    cout<<"Last element:"<<arr.back()<<endl;
    arr.fill(100);  // 将所有元素设置为100
    cout << "Filled array: ";
    for (const auto& elem:arr){
        cout<<elem<<" ";
    }
    cout<<endl;
    array<int,3> arr1={1,2,3};
    array<int,3> arr2={4,5,6};
    arr1.swap(arr2);
    cout<<"Array 1: ";
    for (const auto& elem:arr1) {
        cout<<elem<<" ";
    }
    cout<<endl;
    cout<<"Array 2: ";
    for (const auto& elem:arr2) {
        cout<<elem<<" ";
    }
    cout<<endl;
    return 0;
}
```
