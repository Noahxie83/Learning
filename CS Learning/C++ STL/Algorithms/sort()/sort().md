# sort() — 排序

[查看源码](./sort%28%29.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

sort()即排序算法,时间复杂度nlogn

(一)对基本类型的数组从小到大:

sort(数组名+n1,数组名+n2)

```cpp
    sort(arr.begin(),arr.end());
```

n1、n2为int类型,可以包含变量

排序范围是\[n1,n2)

(二)对类型为T的基本类型数组从大到小:

sort(数组名+n1,数组名+n2,greater&lt;T&gt;());

```cpp
    sort(arr.begin(),arr.end(),greater<T>());
```

(三)用自定义的排序规则,对任何类型T的数组排序

sort(数组名+n1,数组名+n2,排序规则结构名);

sort(arr.begin(),arr.end(),排序规则结构名&lt;T&gt;());

### 排序规则结构定义方式

struct 结构名{

```cpp
    bool operator()(const T &a1,const T &a2)const{
        //若a1应该在a2前面,返回true
        //否则返回false
        }
    }
```

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 26 | ` struct Rule1{ ` | 从大到小 |
| 31 | ` struct Rule2{ ` | 按个位数从小到大 |
| 44 | 独立注释 | sort(a+2,a+6); |
| 45 | 独立注释 | sort(a,a+7,greater&lt;int&gt;()); |

## 完整源码

```cpp
/*
sort()即排序算法,时间复杂度nlogn
(一)对基本类型的数组从小到大:
    sort(数组名+n1,数组名+n2)
    sort(arr.begin(),arr.end());
    n1、n2为int类型,可以包含变量
    排序范围是[n1,n2)
(二)对类型为T的基本类型数组从大到小:
    sort(数组名+n1,数组名+n2,greater<T>());
    sort(arr.begin(),arr.end(),greater<T>());
(三)用自定义的排序规则,对任何类型T的数组排序
    sort(数组名+n1,数组名+n2,排序规则结构名);
    sort(arr.begin(),arr.end(),排序规则结构名<T>());
    排序规则结构定义方式:
    struct 结构名{
    bool operator()(const T &a1,const T &a2)const{
        //若a1应该在a2前面,返回true
        //否则返回false
        }
    }
*/
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;
struct Rule1{//从大到小
    bool operator()(const int &a1,const int &a2)const{
        return a1>a2;
        }
    };
struct Rule2{//按个位数从小到大
    bool operator()(const int &a1,const int &a2)const{
        return a1%10<a2%10;
        }
    };
void Print(int a[],int size){
    for (int i=0;i<size;++i){
        cout<<a[i]<<",";
    }
    cout<<endl;
}
int main(){
    int a[]={12,45,3,98,21,7};
    //sort(a+2,a+6);
    //sort(a,a+7,greater<int>());
    sort(a,a+sizeof(a)/sizeof(int),Rule1());
    Print(a,sizeof(a)/sizeof(int));
    sort(a,a+sizeof(a)/sizeof(int),Rule2());
    Print(a,sizeof(a)/sizeof(int));
}
```
