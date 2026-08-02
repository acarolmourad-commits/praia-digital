#!/usr/bin/env python3
"""
fix_long_meta.py
Trunca titles e meta descriptions excessivamente longos para evitar corte no Google.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
TITLE_MAX = 70
DESC_MAX = 160

exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

updated = 0
skipped = 0
errors = 0

def truncate(text: str, limit: int) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text.rfind(' ', 0, limit)
    if cut == -1:
        cut = limit
    return text[:cut].rstrip() + '...'

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

    modified = False
    # title
    m = re.search(r'<title[^>]*>(.*?)</title>', text, re.S|re.I)
    if m:
        title = re.sub(r'\s+', ' ', m.group(1)).strip()
        new_title = truncate(title, TITLE_MAX)
        if new_title != title:
            text = text.replace(m.group(1), new_title, 1)
            modified = True

    # meta description
    m = re.search(r'(<meta[^>]*name=["\']description["\'][^>]*content=["\'])(.*?)(["\'])', text, re.S|re.I)
    if m:
        desc = re.sub(r'\s+', ' ', m.group(2)).strip()
        new_desc = truncate(desc, DESC_MAX)
        if new_desc != desc:
            text = text.replace(m.group(0), m.group(1) + new_desc + m.group(3), 1)
            modified = True

    if modified:
        try:
            path.write_text(text, encoding='utf-8')
            print('updated', rel)
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
