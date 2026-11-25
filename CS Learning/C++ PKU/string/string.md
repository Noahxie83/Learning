---
title: string — 字符串与整行输入
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
  - string
  - 字符串与整行输入
  - getline
  - cin.getline
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# string — 字符串与整行输入

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/scanf & cin special usage/scanf & cin special usage|scanf & cin special usage — 读入状态与循环输入]]
> 源码：[[CS Learning/C++ PKU/string/string.cpp|查看源码]]

> [!abstract] 本节概览
> 普通的 `cin >> s` 遇到空格就会停止，无法直接读取包含空格的整行文本。本节对比面向 C 风格字符数组的 **`cin.getline()`**（配合 `<cstring>`）与面向 C++ 标准字符串的 **`std::getline()`**（`<string>`），梳理自定义分隔符、换行符消耗机制及混用 `cin >>` 时的经典“吞空行”陷阱。

---

## 1. 字符数组（`<cstring>`）的整行输入与常用函数

### `cin.getline(buf, bufsize)`

```cpp
char buf[100];
cin.getline(buf, 100); // 也可传第三参数指定自定义停止符：cin.getline(buf, 100, delim)
```

- 最多从输入流中读取 **`bufsize - 1`** 个字符（或在遇到换行符 `'\n'` 时提前结束），存入字符数组 `buf`；
- ==自动在末尾追加字符串结束符 `'\0'`==，防止越界；
- 行尾的回车换行符 `'\n'` **不会写入 `buf`**，但会被**从输入流中取出并丢弃**，不影响下一次读取。

### 补充的 `<cstring>` 函数说明

- **`strcat(dst, src)`**：将 `src` 拼接到 `dst` 末尾（带长度上限的安全版本 `strncat` 参见 [[CS Learning/C++ PKU/cstring/cstring|cstring — C 风格字符串函数]]）。
- **`strupr` / `strlwr`**：将字符串转换为全大写 / 全小写。

> [!note] `strupr` / `strlwr` 的可移植性提醒
> `strupr` 与 `strlwr` 是部分 Windows / MSVC 运行库提供的**非标准扩展函数**，在 Linux/GCC 严格标准模式下并不存在。可移植写法应引入 `<cctype>`，遍历字符逐个调用 `toupper((unsigned char)c)` / `tolower((unsigned char)c)`。

---

## 2. `std::string`（`<string>`）的整行输入：`std::getline`

对于 C++ 标准字符串 `std::string`，使用定义在 `<string>` 中的自由函数 `getline`：

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);      // 读取整行，默认以 '\n' 结束
    cout << s.size() << endl;
    cout << s;
    return 0;
}
```

### 自定义结束分隔符

`getline` 支持可选的第三个参数 `delim`，读到该字符或 `EOF` 时停止（分隔符同样**不存入 `s`**，但会从流中移除）：

```cpp
getline(cin, s, 'a'); // 从 cin 读入到 s，直到遇到字符 'a' 停止（'a' 可替换为任意字符）
```

---

## 3. 三种字符串输入方式对比

| 输入方式 | 目标类型 | 是否读入空格 | 长度安全 / 内存管理 | 行尾 `'\n'` 处理 |
| --- | --- | :---: | --- | --- |
| `cin >> s` | `char[]` / `string` | 否（遇空白停止） | `string` 自动扩容；`char[]` 易溢出 | **留在缓冲区** |
| `cin.getline(buf, n)` | `char[]` | **是** | 最多读 `n - 1` 字符并补 `'\0'` | **从流中消耗丢弃** |
| `getline(cin, s)` | `std::string` | **是** | 动态自动扩容，无定长上限烦恼 | **从流中消耗丢弃** |

---

## 4. 高频易错点：`cin >>` 与 `getline` 混用

> [!warning] 先 `cin >> n` 再 `getline(cin, s)` 为什么会读到空串？
> `cin >> n` 在读完数字后，会**把紧随其后的回车 `'\n'` 留在输入缓冲区中**；紧接着调用 `getline(cin, s)` 时，它立刻撞上残留的 `'\n'` 并认为整行已结束，于是 `s` 变成了空字符串 `""`！
>
> **标准解法**——在 `cin >> n` 与 `getline` 之间清理残留换行：
> ```cpp
> int n;
> cin >> n;
> cin.ignore();          // 丢弃紧跟的一个 '\n'（若行尾可能有空格，建议用 cin.ignore(10000, '\n') 或 getline 吃掉余行）
> // 或者：getline(cin >> ws, s);  // 跳过所有前导空白（含换行）后再读整行
> string s;
> getline(cin, s);
> ```

更完整的 `std::string` 成员接口（查找、切片、拼接与迭代器）可进一步参阅 [[CS Learning/C++ STL/Containers/Sequence containers/string/string|STL string 容器详解]]。

---

## 完整源码

```cpp
/*
用于数组类型字符串的cstring:
cin.getline(char buf[],int bufsize);
可以读入一行(行长度不超过bufsize-1)或bufsize-1个字符到buf里
可以自动添加'\0'回车换行符不会写入buf,但是会从输入流中去掉
cstring库函数中新增了
strcat、strupr/strlwr函数,分别起到拼接、转换大/小写的功能
用于string类型的字符串函数库string:
 getline(cin,s,'a')  cin指输入流,s指存入的string类型字符串,'a'指读到'a'停止,a可以在字符中任意替换
*/
#include <iostream>
#include <cstring>
#include <string>
using namespace std;
int main(){
    string s;
    getline(cin,s);
    cout<<s.size()<<endl;
    cout<<s;
    return 0;
}
```
