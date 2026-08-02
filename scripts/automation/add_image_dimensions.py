#!/usr/bin/env python3
"""
add_image_dimensions.py
Adiciona width e height em imagens que ainda não têm esses atributos para reduzir CLS.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600

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

    def add_dimensions(m):
        img = m.group(0)
        if 'width=' in img or 'height=' in img:
            return img
        # insert width/height before closing >
        if img.endswith('/>'):
            return img[:-2] + f' width="{DEFAULT_WIDTH}" height="{DEFAULT_HEIGHT}" />'
        else:
            return img[:-1] + f' width="{DEFAULT_WIDTH}" height="{DEFAULT_HEIGHT}">'

    new_text = re.sub(r'<img[^>]*>', add_dimensions, text, flags=re.S|re.I)
    if new_text != text:
        try:
            path.write_text(new_text, encoding='utf-8')
            print('updated', rel)
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
