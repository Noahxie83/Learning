---
title: "multimap — 允许重复键的有序映射"
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
aliases:
  - std::multimap
  - multimap
  - 允许重复键的有序映射
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# multimap — 允许重复键的有序映射

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Containers/Associative containers/map/map|map — 有序键值映射]] · 下一篇：[[CS Learning/C++ STL/Containers/Associative containers/multiset/multiset|multiset — 允许重复元素的有序集合]]
> 源码：[[CS Learning/C++ STL/Containers/Associative containers/multimap/multimap.cpp|查看源码]]

> [!abstract] 本节概览
> `std::multimap` 与 `std::map` 共用头文件 `<map>`，底层同样基于==红黑树==实现，存储按键自动排序的 `pair<const Key, T>` 元素，但==允许多个元素拥有相同的键==。它**不支持 `operator[]` 和 `at()`**，插入总是成功并返回新元素迭代器；查找与区间定位依赖 `find()`、`lower_bound()`、`upper_bound()` 和 `equal_range()`，复杂度均为 $O(\log n)$。迭代器稳定性与 `map` 一致：插入不失效，删除仅使被删节点迭代器失效。

## 核心概念、底层结构与声明

- **头文件**：`#include <map>`（与 `map` 共用头文件，没有 `<multimap>`）。
- **元素形态**：`multimap<T1, T2> mp;` 中的每个元素均为 `pair<const T1, T2>`，概念上对应：

```cpp
struct {
    T1 first;   // 关键字（排序与查找依据）
    T2 second;  // 对应的值
};
```

- **默认排序规则**：按 `a.first < b.first` 为 `true` 时 `a` 排在 `b` 前面（即 `std::less<T1>` 升序）；同一关键字的多个元素在 C++11 起保证按插入顺序保持相对位置。
- **使用 `typedef` 简化类型别名**（源码技巧）：

```cpp
typedef multimap<int, StudentInfo> MAP_STD; // 此后 MAP_STD 等价于 multimap<int, StudentInfo>
// 同理：typedef int* PINT; 则 PINT p; 等价于 int* p;
// 现代 C++ 亦推荐使用：using MAP_STD = multimap<int, StudentInfo>;
```

## 常用接口与时间复杂度速查

| 成员函数 | 说明 | 时间复杂度 |
| --- | --- | --- |
| `mp.insert(make_pair(k, v))` | 插入键值对，总是成功，返回指向新元素的 `iterator` | $O(\log n)$ |
| `mp.emplace(k, v)` | 原地构造并插入键值对，避免额外构造 `pair` | $O(\log n)$ |
| `mp.find(key)` | 返回任意一个（通常是首个）键等于 `key` 的迭代器，未找到返回 `end()` | $O(\log n)$ |
| `mp.count(key)` | 返回键等于 `key` 的元素个数 | $O(\log n + k)$ |
| `mp.lower_bound(key)` | 返回首个键值 $\ge \text{key}$ 的元素迭代器 | $O(\log n)$ |
| `mp.upper_bound(key)` | 返回首个键值 $> \text{key}$ 的元素迭代器 | $O(\log n)$ |
| `mp.equal_range(key)` | 一次返回 `{lower_bound(key), upper_bound(key)}` 迭代器对，覆盖所有键为 `key` 的元素 | $O(\log n)$ |
| `mp.erase(key)` | ==删除所有键等于 `key` 的元素==，返回删除的元素个数 | $O(\log n + k)$ |
| `mp.erase(it)` | ==仅删除迭代器 `it` 指向的单个元素==，返回下一个元素的迭代器 | 均摊 $O(1)$ |

## 典型实战：按分数段查询最高学号学生

源码演示了经典的动态插入与前驱查询问题（支持 `A name id score` 添加记录、`Q score` 查询严格低于 `score` 的最高分学生中 `id` 最大者）：

1. **插入记录**：使用 `mp.insert(make_pair(st.score, st.info))`，以分数为 `first` 自动升序归档，允许多个学生同分。
2. **定位前驱最高分**：调用 `auto p = mp.lower_bound(score);` 得到第一个分数 $\ge \text{score}$ 的位置：
   - 若 `p == mp.begin()`，说明不存在比查询分数更低的学生，直接输出 `"Nobody"`。
   - 否则执行 `p--`，此时 `p->first` 即为严格小于查询分数的**最高分**。
3. **扫描所有同分学生求最大 `id`**：由于同分学生可能有多人，从当前 `p` 向前（`p--`）遍历所有 `p->first == score` 的节点并维护 `maxID` 与 `maxp`。

```cpp
// 核心边界处理：当回退到 mp.begin() 时循环提前结束，需补检一次首元素
for (; p != mp.begin() && p->first == score; p--) {
    if (p->second.id > maxID) {
        maxp = p;
        maxID = p->second.id;
    }
}
if (p->first == score) { // 防止遗漏位于 mp.begin() 的同分学生
    if (p->second.id > maxID) {
        maxp = p;
        maxID = p->second.id;
    }
}
```

> [!tip] 用 `equal_range` 简化同键遍历
> 若已确定目标分数 `targetScore`，也可以直接用 `equal_range` 获取左闭右开区间，天然避免 `begin()` 边界特判：
> ```cpp
> auto [lo, hi] = mp.equal_range(targetScore);
> for (auto it = lo; it != hi; ++it) { /* 遍历所有同分学生 */ }
> ```

## 常见易错点与迭代器失效规则

> [!warning] `multimap` 高频踩坑点
> 1. **不能使用 `mp[key]`**：因为一个键可对应多个值，下标语义不明确，编译直接报错；必须使用 `insert()` / `emplace()`。
> 2. **区分 `erase(key)` 与 `erase(it)`**：若只想删除重复键中的**某一条记录**，必须先通过 `find` 定位迭代器再调用 `mp.erase(it)`；直接调用 `mp.erase(key)` 会把所有同键元素一次性全部清空！
> 3. **双向迭代器不可做减法或越过 `begin()` 递减**：对 `mp.begin()` 执行 `p--` 属于未定义行为（UB），因此源码中必须先判断 `if (p != mp.begin())` 再 `p--`。

## 完整源码

```cpp
/*
multimap容器里的元素,都是pair形式的
    multimap<T1,T2> mp;
则mp里的元素都是如下类型:
struct {
    T1 first;//关键字
    T2 second;//值
};
multimap中的元素按照first排序,并可以按first进行查找
缺省的排序规则是"a.first<b.first"为true,则a排在b前面
*/
#include <iostream>
#include <map>//使用multimap和map需要包含此头文件
#include <cstring>
using namespace std;
struct StudentInfo {
    int id;
    char name [20];
};
struct Student {
    int score;
    StudentInfo info;
};
typedef multimap<int,StudentInfo> MAP_STD;
// 此后MAP_STD等价于multimap<int, StudentInfo>
// typedef int*PINT;
// 则此后PINT等价于int*.即PINT p;等价于 int*p;
int main (){
    MAP_STD mp;
    Student st;
    char cmd[20];
    while(cin>>cmd){
        if(cmd[0]=='A'){
            cin>>st.info.name>>st.info.id>>st.score;
            mp.insert(make_pair(st.score,st.info));
        } //make_pair生成一个pair<int,StudentInfo>变量
          //其first等于st.score,second等于st.info
        else if(cmd[0]=='Q'){
            int score;
            cin>>score;
            MAP_STD::iterator p=mp.lower_bound(score);
            if (p!=mp.begin()){
                p--;
                score=p->first;//比要查询分数低的最高分
                MAP_STD::iterator maxp=p;
                int maxID=p->second.id;
                for(;p!=mp.begin()&&p->first==score;p--){//遍历所有成绩和score相等的学生
                    if (p->second.id>maxID){
                        maxp=p;
                        maxID=p->second.id;
                    }
                }
                if(p->first==score){//如果上面循环是因为p==mp.begin()而终止,则p指向的元素还要处理
                    if (p->second.id>maxID){
                        maxp=p;
                        maxID=p->second.id;
                    }
                }
                cout<<maxp->second.name<<" "<<maxp->second.id<<" "<<maxp->first<<endl;
            }
            //lower_bound的结果就是begin,说明没人分数比查询分数低
            else cout<<"Nobody"<<endl;
        }
    }
    return 0;
}
```
