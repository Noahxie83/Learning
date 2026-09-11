# Numeric — 数值算法

[查看源码](./Numeric.cpp) · [返回 C++ STL 笔记目录](../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

&lt;numeric&gt; 头文件提供了一组用于数值计算的函数模板

这些函数可以对容器中的元素进行各种数值操作，如求和、乘积、最小值、最大值等。

这些函数模板非常强大，可以应用于任何类型的容器，包括数组、向量、列表等。

头文件 \#include &lt;numeric&gt;

1.accumulate    函数

计算序列的累加和（可自定义二元操作）它接受三个参数：容器的开始迭代器、结束迭代器和初始值。

```cpp
    int accumulate(iterator beg,iterator end,int init);
```

可用于求数组总和、统计累计值

2.inner\_product 函数

计算两个序列的内积（对应元素相乘后累加，可自定义操作） 它接受三个参数：容器的开始迭代器、结束迭代器和初始值。

```cpp
    int inner_product(iter1 b1,iter1 e1,iter2 b2,int init);
```

可用于向量点积、加权求和

3.partial\_sum   函数

计算序列的前缀和（第n个结果=前n个元素的和，可自定义操作）

```cpp
    void partial_sum(iter b,iter e,iter res);
```

可用于生成前缀和数组、累积统计

4.adjacent\_difference   函数

计算序列相邻元素的差值（第n个结果=elem\[n\]-elem\[n-1\]，可自定义操作）

```cpp
    void adjacent_difference(iter b,iter e,iter res);
```

可用于计算差分、检测序列变化量

5.gcd   函数

计算两个整数的最大公约数

```cpp
    void gcd (int a,int b);
```

6.lcm   函数

计算两个整数的最小公倍数：

```cpp
    void lcm (int a,int b);
```

7.iota  函数

用连续递增的值填充序列（从 init 开始，逐个+1）

```cpp
    void iota(iter b,iter e,T init);
```

可用于生成连续整数序列、初始化有序容器

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 46 | 独立注释 | accumulate |
| 49 | ` cout<<"Sum: "<<sum<<endl; ` | 输出: Sum: 15 |
| 50 | 独立注释 | inner\_product |
| 54 | ` cout<<"Product Sum: "<<product_sum<<endl; ` | 输出: Product Sum: 32 |
| 55 | 独立注释 | partial\_sum |
| 60 | ` cout<<i<<" "; ` | 输出: 1 3 6 10 |
| 63 | 独立注释 | adjacent\_difference |
| 68 | ` cout<<i<<" "; ` | 输出: 1 1 1 |
| 71 | 独立注释 | gcd、lcm |
| 74 | ` int result2=gcd(a,b); ` | 计算 48 和 18 的最大公约数 |
| 75 | ` cout<<"GCD: "<<result2<<endl; ` | 输出 6 |
| 76 | ` int result3=lcm(a,b); ` | 计算 48 和 18 的最小公倍数 |
| 78 | 独立注释 | iota |
| 79 | ` vector<int> v5(5); ` | 创建一个包含5个元素的向量 |
| 80 | 独立注释 | 使用 iota 填充向量，起始值为1 |
| 82 | 独立注释 | 输出填充后的向量 |
| 86 | ` cout<<endl; ` | 输出: 1 2 3 4 5 |

## 完整源码

```cpp
/*
<numeric> 头文件提供了一组用于数值计算的函数模板
这些函数可以对容器中的元素进行各种数值操作，如求和、乘积、最小值、最大值等。
这些函数模板非常强大，可以应用于任何类型的容器，包括数组、向量、列表等。

头文件 #include <numeric>

1.accumulate    函数
计算序列的累加和（可自定义二元操作）它接受三个参数：容器的开始迭代器、结束迭代器和初始值。
    int accumulate(iterator beg,iterator end,int init);
    可用于求数组总和、统计累计值

2.inner_product 函数
计算两个序列的内积（对应元素相乘后累加，可自定义操作） 它接受三个参数：容器的开始迭代器、结束迭代器和初始值。
    int inner_product(iter1 b1,iter1 e1,iter2 b2,int init);
    可用于向量点积、加权求和

3.partial_sum   函数
计算序列的前缀和（第n个结果=前n个元素的和，可自定义操作）
    void partial_sum(iter b,iter e,iter res);
    可用于生成前缀和数组、累积统计

4.adjacent_difference   函数
计算序列相邻元素的差值（第n个结果=elem[n]-elem[n-1]，可自定义操作）
    void adjacent_difference(iter b,iter e,iter res);
    可用于计算差分、检测序列变化量

5.gcd   函数
计算两个整数的最大公约数
    void gcd (int a,int b);

6.lcm   函数
计算两个整数的最小公倍数：
    void lcm (int a,int b);

7.iota  函数
用连续递增的值填充序列（从 init 开始，逐个+1）
    void iota(iter b,iter e,T init);
    可用于生成连续整数序列、初始化有序容器
*/
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
int main(){
    //accumulate
    vector<int> v0={1,2,3,4,5};
    int sum=accumulate(v0.begin(),v0.end(),0);
    cout<<"Sum: "<<sum<<endl; // 输出: Sum: 15
    //inner_product
    vector<int> v1={1,2,3};
    vector<int> v2={4,5,6};
    int product_sum=inner_product(v1.begin(),v1.end(),v2.begin(),0);
    cout<<"Product Sum: "<<product_sum<<endl; // 输出: Product Sum: 32
    //partial_sum
    vector<int> v3={1,2,3,4};
    vector<int> result0(v3.size());
    partial_sum(v3.begin(),v3.end(),result0.begin());
    for (int i:result0){
        cout<<i<<" "; // 输出: 1 3 6 10
    }
    cout<<endl;
    //adjacent_difference
    vector<int> v4={1,2,3,4};
    vector<int> result1(v4.size() - 1);
    adjacent_difference(v4.begin(),v4.end(),result1.begin());
    for (int i:result1){
        cout<<i<<" "; // 输出: 1 1 1
    }
    cout<<endl;
    //gcd、lcm
    int a=48;
    int b=18;
    int result2=gcd(a,b);  // 计算 48 和 18 的最大公约数
    cout<<"GCD: "<<result2<<endl;  // 输出 6
    int result3=lcm(a,b);  // 计算 48 和 18 的最小公倍数
    cout<<"LCM: "<<result3<<endl;
    //iota
    vector<int> v5(5); // 创建一个包含5个元素的向量
    // 使用 iota 填充向量，起始值为1
    iota(begin(v5),end(v5),1);
    // 输出填充后的向量
    for (int i:v5){
        cout<<i<<" ";
    }
    cout<<endl; // 输出: 1 2 3 4 5
    return 0;
}
```
