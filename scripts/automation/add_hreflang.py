#!/usr/bin/env python3
"""
add_hreflang.py
Adiciona hreflang tags para indicar idioma/região do conteúdo.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
HOST = 'https://acarolmourad.github.io/praia-digital/'

exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

updated = 0
skipped = 0
errors = 0
for path in sorted(BASE.rglob('*.html')):
    rel = path.relative_to(BASE)
    if any(part in exclude for part in rel.parts):
        skipped += 1
        continue
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        errors += 1
        continue
    if re.search(r'<link[^>]*hreflang', text, re.S|re.I):
        skipped += 1
        continue
    rel_path = str(rel).replace('\\', '/')
    url = HOST + rel_path
    tag = f'  <link rel="alternate" hreflang="pt-BR" href="{url}">'
    if '</head>' in text:
        text = text.replace('</head>', tag + '\n</head>', 1)
    elif '<head>' in text:
        text = text.replace('<head>', '<head>\n' + tag, 1)
    else:
        text = tag + '\n' + text
    try:
        path.write_text(text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    except Exception as e:
        print('write error', rel, e)
        errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
