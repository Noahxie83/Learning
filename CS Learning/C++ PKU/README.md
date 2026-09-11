# C++ PKU

C++ 与程序设计基础课程的代码练习。

课程入口：[PKU 程序设计与算法课程](https://www.icourse163.org/learn/PKU-1001553023?tid=1474162490#/learn/announce)。保留所选课程的学期链接，学习页可能需要登录。

## Markdown 笔记目录

本目录的 9 个 C++ 源文件已整理为同名主题目录：每个目录内包含原源码和一篇 Markdown 笔记，原文件名保留。

Markdown 将原注释整理为正文、用法表格、输入输出样例及带行号的注释索引，文末附完整源码。源码只移动位置，内容、编码和换行保持原样；笔记保留当时的记录，未进行逐项知识校订。

例如 ` string.cpp ` 现整理为：

```text
string/
├── string.cpp
└── string.md
```

下面的链接可直接打开对应笔记。

### 主题

| 原文件名 | 内容 | Markdown | 源码 |
| --- | --- | --- | --- |
| Classes and Objects.cpp | 类与对象 | [阅读笔记](Classes%20and%20Objects/Classes%20and%20Objects.md) | [查看源码](Classes%20and%20Objects/Classes%20and%20Objects.cpp) |
| cstring.cpp | C 风格字符串函数 | [阅读笔记](cstring/cstring.md) | [查看源码](cstring/cstring.cpp) |
| freopen.cpp | 输入输出重定向 | [阅读笔记](freopen/freopen.md) | [查看源码](freopen/freopen.cpp) |
| function pointer.cpp | 函数指针与 qsort | [阅读笔记](function%20pointer/function%20pointer.md) | [查看源码](function%20pointer/function%20pointer.cpp) |
| Loop statesments.cpp | 循环与范围 for | [阅读笔记](Loop%20statesments/Loop%20statesments.md) | [查看源码](Loop%20statesments/Loop%20statesments.cpp) |
| new IO functions.cpp | C++ 输入输出 | [阅读笔记](new%20IO%20functions/new%20IO%20functions.md) | [查看源码](new%20IO%20functions/new%20IO%20functions.cpp) |
| pointer.cpp | void 指针与内存操作 | [阅读笔记](pointer/pointer.md) | [查看源码](pointer/pointer.cpp) |
| scanf &amp; cin special usage.cpp | 读入状态与循环输入 | [阅读笔记](scanf%20%26%20cin%20special%20usage/scanf%20%26%20cin%20special%20usage.md) | [查看源码](scanf%20%26%20cin%20special%20usage/scanf%20%26%20cin%20special%20usage.cpp) |
| string.cpp | 字符串与整行输入 | [阅读笔记](string/string.md) | [查看源码](string/string.cpp) |

### 后续维护

Markdown 是本次整理后的笔记快照。以后若修改源码中的注释或示例，也请更新同目录中的 Markdown；两者不会自动互相修改。

## 内容范围

本目录主要整理 C 语言向 C++ 过渡阶段的学习内容，包含：

- 字符串和 C 风格字符串处理。
- 指针、函数指针和函数调用。
- 循环、流程控制和常用输入输出。
- `scanf`、`cin` 及其他输入输出方式。
- `freopen` 和文件输入输出。
- 类与对象基础。
- C++ 常用头文件和基础库函数。

## 使用建议

阅读代码时可以重点比较 C 与 C++ 在以下方面的差异：

- 输入输出方式。
- 字符串处理方式。
- 内存和指针使用方式。
- 类、对象与封装思想。
- 函数和类型系统的表达方式。

根模块入口：[CS Learning/README.md](../README.md)。
