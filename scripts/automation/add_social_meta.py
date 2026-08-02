#!/usr/bin/env python3
"""
add_social_meta.py
Adiciona Open Graph e Twitter Card tags em páginas públicas sem essas tags.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
CANONICAL_BASE = 'https://acarolmourad.github.io/praia-digital/'
DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=60'

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
    if re.search(r'<meta[^>]*property=["\']og:', text, re.S|re.I):
        skipped += 1
        continue

    # Extract title
    title = ''
    m = re.search(r'<title>(.*?)</title>', text, re.S|re.I)
    if m:
        title = m.group(1).strip()
    # Extract description
    description = ''
    m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', text, re.S|re.I)
    if m:
        description = m.group(1).strip()
    # Extract image
    image = DEFAULT_IMAGE
    m = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\'](.*?)["\']', text, re.S|re.I)
    if not m:
        m = re.search(r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\'](.*?)["\']', text, re.S|re.I)
    if not m:
        m = re.search(r'<img[^>]+src=["\'](.*?)["\']', text, re.S|re.I)
    if m:
        img_src = m.group(1).strip()
        if img_src.startswith('http'):
            image = img_src
        else:
            image = CANONICAL_BASE + str(rel).replace('\\', '/')
    # URL
    rel_path = str(rel).replace('\\', '/')
    url = CANONICAL_BASE + rel_path

    tags = f'''  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{image}">
  <meta property="og:url" content="{url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">'''

    if '</head>' in text:
        text = text.replace('</head>', tags + '\n</head>', 1)
    elif '<head>' in text:
        text = text.replace('<head>', '<head>\n' + tags, 1)
    else:
        text = tags + '\n' + text

    try:
        path.write_text(text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    except Exception as e:
        print('write error', rel, e)
        errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
