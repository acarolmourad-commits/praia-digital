#!/usr/bin/env python3
"""SEO fixes for the praia.digital static site.

Run from the repo root:
    python scripts/seo-fixes.py

What it does:
1. Replaces og:image/twitter:image references to og-image.svg with og-image.png
   (SVG is not rendered by WhatsApp/Facebook/LinkedIn crawlers).
2. Adds og:image:width, og:image:height, og:image:alt and og:site_name
   right after the og:image meta when missing.
3. Percent-encodes non-ASCII URLs in sitemap.xml (invalid per the sitemap protocol).
"""
import pathlib
import re
import urllib.parse

root = pathlib.Path(__file__).resolve().parent.parent
changed = []

SKIP_DIRS = {'.git', 'node_modules', 'backups', 'backup', '.audit'}

for f in root.rglob('*.html'):
    if any(p in SKIP_DIRS for p in f.parts):
        continue
    text = f.read_text(encoding='utf-8', errors='replace')
    orig = text
    text = text.replace('og-image.svg', 'og-image.png')
    if 'property="og:image"' in text and 'og:image:width' not in text:
        text = re.sub(
            r'(<meta property="og:image"[^>]*>)',
            r'\1\n  <meta property="og:image:width" content="1200">'
            r'\n  <meta property="og:image:height" content="630">'
            r'\n  <meta property="og:image:alt" content="Praia Digital — imóveis no litoral com IA">'
            r'\n  <meta property="og:site_name" content="Praia Digital">',
            text,
            count=1,
        )
    if text != orig:
        f.write_text(text, encoding='utf-8')
        changed.append(str(f.relative_to(root)))

sitemap = root / 'sitemap.xml'
if sitemap.exists():
    s = sitemap.read_text(encoding='utf-8')

    def enc(m):
        u = m.group(1)
        if u.isascii():
            return m.group(0)
        p = urllib.parse.urlsplit(u)
        return '<loc>' + urllib.parse.urlunsplit(p._replace(path=urllib.parse.quote(p.path))) + '</loc>'

    s2 = re.sub(r'<loc>(.*?)</loc>', enc, s)
    if s2 != s:
        sitemap.write_text(s2, encoding='utf-8')
        changed.append('sitemap.xml')

print(f'Updated {len(changed)} files')
for c in changed:
    print(' -', c)
