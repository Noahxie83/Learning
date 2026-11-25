---
title: "multiset — 允许重复元素的有序集合"
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
aliases:
  - std::multiset
  - multiset
  - 允许重复元素的有序集合
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# multiset — 允许重复元素的有序集合

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Associative containers/multimap/multimap|multimap — 允许重复键的有序映射]] · 下一篇：[[CS Learning/C++ STL/Containers/Associative containers/set/set|set — 有序集合]]
> 源码：[[CS Learning/C++ STL/Containers/Associative containers/multiset/multiset.cpp|查看源码]]

> [!abstract] 本节概览
> `std::multiset` 定义于头文件 `<set>`，底层基于==平衡二叉搜索树（红黑树）==实现，能够自动维持元素有序并==允许存放重复元素==。当业务需要在**频繁动态增删的同时进行大量查找**时，它以稳定的 $O(\log n)$ 复杂度替代低效的“反复排序 + 二分”。容器提供双向迭代器，支持自定义严格弱序比较器；插入不导致迭代器失效，删除仅使被删元素迭代器失效。

## 为什么需要平衡二叉树容器

在大量动态插入、删除数据的同时若还需频繁检索：

- 若使用“数组排序 + 二分查找”，每次插入新数据都需要重新维护有序性（移动元素 $O(n)$ 或重新排序 $O(n \log n)$），无法满足动态场景需求。
- 使用**平衡二叉树（红黑树）**组织数据，可使**增加、删除、查找**均稳定在 $O(\log n)$ 复杂度。STL 中基于此结构的四种有序关联容器分别是：`multiset`、`set`、`multimap`、`map`。

## 核心概念、自定义排序与“等价”判定

### 1. 声明与基本规则

```cpp
#include <set> // multiset 与 set 共用 <set> 头文件

multiset<int> st;              // 默认按 a < b（std::less<int>）升序排列
multiset<T, Rule<T>> customSt; // 使用自定义比较器 Rule<T> 排序
```

- 插入容器的是原变量的**拷贝（复制品）**（或通过 `emplace` 原地构造）。
- 访问元素需通过**双向迭代器** `multiset<T>::iterator`：支持 `++`、`--`、`==`、`!=` 与 `*it`，**不支持** `<`/`>` 大小比较、`it + n` 加减整数或 `it2 - it1` 相减。
- `st.begin()` 指向首个元素；`st.end()` 指向最后一个元素的**后一位置**（不可解引用）。

### 2. 严格弱序中的“等价”而非 `==`

关联容器判断两个元素 $a$ 与 $b$ 是否“相等”，依据的是比较器的==等价关系（Equivalence）==，而**不是** `operator==`：

$$\text{等价}(a, b) \iff \neg\text{comp}(a, b) \land \neg\text{comp}(b, a)$$

即“$a$ 必须排在 $b$ 前面”和“$b$ 必须排在 $a$ 前面”**都不成立**。

> [!example] 按个位数排序的经典推论
> 若自定义比较规则为按个位数升序（`a % 10 < b % 10`），那么对于 `133` 和 `13`，既不满足 `133 % 10 < 13 % 10`，也不满足 `13 % 10 < 133 % 10`，二者在该排序规则下**等价**。因此调用 `st.find(133)` 可以直接命中容器中的 `13`！

## 常用接口与时间复杂度速查

| 成员函数 | 说明 | 时间复杂度 |
| --- | --- | --- |
| `st.insert(val)` | 插入元素 `val`，总是成功，返回指向新插入元素的迭代器 | $O(\log n)$ |
| `st.find(val)` | 查找等价于 `val` 的元素，找到返回其迭代器，否则返回 `st.end()` | $O(\log n)$ |
| `st.count(val)` | 统计等价于 `val` 的元素个数 | $O(\log n + k)$ |
| `st.lower_bound(val)` | 返回首个 $\ge \text{val}$ 的元素迭代器（使 `[begin(), it)` 均严格在 `val` 前面） | $O(\log n)$ |
| `st.upper_bound(val)` | 返回首个 $> \text{val}$ 的元素迭代器（使 `[it, end())` 均严格在 `val` 后面） | $O(\log n)$ |
| `st.equal_range(val)` | 返回 `{lower_bound(val), upper_bound(val)}` 区间对 | $O(\log n)$ |
| `st.erase(it)` | ==仅删除迭代器 `it` 指向的单个元素== | 均摊 $O(1)$ |
| `st.erase(val)` | ==删除容器中所有等价于 `val` 的元素==，返回删除个数 | $O(\log n + k)$ |
| `st.size()` / `st.empty()` | 返回元素个数 / 判空 | $O(1)$ |

## 源码执行轨迹拆解

源码将 `{1, 14, 12, 13, 7, 13, 21, 19, 8, 8}` 依次插入 `multiset<int>` 后，内部自动有序序列为：

```text
1, 7, 8, 8, 12, 13, 13, 14, 19, 21
```

随后依次执行查找、插入 `22`、上下界定位与删除：
1. `st.find(22)` 首次返回 `st.end()`（输出 `Not Found`）；插入 `22` 后再次查找输出 `Found:22`。
2. `st.lower_bound(14)` 指向首个 $\ge 14$ 的元素 `14`。
3. `st.upper_bound(8)` 指向首个 $> 8$ 的元素 `12`。
4. `st.erase(i)` 仅删除该迭代器指向的 `12`，最终输出 `1,7,8,8,13,13,14,19,21,22,`。

> [!note] 原源码注释勘误说明
> 原源码第 53 行（文末第 154 行）的 `st.lower_bound(14)` 注释笔误写作“都在 13 前面”，准确含义应为：返回最靠后的迭代器 `it`，使得 `[begin(), it)` 中的元素都严格排在 **`14`** 前面（即第一个 $\ge 14$ 的元素）。另外第 52 行注释漏写了刚插入的 `22`。

## 常见易错点与迭代器失效规则

> [!warning] `erase(val)` 与 `erase(it)` 的致命区别
> 在算法题中使用 `multiset` 维护可重集合并“删去一个值 `x`”时，**切勿直接写 `st.erase(x)`**——它会把集合里所有的 `x` 全部删光！正确做法是先判空/查找再按迭代器删除：
> ```cpp
> auto it = st.find(x);
> if (it != st.end()) {
>     st.erase(it); // 只删一个 x
> }
> ```

> [!tip] 成员函数 `lower_bound` 优于通用算法 `std::lower_bound`
> 对 `set` / `multiset` 查找上下界时，务必调用**成员函数 `st.lower_bound(x)`**（复杂度 $O(\log n)$）。若误用 `<algorithm>` 中的 `std::lower_bound(st.begin(), st.end(), x)`，由于双向迭代器不支持随机跳跃，指针步进退化为 **$O(n)$**！

## 完整源码

```cpp
/*
STL中的平衡二叉树数据结构
有时需要在大量增加、删除数据的同时,还要进行大量数据的查找
希望增加数据、删除数据、查找数据都能在 log(n)复杂度完成
排序+二分查找显然不可以,因加入新数据就要重新排序
可以使用“平衡二叉树”数据结构存放数据,体现在STL中,就是以
下四种“排序容器”:multiset set multimap map
(一)multiset
multiset<T> st;
定义了一个multiset变量st,st里面可以存放T类型的数据,并且能自动排序。开始st为空
基础排序规则:表达式“a<b” 为true,则a排在b前面
可用st.insert添加元素,st.find查找元素,st.erase删除元素,复杂度都是log(n)
    multiset<T>::iterator p;
    p是迭代器,相当于指针,可用于指向multiset中的元素。访问multiset中的元素需要通过迭代器
    与指针不同:multiset上的迭代器可以++、--,用!=和==比较,不可比较大小,不可加减整数,不可相减
    st.begin()返回值类型为multiset<l>::iterator,
    是指向st中的头一个元素的迭代器
    st.end()返回值类型为multiset<T>::iterator,
    是指向st中的【最后一个元素后面】的迭代器
    对迭代器++,其就指向容器中下一个元素,--则令其指向上一个元素
与sort一样其还可以自定义排序规则
multiset<T,Rule<T>> st;
同理这里的【等于】的含义:<a必须在b前面>和<b必须在a前面>都不成立;【不是"=="】
e.g. 以个位数大小排序时可以通过find找133而找到数组中的13
*/
#include <iostream>
#include <cstring>
#include <set>//使用multiset和set需要此头文件
using namespace std;
int main (){
    multiset<int> st;
    int a[10]={1,14,12,13,7,13,21,19,8,8 };
    for(int i=0;i<10;i++){
        st.insert(a[i]);
    }//插入的是a[i]的复制品
    multiset<int>::iterator i;//迭代器,近似于指针
    for(i=st.begin();i!=st.end();i++){
        cout<<*i<<",";
    }
    cout<<endl;//1,7,8,8,12,13,13,14,19,21,
    i=st.find(22);//查找22,返回值为迭代器,找不到返回值为end()
    if (i==st.end()){
        cout<<"Not Found"<<endl;
    }
    st.insert(22);
    i=st.find(22);
    if (i==st.end()){//找到则返回指向找的元素的迭代器
        cout<<"Not Found"<<endl;
    }
    else {
        cout<<"Found:"<<*i<<endl;
    }//1,7,8,8,12,13,13,14,19,21,
    i=st.lower_bound(14);//返回最靠后的迭代器it,使得[begin(),it)中的元素都在13前面,复杂度log(n)
    cout<<*i<<endl;
    i=st.upper_bound(8);//返回最靠前的迭代器 it,使得[it,end())中的元素都在8后面,复杂度1og(n)
    cout<<*i<<endl;
    st.erase(i);//删除迭代器 i 指向的元素,即12
    for(i=st.begin();i!=st.end();i++){
        cout<<*i<<",";
    }
    return 0;
}
```
