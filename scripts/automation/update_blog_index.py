#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza blog/index.html com os artigos mais recentes.
Lê blog/*.html, ordena por data no slug/arquivo, atualiza grid.
"""
import re
from pathlib import Path
from datetime import datetime

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
INDEX = BLOG_DIR / 'index.html'

def slug_date(path: Path):
    name = path.stem
    m = re.search(r'(\d{4}-\d{2}-\d{2})', name)
    return m.group(1) if m else '1900-01-01'

def main():
    if not INDEX.exists():
        print('blog/index.html not found')
        return
    articles = sorted(BLOG_DIR.glob('*.html'), key=lambda p: slug_date(p), reverse=True)
    latest = articles[:12]
    cards = []
    for art in latest:
        title_m = re.search(r'<title>\s*(.+?)\s*</title>', art.read_text(encoding='utf-8', errors='ignore'), re.I|re.S)
        title = title_m.group(1) if title_m else art.stem.replace('-', ' ').title()
        desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', art.read_text(encoding='utf-8', errors='ignore'), re.I)
        desc = desc_m.group(1) if desc_m else ''
        cards.append(f'''    <a class="post-card" href="{art.name}">
      <span class="post-tag">Blog</span>
      <div class="post-title">{title}</div>
      <div class="post-excerpt">{desc}</div>
      <span class="post-link">Ler artigo →</span>
    </a>''')
    html = INDEX.read_text(encoding='utf-8', errors='ignore')
    marker = 'class="post-grid"'
    if marker in html:
        prefix, suffix = html.split(marker, 1)
        suffix = suffix.split('</div>', 1)[1] if '</div>' in suffix else ''
        new_grid = marker + '>\n' + '\n'.join(cards) + '\n  </div>'
        new_html = prefix + new_grid + suffix
        INDEX.write_text(new_html, encoding='utf-8')
        print('BLOG_INDEX_UPDATED', len(cards))
    else:
        print('BLOG_INDEX_MARKER_NOT_FOUND')

if __name__ == '__main__':
    main()
