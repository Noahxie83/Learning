---
title: "string — string 字符串容器"
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
aliases:
  - std::string
  - string
  - 字符串容器
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# string — string 字符串容器

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Sequence containers/list/list|list — 双向链表容器]] · 下一篇：[[CS Learning/C++ STL/Containers/Sequence containers/vector/vector|vector — 动态数组容器]]
> 源码：[[CS Learning/C++ STL/Containers/Sequence containers/string/string.cpp|查看源码]]

> [!abstract] 本节概览
> `std::string`（即 `std::basic_string<char>`）定义于头文件 `<string>`，是对 C 风格字符数组的动态安全封装。其底层维护==连续字符缓冲区==（C++11 起保证末尾自动携带 `\0` 终止符，且主流标准库均实现**短字符串优化 SSO**，短串无需堆分配）。支持 $O(1)$ 随机下标访问与均摊 $O(1)$ 尾部追加（`+=` / `push_back`），提供随机访问迭代器；扩容或中间修改会使迭代器、引用及 `c_str()` 返回的指针失效。

## 核心概念、声明与初始化

```cpp
#include <string>

string str;                      // 空字符串 ""
string s1 = "Hello,World!";      // 从 C 字符串初始化
string s2(5, 'a');               // 构造 "aaaaa"
string str1 = "Hello,";
string str2 = "World!";
string result = str1 + str2;     // 使用 + 连接生成新字符串
```

> [!note] 原注释笔误说明
> 原源码注释第 12 行写作 `string result str1+str2;` 漏写了一个 `=`，正确声明应为 `string result = str1 + str2;`。

## 常用运算符与成员函数速查

### 1. 高频运算符与快捷操作

| 作用 | 用法 | 示例与说明 | 时间复杂度 |
| --- | --- | --- | --- |
| 修改 / 查询指定下标字符 | `s[i]` | 无边界检查；需要越界抛异常时用 `s.at(i)` | $O(1)$ |
| 比较是否相等 / 字典序 | `==`、`!=`、`<`、`>` | 逐字符按 ASCII 字典序比较 | $O(\min(n, m))$ |
| 字符串拼接（生成新串） | `s1 + s2` | 产生新的临时 `string` 对象 | $O(n + m)$ |
| 尾接字符串 / 字符 | `s += t` / `s.push_back(c)` | ==原地尾接，强烈推荐在循环中使用 `+=`== | 均摊 $O(|t|)$ / $O(1)$ |
| 截取子串 | `s.substr(pos, len)` | 从下标 `pos` 起截取长度为 `len` 的子串（省略 `len` 则截到末尾） | $O(\text{len})$ |
| 查找子串 | `s.find(sub, pos)` | 从下标 `pos`（默认 0）起查找 `sub`，找不到返回 `string::npos` | 最坏 $O(n \cdot m)$ |

### 2. 完整成员函数速查

| 成员函数 | 说明 | 时间复杂度 |
| --- | --- | --- |
| `size()` / `length()` | 返回字符串当前字符个数（二者完全等价） | $O(1)$ |
| `empty()` | 判断字符串是否为空 | $O(1)$ |
| `operator[]` / `at(pos)` | 按下标访问字符（`at` 带边界检查） | $O(1)$ |
| `substr(pos, len)` | 返回从 `pos` 开始、长度为 `len` 的子串 | $O(\text{len})$ |
| `find(sub, pos)` / `rfind(sub, pos)` | 从前向后 / 从后向前查找子串或字符首次出现位置 | 最坏 $O(n \cdot m)$ |
| `replace(pos, len, str)` | 将从 `pos` 起长度为 `len` 的区间替换为 `str` | $O(n)$ |
| `append(str)` | 在字符串末尾追加内容（与 `+=` 等价，重载更多） | 均摊 $O(|str|)$ |
| `insert(pos, str)` | 在下标 `pos` 前插入内容 | $O(n)$ |
| `erase(pos, len)` | 删除从 `pos` 开始的 `len` 个字符（或按迭代器删） | $O(n)$ |
| `clear()` | 清空字符串内容（通常不释放已分配容量） | $O(1)$ |
| `c_str()` / `data()` | 返回以 `\0` 结尾的 `const char*`（C++17 起非 const `data()` 返回 `char*`） | $O(1)$ |
| `compare(other)` | 字典序比较：相等返回 `0`，小于返回负数，大于返回正数 | $O(\min(n, m))$ |
| `find_first_of(chars)` | 查找首个属于**字符集合 `chars` 中任意字符**的位置 | $O(n \cdot |chars|)$ |
| `find_last_of(chars)` | 查找最后一个属于 `chars` 中任意字符的位置 | $O(n \cdot |chars|)$ |
| `find_first_not_of(chars)` | 查找首个**不属于** `chars` 中任意字符的位置 | $O(n \cdot |chars|)$ |
| `find_last_not_of(chars)` | 查找最后一个**不属于** `chars` 中任意字符的位置 | $O(n \cdot |chars|)$ |

## 典型用法与性能陷阱

### 1. 为什么“尾接字符串一定要用 `+=`”

```cpp
// ❌ 极慢：每次 s + 'a' 都要拷贝整条旧串，循环 n 次退化为 O(n^2)
for (int i = 0; i < n; ++i) s = s + 'a';

// ✅ 高效：原地倍增扩容追加，循环 n 次总复杂度 O(n)
for (int i = 0; i < n; ++i) s += 'a';
```

### 2. 查找失败判断：`string::npos`

`find` 系列函数的返回类型是无符号整数 `size_t`；查找失败时返回常量 `string::npos`（通常为 `size_t(-1)`）：

```cpp
size_t pos = str.find("World");
if (pos != string::npos) {
    str.replace(pos, 5, "C++"); // 将 "World" 替换为 "C++"
}
```

### 3. `find_first_of` 匹配的是“字符集合”而非整串

源码中 `str.find_first_of("aeiou")` 会查找 `"Hello,C++!"` 中**第一个元音字母**（`'e'`，下标 `1`），而不是查找子串 `"aeiou"`；常用于按多种分隔符切分或去除首尾空白（`find_first_not_of(" \t\r\n")`）。

## 常见易错点与迭代器失效规则

> [!warning] `string` 高频易错点
> 1. **`substr(pos, len)` 的第二个参数是长度而非结束下标**：例如从下标 `7` 截取 5 个字符写作 `str.substr(7, 5)`，不是 `[7, 5)`。
> 2. **警惕 `size_t` 无符号下溢**：当 `s` 为空时，`s.size() - 1` 会发生无符号整数回绕变成极大正数，循环写 `i < (int)s.size() - 1` 或先判 `!s.empty()`。
> 3. **与 `c_str()` / 迭代器的失效规则**：任何导致字符串内容修改或扩容的操作（如 `+=`、`append`、`insert`、`replace`、`erase`、`clear`）都可能使之前获取的迭代器、引用以及 `c_str()` / `data()` 指针**立即失效**。

## 完整源码

```cpp
/*
string的定义：
在C++中，字符串是由字符组成的序列。<string> 头文件提供了string类，它是对C风格字符串的封装，提供了更安全、更易用的字符串操作功能。

string的声明：
头文件 #include <string>
初始化：
       string str;
       string str="Hello,World!";
       string str1="Hello,";
       string str2="World!";
       string result str1+str2;「可以使用+实现两个string的连接」

作用	                  用法
修改、查询指定下标字符  	[]
是否相同	               ==
字符串连接	                +
尾接字符串	               +=	                   尾接字符串一定要用 +=
取子串	            .substr(起始下标,子串长度)	string sub=s.substr(2,10);
查找字符串	         .find(字符串,起始下标)	    int pos=s.find("awa");

成员函数：
size()	            返回字符串的长度（字符数）。
length()	        与 size() 相同，返回字符串的长度。
empty()	            判断字符串是否为空。
operator[]	        访问字符串中指定位置的字符。
at()	            访问字符串中指定位置的字符（带边界检查）。
substr()	        返回从指定位置开始的子字符串。
find()	            查找子字符串在字符串中的位置。
rfind()	            从字符串末尾开始查找子字符串的位置。
replace()	        替换字符串中的部分内容。
append()	        在字符串末尾添加内容。
insert()	        在指定位置插入内容。
erase()	            删除指定位置的字符或子字符串。
clear()	            清空字符串。
c_str()	            返回 C 风格的字符串（以 null 结尾）。
data()	            返回指向字符数据的指针（C++11 及之后的版本）。
compare()	        比较两个字符串。
find_first_of()	    查找第一个匹配任意字符的位置。
find_last_of()	    查找最后一个匹配任意字符的位置。
find_first_not_of()	查找第一个不匹配任意字符的位置。
find_last_not_of()	查找最后一个不匹配任意字符的位置。
*/
#include <iostream>
#include <string>
using namespace std;
int main() {
    string str="Hello,World!";
    // size()
    cout<<"Length: "<<str.size()<<endl;
    // empty()
    cout<<"Is empty? "<<(str.empty()?"Yes":"No")<<endl;
    // operator[]
    cout<<"First character: "<<str[0]<<endl;
    // at()
    cout<<"Character at position 7: "<<str.at(7)<<endl;
    // substr()
    string sub=str.substr(7,5);
    cout<<"Substring from position 7 with length 5: "<<sub<<endl;
    // find()
    size_t pos=str.find("World");
    cout<<"Position of 'World': "<<pos<<endl;
    // replace()
    str.replace(pos,5,"C++");
    cout<<"Modified string: "<<str<<endl;
    // append()
    str.append(" How are you?");
    cout<<"Appended string: "<<str<<endl;
    // insert()
    str.insert(7," Beautiful");
    cout<<"String after insert: "<<str<<endl;
    // erase()
    str.erase(7,10);
    cout<<"String after erase: "<<str<<endl;
    // clear()
    str.clear();
    cout<<"String after clear: "<<(str.empty()?"Empty":"Not empty")<< std::endl;
    // c_str()
    str="Hello,C++!";
    const char* cstr=str.c_str();
    cout<<"C-style string: "<<cstr<<endl;
    // compare()
    int cmp=str.compare("Hello,C++!");
    cout<<"Comparison result: "<<cmp<<endl;
    // find_first_of()
    size_t pos_first_vowel=str.find_first_of("aeiou");
    cout<<"First vowel at position: "<<pos_first_vowel<<endl;
    // find_last_of()
    size_t pos_last_vowel=str.find_last_of("aeiou");
    cout<<"Last vowel at position: "<<pos_last_vowel<<endl;
    // find_first_not_of()
    size_t pos_first_non_vowel=str.find_first_not_of("aeiou");
    cout<<"First non-vowel at position: "<<pos_first_non_vowel<<endl;
    // find_last_not_of()
    size_t pos_last_non_vowel=str.find_last_not_of("aeiou");
    cout<<"Last non-vowel at position: "<<pos_last_non_vowel<<endl;
    return 0;
}
```
