---
title: pointer — void 指针与内存操作
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
  - pointer
  - void 指针
  - void*
  - memset 与 memcpy
  - void 指针与内存操作
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# pointer — void 指针与内存操作

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/new IO functions/new IO functions|new IO functions — C++ 输入输出]] · 下一篇：[[CS Learning/C++ PKU/scanf & cin special usage/scanf & cin special usage|scanf & cin special usage — 读入状态与循环输入]]
> 源码：[[CS Learning/C++ PKU/pointer/pointer.cpp|查看源码]]

> [!abstract] 本节概览
> 本节梳理 C++ 中通用指针类型 **`void*`** 的语义规则与操作限制，并通过 `<cstring>` 中的底层按字节内存操作函数 **`memset`** 和 **`memcpy`** 说明 `void*` 如何支持与具体类型无关的内存初始化与块拷贝，同时剖析源码中关于 `memset` 字符 `'0'` 与整型数组打印的典型易错点。

---

## 1. `void*` 通用指针的规则与限制

`void*`（无类型指针）可以指向**任意对象类型的内存地址**，因此广泛用于与数据类型无关的底层库函数接口（例如 `memset`、`memcpy`、以及 [[CS Learning/C++ PKU/function pointer/function pointer|qsort]]）。

但由于编译器不知道 `void*` 所指对象的具体类型与字节宽度，标准 C++ 对 `void* p` 施加了严格限制：

| 操作 | 标准 C++ 是否允许 | 原因说明 |
| --- | :---: | --- |
| `void* p = &x;`（其他对象指针转 `void*`） | 允许（隐式转换） | 任意非 `const` 对象指针都可隐式转为 `void*` |
| `int* q = p;`（`void*` 转具体指针） | **禁止隐式转换** | 与 C 语言不同，C++ 必须显式转换：`static_cast<int*>(p)` 或 `(int*)p` |
| `sizeof(void)` | **无定义（编译错误）** | `void` 是不完整类型，没有确定字节大小 |
| `*p`（解引用） | **无定义（编译错误）** | 不知道读取多少字节、按什么类型解释 |
| `++p`、`p += n`、`p + n`（指针算术） | **无定义（编译错误）** | 无法计算步长 `n * sizeof(void)` |

---

## 2. 按字节内存操作函数：`memset` 与 `memcpy`

两者均声明于 `<cstring>`（C 语言为 `<string.h>`），以**字节（byte）**为基本单位直接操作连续内存：

| 函数原型 | 核心语义 | 返回值 |
| --- | --- | --- |
| `void* memset(void* dest, int ch, size_t n);` | 将从 `dest` 开始的连续 `n` 个**字节**全部设为 `(unsigned char)ch`（仅 `ch` 最低 1 字节起作用） | `dest` |
| `void* memcpy(void* dest, const void* src, size_t n);` | 从 `src` 开始拷贝连续 `n` 个**字节**到 `dest` | `dest` |

### 源码示例解析

1. **初始化字符数组**：
   ```cpp
   char szName[200] = "";
   memset(szName, 'a', 10);
   cout << szName << endl; // 输出 10 个 'a'（aaaaaaaaaa）
   ```
   因为 `szName` 初始化为 `""` 时剩余位置全为 `'\0'`，把前 10 个字节改成 `'a'` 后，下标 `10` 处仍是 `'\0'`，因此按 C 字符串打印恰好输出 `10` 个 `'a'`。
2. **拷贝整型数组**：
   ```cpp
   int a1[10], a2[10];
   memcpy(a2, a1, 10 * sizeof(int)); // 按总字节数 10 * sizeof(int) 完整拷贝
   ```

---

## 3. 源码注释核对与常见内存操作陷阱

> [!warning] 源码中 `memset(a, '0', sizeof(a)); cout << a;` 背后的三个经典坑
> 原源码记录了以下学习代码：
> ```cpp
> int a[20];
> memset(a, '0', sizeof(a));
> cout << a << endl; // 源码中记录为：“输出20个0”
> return 0;
> ```
> 在回顾这段代码时，务必注意实际运行中的三个关键差异：
> 1. **`'0'`（ASCII `48` / `0x30`）不是数字 `0`**：`memset` 是**逐字节**填充的！`memset(a, '0', sizeof(a))` 会把每个 4 字节 `int` 填成 `0x30303030`（十进制 `808464432`），而不是 `0`。将整型数组清零应写 `memset(a, 0, sizeof(a))`（对于 `int` 数组，`memset` 仅适合整体置 `0`、`-1`，或竞赛中用 `0x3f` 构造近似无穷大 `0x3f3f3f3f`）。
> 2. **`cout << a` 输出的是首地址而非数组内容**：`a` 是 `int[20]`，传给 `cout <<` 时会退化为 `int*` 指针，实际打印的是十六进制内存地址（只有 `char*` 会被 `cout` 特殊重载为按字符串打印）。打印整型数组必须借助循环遍历。
> 3. **提前 `return 0;`**：原源码在第 62 行提前返回，因此其后的 `memcpy` 片段在直接编译运行时不会被执行，仅作语法演示。

> [!important] `memcpy` 的两条安全红线
> 1. **内存重叠禁止用 `memcpy`**：若 `src` 与 `dest` 指向的区间有重叠，调用 `memcpy` 属于未定义行为，应改用支持重叠区间的 **`memmove`**。
> 2. **仅限平凡可复制类型（Trivially Copyable）**：`memset` 和 `memcpy` 直接覆写底层字节，绝不能用于包含 `std::string`、`std::vector` 或虚函数的 C++ 复杂对象（会破坏内部指针与资源管理，导致内存泄漏或崩溃）。

---

## 完整源码

```cpp
/*
与C语言不同,在C++中,对于Void* 指针类型的指针p
sizeof(void)没有定义,*p、++p、p+=n、p+n等均无定义
*/
#include <iostream>
#include <cstring>
using namespace std;
int main(){
    char szName[200]="";
    int a[20];
    memset(szName,'a',10);//void*的用途之一,memset(void* dest,int ch,int n)即把从dest开始的n个字节都设置成ch,返回dest,ch只有第一个字节起作用
    cout<<szName<<endl;//输出了10个a，memset可用于初始化字符串数组
    memset(a,'0',sizeof(a));
    cout<<a<<endl;//输出20个0,体现出void* 可以用于memset函数中让第一个参数可以是任何类型的指针
    return 0;
    int a1[10],a2[10];
    memcpy(a2,a1,10*sizeof(int));//memcpy(void* dest,void* src,int n)把地址scr开始的n个字节拷贝到地址dest,返回dest
}
```
