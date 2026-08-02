#!/usr/bin/env python3
"""
add_canonical.py
Adiciona <link rel="canonical"> em páginas públicas que estão sem essa tag.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
CANONICAL_BASE = 'https://acarolmourad.github.io/praia-digital/'

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
    if re.search(r'<link[^>]*rel=["\']canonical["\']', text, re.S|re.I):
        skipped += 1
        continue
    rel_path = str(rel).replace('\\', '/')
    canonical_url = CANONICAL_BASE + rel_path
    tag = f'  <link rel="canonical" href="{canonical_url}">'
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
