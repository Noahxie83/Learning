---
title: freopen — 输入输出重定向
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
  - freopen
  - 输入输出重定向
  - 文件重定向
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# freopen — 输入输出重定向

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/cstring/cstring|cstring — C 风格字符串函数]] · 下一篇：[[CS Learning/C++ PKU/function pointer/function pointer|function pointer — 函数指针与 qsort]]
> 源码：[[CS Learning/C++ PKU/freopen/freopen.cpp|查看源码]]

> [!abstract] 本节概览
> 调试算法程序时，每次运行都手动敲入大量测试数据既耗时又容易出错。本节整理 `<cstdio>` 中的 `freopen` 函数，可将标准输入流 `stdin` 与标准输出流 `stdout` 无缝重定向到磁盘文件，从而在不修改业务 I/O 代码（`scanf`/`printf`/`cin`/`cout`）的前提下完成批量文件测试。

---

## 1. 核心语法与常用示例

`freopen` 声明于 `<cstdio>`（C 语言为 `<stdio.h>`）：

```cpp
FILE* freopen(const char* filename, const char* mode, FILE* stream);
```

### 典型重定向写法

```cpp
#include <cstdio>

int main() {
    // 1. 将标准输入从键盘重定向到测试文件
    freopen("c:\\tmp\\test.txt", "r", stdin);
    // 2. 将标准输出从屏幕重定向到结果文件
    freopen("output.txt", "w", stdout);

    // 此后所有 scanf/cin 都会从 test.txt 读取，printf/cout 都会写入 output.txt
    return 0;
}
```

- **路径转义提醒**：在 C/C++ 字符串字面量中，Windows 路径分隔符 `\` 是转义字符，因此必须写成双反斜杠 `\\`（如 `"c:\\tmp\\test.txt"`），或者直接使用正斜杠 `"c:/tmp/test.txt"`。
- **流对象参数（`stream`）**：
  - `stdin`：替换**标准输入流**（键盘 → 输入文件）。
  - `stdout`：替换**标准输出流**（控制台屏幕 → 输出文件）。

---

## 2. 文件打开模式（`mode`）对照表

`freopen` 的模式参数与 C 语言 `fopen` 完全一致：

| 模式 | 读写权限 | 文件不存在时 | 文件已存在时 | 初始文件指针位置 |
| :---: | --- | --- | --- | --- |
| `"r"` | 只读 | 打开失败（返回 `NULL`） | 正常打开 | 文件头 |
| `"r+"` | 读写 | 打开失败（返回 `NULL`） | 正常打开 | 文件头 |
| `"w"` | 只写 | 自动新建 | **清空原内容** | 文件头 |
| `"w+"` | 读写 | 自动新建 | **清空原内容** | 文件头 |
| `"a"` | 追加只写 | 自动新建 | 保留原内容 | 文件尾 |
| `"...x"` | 独占新建修饰符（如 `"wx"` / `"w+x"`） | 自动新建 | **打开失败（防止覆盖）** | 文件头 |

> [!note] 补充说明
> 二进制读写可在模式后附加 `b`（如 `"rb"`、`"wb"`）；`"x"` 为 C11 / C++17 标准的独占创建修饰符，用于避免意外覆盖已有文件。

---

## 3. 刷题与本地调试最佳实践

> [!tip] 用条件编译宏隔离 `freopen`，防止提交 OJ 时忘删
> 在线评测系统（OJ）通常使用标准输入输出评测（除非题目明确要求文件 I/O，如 NOI/CSP）。如果本地调试时直接硬编码 `freopen` 而提交前忘记注释，极易导致 **WA / RE / TLE**。推荐用宏开关包裹：
>
> ```cpp
> #ifdef LOCAL
>     freopen("in.txt", "r", stdin);
>     freopen("out.txt", "w", stdout);
> #endif
> ```
>
> 本地编译时加上 `-DLOCAL` 参数即可启用文件重定向，提交到 OJ 时自动失效，零风险！

> [!tip] 搭配 `EOF` 循环读入整份测试文件
> 使用 `freopen` 重定向输入文件后，文件末尾会自动触发 `EOF`，非常适合配合 [[CS Learning/C++ PKU/scanf & cin special usage/scanf & cin special usage|scanf & cin special usage — 读入状态与循环输入]] 中的 `while (cin >> n >> m)` 或 `while (scanf(...) != EOF)` 一次性跑完所有测试样例。

---

## 完整源码

```cpp
/*
调试程序时,每次运行程序都要输入测试数据,太麻烦
可以将测试数据存入文件,然后用freopen将输入由键盘重新定下为文件
使用示例:freopen("c:\\tmp\\test.txt","r",stdin);
    关于r的用途详细与C相同:
    r打开只读
    r+打开读写,从文件头开始
    w打开只写。如果不存在则新建,如果存在则清空
    w+打开读写。如果不存在则新建,如果存在则清空
    a打卡追加。如果不存在则新建,如果存在则从文件尾开始
    ...x只新建，如果文件已存在则不能打开
    stdin 为替换类型,这里指的就是替换标准输入流
    相应的还可以替换stdout即标准输出流,常见于freopen("output.txt", "w", stdout);
*/
```
