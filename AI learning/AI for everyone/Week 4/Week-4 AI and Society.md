---
title: Week 4：AI and Society
date: '2026-09-02'
date_source: 文件修改日期
subject: 人工智能
note_type: 课程笔记
course: AI for Everyone
tags:
  - 领域/人工智能
  - 类型/课程笔记
  - 课程/AI_for_Everyone
aliases:
  - AI for Everyone Week 4
  - AI and Society
cssclasses:
  - learning-note
  - subject-ai
  - learning-study
---

# Week 4：AI and Society

%% learning-vault-navigation:v1 %%
> [!abstract]- 笔记导航
> 目录：[[AI learning/AI for everyone/AI for Everyone导航|AI for Everyone 导航]]
> 上一章：[[AI learning/AI for everyone/Week 3/Week-3 AI in Your Company|Week 3：AI in Your Company]]

> [!abstract] 本周学习概览与原始资料
> 本周跳出企业视角，站在**社会与伦理（AI and Ethics）**高度审视人工智能：建立不盲目乐观也不过度恐慌的 ==“金发姑娘原则（Goldilocks Rule）”==，剖析当前 AI 的四大技术局限（性能边界、可解释性、偏见与歧视、对抗攻击），警惕 AI 的恶意滥用，探讨发展中国家的“蛙跳”机遇，并结合 McKinsey 2023 最新数据理性评估 AI 对全球就业结构的深远影响与社会应对策略。
> - 原始课件：[[AI learning/AI for everyone/Week 4/W4.pdf|W4.pdf]]（27 页）
> - 配套测验：[[AI learning/AI for everyone/Week 4/Week-4_Quiz|Week-4 Quiz]]（10 题）

---

## 1. 务实看待 AI：金发姑娘原则与四大技术局限

### 1.1 AI 的金发姑娘原则（Goldilocks Rule for AI）

面对舆论场上两个极端声音，吴恩达倡导保持“恰到好处（Just right）”的务实态度：

| 态度立场 | 典型论调 | 问题所在 |
| :--- | :--- | :--- |
| **过度乐观（Too optimistic）** | AI 将解决人类所有难题并缔造乌托邦 | 忽视技术瓶颈、数据偏见与落地风险，容易引发泡沫与盲目投资 |
| **过度悲观（Too pessimistic）** | 超级智能/有意识的杀手 AI 将很快导致人类灭绝 | 混淆 ANI 与 AGI，把宝贵资源浪费在防御虚幻的“巨型杀手机器人”上 |
| **恰到好处（Just right）** | ==AI 是极其强大的工具，但存在真实局限；我们完全可以主动缓解其潜在危害，并善用它创造巨大社会价值== | 聚焦当下可解决的真实风险（偏见、安全、就业转型） |

### 1.2 当前 AI 技术的四大局限

1. **性能局限（Performance limitations）**：受数据量、任务复杂度与分布偏移限制，远非万能。
2. **可解释性困难（Explainability is hard, but sometimes doable）**：
   - 神经网络参数庞大，很难像规则代码一样直接给出清晰因果逻辑；
   - **缺乏可解释性会严重削弱用户的信任与采纳意愿**（例如医疗场景下医生需要知道系统为何判定为肺炎）；
   - 但 AI 并非绝对无法解释：以斯坦福 **CheXNet（Rajpurkar et al., 2018）** 胸片诊断为例，模型可以输出病灶热力图高亮“右侧气胸（Right-sided Pneumothorax）”所在肺部区域，辅助医生核查判断。
3. **数据驱动的偏见与歧视（Biased AI through biased data）**；
4. **易受对抗攻击（Adversarial attacks on AI）**。

---

## 2. 歧视与偏见（Discrimination / Bias）

### 2.1 AI 如何学会不健康的刻板印象？

机器学习忠实复刻训练数据中的统计规律。如果人类历史文本本身包含偏见，AI 就会将其编码进模型内部。

课件第 8 页引用了经典词向量研究 **Bolukbasi et al. (2016)**——*Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings*：
- 词向量在几何空间中自然学会了合理类比：
  - `Man : Woman` $\approx$ `Father : Mother`
  - `Man : Woman` $\approx$ `King : Queen`
- 但同时也从互联网语料中学到了严重的性别刻板印象：
  - `Man : Computer programmer` $\approx$ `Woman : Homemaker`（在二维向量示意中，$\vec{v}_{\text{Programmer}} - \vec{v}_{\text{Man}} = (3,2)-(1,1) = (2,1)$，而 $\vec{v}_{\text{Homemaker}} - \vec{v}_{\text{Woman}} = (4,4)-(2,3) = (2,1)$）。

> [!note] 偏见来自数据而非模型“主观恶意”
> 若模型学习自带有偏见的语料，它会再现类似偏见；反之，如果训练语料完全中立、不含性别偏见，现有 ML 系统也预期几乎不会表现出性别偏见（对应 [[AI learning/AI for everyone/Week 4/Week-4_Quiz|Week-4 Quiz]] 第 4、5 题）。

### 2.2 偏见的现实危害

- **招聘筛选工具**：基于历史录用数据训练的系统可能系统性歧视女性求职者；
- **人脸识别系统**：因训练样本肤色不均衡，将深色皮肤个体误匹配为罪犯档案照（Mugshots）的错误率更高；
- **银行贷款审批**：放大历史信贷歧视，剥夺弱势群体获得金融服务的机会；
- **社会毒害效应**：大规模部署的算法不断循环强化不健康的社会刻板印象。

### 2.3 对抗偏见的三大系统性对策

1. **技术手段（Technical solutions）**：
   - 在表示空间中对偏见维度“归零（Zeroing out the bias）”，如词向量去偏算法；
   - 采集和使用**偏见更少、更具包容性与代表性的数据（More inclusive / less biased data）**。
2. **透明化与系统审计流程（Transparency & Systematic auditing processes）**：上线前与运行中持续按人群分组审计模型表现，主动暴露并修复公平性偏差。
3. **多元化团队（Diverse workforce）**：具备多元背景的工程师与产品团队更容易在早期识别出盲区，构建更少偏见的应用。

---

## 3. 对抗攻击（Adversarial Attacks on AI）

==对抗攻击（Adversarial Attack）==是指攻击者通过对输入施加人眼/人耳难以察觉的**微小扰动（Minor perturbation）**或特定物理伪装，诱导 AI 系统做出完全荒谬的错误判断。

### 3.1 数字攻击与物理攻击实例

| 攻击类型 | 课件代表案例 | 攻击效果 | 代表文献 |
| :--- | :--- | :--- | :--- |
| **数字像素/音频扰动** | 蜂鸟图片加微小噪声；野兔图片加微小噪声；语音片段微调 | 蜂鸟被误判为**锤子（Hammer）**；野兔被误判为**桌子（Desk）**；“No, reject”被听成“Yes, authorized” | —— |
| **物理眼镜伪装** | 佩戴特殊打印纹理的彩色眼镜 | 欺骗顶尖人脸识别系统，把佩戴者误认成女演员“Milla Jovovich” | Sharif et al. (2016) *Accessorize to a Crime* |
| **物理贴纸遮挡路标** | 在停车标志（Stop sign）上粘贴几枚特殊贴纸 | 使自动驾驶目标检测器完全漏检停车标志 | Eykholt et al. (2018) *Physical Adversarial Examples for Object Detectors* |
| **物理对抗补丁** | 在香蕉旁边放一张印有特定图案的圆形贴片 | 使视觉分类器把场景强行误判为烤面包机等无关物体 | Brown et al. (2018) *Adversarial Patch* |

### 3.2 对抗防御的现实
- 确实存在针对性的防御技术（如对抗训练等），但往往会带来**额外的算力、工程成本或正常准确率折损**；
- 如同垃圾邮件与反垃圾邮件的长期拉锯，许多高对抗场景中的攻防将演变为一场持续的 **军备竞赛（Arms race）**。

---

## 4. AI 的恶意滥用（Adverse Uses of AI）

注意区分 **对抗攻击**（欺骗现有 AI 模型）与 **AI 恶意滥用**（直接利用 AI 能力作恶）：

- **深度伪造（DeepFakes）**：利用生成式 AI 合成政客或普通人从未说过的话、从未做过的视频（注：在 [[AI learning/AI for everyone/Week 4/Week-4_Quiz|Week-4 Quiz]] 第 7 题中，合成虚假政客视频属于 **Adverse use**，而**不属于**针对 AI 系统的对抗攻击）；
- **破坏民主与侵犯隐私**：利用大规模监控与识别技术对个人进行压迫性监视（Oppressive monitoring）；
- **批量生成虚假评论（Fake comments）**：操纵电商口碑或公共舆论；
- **垃圾信息与金融欺诈升级**：形成 `Spam vs. Anti-spam` 与 `Fraud vs. Anti-fraud` 的攻防对抗。

---

## 5. AI 与发展中国家（AI and Developing Economies）

尽管美国、中国、英国、加拿大等国家已建立活跃的 AI 生态，但全球各国在 AI 浪潮中仍处于早期阶段，发展中国家同样拥有独特机会：

1. **技术“蛙跳（Leapfrog）”效应**：正如许多发展中国家跳过固定电话直接进入**移动手机**、跳过信用卡直接进入**移动支付**、并借助**在线教育**缩小鸿沟一样，AI 也有望帮助其跨越部分传统基础设施代差。
2. **聚焦优势垂直行业（Vertical Industries）**：==不必在通用底层框架上全面硬碰硬，而应结合本国具有全球竞争力的优势垂直产业发力==（例如某国拥有发达的咖啡豆加工产业，将 AI 应用于咖啡豆质检、分选与供应链优化便具有天然的数据与场景优势）。
3. **公私合作（Public-Private Partnerships）**：政府与企业协同投入算力、人才培养与开放生态，加速 AI 赋能实体经济。

---

## 6. AI 与全球就业（AI and Jobs）

### 6.1 宏观替代与创造规模

根据 **McKinsey Global Institute** 预测（到 2030 年）：
- **可能被替代的岗位**：约 **4 亿–8 亿**（400–800 million）；
- **同时新创造的岗位**：约 **5.55 亿–8.9 亿**（555–890 million）。

未来几年内，最容易被 AI 替代的是 ==主要由常规、重复性工作构成的岗位（Routine, repetitive work）==；而高度非重复、强人际共情或复杂综合判断的工作替代难度更高。

### 6.2 各职业群体的技术自动化潜力（McKinsey Digital, 2023）

课件第 23 页引用了 McKinsey 2023 年 6 月报告 *The Economic Potential of Generative AI*，展示了引入生成式 AI 后，占全球就业总量 **74%** 的十大职业群体到 2033 年的综合技术自动化潜力：

| 职业群体（Occupation Group） | 2033 年综合技术自动化潜力（含生成式 AI） | 占全球就业比重（%） |
| :--- | :---: | :---: |
| 办公行政支持（Office support） | **87%** | 9% |
| 生产制造作业（Production work） | **82%** | 12% |
| 餐饮服务（Food services） | **78%** | 5% |
| 机械安装与维修（Mechanical installation & repair） | **67%** | 4% |
| 社区服务（Community services） | **65%** | 3% |
| 农业（Agriculture） | **63%** | 21% |
| 商业与法律专业人士（Business & legal professional） | **62%** | 5% |
| 客户服务与销售（Customer service & sales） | **57%** | 10% |
| 教育与职业培训（Educator & workforce training） | **54%** | 4% |
| 创意与艺术管理（Creatives & arts management） | **53%** | 1% |

> [!important] 生成式 AI 的结构性变化
> 在生成式 AI 出现之前，自动化主要冲击重复性体力与流程作业；而生成式 AI 显著抬升了**办公支持、商业法律、客服销售、教育培训乃至创意艺术**等知识型白领工作的自动化潜力。但“高自动化潜力”意味着岗位中的**大量子任务将被重构或辅助**，而非整类职业瞬间消失。

### 6.3 面向社会的三大应对方案

1. **有条件基本收入（Conditional Basic Income）**：相比无条件发钱，更推荐为受冲击劳动者提供基本生活安全网，同时**与再学习/技能培训挂钩**，激励其向新岗位转型；
2. **终身学习（Lifelong Learning）**：个体与教育体系必须适应持续演进的技术浪潮，通过在线课程、书籍、社区保持终生更新；
3. **政策与政治层面解决方案（Political Solutions）**：通过税收、教育投资、劳动保障与产业政策平滑转型阵痛。

---

## 7. 全课程回顾与测验复盘

```mermaid
flowchart LR
    W1["Week 1: What is AI (祛魅概念/数据/能力边界)"] --> W2["Week 2: Building AI Projects (ML与DS工作流/项目尽调/团队协作)"]
    W2 --> W3["Week 3: AI in Your Company (复杂产品/角色分工/转型五步法)"]
    W3 --> W4["Week 4: AI and Society (金发姑娘原则/偏见与攻击/就业与社会)"]
```

> [!question]- Week 4 核心考点自检（对应 Week-4 Quiz）
> 1. **什么是 AI 的 Goldilocks Rule？**
>    - 对 AI 既不要过度乐观（包治百病），也不要过度悲观（超级杀手机器人灭世），应正视局限、缓解危害并善用其创造价值。
> 2. **面对胸片诊断等高风险应用，AI 缺乏可解释性会产生什么影响？**
>    - 会阻碍用户（如医生与患者）信任并采纳该 AI 系统；但 AI 并非完全不可解释（如病灶热力图）。
> 3. **对抗 AI 偏见的正确做法有哪些？**
>    - 系统性偏见审计、技术去偏（如“归零”词向量偏见）、采用更包容/少偏见的数据（以及建设多元团队）；注意**不能**靠对抗攻击来“修偏见”。
> 4. **合成政客虚假视频属于对抗攻击吗？**
>    - **不属于**。那是 AI 的恶意滥用（DeepFake / Adverse use）；而微调图像把狗认成猫、在 Stop 路标贴贴纸、微调音频欺骗语音识别才属于**对抗攻击**。
> 5. **发展中国家如何在 AI 时代建立优势？未来几年哪类工作最易被替代？**
>    - 聚焦本国已有优势的**垂直行业**（如咖啡豆加工）结合 AI 发力；最易被替代的是**常规、重复性工作（Routine, repetitive work）**。
> 
> 完整原题见：[[AI learning/AI for everyone/Week 4/Week-4_Quiz|Week-4 Quiz]]
