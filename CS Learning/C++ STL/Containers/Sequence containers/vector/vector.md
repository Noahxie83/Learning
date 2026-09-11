# vector — 动态数组容器

[查看源码](./vector.cpp) · [返回 C++ STL 笔记目录](../../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

### vector的定义:\[时间复杂度O(n)\]

&lt;vector&gt; 是 STL 中的一个容器类，用于存储动态大小的数组。

&lt;vector&gt; 是一个序列容器，它允许用户在容器的末尾快速地添加或删除元素。

与数组相比，&lt;vector&gt; 提供了更多的功能，如自动调整大小、随机访问等。

### vector的声明

头文件:\#include &lt;vector&gt;(长度,\[初值\])

```cpp
vector<int> myVector;
```

| 用法 / 项目 | 原笔记 |
| --- | --- |
| 添加元素: | myVector.push\_back(10); |
| 访问元素: | int firstElement = myVector\[0\]; |

获取元素数量:size\_t size = myVector.size();

清空vector: myVector.clear();

### 以下是常用成员函数

| 用法 / 项目 | 原笔记 |
| --- | --- |
| push\_back(const T&amp; val) | 在末尾添加元素(尾接) |
| pop\_back() | 删除末尾元素(尾删) |
| at(size\_t pos) | 返回指定位置的元素，带边界检查 |
| operator\[\] | 返回指定位置的元素，不带边界检查 |
| front() | 返回第一个元素 |
| back() | 返回最后一个元素 |
| data() | 返回指向底层数组的指针 |
| size() | 返回当前元素数量 |
| capacity() | 返回当前分配的容量 |
| reserve(size\_t n) | 预留至少 n 个元素的存储空间 |
| resize(size\_t n, val) | 将元素数量调整为 n;如果是缩短，则删除多余的值;如果是扩大，且指定了val(未指定为默认值)，则新元素均为val（旧元素不变） |
| clear() | 清空所有元素如果是空返回 true 反之返回 false. |
| empty() | 判断是否空 |
| insert(iterator pos, val) | 在指定位置插入元素 |
| erase(iterator pos) | 删除指定位置的元素,同时参数用(const\_iterator first, const\_iterator last)可区间删除\[first,last)的元素并返回指向被删除元素的下一个有效元素的迭代器 |
| begin() / end() | 返回起始/结束迭代器 |

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 33 | 独立注释 | &lt;vector&gt; 需要指定元素类型，可通过多种方式进行初始化： |
| 38 | 独立注释 | 声明和初始化示例 |
| 39 | ` vector<int> vec1; ` | 空的vector |
| 40 | ` vector<int> vec2(5); ` | 长度为5的vector，元素默认初始化 |
| 41 | ` vector<int> vec3(5,10); ` | 长度为5的vector，元素值为10 |
| 42 | ` vector<int> vec4={1,2,3,4}; ` | 使用初始化列表初始化 |
| 43 | ` vector<vector<int>> mat(100,vector<int> ()); ` | 构造初始100行，不指定列数的二维数组 |
| 44 | ` vector<vector<int>> mat(100,vector<int> (666, -1)); ` | 构造初始100行，初始666列的二维数组，初值为-1 |
| 45 | 独立注释 | 具体示例 |
| 46 | 独立注释 | 声明一个存储整数的 vector |
| 48 | 独立注释 | 添加元素 |
| 52 | 独立注释 | 输出 vector 中的元素 |
| 58 | 独立注释 | 添加更多元素 |
| 61 | 独立注释 | 再次输出 vector 中的元素 |
| 67 | 独立注释 | 访问特定元素 |
| 69 | 独立注释 | 清空 vector |
| 71 | 独立注释 | 检查 vector 是否为空 |
| 76 | 独立注释 | 以下是常用成员函数操作示例 |
| 77 | 独立注释 | 基本操作 |
| 80 | 独立注释 | 输出所有元素 |
| 86 | 独立注释 | 获取第一个和最后一个元素 |
| 90 | 独立注释 | 动态增加和删除元素 |
| 98 | 独立注释 | 删除最后一个元素 |
| 102 | 独立注释 | 预分配容量 |
| 105 | ` vec7.reserve(10); ` | 预留容量，避免频繁分配内存 |

## 完整源码

```cpp
/*
vector的定义:[时间复杂度O(n)]
<vector> 是 STL 中的一个容器类，用于存储动态大小的数组。
<vector> 是一个序列容器，它允许用户在容器的末尾快速地添加或删除元素。
 与数组相比，<vector> 提供了更多的功能，如自动调整大小、随机访问等。

vector的声明:
头文件:#include <vector>(长度,[初值])
vector<int> myVector;
添加元素:   myVector.push_back(10);
访问元素:   int firstElement = myVector[0];
获取元素数量:size_t size = myVector.size();
清空vector: myVector.clear();

以下是常用成员函数
push_back(const T& val)	    在末尾添加元素(尾接)
pop_back()	                删除末尾元素(尾删)
at(size_t pos)	            返回指定位置的元素，带边界检查
operator[]	                返回指定位置的元素，不带边界检查
front()	                    返回第一个元素
back()	                    返回最后一个元素
data()	                    返回指向底层数组的指针
size()	                    返回当前元素数量
capacity()	                返回当前分配的容量
reserve(size_t n)	        预留至少 n 个元素的存储空间
resize(size_t n, val)	    将元素数量调整为 n;如果是缩短，则删除多余的值;如果是扩大，且指定了val(未指定为默认值)，则新元素均为val（旧元素不变）
clear()	                    清空所有元素如果是空返回 true 反之返回 false.
empty()                     判断是否空
insert(iterator pos, val)	在指定位置插入元素
erase(iterator pos)	        删除指定位置的元素,同时参数用(const_iterator first, const_iterator last)可区间删除[first,last)的元素并返回指向被删除元素的下一个有效元素的迭代器
begin() / end()	            返回起始/结束迭代器
*/
//<vector> 需要指定元素类型，可通过多种方式进行初始化：
#include <iostream>
#include <vector>
using namespace std;
int main() {
    //声明和初始化示例
    vector<int> vec1;                 // 空的vector
    vector<int> vec2(5);              // 长度为5的vector，元素默认初始化
    vector<int> vec3(5,10);           // 长度为5的vector，元素值为10
    vector<int> vec4={1,2,3,4};       // 使用初始化列表初始化
    vector<vector<int>> mat(100,vector<int> ());       // 构造初始100行，不指定列数的二维数组
    vector<vector<int>> mat(100,vector<int> (666, -1)); // 构造初始100行，初始666列的二维数组，初值为-1
    //具体示例
    // 声明一个存储整数的 vector
    vector<int> numbers;
    // 添加元素
    numbers.push_back(10);
    numbers.push_back(20);
    numbers.push_back(30);
    // 输出 vector 中的元素
    cout<<"Vector contains: ";
    for (int i=0;i<numbers.size();i++){
        cout<<numbers[i]<<" ";
    }
    cout<<endl;
    // 添加更多元素
    numbers.push_back(40);
    numbers.push_back(50);
    // 再次输出 vector 中的元素
    cout<<"After adding more elements, vector contains: ";
    for (int i=0;i<numbers.size();i++){
        cout<<numbers[i]<<" ";
    }
    cout<<endl;
    // 访问特定元素
    cout<<"The first element is: "<<numbers[0]<<endl;
    // 清空 vector
    numbers.clear();
    // 检查 vector 是否为空
    if (numbers.empty()){
        cout<<"The vector is now empty."<<endl;
    }

    //以下是常用成员函数操作示例
    //基本操作

    vector<int> vec5={1,2,3,4,5};
    // 输出所有元素
    cout << "Vector elements: ";
    for (int i=0;i<vec5.size();i++) {
        cout<<vec5[i]<<" ";
    }
    cout<<endl;
    // 获取第一个和最后一个元素
    cout<<"First element: "<<vec5.front()<<endl;
    cout<<"Last element: "<<vec5.back()<<endl;

    //动态增加和删除元素

    vector<int> vec6;
    vec6.push_back(10);
    vec6.push_back(20);
    vec6.push_back(30);
    cout<<"Vector size: "<<vec6.size()<<endl;
    cout<<"Vector capacity: "<<vec6.capacity()<<endl;
    // 删除最后一个元素
    vec6.pop_back();
    cout<<"After pop_back, size: "<<vec6.size()<<endl;

    //预分配容量

    vector<int> vec7;
    vec7.reserve(10);  // 预留容量，避免频繁分配内存
    for (int i=0;i<10;i++) {
        vec7.push_back(i);
        cout<<"Capacity after push_back("<<i<<"): "<<vec7.capacity()<<endl;
    }
    return 0;
}
```
