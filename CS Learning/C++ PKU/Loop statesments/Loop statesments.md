---
title: Loop statesments — 循环与范围 for
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: 北大 C++
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/北大_Cpp
aliases:
  - Loop statesments
  - Loop statements
  - 范围 for
  - Range-based for
  - 循环与范围 for
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# Loop statesments — 循环与范围 for

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/function pointer/function pointer|function pointer — 函数指针与 qsort]] · 下一篇：[[CS Learning/C++ PKU/new IO functions/new IO functions|new IO functions — C++ 输入输出]]
> 源码：[[CS Learning/C++ PKU/Loop statesments/Loop statesments.cpp|查看源码]]

> [!abstract] 本节概览
> 本节对比传统计数 `for` 循环与 C++11 引入的**基于范围的 `for` 循环（Range-based `for`）**以及 **`auto` 类型自动推导**，重点说明冒号前后两部分的作用域与语义、引用绑定 `&` 实现原地修改的原理，以及范围 `for` 的适用边界。

---

## 1. 传统计数 `for` vs C++11 范围 `for`

### 传统计数 `for` 循环

```cpp
for (int a = 10; a < 20; a++) {
    cout << "a 的值：" << a << endl;
}
```

适合需要明确下标索引、自定义步长（如 `a += 2`）、倒序遍历或与相邻元素比较（如 `arr[i]` 与 `arr[i-1]`）的场景。

### C++11 范围 `for`（Range-based `for`）

```cpp
for (迭代变量声明 : 被迭代的范围) {
    // 循环体
}
```

- **冒号 `:` 左侧（第一部分）**：声明用于接收当前元素的迭代变量；与普通 `for` 循环初始化变量一致，==其作用域仅限于该循环内部==。
- **冒号 `:` 右侧（第二部分）**：表示将被遍历的序列范围（例如定长内置数组、STL 容器如 `vector` / `string` / `map`、花括号初始化列表等）。

---

## 2. `auto` 自动类型推导与引用修饰对比

C++11 同时引入了 `auto` 关键字，允许编译器在**编译期**根据初始化表达式自动推导变量类型，大幅简化冗长的容器元素或迭代器类型写法。

在范围 `for` 中，迭代变量的声明形式直接决定了**性能**与**能否修改原容器元素**：

| 写法 | 底层行为 | 能否修改原元素 | 典型适用场景 |
| --- | --- | :---: | --- |
| `for (auto x : arr)` | 每次迭代**值拷贝**一份元素副本 | 不能 | 仅读取小型内置类型（`int`、`char`、`double`） |
| `for (auto &x : arr)` | 绑定元素的**引用**，无拷贝 | **可以原地修改** | 需要原地更新元素值（如源码中的 `x *= 2`） |
| `for (const auto &x : arr)` | 绑定元素的**常引用**，零拷贝且防误改 | 不能（只读保护） | 只读遍历大对象（`string`、`vector`、结构体等）的首选 |

### 源码执行过程追踪

初始数组：`int my_array[5] = {1, 2, 3, 4, 5};`

1. 第一次范围循环 `for (int &x : my_array)`：借助引用 `int &x` 将每个元素原地乘以 `2`，数组变为 `{2, 4, 6, 8, 10}` 并逐行输出。
2. 第二次范围循环 `for (auto &x : my_array)`：`auto` 自动推导出 `int`，结合 `&` 再次原地乘以 `2`，数组变为 `{4, 8, 12, 16, 20}` 并逐行输出。

---

## 3. 常见易错点

> [!warning] 范围 `for` 的两大注意事项
> 1. **不能用于退化为指针的数组形参**：当数组作为函数参数传递（如 `void func(int a[])`）时，它已退化为 `int*` 指针并丢失长度信息，因此在函数内部**无法**对 `a` 使用 `for (auto x : a)`；若要支持范围遍历，可改用 `std::array`、`std::vector` 或 C++20 `std::span`。
> 2. **遍历期间避免破坏容器结构**：在范围 `for` 遍历 `vector` 等动态容器时，执行 `push_back` 或 `erase` 可能引发扩容或迭代器失效，导致未定义行为。

---

## 完整源码

```cpp
#include <iostream>
using namespace std;
int main (){
   // for 循环执行
   for(int a=10;a<20;a++){
       cout<<"a 的值："<<a<<endl;
   }
   //以下是数组循环新表达方式示例
   int my_array[5]={1,2,3,4,5};
    // 每个数组元素乘于 2
    for (int &x:my_array){
        x*=2;
        cout<<x<<endl;
    }
    // auto 类型也是 C++11 新标准中的，用来自动获取变量的类型
    for (auto &x:my_array){
        x*=2;
        cout<<x<<endl;
    }
   return 0;
   //上面for述句的第一部分定义被用来做范围迭代的变量，就像被声明在一般for循环的变量一样，其作用域仅只于循环的范围。
   //而在":"之后的第二区块，代表将被迭代的范围。
}
```
