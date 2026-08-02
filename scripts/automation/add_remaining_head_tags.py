#!/usr/bin/env python3
"""
add_remaining_head_tags.py
Adiciona favicon, manifest, robots meta e og:locale nas páginas públicas faltantes.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
CANONICAL_BASE = 'https://acarolmourad.github.io/praia-digital/'
FAVICON = 'https://acarolmourad.github.io/praia-digital/favicon.ico'
MANIFEST = 'https://acarolmourad.github.io/praia-digital/manifest.json'
THEME_COLOR = '#0ea5e9'

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

    tags = []
    if not re.search(r'<link[^>]*rel=["\'](icon|shortcut icon)', text, re.S|re.I):
        tags.append(f'<link rel="icon" type="image/x-icon" href="{FAVICON}">')
        tags.append(f'<link rel="apple-touch-icon" href="{FAVICON}">')
    if not re.search(r'<link[^>]*rel=["\']manifest', text, re.S|re.I):
        tags.append(f'<link rel="manifest" href="{MANIFEST}">')
    if not re.search(r'<meta[^>]*name=["\']robots["\']', text, re.S|re.I):
        tags.append('<meta name="robots" content="index, follow">')
    if not re.search(r'<meta[^>]*property=["\']og:locale', text, re.S|re.I):
        tags.append('<meta property="og:locale" content="pt_BR">')
    if not re.search(r'<meta[^>]*name=["\']theme-color["\']', text, re.S|re.I):
        tags.append(f'<meta name="theme-color" content="{THEME_COLOR}">')

    if not tags:
        skipped += 1
        continue

    tag_block = '\n'.join(tags)
    if '</head>' in text:
        text = text.replace('</head>', tag_block + '\n</head>', 1)
    elif '<head>' in text:
        text = text.replace('<head>', '<head>\n' + tag_block, 1)
    else:
        text = tag_block + '\n' + text

    try:
        path.write_text(text, encoding='utf-8')
        print('updated', rel, 'added', len(tags), 'tags')
        updated += 1
    except Exception as e:
        print('write error', rel, e)
        errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
