# Learning

个人学习资料、课程笔记、代码练习与算法题归档。

本仓库以 `D:\Learning` 为本地归档根目录，持续收纳人工智能、计算机基础课程和算法练习。本页是总导航，各课程 README 再提供章节、笔记与源码入口，可在 GitHub 或 Obsidian 中阅读。

仓库地址：[Noahxie83/Learning](https://github.com/Noahxie83/Learning)

## 内容导航

| 模块 | 范围 | 本地导航 |
| --- | --- | --- |
| AI Learning | 人工智能入门，以及后续机器学习、强化学习等方向 | [模块 README](./AI%20learning/README.md) |
| CS Learning | C/C++、数据结构与算法、Python、计算机工具课程 | [模块 README](./CS%20Learning/README.md) |
| Practice | 洛谷算法题练习与复盘 | [模块 README](./Practice/README.md) |

## 课程与学习资料

### AI Learning：人工智能学习主线

AI Learning 不限于 AI for Everyone；这门课是当前已经归档的起点。机器学习目前进入学习阶段，数学课程作为按需基础材料，强化学习仍是后续方向；课程选择、笔记和代码会随着学习逐步补充。

| 课程或方向 | 当前归档情况 | 本地导航 |
| --- | --- | --- |
| [AI for Everyone](https://www.deeplearning.ai/courses/ai-for-everyone) | 已有 Week 1–4 的课件与测验记录，覆盖 AI 概念、AI 项目、企业中的 AI、AI 与社会 | [课程 README](./AI%20learning/AI%20for%20everyone/README.md) |
| [Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction/) | 已建立课程资料目录，当前进入机器学习学习阶段；个人学习笔记来源见课程 README | [课程 README](./AI%20learning/Machine%20Learning%20Specialization%20Coursera/README.md) |
| 数学基础（按需） | 已归档数学课程资料，作为机器学习阶段的按需补充；尚未计作已学习课程 | [课程 README](./AI%20learning/Mathematics%20for%20Machine%20Learning%20and%20Data%20Science%20Specialization/README.md) |
| 强化学习 | 后续规划，具体课程网址待选定后补充；尚未建立课程资料目录 | [方向说明](./AI%20learning/README.md#强化学习) |

### CS Learning：计算机基础与工具

课程名称链接到课程网站，“本地导航”进入仓库中的学习资料。保留已选课程的具体学期链接；中国大学 MOOC 的学习页面可能需要登录或选课。

| 课程或专题网址 | 内容与当前归档 | 本地导航 |
| --- | --- | --- |
| [C wengkai](https://www.icourse163.org/learn/ZJU-9001?tid=9001#/learn/announce) | 翁恺 C 语言课程；47 个章节目录采用“章号-节号 中文标题”，保留源码及配套 Markdown | [课程 README](./CS%20Learning/C%20wengkai/README.md) |
| [C++ PKU](https://www.icourse163.org/learn/PKU-1001553023?tid=1474162490#/learn/announce) | PKU 程序设计与算法相关 C++ 学习；9 个源码与笔记主题 | [课程 README](./CS%20Learning/C++%20PKU/README.md) |
| C++ STL · [标准库参考](https://en.cppreference.com/cpp/standard_library) | 容器、迭代器、算法和适配器；独立学习专题，参考文档不是指定课程官网 | [专题 README](./CS%20Learning/C++%20STL/README.md) |
| [ZJU DSA](https://www.icourse163.org/learn/ZJU-93001?tid=1487509453#/learn/announce) | 浙江大学数据结构课程；已建立分区，课程笔记待归档 | [课程 README](./CS%20Learning/Data%20Structures%20and%20Algorithms/ZJU%20DSA/README.md) |
| [THU DSA](https://dsa.cs.tsinghua.edu.cn/~deng/ds/dsacpp/) | 清华大学数据结构（C++ 语言版）学习；目前已有绪论、向量笔记和示例 | [课程 README](./CS%20Learning/Data%20Structures%20and%20Algorithms/THU%20Advanced%20DSA/README.md) |
| [Python MIT6.100L](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/material-by-lecture/) | MIT 6.100L Python 课堂代码、练习、Problem Set 与资源 | [课程 README](./CS%20Learning/Python%20MIT6.100L/README.md) |
| [MIT Missing Semester](https://missing.csail.mit.edu/) | 已选择性学习 L1–3、L5、L7；L4、L6–L9 资料已归档但尚未学习 | [课程 README](./CS%20Learning/MIT%20missing%20semester/README.md) |

数据结构与算法的两个课程分开归档，共用 [DSA 总导航](./CS%20Learning/Data%20Structures%20and%20Algorithms/README.md)。目录 `THU Advanced DSA` 保留现有命名，不代表本仓库已经覆盖清华课程的全部高级内容。

### Practice：算法题练习

主要归档洛谷题目，按语言基础、数组、字符串、递归和动态规划等类别组织。包含 C 语言向 C++ 过渡的练习；题号与说明见 [Practice README](./Practice/README.md) 和 [Luogu 分类导航](./Practice/Luogu/README.md)。

## 仓库结构

```text
Learning/
├── AI learning/
│   ├── AI for everyone/
│   │   ├── Week 1/ ... Week 4/
│   │   └── README.md
│   ├── Machine Learning Specialization Coursera/
│   │   ├── C1 - Supervised Machine Learning - Regression and Classification/
│   │   ├── C2 - Advanced Learning Algorithms/
│   │   ├── C3 - Unsupervised Learning, Recommenders, Reinforcement Learning/
│   │   ├── resources/
│   │   ├── 黄博士机器学习个人笔记完整版v5.52.pdf
│   │   └── README.md
│   ├── Mathematics for Machine Learning and Data Science Specialization/
│   │   ├── Course-1/ ... Course-3/
│   │   └── README.md
│   └── README.md
├── CS Learning/
│   ├── C wengkai/
│   ├── C++ PKU/
│   ├── C++ STL/
│   ├── Data Structures and Algorithms/
│   │   ├── ZJU DSA/
│   │   ├── THU Advanced DSA/
│   │   │   ├── 1. Itroduction/
│   │   │   └── 2. Vector/
│   │   └── README.md
│   ├── Python MIT6.100L/
│   ├── MIT missing semester/
│   ├── Obsidian-Plugins-Sync.md
│   └── README.md
├── Practice/
│   ├── Luogu/
│   └── README.md
├── github-ai-cs-weekly-top3.md
└── README.md
```

树中只列主要学习入口。机器学习已有课程资料目录，数学课程作为按需基础材料归档；强化学习仍是后续规划方向。现有 `1. Itroduction` 沿用原目录拼写。

## 其他资料

- [每周 GitHub AI/CS 项目 Top 3](./github-ai-cs-weekly-top3.md)：项目推荐与后续探索记录，不等同于已经完成的项目。
- [Obsidian 插件同步清单](./CS%20Learning/Obsidian-Plugins-Sync.md)：记录本机插件与迁移注意事项，使用前核对记录日期；实际插件配置不随 Git 上传。

## Obsidian 与 Git 使用

可以将 `D:\Learning` 整体作为 Obsidian 仓库打开，通过本页进入全部学习材料。若继续使用现有的 AI、CS 分库，也直接打开对应文件夹，不额外复制笔记；Git 同步统一在 Learning 根目录进行。

两台电脑交替使用时，先保存并检查本机修改；工作区干净后拉取，再开始学习：

```powershell
Set-Location 'D:\Learning'
git status
git pull --ff-only origin main
```

结束学习后确认变更中没有敏感信息、意外删除或编译产物，再分步提交与推送：

```powershell
git add -A
git diff --cached --stat
git commit -m "更新学习资料"
git push origin main
```

任一步出错先停止处理，不强制推送。没有变化时无需创建空提交。本机已有每日 GitHub 同步任务；它不是实时双向同步服务，也不会随克隆自动安装到另一台电脑。README 每日自动维护仍待另行配置，不应假定已经启用。

## 归档约定

- 课程学习持续进行：已有文件不等于学完课程，规划方向不等于已有学习成果。
- 源码、笔记、课件和必要测试资源可以归档；编辑器、AI 助手配置、虚拟环境及编译产物留在本地。
- 同目录的源码与 Markdown 不会自动双向同步；修改源码中的学习记录后，需要相应维护笔记。
- 新增课程、移动目录或重命名后，同步维护本页和对应模块 README；链接路径大小写与磁盘目录保持一致。

最后更新：2026-09-13
