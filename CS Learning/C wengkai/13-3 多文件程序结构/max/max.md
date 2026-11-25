---
title: max — 多文件程序的 max 函数
date: '2026-09-12'
date_source: 文件修改日期
subject: 计算机基础
note_type: 程序笔记
course: 翁恺 C 语言
tags:
  - 领域/计算机基础
  - 类型/程序笔记
  - 课程/翁恺_C_语言
aliases:
  - 13-3 max
  - 多文件程序的 max 函数
cssclasses:
  - learning-note
  - subject-cs
  - learning-code
---

# max — 多文件程序的 max 函数

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/C wengkai/翁恺C语言导航|翁恺 C 语言导航]]
> 上一篇：[[CS Learning/C wengkai/13-3 多文件程序结构/main/main|main — 多文件程序的入口]] · 下一篇：[[CS Learning/C wengkai/14-1 格式化输入输出与文件操作/14-1-learning format|14-1-learning format — 格式化输入输出与文件操作]]
> 源码：[[CS Learning/C wengkai/13-3 多文件程序结构/max/max.c|查看源码]]

> [!abstract] 本节概览
> 多文件程序示例的独立实现模块 `max.c`：用三目条件运算符 `a > b ? a : b` 实现两整数取较大值函数 `max`，不依赖 `main()` 入口，可被 [[CS Learning/C wengkai/13-3 多文件程序结构/main/main|main.c]] 或其他编译单元链接复用。

---

## 核心知识点

- **模块化职责**：该编译单元只负责提供 `max` 的实现，不包含 `main` 函数，也不能单独链接生成可执行文件（单独 `gcc -c max.c` 可生成目标文件 `max.o`）。
- **静态函数隐藏**：如果某个辅助函数仅希望在本 `.c` 文件内部可见、不暴露给外部链接单元，应加上 `static` 关键字修饰（内部链接性）。

---

## 多文件编译

配套入口文件：[[CS Learning/C wengkai/13-3 多文件程序结构/main/main.c|main.c]]（说明见 [[CS Learning/C wengkai/13-3 多文件程序结构/main/main|main — 多文件程序的入口]]）。在上一级 `13-3 多文件程序结构` 目录运行：

```powershell
gcc "main/main.c" "max/max.c" -o example.exe
```

## 完整源码

```c
int max(int a,int b){
    return a>b?a:b;
}
```
