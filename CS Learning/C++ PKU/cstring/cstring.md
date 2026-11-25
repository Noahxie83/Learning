---
title: cstring — C 风格字符串函数
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
  - cstring
  - C 风格字符串函数
  - string.h
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# cstring — C 风格字符串函数

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/Classes and Objects/Classes and Objects|Classes and Objects — 类与对象]] · 下一篇：[[CS Learning/C++ PKU/freopen/freopen|freopen — 输入输出重定向]]
> 源码：[[CS Learning/C++ PKU/cstring/cstring.cpp|查看源码]]

> [!abstract] 本节概览
> 本节演示 C++ `<cstring>` 头文件（对应 C 语言 `<string.h>`）中处理以 `'\0'` 结尾的字符数组的核心库函数：带长度限制的拼接/拷贝/比较（`strncat`、`strncpy`、`strncmp`）、字符与子串定位（`strchr`、`strstr`），以及按多分隔符切分字符串的 `strtok`。

---

## 1. 常用 `<cstring>` 函数速查

| 函数原型 | 核心功能 | 返回值与关键细节 |
| --- | --- | --- |
| `strncat(dst, src, n)` | 将 `src` 前 `n` 个字符追加到 `dst` 末尾 | 返回 `dst`；==总是会在末尾自动补 `'\0'`==，需确保 `dst` 剩余空间足够 |
| `strncpy(dst, src, n)` | 将 `src` 最多 `n` 个字符拷贝到 `dst` 起始位置 | 若 `src` 前 `n` 字节含 `'\0'`，拷贝至 `'\0'` 并用 `'\0'` 填满剩余位数；若不含 `'\0'`，**不会自动补 `'\0'`** |
| `strncmp(s1, s2, n)` | 按字典序比较 `s1` 与 `s2` 的前 `n` 个字符 | 相等返回 `0`；`s1 < s2` 返回负值；`s1 > s2` 返回正值 |
| `strchr(s, ch)` | 在 `s` 中查找字符 `ch` **首次**出现的位置 | 找到返回指向该字符的 `char*`；未找到返回 `NULL` |
| `strstr(s, sub)` | 在 `s` 中查找子串 `sub` **首次**出现的位置 | 找到返回指向子串首字符的 `char*`；未找到返回 `NULL` |
| `strtok(str, delim)` | 按分隔符集合 `delim` 逐个切分 `str` | 首次调用传入 `str`，==后续调用首参必须传 `NULL`==；无更多子串时返回 `NULL` |

---

## 2. 源码执行轨迹与内存状态分析

初始状态：`s1 = "12345"`、`s2 = "abcdefg"`、`s3 = "ABCDE"`（缓冲区容量均为 `100`）。

| 步骤 | 执行语句 | 关键机制说明 | 实际输出 |
| :---: | --- | --- | --- |
| 1 | `strncat(s1, s2, 3);` | 取 `s2` 前 3 字符 `"abc"` 拼接到 `s1` 尾部 | `1)12345abc` |
| 2 | `strncpy(s1, s3, 3);` | 仅覆盖 `s1` 前 3 字节为 `"ABC"`，原有 `"45abc"` 不变 | `2)ABC45abc` |
| 3 | `strncpy(s2, s3, 6);` | `s3` 第 6 个字符恰好是结束符 `'\0'`，拷贝后 `s2` 在 `'E'` 处截断 | `3)ABCDE` |
| 4 | `strncmp(s1, s3, 3)` | 比较 `"ABC"` 与 `"ABC"`，完全一致 | `4)0` |
| 5 | `p = strchr(s1, 'B');` | 找到 `'B'` 的指针，利用指针相减 `p - s1` 得下标 `1` | `5)1,B` |
| 6 | `p = strstr(s1, "45a");` | 匹配位置下标 `p - s1 == 3`，`cout << p` 会从此处输出至 `'\0'` | `6)3,45abc` |

### `strtok` 切分流程拆解

源码对 `char str[] = "- This, a sample string, OK.";` 使用分隔符集 `" ,.-"`（空格、逗号、句点、连字符）切分：

```cpp
p = strtok(str, " ,.-");   // 首次调用：传入目标字符串
while (p) {                // 只要 p != NULL，说明提取到一个子串
    cout << p << endl;
    p = strtok(NULL, " ,.-"); // 后续调用：第一个参数必须是 NULL
}
```

逐行输出结果：

```text
strtok usage demo:
This
a
sample
string
OK
```

---

## 3. 易错点与 C++ 迁移建议

> [!warning] `strncpy` 与 `strtok` 的两大经典陷阱
> 1. **`strncpy` 不保证末尾补 `'\0'`**：当 `strlen(src) >= n` 时，`strncpy(dst, src, n)` 拷贝完 `n` 字节即停止，不会写入 `'\0'`。若是写入新缓冲区，应手动设置 `dst[n] = '\0'`（本例第 2 步是因为 `s1` 原本已有尾部的 `'\0'` 才未越界）。
> 2. **`strtok` 会原地修改原字符串**：`strtok` 的底层实现是把找到的分隔符直接改写成 `'\0'` 并借助内部静态指针记录扫描进度，因此：
>    - 不能直接对只读字符串字面量（`const char*`）调用 `strtok`；
>    - 不具备可重入性/线程安全性（多线程或嵌套切分应使用 `strtok_r` / `strtok_s` 或改用 C++ 流处理）。

> [!tip] C++ 中的现代替代方案
> 在现代 C++ 编程中，若非接口兼容或底层性能约束，通常推荐直接使用 `std::string`（参见 [[CS Learning/C++ PKU/string/string|string — 字符串与整行输入]] 与 [[CS Learning/C++ STL/Containers/Sequence containers/string/string|STL string 容器详解]]），配合 `std::stringstream` 实现安全、自动管理内存的字符串处理与切分。

---

## 完整源码

```cpp
#include <iostream>
#include <cstring>
using namespace std;
int main(){
    char s1[100]="12345";
    char s2[100]="abcdefg";
    char s3[100]="ABCDE";
    strncat(s1,s2,3);
    cout<<"1)"<<s1<<endl;//1)12345abc
    strncpy(s1,s3,3);
    cout<<"2)"<<s1<<endl;//2)ABC45abc s3的前三个字符拷贝到s1
    strncpy(s2,s3,6);
    cout<<"3)"<<s2<<endl;//3)ABCDE s3的第六个字符为\0故此处到E就结束了
    cout<<"4)"<<strncmp(s1,s3,3)<<endl;//4)0  比较两者前3个字符
    char *p=strchr(s1,'B');//在s1中查找'B'第一次出现的位置,字串中找字符
    if (p){
        cout<<"5)"<<p-s1<<","<<*p<<endl;
    }
    else {
        cout<<"5)Not Found"<<endl;
    }
    p=strstr(s1,"45a");//strstr字串中找子串
    if (p){
        cout<<"6)"<<p-s1<<","<<p<<endl;
    }
    else {
        cout<<"6)Not Found"<<endl;
    }
    cout<<"strtok usage demo:"<<endl;
    char str[]="- This, a sample string, OK.";
    p=strtok(str," ,.-");//从str中逐个抽出被",.-"字符分隔的字串
    while (p){  //只要p不是NULL,就说明找到了一个子串
        cout<<p<<endl;
        p=strtok(NULL," ,.-");//后续调用,第一个参数必须是NULL
    }
    return 0;
}
```
