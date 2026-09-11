# stack — 栈

[查看源码](./stack.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### stack的定义

&lt;stack&gt; 是 C++ 标准模板库（STL）的一部分，它实现了一个后进先出（LIFO，Last In First Out）的数据结构。这种数据结构非常适合于需要"最后添加的元素最先被移除"的场景。

&lt;stack&gt; 容器适配器提供了一个栈的接口，它基于其他容器（如 deque 或 vector）来实现。栈的元素是线性排列的，但只允许在一端（栈顶）进行添加和移除操作。

ps:不可访问stack的内部元素

头文件:\#include &lt;stack&gt;

基本成员函数:

push(): 在栈顶添加一个元素。

| 用法 / 项目 | 原笔记 |
| --- | --- |
| pop(): | 移除栈顶元素。 |
| top(): | 返回栈顶元素的引用，但不移除它。 |

empty():检查栈是否为空。ps：无clear

size(): 返回栈中元素的数量。

如果不卡常的话，就可以直接用它而不需要手写栈了。

另外,vector也可以当栈用,vector的.back()取尾部元素,就相当于取栈顶,.push\_back() 相当于进栈,.pop\_back() 相当于出栈。

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 19 | 独立注释 | 下为具体示例 |
| 25 | 独立注释 | 向栈中添加元素 |
| 29 | 独立注释 | 打印栈顶元素 |
| 30 | ` cout<<"Top element is: "<<s.top()<<std::endl; ` | 输出: Top element is: 30 |
| 31 | 独立注释 | 移除栈顶元素 |
| 33 | ` cout<<"After popping, top element is: "<<s.top()<<endl; ` | 输出: After popping, top element is: 20 |
| 34 | 独立注释 | 检查栈是否为空 |
| 36 | ` cout<<"Stack is not empty."<<endl; ` | 输出: Stack is not empty. |
| 38 | 独立注释 | 打印栈的大小 |
| 39 | ` cout<<"Size of stack: "<<s.size()<<endl; ` | 输出: Size of stack: 2 |
| 40 | 独立注释 | 继续移除元素 |
| 43 | 独立注释 | 检查栈是否为空 |
| 45 | ` cout<<"Stack is empty."<<endl; ` | 输出: Stack is empty. |

## 完整源码

```cpp
/*
stack的定义:
<stack> 是 C++ 标准模板库（STL）的一部分，它实现了一个后进先出（LIFO，Last In First Out）的数据结构。这种数据结构非常适合于需要"最后添加的元素最先被移除"的场景。
<stack> 容器适配器提供了一个栈的接口，它基于其他容器（如 deque 或 vector）来实现。栈的元素是线性排列的，但只允许在一端（栈顶）进行添加和移除操作。
ps:不可访问stack的内部元素

头文件:#include <stack>

基本成员函数:
push(): 在栈顶添加一个元素。
pop():  移除栈顶元素。
top():  返回栈顶元素的引用，但不移除它。
empty():检查栈是否为空。ps：无clear
size(): 返回栈中元素的数量。

如果不卡常的话，就可以直接用它而不需要手写栈了。
另外,vector也可以当栈用,vector的.back()取尾部元素,就相当于取栈顶,.push_back() 相当于进栈,.pop_back() 相当于出栈。
*/
//下为具体示例
#include <iostream>
#include <stack>
using namespace std;
int main() {
    stack<int> s;
    // 向栈中添加元素
    s.push(10);
    s.push(20);
    s.push(30);
    // 打印栈顶元素
    cout<<"Top element is: "<<s.top()<<std::endl; // 输出: Top element is: 30
    // 移除栈顶元素
    s.pop();
    cout<<"After popping, top element is: "<<s.top()<<endl; // 输出: After popping, top element is: 20
    // 检查栈是否为空
    if (!s.empty()) {
        cout<<"Stack is not empty."<<endl; // 输出: Stack is not empty.
    }
    // 打印栈的大小
    cout<<"Size of stack: "<<s.size()<<endl; // 输出: Size of stack: 2
    // 继续移除元素
    s.pop();
    s.pop();
    // 检查栈是否为空
    if (s.empty()) {
        cout<<"Stack is empty."<<endl; // 输出: Stack is empty.
    }
    return 0;
}
```
