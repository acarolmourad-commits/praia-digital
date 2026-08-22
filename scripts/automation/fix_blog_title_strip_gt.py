import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = REPO / 'blog'

FIXED = 0
for path in sorted(BLOG_DIR.glob('*.html')):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    def repl(m):
        text = m.group(1).strip()
        if text.startswith('>'):
            text = text[1:].lstrip()
        return '<title>' + text + '</title>'
    new_txt = re.sub(r'<title(?:=[^>]*)?\s*([^<]+)</title>', repl, txt, count=1, flags=re.I)
    if new_txt != txt:
        path.write_text(new_txt, encoding='utf-8')
        FIXED += 1
print(f'FIXED={FIXED}')
