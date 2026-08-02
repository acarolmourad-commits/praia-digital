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

non_critical = ['style.css', 'print.css', 'components.css']

updated = 0
for rel in pages:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    new_text = re.sub(
        r'(<link\s+[^>]*href="[^"]*(?:' + '|'.join(non_critical) + r')[^"]*"[^>]*>)',
        lambda m: m.group(1).rstrip('>').rstrip() + (' media="print" onload="this.media=\'all\'"' if 'media=' not in m.group(1) else '') + '>',
        text,
        flags=re.I
    )
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    else:
        print('skip', rel)

print('updated', updated, 'pages')
