import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = REPO / 'blog'

FIXED = 0
for path in sorted(BLOG_DIR.glob('*.html')):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    # pattern 1: <title=...>
    new_txt = re.sub(r'<title=([^>]+)>', r'<title \1>', txt, count=1, flags=re.I)
    # pattern 2: <title text>... with text inline before closing >
    new_txt = re.sub(r'<title([^>]*?)\s*([^<]+?)\s*>', lambda m: '<title' + m.group(1).strip() + '>' + m.group(2).strip() + '</title>' if m.group(1).strip() else '<title>' + m.group(2).strip() + '</title>', new_txt, count=1, flags=re.I)
    if new_txt != txt:
        path.write_text(new_txt, encoding='utf-8')
        FIXED += 1
print(f'FIXED={FIXED}')
