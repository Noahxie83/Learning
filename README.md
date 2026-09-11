# Learning

个人学习资料、课程笔记、代码练习与算法题归档。

这个仓库以 `D:\Learning` 为根目录，统一收纳 AI、计算机基础课程和算法练习。根目录 README 作为总入口，方便在 GitHub 或 Obsidian 中快速定位不同学习模块。

仓库地址：[Noahxie83/Learning](https://github.com/Noahxie83/Learning)

## 内容导航

| 模块 | 说明 | README |
| --- | --- | --- |
| [AI_learning](./AI_learning/) | 人工智能入门课程笔记与课程资料 | [模块说明](./AI_learning/README.md) |
| [CS Learning](./CS%20Learning/) | C/C++、数据结构、算法和 Python 课程学习资料 | [模块说明](./CS%20Learning/README.md) |
| [Practice](./Practice/) | 洛谷等算法题练习与代码归档 | [模块说明](./Practice/README.md) |

## 仓库结构

```text
Learning/
├── AI_learning/                         # AI 入门课程与笔记
│   ├── AI for everyone/                 # AI for Everyone 课程
│   │   ├── Week 1/                      # 第 1 周资料、测验与图片
│   │   ├── Week 2/                      # 第 2 周资料与测验
│   │   ├── Week 3/                      # 第 3 周资料、测验与图片
│   │   └── Week 4/                      # 第 4 周资料与测验
│   └── README.md
│
├── CS Learning/                         # 计算机基础课程学习
│   ├── C wengkai/                       # 翁恺课程 C 语言练习
│   ├── C++ PKU/                         # PKU C++/程序设计课程代码
│   ├── C++ STL/                         # C++ STL 学习与示例
│   ├── Data Structures and Algorithms/  # 数据结构与算法笔记、代码
│   ├── Python MIT6.100L/                # MIT 6.100L Python 课程
│   ├── output/                          # 编译或运行产生的输出文件
│   └── README.md
│
├── Practice/                            # 算法题练习
│   ├── luogu/                           # 洛谷题目
│   └── README.md
│
└── README.md                            # 总目录与仓库说明
```

## 子模块介绍

### 1. AI_learning：人工智能入门

主要记录 **AI for Everyone** 课程的学习资料，目前按课程周次整理：

- `Week 1`：人工智能基础概念、课程资料和测验。
- `Week 2`：人工智能项目与数据相关内容。
- `Week 3`：机器学习、神经网络等内容及配套资料。
- `Week 4`：课程后续主题、资料和测验。

该模块以 Markdown 笔记、PDF 课程资料、测验文件和图片为主，适合在 Obsidian 中阅读和补充学习记录。

入口：[AI_learning/README.md](./AI_learning/README.md)

### 2. CS Learning：计算机基础课程

这是仓库中内容最集中的课程学习模块，覆盖 C、C++、数据结构、算法和 Python：

| 子目录 | 内容 | README |
| --- | --- | --- |
| `C wengkai` | 翁恺课程相关 C 语言示例代码与练习 | [进入](./CS%20Learning/C%20wengkai/README.md) |
| `C++ PKU` | 程序设计与算法课程相关 C++ 代码 | [进入](./CS%20Learning/C++%20PKU/README.md) |
| `C++ STL` | C++ 标准模板库学习与示例 | [进入](./CS%20Learning/C++%20STL/README.md) |
| `Data Structures and Algorithms` | 数据结构与算法笔记、代码和图片 | [进入](./CS%20Learning/Data%20Structures%20and%20Algorithms/README.md) |
| `Python MIT6.100L` | MIT 6.100L Python 课程与练习 | [进入](./CS%20Learning/Python%20MIT6.100L/README.md) |

详细入口：[CS Learning/README.md](./CS%20Learning/README.md)

### 3. Practice：算法题练习

主要归档洛谷算法题，代码以 C/C++ 为主，按知识点分为语言基础、数组、字符串、递归和动态规划等类别。

入口：[Practice/README.md](./Practice/README.md)

## Obsidian 使用方式

建议将以下两个目录分别作为 Obsidian Vault 打开：

- `D:\Learning\AI_learning`
- `D:\Learning\CS Learning`

`Practice` 更偏向代码练习目录，可以在 VS Code 或其他代码编辑器中使用。

## Git 同步

根目录 `D:\Learning` 是 GitHub 同步入口。执行 Git 操作时，建议在根目录进行：

```powershell
Set-Location D:\Learning
git status
git add -A
git commit -m "更新学习资料"
git push origin main
```

仓库已配置每日更新任务，会检查根目录中的变更并同步到 GitHub；当天没有文件变化时不会创建空提交。

## 说明

- 这是一个持续更新中的个人学习仓库，内容会随着课程进度不断补充和整理。
- 课程资料、代码和笔记按学习过程归档，不保证所有代码都已经重构或达到生产级质量。
- 根 README 主要承担导航作用；进入具体模块后，应优先阅读对应模块自己的 README。

最后更新：2026-09-11
