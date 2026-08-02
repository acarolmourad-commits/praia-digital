#!/usr/bin/env python3
"""
add_blog_titles.py
Adiciona <title> em páginas de blog que estão sem essa tag.
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
    if re.search(r'<title[^>]*>', text, re.S|re.I):
        skipped += 1
        continue
    slug = path.stem
    title = slug.replace('-', ' ').title()
    # melhorias manuais para slugs conhecidos
    title = re.sub(r'\bLitoral\b', 'Litoral', title, flags=re.I)
    title = re.sub(r'\b2026\b', '', title).strip()
    if not title.endswith('.'):
        title += ' | Litoral Prime Imóveis'
    else:
        title = title[:-1] + ' | Litoral Prime Imóveis'
    tag = f'<title>{title}</title>'
    if '<meta charset' in text:
        text = text.replace('<meta charset', tag + '\n  <meta charset', 1)
    elif '<title>' in text:
        text = re.sub(r'<title>.*?</title>', tag, text, count=1, flags=re.S|re.I)
    else:
        text = text.replace('<head>', '<head>\n  ' + tag, 1)
    try:
        path.write_text(text, encoding='utf-8')
        print('updated', path.relative_to(BASE))
        updated += 1
    except Exception as e:
        print('write error', path.relative_to(BASE), e)
        errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
