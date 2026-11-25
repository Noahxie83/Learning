---
title: L25 数据可视化与绘图（Plotting）
date: '2026-09-01'
date_source: 文件修改日期
subject: 计算机基础
note_type: 课程笔记
course: Python MIT 6.100L
tags:
  - 领域/计算机基础
  - 类型/课程笔记
  - 课程/Python_MIT_6_100L
  - 主题/数据可视化
  - 主题/Matplotlib
aliases:
  - Lecture 25 Plotting
  - L25 数据可视化与绘图
cssclasses:
  - learning-note
  - subject-cs
  - learning-study
---

# L25 数据可视化与绘图（Plotting）

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[CS Learning/Python MIT6.100L/MIT Python导航|MIT Python 导航]]
> 上一章：[[CS Learning/Python MIT6.100L/Lecture 24 Sorting Algorithms/L24 经典排序算法|L24 经典排序算法]] · 下一章：[[CS Learning/Python MIT6.100L/Lecture 26 List Access, Hashing, Simulations, and Wrap-Up/L26 列表访问、哈希、仿真与课程总结|L26 列表访问、哈希、仿真与课程总结]]

> [!abstract] 本讲核心概览
> 数据可视化不仅用于展示结果，更是**发现隐藏趋势、暴露异常模式、提出可验证计算假设**的探索工具。本讲以 Python 科学计算生态的核心绘图库 **`matplotlib.pyplot`** 为载体，系统梳理图形窗口管理、样式定制、子图布局、对数坐标与统计图表 API，并围绕 **美国历史人口**、**全球国家人口与本福特定律（Benford's Law）**、**美国 21 城 55 年逐日气温**三大真实数据集开展端到端的数据可视化分析。
>
> **配套源文件**：[[CS Learning/Python MIT6.100L/Lecture 25 Plotting/mit6_100l_f22_lec25.pdf|Lecture 25 讲义 PDF]] · [[CS Learning/Python MIT6.100L/Lecture 25 Plotting/mit6_100l_f22_lec25_code/lec25.py|课堂完整绘图代码 lec25.py]] · [[CS Learning/Python MIT6.100L/Lecture 25 Plotting/mit6_100l_f22_lec25_code/lec25_USPopulation.txt|美国人口数据]] · [[CS Learning/Python MIT6.100L/Lecture 25 Plotting/mit6_100l_f22_lec25_code/lec25_countryPops.txt|世界国家人口数据]] · [[CS Learning/Python MIT6.100L/Lecture 25 Plotting/mit6_100l_f22_lec25_code/lec25_temperatures.csv|美国城市气温数据 CSV]]

---

## 1. Matplotlib 核心机制与基础 API 速查

导入惯例：`import matplotlib.pyplot as plt`，并通过全局字典 `plt.rcParams` 统一配置画布大小、线宽、字号与刻度风格（见 [[CS Learning/Python MIT6.100L/Lecture 25 Plotting/mit6_100l_f22_lec25_code/lec25.py|lec25.py]] 顶部第 4–26 行）：

```python
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['lines.markersize'] = 10
plt.rcParams['figure.figsize'] = (15, 10)
```

### 1.1 折线图 `plot` vs 散点图 `scatter`：点序至关重要

- `plt.plot(xVals, yVals)` 要求两个序列等长，按**列表中的先后顺序**逐点连线；
- 如果横坐标序列未排序（例如课堂中乱序的 `testSamples = [0, 5, 3, 6, 15, 2, ...]`），`plt.plot` 会画出杂乱交叉的折线网；
- 若仅展示离散样本点而不连线，应使用 **`plt.scatter(xVals, yVals)`**（或只传 marker 不传线型）。

### 1.2 多画布管理与子图布局

| API | 作用与行为 | 典型用法 |
| --- | --- | --- |
| `plt.figure(name)` | 若名为 `name` 的画布不存在则新建；==若已存在则重新激活该画布继续叠加绘图== | `plt.figure('expo')` 先画 $1.5^i$，切到别的图后再 `plt.figure('expo')` 叠加 $1.6^i$ |
| `plt.subplot(r, c, idx)` | 将当前画布划分为 $r \times c$ 网格，选中第 `idx` 个子图（**从 1 开始编号**，按行优先） | `plt.subplot(2, 1, 1)`、`plt.subplot(2, 2, 3)` |
| `plt.title / xlabel / ylabel` | 设置标题与坐标轴说明 | `plt.title('Ave. Temperature in Boston')` |
| `plt.xlim(lo, hi)` / `plt.ylim(lo, hi)` | 手动固定横/纵坐标轴显示范围 | `plt.xlim(1, 12)`、`plt.ylim(0, 100)` |
| `plt.xticks(locs, labels)` | 自定义刻度位置与文字标签 | `plt.xticks(range(1, 13), ('Jan', ..., 'Dec'))` |
| `plt.grid()` | 切换网格线显示 | `plt.grid()` |
| `plt.legend(loc='best')` | 依据各曲线的 `label=` 参数自动寻找不遮挡数据的位置放置图例 | `plt.legend(loc='best', fontsize=20)` |
| `plt.semilogy()` | 将 **y 轴切换为对数刻度**（x 轴保持线性） | 观察指数增长率 |
| `plt.hist(data, bins=9)` | 自动分箱统计频数并绘制直方图 | 验证本福特定律首位数字分布 |
| `plt.bar(x, h, alpha=0.5)` | 按给定横坐标与高度绘制柱状图，`alpha` 控制透明度以便重叠对比 | 1961 vs 2015 气温天数分布叠加 |
| `plt.close()` / `plt.show()` | 关闭当前图窗 / 渲染并展示图形 | 脚本末尾调用 `plt.show()` |

### 1.3 样式控制：格式化简写字符串 vs 关键字参数

`plt.plot` 支持把 **标记（marker）+ 线型（linestyle）+ 颜色（color）** 拼成一个不限顺序的格式化字符串（如 `'.b-'`、`'or--'`、`'*g-.'`），也支持更清晰的关键字写法：

```python
# 格式化字符串写法（简短）
plt.plot(months, phoenix, 'or--', label='Phoenix')

# 关键字参数写法（更易读，且可控线宽、透明度）
plt.plot(months, phoenix, label='Phoenix', color='r', linestyle='--', marker='o', linewidth=4)
```

| 类别 | 常用选项速查 |
| --- | --- |
| **线型（linestyle）** | `'-'` 实线 · `'--'` 虚线 · `'-.'` 点划线 · `':'` 点线 |
| **颜色（color）** | `'b'` 蓝 · `'g'` 绿 · `'r'` 红 · `'c'` 青 · `'m'` 品红 · `'y'` 黄 · `'k'` 黑 · `'w'` 白 |
| **标记（marker）** | `'.'` 点 · `'o'` 圆圈 · `'v'` 下三角 · `'^'` 上三角 · `'*'` 星号 |

> [!warning] 数据可视化头号视觉陷阱：子图 Y 轴刻度不统一（Slides 38 & 68–70）
> Matplotlib 默认根据每张子图自身的数据范围自动缩放坐标轴。例如分别画波士顿（$0 \sim 80\,^\circ\text{F}$）、迈阿密（$40 \sim 90\,^\circ\text{F}$）和圣地亚哥（$50 \sim 90\,^\circ\text{F}$）时，**如果不手动统一设置 `plt.ylim(0, 100)`，读者会误以为三城温差幅度差不多**！做多组对比图时，务必显式对齐坐标轴范围。

---

## 2. 三大真实数据集探索实战

### 2.1 案例一：美国四百年人口增长与对数坐标系（`lec25_USPopulation.txt`）

- **数据读取**：`getUSPop()` 逐行过滤非数字/空格字符，拆分年份 `dates` 与人口 `pops`。
- **线性坐标 vs 半对数坐标（`plt.semilogy()`）**：
  - 在常规线性坐标下，早期（17–18 世纪）人口曲线几乎贴着横轴压成一条水平线，只能模糊看出南北战争（Civil War）与二战（WWII）时期的波动；
  - 切换到 **`plt.semilogy()`**（y 轴每格代表 $10\times$ 指数倍增）后，**指数函数 $P(t) = P_0 e^{rt}$ 会拉直成一条直线**：
    $$
    \log P(t) = \log P_0 + r \cdot t
    $$
    直线的**斜率直接反映相对增长率 $r$**！
  - ==视觉发现==：对数图清晰暴露出早期美国人口实际处于**比近代更陡峭的高速指数增长期**，且整体呈现三段斜率不同的增长阶段——这正是更换坐标系带来的洞察力。

### 2.2 案例二：全球国家人口与本福特定律（`lec25_countryPops.txt`）

1. `getCountryPops()` 按制表符 `\t` 切分，提取第 3 列并清洗千分位逗号转为整数；按国家人口排名绘制半对数图，呈现典型的长尾/幂律衰减形态。
2. **奇特的探索问题**：提取每个国家人口数字的**最高位首位数字**（`int(str(p)[0])`，取值 $1 \sim 9$），用 `plt.hist(firstDigits, bins=9)` 绘制频数分布——你会惊讶地发现首位数字**绝不是均匀分布**，而是 `1` 出现得最多、`9` 出现得最少！

> [!important] 本福特定律（Benford's Law）
> 在跨越多数量级的真实自然与社会数据集（国家人口、股价、社交媒体粉丝数、商品价格、建筑高度、纳税额等）中，首位非零数字 $d \in \{1, 2, \dots, 9\}$ 出现的理论概率满足对数分布：
> $$
> P(d) = \log_{10}\!\left(1 + \frac{1}{d}\right)
> $$
> 例如 $P(1) = \log_{10}(2) \approx 30.1\%$，$P(2) \approx 17.6\%$，而 $P(9) \approx 4.6\%$。该定律甚至被广泛用于财务审计与数据造假检测（人为编造的数字往往过于均匀）。

### 2.3 案例三：美国 21 城 55 年逐日气温深度探索（`lec25_temperatures.csv`）

该 CSV 包含 21 座美国城市 1961–2015 年共 55 年的日均气温（摄氏度，经 `CtoF(c)` 转为华氏度），课堂代码循序渐进地展示了**多视角探索性数据分析（EDA）**的完整范式：

```mermaid
flowchart LR
    A["视角 1：21 城 55 年总均温<br/>plt.scatter（城市两字母缩写刻度）"] --> B["视角 2：4 城逐年均温折线<br/>plt.plot 多曲线 + legend"]
    B --> C["视角 3：年均/最高/最低温波动带<br/>统一 plt.ylim(0, 100) 暴露气候差异"]
    C --> D["视角 4：某年各温度出现天数分布<br/>100 桶计数数组 + plt.bar（1961 vs 2015）"]
```

- **气候形态对比洞察（视角 3）**：统一 `plt.ylim(0, 100)` 后一眼可见：波士顿全年温差跨度极大；圣地亚哥曲线窄而平稳；迈阿密的年均温线明显更贴近最高温线而非最低温线（分布左偏，说明大部分日子偏热、偶有短暂降温）。
- **分布形态与跨年代对比（视角 4）**：
  - `getDayDistributionForCity(city, year)` 初始化长度为 100 的频数桶 `d = [0] * 100`，对每日气温四舍五入后计数 `d[round(t)] += 1`，并用 `plt.bar` 绘图（引出后续统计学问题：圣地亚哥的分布接近高斯/正态钟形曲线，而波士顿更接近平坦/双峰分布）；
  - 对比 1961 与 2015 两年分布时，演示了两种并列策略：**半透明叠加柱状图（`alpha=0.5`）** 与 **上下双子图（统一 `plt.ylim(0, 20)`）**。

---

## 3. 自测与复习思考

> [!question]- 自测 1：如果在半对数图（`plt.semilogy()`）上观察到一条向上倾斜的直线，说明原始数据正在以什么规律增长？如果直线变平缓了呢？
> 在半对数图上呈直线，说明原始数据正在**指数增长**（$y = a \cdot b^x \implies \log y = \log a + x \log b$）。直线斜率变平缓并不代表总量在下降，而是说明**指数增长率（百分比增速）在放缓**（如美国近代人口增长率低于殖民与建国初期）。

> [!question]- 自测 2：如何在 `matplotlib` 中向同一张已经绘制过的图表追加新曲线，又如何把多张独立的图分开保存或展示？
> - 想叠加到同一张图：在未切换 `figure` 时连续调用多次 `plt.plot(...)`，或通过 `plt.figure('相同名称')` 重新激活已有画布后再调用 `plt.plot(...)`；
> - 想分开画多张图：调用 `plt.figure('新名称')` 开启新画布，或在同一画布内用 `plt.subplot(rows, cols, index)` 划分网格子图。
>
> 更多面向对象式绘图（`fig, ax = plt.subplots()`）与科学计算联动实践，参见 [[CS Learning/Python MIT6.100L/Extention/Extention NumPy、Pandas 与 Matplotlib 扩展练习|Extention：NumPy、Pandas 与 Matplotlib 扩展练习]]。
