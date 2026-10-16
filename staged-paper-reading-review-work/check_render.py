from markdown_it import MarkdownIt

md = MarkdownIt('commonmark').enable('table')
for prefix in ['text\n', '| a | b |\n|---|---|\n|1|2|\n', '```text\ncode\n```\n']:
    old = md.render(prefix + '<a id="fig1"></a>\n#### Fig1:\nbody')
    new = md.render(prefix + '#### <a id="fig1"></a>Fig1:\nbody')
    print('old h4:', '<h4>' in old, 'new h4:', '<h4>' in new)
    assert '<h4>' in new
