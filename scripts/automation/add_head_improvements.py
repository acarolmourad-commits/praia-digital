#!/usr/bin/env python3
"""
add_head_improvements.py
Adiciona tags head faltantes: viewport, charset, X-UA-Compatible e lang no <html>.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
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
    if not re.search(r'<meta[^>]*charset', text, re.S|re.I):
        tags.append('<meta charset="UTF-8">')
    if not re.search(r'<meta[^>]*name=["\']viewport["\']', text, re.S|re.I):
        tags.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    if not re.search(r'<meta[^>]*http-equiv=["\']X-UA-Compatible["\']', text, re.S|re.I):
        tags.append('<meta http-equiv="X-UA-Compatible" content="IE=edge">')

    modified = False
    if tags:
        tag_block = '\n'.join(tags)
        if '</head>' in text:
            text = text.replace('</head>', tag_block + '\n</head>', 1)
            modified = True
        else:
            print('no </head> found', rel)

    if re.search(r'<html[^>]*>', text, re.S|re.I):
        if not re.search(r'<html[^>]*lang=', text, re.S|re.I):
            text = re.sub(r'<html([^>]*)>', r'<html\1 lang="pt-BR">', text, count=1, flags=re.S|re.I)
            modified = True

    if modified:
        try:
            path.write_text(text, encoding='utf-8')
            print('updated', rel, 'added', len(tags), 'meta tags')
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
    else:
        skipped += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
