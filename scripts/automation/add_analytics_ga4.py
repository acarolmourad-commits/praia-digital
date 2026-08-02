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

ga_block = '''  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX', { anonymize_ip: true });
  </script>
'''

updated = 0
for rel in pages:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'googletagmanager.com/gtag/js' in text:
        print('skip', rel)
        continue
    if '<meta name="viewport"' in text:
        new_text = text.replace('<meta name="viewport"', ga_block + '<meta name="viewport"', 1)
    else:
        new_text = text.replace('</head>', ga_block + '</head>', 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    else:
        print('no-insert', rel)

print('updated', updated, 'pages')
