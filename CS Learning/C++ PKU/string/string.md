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
cssclasses:
- learning-note
- subject-cs
- learning-code
---

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/README|C++ PKU]]

# string — 字符串与整行输入

[查看源码](./string.cpp) · [返回 C++ PKU 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

用于数组类型字符串的cstring:

```cpp
cin.getline(char buf[],int bufsize);
```

可以读入一行(行长度不超过bufsize-1)或bufsize-1个字符到buf里

可以自动添加'\\0'回车换行符不会写入buf,但是会从输入流中去掉

cstring库函数中新增了

strcat、strupr/strlwr函数,分别起到拼接、转换大/小写的功能

用于string类型的字符串函数库string:

getline(cin,s,'a')  cin指输入流,s指存入的string类型字符串,'a'指读到'a'停止,a可以在字符中任意替换

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
