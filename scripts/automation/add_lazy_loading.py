#!/usr/bin/env python3
"""
add_lazy_loading.py
Adiciona loading="lazy" em imagens que ainda não têm esse atributo.
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

    def add_lazy(m):
        img = m.group(0)
        if 'loading=' in img:
            return img
        # insert loading="lazy" before closing >
        if img.endswith('/>'):
            return img[:-2] + ' loading="lazy" />'
        else:
            return img[:-1] + ' loading="lazy">'

    new_text = re.sub(r'<img[^>]*>', add_lazy, text, flags=re.S|re.I)
    if new_text != text:
        try:
            path.write_text(new_text, encoding='utf-8')
            print('updated', rel)
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
