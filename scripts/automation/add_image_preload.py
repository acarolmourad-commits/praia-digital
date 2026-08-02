from pathlib import Path
import re

root = Path('.')
pages = [
    'index.html',
    'servicos.html',
    'imoveis.html',
    'cases.html',
    'blog/index.html',
    'litoral-prime-imoveis/index.html',
    'litoral-prime-imoveis/imoveis.html',
]

preloads = {
    'index.html': [
        ('https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/default-home.jpg', 'image/jpeg'),
    ],
    'servicos.html': [],
    'imoveis.html': [
        ('img/santos-apartamento-vista-mar.webp', 'image/webp'),
    ],
    'cases.html': [],
    'blog/index.html': [
        ('https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/default-home.jpg', 'image/jpeg'),
    ],
    'litoral-prime-imoveis/index.html': [
        ('https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/default-home.jpg', 'image/jpeg'),
    ],
    'litoral-prime-imoveis/imoveis.html': [
        ('img/santos-apartamento-vista-mar.webp', 'image/webp'),
    ],
}

updated = 0
for rel in pages:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'rel="preload"' in text:
        print('skip', rel)
        continue
    items = preloads.get(rel, [])
    if not items:
        print('skip', rel, '(no preloads defined)')
        continue
    preload_tags = '\n'.join(
        f'  <link rel="preload" as="image" href="{href}" type="{mime}" fetchpriority="high">'
        for href, mime in items
    )
    new_text = text.replace('<meta name="viewport"', preload_tags + '\n  <meta name="viewport"', 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    else:
        print('no-insert', rel)

print('updated', updated, 'pages')
