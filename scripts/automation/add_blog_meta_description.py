#!/usr/bin/env python3
"""
add_blog_meta_description.py
Adiciona meta description em páginas do blog que estão sem essa tag.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
BLOG = BASE / 'blog'

updated = 0
skipped = 0
errors = 0
for path in sorted(BLOG.glob('*.html')):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        errors += 1
        continue
    if re.search(r'<meta[^>]*name=["\']description["\']', text, re.S|re.I):
        skipped += 1
        continue
    title = ''
    m = re.search(r'<title>(.*?)</title>', text, re.S|re.I)
    if m:
        title = m.group(1).strip()
    if not title:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S|re.I)
        if m:
            title = m.group(1).strip()
    description = title or path.stem.replace('-', ' ')
    # limit to ~155 chars for SEO
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
        print('updated', path.relative_to(BASE))
        updated += 1
    except Exception as e:
        print('write error', path.relative_to(BASE), e)
        errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
