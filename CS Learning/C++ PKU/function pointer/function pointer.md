---
title: function pointer — 函数指针与 qsort
date: '2026-09-11'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: 北大 C++
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/北大_Cpp
aliases:
  - function pointer
  - 函数指针
  - qsort
  - 函数指针与 qsort
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# function pointer — 函数指针与 qsort

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C++ PKU/北大C++导航|北大 C++ 导航]]
> 上一篇：[[CS Learning/C++ PKU/freopen/freopen|freopen — 输入输出重定向]] · 下一篇：[[CS Learning/C++ PKU/Loop statesments/Loop statesments|Loop statesments — 循环与范围 for]]
> 源码：[[CS Learning/C++ PKU/function pointer/function pointer.cpp|查看源码]]

> [!abstract] 本节概览
> 本节介绍**函数指针（Function Pointer）**的定义与调用方式，并重点拆解 C 标准库通用快速排序函数 `qsort` 如何借助 `void*` 与**比较器回调函数指针**实现对任意类型数组按自定义规则排序，同时对比 C++ 现代替代方案 `std::sort`。

---

## 1. 函数指针的定义与调用

函数名在表达式中代表函数的入口地址，可以用**函数指针**保存该地址并在运行时动态调用目标函数。

### 基本定义形式

```cpp
返回类型 (*指针变量名)(参数类型1, 参数类型2, ...);
```

- 示例：`int (*pf)(int, char);` 表示指向“接收 `(int, char)` 并返回 `int`”的函数指针。
- **括号 `(*pf)` 不可省略**：若漏写括号变成 `int *pf(int, char);`，优先级会使它成为“返回 `int*` 指针的普通函数声明”。

### 赋值与调用示例（来自源码注释）

```cpp
void (*pf)(int, int);
int x = 4, y = 5;
pf = PrintMin; // 将函数入口地址赋给函数指针（也可写 &PrintMin）
pf(x, y);      // 通过函数指针调用所指向的函数（等价于 (*pf)(x, y)）
```

---

## 2. 泛型排序库函数 `qsort`

C 标准库提供的 `qsort`（标准头文件 `<cstdlib>` / `<stdlib.h>`）通过 **`void*` 抹平元素类型** + **函数指针回调定制比较规则**，实现对任意数据类型数组的排序。

```cpp
// 课程教学原型（标准库中 nelem 与 width 类型为 size_t）
void qsort(void* base, int nelem, unsigned int width,
           int (*pfCompare)(const void*, const void*));
```

### 四个参数与排序所需四要素的一一对应

| 参数 | 对应排序要素 | 说明 |
| --- | --- | --- |
| `base` | **数组起始地址** | `void*` 类型，可接收任意类型数组首地址 |
| `nelem`（`num`） | **数组元素个数** | 待排序元素总数 |
| `width`（`size`） | **每个元素占用的字节数** | 通常使用 `sizeof(元素类型)`，供底层按字节跨步定位元素 |
| `pfCompare` | **先后顺序比较规则** | 由程序员编写的比较函数地址，决定谁排在前面 |

### 比较函数 `pfCompare` 的返回值契约

`qsort` 在内部需要比较两个元素 `*elem1` 与 `*elem2` 时，会回调 `pfCompare(elem1, elem2)` 并依据返回值符号决策顺序：

| `pfCompare(elem1, elem2)` 返回值 | 排序语义 |
| :---: | --- |
| **负整数（`< 0`）** | 前者 `elem1` 应该排在后者 `elem2` **前面** |
| **零（`== 0`）** | 前者与后者顺序等价，哪个在前都行 |
| **正整数（`> 0`）** | 前者 `elem1` 应该排在后者 `elem2` **后面** |

---

## 3. 源码实战拆解：按个位数升序排序

源码实现了一个按**无符号整数个位数从小到大**排序的比较函数 `MyCompare`：

```cpp
int MyCompare(const void* elem1, const void* elem2) {
    unsigned int *p1, *p2;
    p1 = (unsigned int*)elem1; // *elem1 非法：void* 不能直接解引用
    p2 = (unsigned int*)elem2; // *elem2 非法：必须先强转为具体类型指针
    return (*p1 % 10) - (*p2 % 10); // 个位数小者差值为负 -> 排在前面
}
```

- **为何必须强转？** 形参是 `const void*`，在 C++ 中不能对 `void*` 执行解引用 `*elem1`（参见 [[CS Learning/C++ PKU/pointer/pointer|pointer — void 指针与内存操作]]），必须先转换为指向实际元素类型的指针后再取值。
- **执行结果追踪**：
  - 原数组：`an[5] = {8, 123, 11, 10, 4}`
  - 对应个位数：`{8, 3, 1, 0, 4}`
  - 按个位数升序排列后：`{10, 11, 123, 4, 8}`
  - 源码循环 `cout << an[i];`（未加空格分隔）最终输出：`101112348`。

---

## 4. 工程细节与 C++ 进阶对比

> [!warning] 编写 `qsort` 比较器的三项注意事项
> 1. **避免直接相减引发溢出**：本例中 `*p1 % 10` 取值范围为 $0 \sim 9$，做减法绝对安全；但若比较一般 `int`（如 `INT_MIN` 与正数相减）或 `unsigned int`（无符号下溢回绕），直接写 `return *p1 - *p2;` 属于经典 bug！通用安全写法应显式比较大小：
>    ```cpp
>    if (*p1 < *p2) return -1;
>    if (*p1 > *p2) return 1;
>    return 0;
>    ```
> 2. **保留 `const` 修饰与显式包含头文件**：更规范的指针强转应写 `const unsigned int* p1 = static_cast<const unsigned int*>(elem1);`；且 `qsort` 标准定义于 `<cstdlib>`、`printf` 定义于 `<cstdio>`，规范代码应显式 `#include` 而非依赖 `<iostream>` 的间接包含。
> 3. **C++ 推荐优先使用 `std::sort`**：`qsort` 仅适用于平凡可复制（POD）类型且通过函数指针调用存在间接调用开销；在 C++ 中更推荐使用 `<algorithm>` 中的 [[CS Learning/C++ STL/Algorithms/sort()/sort()|std::sort]]——模板类型安全、支持内联优化，且比较器只需返回 `bool`（满足严格弱序 `<` 即可），还能直接配合 Lambda 表达式使用。

---

## 完整源码

```cpp
/*
函数指针定义形式:类型名(*指针变量名)(参数类型1,参数类型2)
如 int (*pf)(int,char)
快速排序库函数
void qsort(void* base,int nelem,unsigned int width,int(*pfCompare)(const void*,const void*))
使用了函数指针使之可以对任意类型的数组进行排序
对数组排排序,需要知道：(4个参数一一对应)
1)数组起始地址 2)数组元素个数 3)每个元素大小 4)元素谁在前谁在后的规则
pfCompare由程序员自己编写,规则:
1)如果函数参数的前者应该排在后者前面，函数返回值为负整数
2)如果函数参数的前者与后者哪个排在前面都行，函数返回值为0
3)如果函数参数的前者应该排在后者后面，函数返回值为正整数
*/
#include <iostream>
using namespace std;
void PrintMin(int a,int b){
    if (a<b){
        printf("%d",a);
    }else {
        printf("%d",b);
    }
}
int MyCompare(const void* elem1,const void* elem2){
    unsigned int *p1,*p2;
    p1=(unsigned int*)elem1;//"*elem1"非法
    p2=(unsigned int*)elem2;//"*elem2"非法
    return (*p1%10)-(*p2%10);//返回规则:谁的个位数小谁排在前面,故结果为负整数
}
#define NUM 5
int main(){
    /*void(*pf)(int,int);
    int x=4,y=5;
    pf=PrintMin;//用pf调用所指向的函数
    pf(x,y);*/
    unsigned int an[NUM]={8,123,11,10,4};
    qsort(an,NUM,sizeof(unsigned int),MyCompare);
    for(int i=0;i<NUM;i++){
        cout<<an[i];
    }
    return 0;
}
```
