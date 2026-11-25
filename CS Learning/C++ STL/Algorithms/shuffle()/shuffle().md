---
title: shuffle() — 随机打乱
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: C++ STL
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/Cpp_STL
aliases:
  - shuffle
  - shuffle()
  - 洗牌
  - 随机打乱
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# `shuffle()` — 随机打乱

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ STL/C++ STL导航|C++ STL 导航]]
> 上一篇：[[CS Learning/C++ STL/Algorithms/reverse()/reverse()|reverse() — 反转序列]] · 下一篇：[[CS Learning/C++ STL/Algorithms/sort()/sort()|sort() — 排序]]
> 源码：[[CS Learning/C++ STL/Algorithms/shuffle()/shuffle().cpp|查看源码]]

> [!abstract] 本节概览
> `std::shuffle()` 定义在头文件 `#include <algorithm>` 中（需配合 `#include <random>` 提供随机数引擎），使用 **Fisher–Yates 洗牌算法**将区间 `[first, last)` 内的元素==等概率随机打乱==。时间复杂度为 $O(n)$，是 C++11 起替代已移除的 `std::random_shuffle()` 的标准方案。

## 核心语法与参数说明

```cpp
#include <algorithm>
#include <random>

void shuffle(RandomIt first, RandomIt last, URBG&& g);
```

| 参数 | 含义与要求 |
| :--- | :--- |
| `first`, `last` | **随机访问迭代器（RandomAccessIterator）**，指定待打乱的左闭右开区间 `[first, last)` |
| `g` | 均匀随机位生成器对象（如 `std::mt19937`、`std::default_random_engine`，详见 [[CS Learning/C++ STL/Algorithms/Random/Random\|Random — 随机数]]） |
| **复杂度** | 时间 $O(n)$，原地操作额外空间 $O(1)$ |

## 典型用法与最佳实践

推荐在循环外部初始化一次 `std::mt19937` 引擎，并在需要洗牌时复用该引擎：

```cpp
#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::random_device rd;
    std::mt19937 gen(rd());  // 引擎初始化一次即可复用

    for (int i = 0; i < 5; ++i) {
        std::shuffle(vec.begin(), vec.end(), gen);
        for (int x : vec) std::cout << x << ' ';
        std::cout << '\n';
    }
}
```

## 常见易错点与注意事项

> [!note] 对原注释迭代器要求的勘误
> 文末原注释写了“双向或随机访问迭代器”，但 C++ 标准明确要求 `std::shuffle()` 的迭代器必须是==随机访问迭代器==（如 `vector`、`deque`、`array`、`string`、普通数组）。因此 `std::list`（仅支持双向迭代器）**不能**直接调用 `std::shuffle()`。

> [!warning] 不要使用已废弃/移除的 `std::random_shuffle()`
> 旧标准中的 `std::random_shuffle()` 依赖质量低且范围受限的 `std::rand()`，已在 **C++14 弃用、C++17 彻底移除**。现代 C++ 应始终使用 `std::shuffle()` 搭配 `std::mt19937`。

> [!tip] 避免在高频循环内重复构造 `random_device` 与引擎
> 文末示例在 `for` 循环内部每次重新创建 `random_device rd` 并播种引擎；在实战中把引擎提到循环外复用，不仅开销更小，还能避免部分平台上短时间内种子重复的问题。

## 完整源码

```cpp
/*
shuffle 是用于将指定范围内的元素随机打乱顺序(即洗牌)。
头文件<algorithm> 和 <random>
语法
shuffle(RandomIt first,RandomIt last,URBG&& g);
first / last：双向或随机访问迭代器，指定要打乱的区间 [first, last)。
g：随机数引擎对象(如 std::default_random_engine)
*/
#include <iostream>
#include <random>
#include <algorithm>
#include <vector>
using namespace std;
template <typename T>
void PrintVector(const vector<T>& vector){
    for_each(vector.begin(),vector.end(),[](T x) {
        cout<<x<<" ";
        });
    cout<<endl;
}
int main(){
    for (int i=0; i<5;i++){
        vector<int> vec={1,2,3,4,5,6,7,8,9,10};
        random_device rd;
        shuffle(vec.begin(),vec.end(),default_random_engine(rd()));
        PrintVector(vec);
    }
    return 0;
}
```
