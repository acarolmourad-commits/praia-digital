from pathlib import Path
from datetime import datetime

ROOT = Path('.')
OUT = ROOT / 'sitemap.xml'
DATE = datetime.utcnow().strftime('%Y-%m-%d')

SKIP_DIRS = {'.git', '.github', 'node_modules', '__pycache__', 'partials', 'templates', 'backup', 'backups', 'tmp', 'tmp_adversarial', 'scripts', 'tests'}

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(SKIP_DIRS & parts) or path.name.startswith('tmp_')

html_files = [p for p in ROOT.rglob('*.html') if not should_skip(p)]
html_files.sort()

urls = []
for p in html_files:
    rel = p.relative_to(ROOT)
    loc = 'https://praia.digital/' + str(rel).replace('\\', '/')
    urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{DATE}</lastmod>\n    <priority>0.70</priority>\n  </url>")

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n'
OUT.write_text(xml, encoding='utf-8')
print('wrote', OUT, 'entries=', len(urls))
