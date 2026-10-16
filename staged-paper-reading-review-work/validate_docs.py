from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
from collections import Counter
import re, json, html
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

root=Path(r'D:\Learning\staged-paper-reading-review')
md=MarkdownIt('commonmark', {'html':True}).enable('table').use(dollarmath_plugin)
failures=[]
diagrams=[]
link_count=0

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(); self.targets=[]; self.ids=[]; self.emphasis=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag=='a' and 'href' in attrs: self.targets.append(attrs['href'])
        if tag=='img' and 'src' in attrs: self.targets.append(attrs['src'])

def anchors_for(path):
    text=path.read_text(encoding='utf-8-sig')
    tokens=md.parse(text); anchors=[]
    for i,token in enumerate(tokens):
        if token.type=='heading_open':
            label=re.sub('<[^>]*>', '', tokens[i+1].content)
            label=re.sub(r'[^\w\-\s]', '', label.lower()).replace(' ', '-')
            anchors.append(label)
    tags=Tags(); tags.feed(md.render(text)); anchors+=tags.ids
    return set(anchors)

for p in root.rglob('*.md'):
    if '.git' in p.parts: continue
    text=p.read_text(encoding='utf-8-sig')
    tokens=md.parse(text)
    rendered=md.render(text)
    tags=Tags(); tags.feed(rendered)
    duplicate=[name for name,n in Counter(tags.ids).items() if n>1]
    if duplicate: failures.append((str(p), 'duplicate ids', duplicate))
    targets=tags.targets
    for token in tokens:
        if token.type=='fence' and token.info=='mermaid':
            diagrams.append({'path':str(p.relative_to(root)), 'source':token.content})
    for target in targets:
        url=urlsplit(target)
        if url.scheme or url.netloc: continue
        link_count+=1
        dest=(p.parent/unquote(url.path)).resolve() if url.path else p
        if not dest.exists(): failures.append((str(p.relative_to(root)), target, 'missing file')); continue
        if url.fragment and dest.suffix=='.md' and unquote(url.fragment) not in anchors_for(dest):
            failures.append((str(p.relative_to(root)),target,'missing anchor'))
    if p.name=='attention-is-all-you-need.md':
        assert rendered.count('<h4>')==5
        assert not re.search(r'<(?:font|strong|em)[^>]*>[^<]*\$', rendered)
        # A real table must retain three cells for every notation row.
        assert rendered.count('<th>')==3
        assert rendered.count('<td>')==30
        active=None; nums=[]
        for line in text.splitlines():
            if line in ['# First Time','# Second Time']:
                if nums: assert nums==list(range(1,len(nums)+1))
                active=line; nums=[]
            if line=='# Overall Review':
                assert nums==list(range(1,len(nums)+1)); active=None
            if active and line.startswith('## '):
                nums.append(int(re.search(r'(\d+)\.',line).group(1)))
        (Path(__file__).parent/'example.html').write_text(rendered,encoding='utf-8')

(Path(__file__).parent/'diagrams.json').write_text(json.dumps(diagrams,ensure_ascii=False),encoding='utf-8')
print(f'{link_count} local links checked; {len(diagrams)} Mermaid blocks; 5 figure headings; 10 notation rows.')
print('Issues:',json.dumps(failures,ensure_ascii=False))
assert not failures
