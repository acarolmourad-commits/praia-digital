from pathlib import Path
import re

pages = [
    'index.html',
    'servicos.html',
    'imoveis.html',
    'cases.html',
    'blog/index.html',
    'litoral-prime-imoveis/index.html',
    'litoral-prime-imoveis/imoveis.html',
]

inject = '<link rel="alternate" hreflang="x-default" href="https://acarolmourad.github.io/praia-digital/{rel}" />\n  '

for rel in pages:
    p = Path(rel)
    text = p.read_text(encoding='utf-8', errors='ignore')
    if 'hreflang="x-default"' in text:
        print('skip', rel)
        continue
    if '<link rel="alternate" hreflang="pt-BR"' in text:
        text = text.replace(
            '<link rel="alternate" hreflang="pt-BR"',
            inject.replace('{rel}', rel) + '<link rel="alternate" hreflang="pt-BR"',
            1,
        )
    else:
        head_end = text.find('</head>')
        text = text[:head_end] + inject.replace('{rel}', rel) + text[head_end:]
    p.write_text(text, encoding='utf-8')
    print('updated', rel)
