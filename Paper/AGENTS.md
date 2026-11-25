# Paper 目录整理与维护规范

本文件是 `Paper/` 目录结构、命名、YAML 元数据、论文流转与双导航维护的**单一事实来源**。凡在 `Paper/` 中新增论文 PDF、开始精读、维护笔记元数据、调整路径或更新论文导航，必须按本规范执行。与根仓库通用的原始保护及 Git 安全规则见 [../AGENTS.md](../AGENTS.md)。

## 1. 目录结构与归类原则

- **主题与状态解耦**：文件夹只按**稳定的研究领域（Topic）**划分；阅读进度与复现状态一律由笔记 YAML 与导航页记录，不按“已读/未读”建文件夹。
- **两至三层拓扑**：
  - `Paper/Foundations/<ShortName>/`：深度学习经典奠基论文（视觉、序列/语言、图神经网络等）。
  - `Paper/Generative-Models/Foundations/<ShortName>/`：生成模型早期基础（如 `GAN`）。
  - `Paper/Generative-Models/Diffusion-and-Flow/<ShortName>/`：扩散、分数模型与流匹配精读论文；同级 `PDFs/` 存放该专题待读/参考 PDF（物理平铺，逻辑子线在导航页分组）。
  - `Paper/Generative-Models/Inverse-Problems/<ShortName>/`：基于扩散/流模型的逆问题求解精读论文；同级 `PDFs/` 存放该专题待读/参考 PDF。
- **扩展新专题**：新增研究方向时，以**领域英文短名**（连字符分词，如 `Reinforcement-Learning`、`Multimodal`）在 `Paper/` 或对应大专题下建目录，**不用具体论文名组合命名专题**。

## 2. 命名规范（目录 / 笔记 / PDF 三统一）

- **单篇论文目录**：简洁公认英文短名，采用 `Title-Case` 或通用缩写（如 `DDPM`、`Score-SDE`、`Flow-Matching`、`Rectified-Flow`、`HDPS`），不用空格、全大写、截断长标题或中文顿号。
- **精读笔记**：`<ShortName>.md`（与所在目录同名，如 `Score-SDE/Score-SDE.md`、`HDPS/HDPS.md`），不使用 `Note.md` 或中文后缀名。
- **论文 PDF**：`<ShortName>_<arXivID或会议年份>.pdf`（如 `DDPM_2006.11239.pdf`、`AlexNet_NIPS2012.pdf`、`GNN_Distill2021.pdf`）。同一论文附带离线网页 `.html` 与 `*_files/` 资源目录时，保持 HTML 与资源目录原名配对以免断链。
- **待读 `PDFs/`**：优先沿用 `<ShortName>_<arXivID>.pdf`；已有清晰英文标题的文件名可保持稳定，入库前必须检查重复（按文件名与 SHA256 哈希去重，不保留多份副本）。

## 3. 论文入库与升级流转流程

### 分支 A：新增待读论文 PDF
1. 先在 `Paper/` 全目录做标题与 SHA256 查重，确认无重复副本。
2. 将 PDF 放入对应专题的 `PDFs/` 目录，并按 `<ShortName>_<arXivID>.pdf` 命名。
3. 在对应专题的 `README.md` 与 `<中文主题>导航.md` 的待读分组中同步追加一行。
4. **完成标准**：全库无重复 PDF，且双导航中新增条目链接均可正常解析。

### 分支 B：待读论文升格为精读论文
1. 在对应专题下新建 `<ShortName>/` 目录。
2. 将原 PDF 从 `PDFs/` 移入 `<ShortName>/` 并按 `<ShortName>_<arXivID或会议年份>.pdf` 命名。
3. 创建 `<ShortName>/<ShortName>.md`，顶部写入标准 YAML Frontmatter（见第 4 节），正文沿用既有三遍精读结构（`First Time` / `Second Time` / `Third Time` 或 `Overall Review`）。
4. 更新同层及上级 `README.md` 与 `*导航.md`：将该论文从待读表移至精读表。
5. **完成标准**：`PDFs/` 中已无该文件，新笔记含合法 YAML，所有受影响双导航同步更新。

### 分支 C：调整或重命名已有论文路径
1. 仅在明确获得用户授权时移动或重命名已有目录与文件。
2. 全库检索旧路径（覆盖根目录、各子目录双导航、`Concepts/`、`ai-research-weekly.md`、`github-ai-cs-weekly-top3.md`）。
3. 同步更新全部旧路径链接（修复周报时只改链接路径，不改写历史文字）。
4. **完成标准**：全库旧路径引用归零，且每个更新后的相对路径与 Wiki 链接均指向真实存在的文件。

## 4. 精读笔记 YAML Frontmatter 规范

每篇论文精读笔记顶部使用如下结构；修改元数据时只改 Frontmatter，**保持正文、公式推导与实验记录原样不动**：

```yaml
---
title: "完整英文论文标题"
short_name: "ShortName"
year: 2025
venue: "ICLR 2025"          # 正式会议/期刊名，未发表预印本填 "arXiv"
arxiv: "2503.08136"         # 无 arXiv 号时省略此行
category: "Generative-Models/Inverse-Problems"
topics:
  - 生成模型
  - 逆问题求解
note_type: 论文精读
note_status: 三遍精读已归档   # 待建笔记 | 精读中 | 三遍精读已归档
read_status: 待确认          # 待读 | 阅读中 | 已完成 | 待确认
status_note: ""             # 可选：记录用户确认日期与依据
repro_status: 未复现         # 未复现 | 进行中 | 已完成 | 待确认
tags:
  - 类型/论文精读
  - 论文/生成模型
---
```

- **状态真实性**：`read_status` 与 `repro_status` 必须有明确依据；未经用户确认不得把归档笔记、长文总结或本地代码/实验目录推断为 `已完成`，未知一律填 `待确认`（无复现实验归档填 `未复现`）。

## 5. 双导航与重型产物边界

- **双导航配对**：已维护的论文专题目录成对维护 `README.md` 与 `<中文主题>导航.md`（当前三层：`Paper/`、`Paper/Generative-Models/`、`Paper/Generative-Models/Inverse-Problems/`）。
  - `README.md`（GitHub 入口）：使用 Markdown 相对链接，路径含空格或中文时按标准 URL 编码，不指向本地 `*导航.md`。
  - `*导航.md`（Obsidian 入口）：使用带库根路径的 Wiki 链接（如 `[[Paper/Foundations/ViT/ViT|阅读笔记]]`），**保留原始空格与中文，禁止混入 `%20`**。
  - 两者增删论文与状态更新必须保持内容一致。
- **重型实验与临时文件边界**：
  - 拆页图、文本提取缓存等临时产物不长期遗留在 `Paper/` 中；如临时生成解析目录 `Paper/tmp/`（已由 `.gitignore` 忽略），任务结束后应及时清理。
  - 第三方代码仓库与 `Experiments/`、`Code/` 目录内的源码、配置、日志、检查点及嵌套 `.git` 保持原样，不自动改写或做双导航改造。

## 6. 交付前必查清单

完成任何 `Paper/` 整理或入库操作后，提交/汇报前逐项核实：
1. 新增或移动的文件全部符合 `<ShortName>/`、`<ShortName>.md`、`<ShortName>_<ID>.pdf` 规范且全库无重复 PDF。
2. 受影响的精读笔记包含合法 YAML Frontmatter，且正文与实验文件一字未改。
3. 受影响的 `README.md` 与 `*导航.md` 条目一致，Wiki 链接无 `%20`，Markdown 链接无字面量 `\n` 或失效路径。
4. 全库跨文件链接检查零断链（含各级导航与历史周报）。
5. 遵守根仓库 Git 安全边界：不执行 `git add .`，不擅自提交或推送未授权变更，不触碰范围外既有修改。
