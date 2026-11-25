---
title: "scanf & cin special usage — 读入状态与循环输入"
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
  - scanf & cin special usage
  - 读入状态与循环输入
  - while cin
  - EOF 循环输入
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# scanf & cin special usage — 读入状态与循环输入

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/pointer/pointer|pointer — void 指针与内存操作]] · 下一篇：[[CS Learning/C++ PKU/string/string|string — 字符串与整行输入]]
> 源码：[[CS Learning/C++ PKU/scanf & cin special usage/scanf & cin special usage.cpp|查看源码]]

> [!abstract] 本节概览
> 在算法竞赛和文件批处理场景中，经常遇到**事先不给出数据组数、也没有特殊结束哨兵**的多组测试输入。本节对比 `scanf` 返回值与 `cin` 流状态两种判定机制，掌握读取至输入结束（`EOF`）的标准循环写法。

---

## 1. 无结束标记的多组数据循环写法

面对“持续读入多组 `(n, m)` 并输出 `n + m`，直到输入流结束”的经典题型，C 与 C++ 分别有各自最常用的惯用法：

### 写法一：C 风格 `scanf` 判定 `!= EOF`

```cpp
int n, m;
while (scanf("%d%d", &n, &m) != EOF) {
    printf("%d\n", n + m);
}
```

- `scanf` 的返回类型为 **`int`**：
  - 正常读取时，返回**成功匹配并赋值的变量个数**（例如读入两个 `%d` 成功时返回 `2`）；
  - 当遇到输入流末尾（文件结束）或发生读取错误时，返回宏常量 **`EOF`**（通常定义为 `-1`）。
- **更严谨的变体**：写 `while (scanf("%d%d", &n, &m) == 2)` 不仅能响应 `EOF`，还能在遇到非数字脏字符（此时 `scanf` 返回 `0`）时安全退出，避免死循环。

### 写法二：C++ 风格 `while (cin >> n >> m)`

```cpp
int n, m;
while (cin >> n >> m) {
    printf("%d\n", n + m);
}
```

- 链式提取表达式 `cin >> n >> m` 返回的是输入流对象 `cin` 自身的引用；
- 当它置于 `while (...)` 条件判断中时，会触发流对象的布尔状态转换（C++11 起为 `explicit operator bool()`）：
  - ==所有变量都成功读入且流状态正常时求值为 `true`==；
  - 遇到 `EOF` 或类型不匹配导致读入失败时求值为 `false`，循环自动终止。

---

## 2. `scanf` vs `cin` 循环读入对比

| 对比项 | `while (scanf("%d%d", &n, &m) != EOF)` | `while (cin >> n >> m)` |
| --- | --- | --- |
| **判断依据** | `int` 返回值是否不等于 `EOF`（`-1`） | `cin` 流对象的状态标志（`!fail()`） |
| **遇到非法输入字符** | 返回 `0`（不等于 `EOF`），容易引发**死循环**（改写 `== 2` 可避免） | 自动置 `failbit`，条件变为 `false` 并立即退出循环 |
| **所需头文件** | `<cstdio>` | `<iostream>` |
| **适用场景** | 数据量大、追求高 I/O 吞吐时 | 代码简洁、类型安全，搭配关闭同步后速度同样很快 |

---

## 3. 本地测试手动触发 `EOF` 技巧

> [!tip] 在控制台测试 `while (cin >> ...)` 时如何结束输入？
> 如果直接从键盘输入而非通过文件重定向，需要手动向终端发送 `EOF` 信号才能让循环退出：
> - **Windows 控制台（CMD / PowerShell）**：新起一行按 **`Ctrl + Z`**，再按 **`Enter`**；
> - **Linux / macOS 终端**：新起一行按 **`Ctrl + D`**。
>
> 若测试数据较多，建议搭配 [[CS Learning/C++ PKU/freopen/freopen|freopen — 输入输出重定向]] 直接从文件读入；更多流特性与提速技巧见 [[CS Learning/C++ PKU/new IO functions/new IO functions|new IO functions — C++ 输入输出]]。

---

## 完整源码

```cpp
#include <iostream>
using namespace std;
int main(){
    //注意scanf的返回值为int类型,故当值为EOF时输入结束
    //而cin表达式的值在成功读入所有变量时为true,否则为flase
    int n,m;
    /*while ((scanf("%d%d",&n,&m))!=EOF){
        printf("%d\n",n+m);
    }*/
    while (cin>>n>>m){
        printf("%d\n",n+m);
    }
    //以上两种都可用于无结束标记的数据输入情况
    return 0;
}
```
