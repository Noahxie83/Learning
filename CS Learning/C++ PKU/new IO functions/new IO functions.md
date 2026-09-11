# new IO functions — C++ 输入输出

[查看源码](./new%20IO%20functions.cpp) · [返回 C++ PKU 笔记目录](../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### 原注释 1（源码第 11–15 行）

```cpp
char c;
    cin >>c;
    cout <<"  "<<c<<endl;
    cout <<" "<<c<<c<<c<<endl;
    cout <<c<<c<<c<<c<<c<<endl;
```

### 原注释 2（源码第 20–23 行）

cin用于输入,cout用于输出,cout中的endl相当于换行

使用cin.get()可以读入所有的字符包括' '、'\\n'而不跳过

但是cin和cout比scanf和printf速度慢,后者用于IO数据量大时

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 3 | ` using namespace std; ` | 注意以上三行与C的不同 |
| 5 | 独立注释 | printf("Hello,world!\\n"); |
| 6 | 独立注释 | int k='a'; |
| 7 | 独立注释 | printf("%d\\n",k); |
| 8 | 独立注释 | int n=254;//与C相同整型只保留最右边的一个字节(0~7位,即0~255) |
| 9 | 独立注释 | char k=n; |
| 10 | 独立注释 | printf("%c",k); |

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
