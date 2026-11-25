---
title: new IO functions — C++ 输入输出
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
  - new IO functions
  - C++ 输入输出
  - cin 与 cout
  - cin.get
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# new IO functions — C++ 输入输出

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/Loop statesments/Loop statesments|Loop statesments — 循环与范围 for]] · 下一篇：[[CS Learning/C++ PKU/pointer/pointer|pointer — void 指针与内存操作]]
> 源码：[[CS Learning/C++ PKU/new IO functions/new IO functions.cpp|查看源码]]

> [!abstract] 本节概览
> 本节聚焦从 C 语言向 C++ 过渡的第一步：认识 C++ 标准头文件的引入方式与命名空间 `std`，对比标准流对象 `cin` / `cout` 与 C 风格 `scanf` / `printf` 的特性及性能差异，并掌握保留空白字符的逐字符读入函数 `cin.get()` 以及整型向 `char` 赋值的低字节截断规则。

---

## 1. 从 C 到 C++：程序头部框架变化

源码开头的三行体现了 C++ 程序与传统 C 程序最直观的差异：

```cpp
#include <iostream>  // C++ 标准输入输出流库（提供 cin / cout / endl）
#include <cstdio>    // C 标准库 <stdio.h> 的 C++ 版本（去 .h、加前缀 c）
using namespace std; // 引入 std 命名空间，免去每次写 std::cin / std::cout
```

---

## 2. 字符、ASCII 码与整型截断（源码注释实验）

源码第 5–10 行保留了一组从 C 延续下来的类型转换小实验：

```cpp
int k = 'a';
printf("%d\n", k); // 输出字符 'a' 对应的 ASCII 码：97

int n = 254;       // 二进制低 8 位为 1111 1110
char c = n;        // 仅保留最低 1 个字节（0~7 位，共 8 bit，无符号范围 0~255）
printf("%c", c);
```

- 与 C 语言一致，将 `int` 赋值给 `char` 时只截断保留**最右边 1 个字节（低 8 位）**；若当前平台 `char` 默认为有符号类型（`signed char`，范围 $-128 \sim 127$），`254` 会以补码解释为 `-2`。

---

## 3. `cin` / `cout` 与 `cin.get()` 用法详解

### 格式化流输入输出（`cin >>` / `cout <<`）

- `cin` 用于标准输入，`cout` 用于标准输出，无需像 `scanf`/`printf` 那样手写 `%d`、`%c`、`%s` 格式说明符，编译器会根据变量类型自动匹配。
- `endl` 不仅输出换行符 `'\n'`，还会**立即刷新输出缓冲区**（flush）。
- 源码注释中的字符金字塔示例：

```cpp
char c;
cin >> c;
cout << "  " << c << endl;
cout << " " << c << c << c << endl;
cout << c << c << c << c << c << endl;
```

### 逐字符原样读入（`cin.get()`）

`cin >> c` 会自动**跳过空格 `' '`、制表符 `'\t'` 和换行符 `'\n'`**；如果需要逐个读入所有原始字符（包含空白与换行），应使用 `cin.get()`：

```cpp
int a;
while ((a = cin.get()) != EOF) {
    cout << (char)a;
}
```

> [!important] 为什么用 `int a` 而不是 `char a` 接收 `cin.get()`？
> 无参版本的 `cin.get()` 返回类型是 **`int`**（等价于 C 的 `getchar()`）：
> - 读到合法字符时，返回该字符对应的无符号字节值（$0 \sim 255$）；
> - 遇到文件尾或输入结束时，返回特殊常量 `EOF`（通常为 `-1`）。
>
> 若用 `char` 接收，在某些平台上无法区分合法字节 `0xFF`（`-1`）与 `EOF`，因此必须先用 `int` 接住并判断 `!= EOF`，确认有效后再转为 `(char)a` 输出。

---

## 4. `cin` / `cout` vs `scanf` / `printf` 性能对比

| 维度 | `cin` / `cout` | `scanf` / `printf` |
| --- | --- | --- |
| **类型安全** | 编译期自动识别类型，不易写错格式符 | 需手动指定 `%d`/`%lld`/`%lf`，错配会导致未定义行为 |
| **默认速度** | **较慢**（默认与 C 标准 I/O 保持同步，且 `cin` 与 `cout` 绑定） | **较快**，适合大数据量 I/O 场景 |
| **空白处理** | `cin >>` 跳过空白；`cin.get()` / `getline()` 保留空白 | `%c` 读取空白，`%d`/`%s` 跳过空白 |

> [!tip] 在算法竞赛中如何给 `cin` / `cout` 提速？
> 当 I/O 数据量很大（如 $10^5 \sim 10^6$ 级别）时，除了改用 `scanf`/`printf`，也可以在 `main()` 开头加上以下两句解除同步与绑定，并==用 `'\n'` 替代 `endl`==（避免每次换行都刷缓冲区）：
>
> ```cpp
> ios::sync_with_stdio(false);
> cin.tie(nullptr);
> ```
>
> **注意**：关闭 `sync_with_stdio(false)` 后，**不要再将 `cin`/`cout` 与 `scanf`/`printf` 混用**，否则输出顺序可能错乱！

相关笔记延伸：[[CS Learning/C++ PKU/scanf & cin special usage/scanf & cin special usage|scanf & cin special usage — 读入状态与循环输入]] · [[CS Learning/C++ PKU/string/string|string — 字符串与整行输入]]。

---

## 完整源码

```cpp
#include <iostream>
#include <cstdio>
using namespace std;//注意以上三行与C的不同
int main(){
    //printf("Hello,world!\n");
    //int k='a';
    //printf("%d\n",k);
    //int n=254;//与C相同整型只保留最右边的一个字节(0~7位,即0~255)
    //char k=n;
    //printf("%c",k);
    /*char c;
    cin >>c;
    cout <<"  "<<c<<endl;
    cout <<" "<<c<<c<<c<<endl;
    cout <<c<<c<<c<<c<<c<<endl;*/
    int a;
    while ((a=cin.get())!=EOF){
        cout<<(char)a;
    }
    /*cin用于输入,cout用于输出,cout中的endl相当于换行
    使用cin.get()可以读入所有的字符包括' '、'\n'而不跳过
    但是cin和cout比scanf和printf速度慢,后者用于IO数据量大时
    */
    return 0;
}
```
