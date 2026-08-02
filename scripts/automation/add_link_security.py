#!/usr/bin/env python3
"""
add_link_security.py
Adiciona rel="noopener" em links externos para segurança e performance.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
SAME_HOST = ['acarolmourad.github.io', 'praia-digital', 'github.io']

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

    def add_noopener(m):
        a = m.group(0)
        href = m.group(1)
        if 'noopener' in a or 'noreferrer' in a:
            return a
        if any(host in href for host in SAME_HOST):
            return a
        if 'target=' in a:
            a = re.sub(r'target="[^"]*"', lambda mm: mm.group(0) + ' rel="noopener"', a, count=1, flags=re.I)
        else:
            a = a.replace('>', ' rel="noopener">', 1)
        return a

    new_text = re.sub(r'<a[^>]+href=["\'](https?://[^"\']+)["\'][^>]*>', add_noopener, text, flags=re.S|re.I)
    if new_text != text:
        try:
            path.write_text(new_text, encoding='utf-8')
            print('updated', rel)
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
