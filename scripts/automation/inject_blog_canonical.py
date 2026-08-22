import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = REPO / 'blog'

FIXED = 0
for path in sorted(BLOG_DIR.glob('*.html')):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if 'rel="canonical"' in txt or "rel='canonical'" in txt:
        continue
    url = f'https://praia.digital/blog/{path.name}'
    block = f'  <link rel="canonical" href="{url}">\n'
    txt = txt.replace('</head>', block + '</head>', 1)
    path.write_text(txt, encoding='utf-8')
    FIXED += 1
print(f'INJECTED={FIXED}')
