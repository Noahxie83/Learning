from pathlib import Path
import re

p=Path(r'D:\Learning\staged-paper-reading-review\examples\attention-is-all-you-need.md')
s=p.read_text(encoding='utf-8')
s=s.replace('# Attention Is All You Need', '# Attention Is All You Need · 格式片段', 1)
s=s.replace('# First Time', '<!-- 本文件仅演示组织与格式，不是完整逐段精读或全量推导。范围说明见仓库 README。 -->\n\n# First Time', 1)
start=s.index('## 3.Figure & Table')
end=s.index('# Second Time')
figures=s[start:end].strip()
s=s[:start]+s[end:]
for match in list(re.finditer(r'^## (\d+)\.',s,re.M))[::-1]:
    if match.start()>s.index('# Second Time'):
        n=int(match.group(1))
        s=s[:match.start(1)]+str(n+1)+s[match.end(1):]

notation=r'''## 1.Notation & Parameters
以下选取本片段使用的主线记号；完整导读应按实际正文补齐重点表，局部符号就地解释。

| 符号/参数 | 含义与作用 | 关键设定/约束 |
|---|---|---|
| $Q$ | 查询矩阵，用于与键计算匹配 | 交叉注意力中来自解码器 |
| $K$ | 键矩阵 | 交叉注意力中来自编码器输出 |
| $V$ | 值矩阵，被注意力权重加权汇聚 | 与键的位置数一致 |
| $d_{\mathrm{model}}$ | 模型隐藏表示维度 | base 为 512 |
| $d_k$ | 每头键与查询的维度，同时决定缩放量 | base 为 64 |
| $d_v$ | 每头值的维度 | base 为 64 |
| $M$ | 讲解辅助：显式表示因果掩码 | 允许位置 0，禁止位置 $-\infty$；原式 (1) 未写出 |
| $W_1,W_2,b_1,b_2$ | FFN 两层仿射变换参数 | base 的特征维度为 $512\rightarrow2048\rightarrow512$ |
| $\beta_1,\beta_2$ | Adam 一阶与二阶矩估计系数 | 0.9 与 0.98 |
| $\epsilon$ | Adam 数值稳定常数 | $10^{-9}$ |

'''
s=s.replace('# Second Time\n\n', '# Second Time\n\n'+notation)
s=s.replace('## 3.Encoder and Decoder', '## <font color="#ff0000">3.Encoder and Decoder</font>')
s=s.replace('原文章节：§3.1。', '原文章节：§3.1。\n图表对应：[Fig1 精读](#fig1)。')
s=s.replace('原文章节：§3.2。', '原文章节：§3.2。\n图表对应：[Fig2 精读](#fig2)。')
s=s.replace('原文章节：§4。', '原文章节：§4。\n图表对应：[Table1 精读](#table1)。')
figures=figures.replace('## 3.Figure & Table', '## 8.Figure & Table')
for number in ['Fig1','Fig2','Table1','Table2','Table3']:
    pattern=r'^(#### .*?'+number+r':.*)$'
    figures=re.sub(pattern, '<a id="'+number.lower()+'"></a>\n'+r'\1', figures,flags=re.M)
s=s.replace('# Overall Review', figures+'\n\n# Overall Review')
s=re.sub(r'\*\*([^*\n]+)\*\*', r'<font color="#ff0000">\1</font>', s)
p.write_text(s,encoding='utf-8')
print('Migrated format excerpt; no claim of complete reading coverage.')
