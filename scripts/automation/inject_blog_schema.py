import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = REPO / 'blog'

def inject_schema(path: Path) -> bool:
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if 'application/ld+json' in txt:
        return False
    title = re.search(r'<title[^>]*>(.*?)</title>', txt, re.S|re.I)
    title_text = title.group(1).strip() if title else path.stem
    canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', txt, re.I)
    url = canonical.group(1) if canonical else f'https://praia.digital/blog/{path.name}'
    meta = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', txt, re.I)
    desc = meta.group(1) if meta else ''
    block = f'<script type="application/ld+json">\n{{\n  "@context": "https://schema.org",\n  "@type": "BlogPosting",\n  "headline": "{title_text}",\n  "description": "{desc}",\n  "url": "{url}",\n  "author": {{"@type": "Organization", "name": "Praia Digital"}},\n  "publisher": {{"@type": "Organization", "name": "Praia Digital", "url": "https://praia.digital/"}}\n}}\n</script>'
    txt = txt.replace('</head>', block + '\n</head>', 1)
    path.write_text(txt, encoding='utf-8')
    return True

injected = 0
skipped = 0
for path in sorted(BLOG_DIR.glob('*.html')):
    if inject_schema(path):
        injected += 1
    else:
        skipped += 1
print(f'INJECTED={injected} SKIPPED={skipped}')
