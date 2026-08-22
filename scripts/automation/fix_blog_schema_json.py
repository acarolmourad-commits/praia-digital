import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = REPO / 'blog'

FIXED = 0
for path in sorted(BLOG_DIR.glob('*.html')):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if 'application/ld+json' not in txt:
        continue
    new_txt = txt
    new_txt = re.sub(r'\{\{', '{', new_txt)
    new_txt = re.sub(r'\}\}', '}', new_txt)
    new_txt = re.sub(r'(datePublished|dateModified)": "([^"]+)\.\d+Z"', lambda m: f'{m.group(1)}": "{m.group(2)[:19]}Z"', new_txt)
    if new_txt != txt:
        path.write_text(new_txt, encoding='utf-8')
        FIXED += 1
print(f'FIXED={FIXED}')
