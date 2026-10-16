from pathlib import Path
import re

root = Path(r'D:\Learning\staged-paper-reading-review\skills\staged-paper-reading')

def replace(path, old, new):
    p = root / path
    s = p.read_text(encoding='utf-8')
    assert old in s, (path, old)
    p.write_text(s.replace(old, new), encoding='utf-8')

replace('SKILL.md', 'description: "主要面向模型、算法类论文的分阶段导读：第一次阅读精读标题、摘要与结论；第二次阅读先给出重点符号与参数含义表，再精读全部正文非实验部分，按选择详解正文图表、推导正文公式；可选速读剩余实验与附录并循环答疑，最后通篇总结，逐阶段保存到同一份完整阅读 Markdown，不另生成精简笔记。用于提供 PDF、论文链接或正文并要求分阶段阅读、图表公式解读或保存完整阅读记录时。"', 'description: "用于模型、算法类论文的分阶段导读、正文精读、图表解读、公式推导与完整阅读记录保存。接受 PDF、论文链接或正文；用户要求审查或修改本 skill 时执行维护任务，不启动论文阅读流程。"')
replace('SKILL.md', '## 阅读约定\n', '## 阅读约定\n\n- 先区分论文阅读与 skill 维护。审查、修改或发布本 skill 时，仅处理规则、资源与文档；不把 skill 文件当论文，也不触发阅读选择或一分钟等待。\n')
replace('SKILL.md', '第一次阅读仅创建一次文件并记录唯一固定绝对路径 reading_md_path', '首次实际开展阅读时仅初始化一次文件（默认在第一次阅读；用户明确跳读时在所选阶段），并记录唯一固定绝对路径 reading_md_path')
replace('SKILL.md', '第一次阅读开始时确定本轮唯一累计文件', '首次实际阅读开始时确定本轮唯一累计文件')
replace('SKILL.md', '只有用户明确更换论文版本或指定新文件才重新初始化。', '用户更换论文时为新论文单独初始化；同篇同版本只有用户明确更换版本或指定新文件才重新初始化。')
replace('SKILL.md', '进行中只保留已完成的主分组，最后形成三组', '进行中只保留已有实际内容的主分组，分组存在不等于阶段完成；默认完整流程最后形成三组，明确跳过的阶段不补造分组或内容')
replace('SKILL.md', '需要细分讲解时使用列表或加粗标签', '需要细分讲解时使用列表或文字标签（聊天可加粗，文件重点按红色规则）')
replace('SKILL.md', '原文没有编号时，按文章实际出现顺序为图、表分别从 1 连续编号', '原文没有编号时，按文章实际出现顺序为图、表分别从 1 连续编号')
replace('SKILL.md', '同类图表同时包含已有编号和无编号条目时', '补充阅读新增无编号图表时接续已分配编号，不重排已有 ID。同类图表同时包含已有编号和无编号条目时')
replace('references/reading-markdown.md', '第一次阅读只初始化一次文件', '首次实际开展阅读时只初始化一次文件（默认第一次阅读；用户明确跳读时在所选阶段）')
replace('references/reading-markdown.md', '只有用户明确指定新文件或更换论文版本才重新初始化', '用户更换论文时为新论文单独初始化；同篇同版本只有用户明确指定新文件或更换版本才重新初始化')
replace('references/reading-markdown.md', '进行中仅保留已产生内容的分组，不提前放空章节；结束时形成三组', '进行中仅保留已产生内容的分组，不提前放空章节；分组存在不等于阶段完成。默认完整流程结束时形成三组，用户明确跳过的阶段不补造分组或内容')
replace('references/reading-markdown.md', '进一步细分用列表或加粗', '进一步细分用列表或文字标签')
replace('references/reading-markdown.md', '`**图表对应：** [Fig2 精读](#fig2)、[Table1 精读](#table1)`', '`图表对应：[Fig2 精读](#fig2)、[Table1 精读](#table1)`')
replace('references/reading-markdown.md', '或 `**时间状态：** $x_t$`', '或 `时间状态：$x_t$`')
replace('references/reading-markdown.md', '不生成额外精简笔记或分阶段副本。', '不生成额外精简笔记或分阶段副本。用户明确跳读时，直接按所选阶段开展并初始化同一文件，不为凑齐三个分组补写未读内容。')
replace('references/reading-markdown.md', '## 文件数学与转换\n', '## 文件数学与转换\n\n- Markdown 表格内的数学关系、条件概率或范数含竖线时，优先用 `\\mid`、`\\lvert`、`\\rvert`、`\\lVert`、`\\rVert` 表达，避免裸 `|` 被表格解析器切成新单元格；渲染后核对列数与数学含义。\n')
replace('references/reading-markdown.md', '图表精读完成后可回填', '补充阅读遇到无编号图表时，接续已有同类编号；正文和附录出现相同原编号时，保留可见原编号并以章节后缀区分锚点，例如 fig1-appendix，链接使用实际 ID。图表精读完成后可回填')
replace('references/reading-markdown.md', '移除强调星标。', '移除用于强调的星标；普通组织标签用纯文字，重点标签用红色。')
replace('references/first-read.md', '遇到结论替代选择时先输出已经完成的内容和选择问题。', '遇到结论替代或材料缺失选择时，先把已完成内容保存到固定文件并交付链接，再提出未决问题；尚未完成第一次阅读，不提出阶段末尾两个选择。')
replace('references/first-read.md', '再按 choices-and-waiting.md 清点全部正文图表和公式', '使用按 choices-and-waiting.md 预先核对的全部正文图表和公式清单')
replace('references/figures-and-tables.md', '条目内用列表或加粗标签组织解释', '条目内用列表或文字标签组织解释（聊天可加粗，文件重点用红色）')
replace('references/formula-derivation.md', '公式条目用加粗标签或列表', '公式条目用文字标签或列表（聊天可加粗，文件重点用红色）')
replace('references/second-read-and-summary.md', '章节与重要小节使用论文实际英文标题的编号二级标题 `## 1.Title`', '章节与重要小节使用论文实际英文标题的编号二级标题，符号表占第 1 节，正文从 `## 2.Introduction` 等实际标题接续')
replace('assets/full-reading-template.md', '`**图表对应：** [Fig1 精读](#fig1)、[Table1 精读](#table1)`', '`图表对应：[Fig1 精读](#fig1)、[Table1 精读](#table1)`')
replace('assets/full-reading-template.md', '进行中仅保留已完成主分组', '进行中仅保留已有实际内容的主分组，分组存在不等于阶段完成；跳过阶段不补造分组')
replace('assets/full-reading-template.md', '仅首次创建并记录 reading_md_path', '首次实际阅读时创建并记录 reading_md_path（明确跳读同样适用）')
p = root / 'assets/full-reading-template.md'
s = p.read_text(encoding='utf-8')
s = re.sub(r'\*\*([^*]+)：\*\*', r'<font color="#ff0000">\1：</font>', s)
p.write_text(s, encoding='utf-8')

for p in root.rglob('*.md'):
    s = p.read_text(encoding='utf-8')
    s = s.replace('文件是完整导读，不是精简笔记', '文件保留完整导读')
    p.write_text(s, encoding='utf-8')

print('Updated skill contracts, references and template.')
