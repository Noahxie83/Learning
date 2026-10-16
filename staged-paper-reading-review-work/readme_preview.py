from pathlib import Path
import re
from markdown_it import MarkdownIt

repo=Path(r'D:\Learning\staged-paper-reading-review')
output=Path(__file__).parent
md=MarkdownIt('commonmark',{'html':True}).enable('table')
body=md.render((repo/'README.md').read_text(encoding='utf-8'))
body=re.sub(r'src="(assets/[^"\n]+|examples/assets/[^"\n]+)"', lambda m: 'src="'+(repo/m[1]).as_uri()+'"', body)
css='''body{margin:0;padding:24px;background:#f6f8fa;color:#1f2328;font:16px/1.6 system-ui,"Microsoft YaHei",sans-serif}main{box-sizing:border-box;max-width:1012px;margin:auto;padding:32px;background:#fff;border:1px solid #d1d9e0;border-radius:6px}img{max-width:100%;box-sizing:border-box}a{color:#0969da;text-decoration:none}p{margin:0 0 16px}h2{font-size:24px;border-bottom:1px solid #d1d9e0;margin-top:24px;padding-bottom:8px}h3{font-size:20px}pre{background:#f6f8fa;padding:16px;overflow:auto}table{border-collapse:collapse;display:block;overflow:auto}td,th{border:1px solid #d1d9e0;padding:6px 13px}details{margin-bottom:16px}summary{cursor:pointer}@media(max-width:600px){body{padding:0}main{padding:16px;border:0}}'''
(output/'readme-preview.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>'+css+'</style><main>'+body+'</main>',encoding='utf-8')
print('README preview prepared.')
