#!/usr/bin/env python3
"""
add_meta_descriptions.py
Adiciona meta description em páginas públicas sem essa tag.
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
    if re.search(r'<meta[^>]*name=["\']description["\']', text, re.S|re.I):
        skipped += 1
        continue
    # Try to extract description from content
    title = ''
    m = re.search(r'<title>(.*?)</title>', text, re.S|re.I)
    if m:
        title = m.group(1).strip()
    # Try to find a good description from first paragraph or subtitle
    description = ''
    m = re.search(r'<p[^>]*>(.*?)</p>', text, re.S|re.I)
    if m:
        description = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if not description:
        m = re.search(r'<h2[^>]*>(.*?)</h2>', text, re.S|re.I)
        if m:
            description = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if not description:
        description = title or path.stem.replace('-', ' ')
    # Clean and limit
    description = description.replace('\n', ' ').replace('\r', ' ')
    description = re.sub(r'\s+', ' ', description).strip()
    if len(description) > 155:
        description = description[:152].rsplit(' ', 1)[0] + '...'
    tag = f'  <meta name="description" content="{description}">'
    if '<meta charset' in text:
        text = text.replace('<meta charset', tag + '\n  <meta charset', 1)
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
