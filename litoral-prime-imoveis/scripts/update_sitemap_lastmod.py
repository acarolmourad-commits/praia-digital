from pathlib import Path
import re
from datetime import datetime, timezone

REPO = Path('.').resolve()
SITEMAP_XML = REPO / 'sitemap.xml'

if not SITEMAP_XML.exists():
    raise SystemExit('sitemap.xml not found')

now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')

text = SITEMAP_XML.read_text(encoding='utf-8', errors='ignore')
urls = re.findall(r'<loc>(.*?)</loc>', text)

new_blocks = []
for url in urls:
    new_blocks.append(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{now}</lastmod>\n  </url>')

xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
xml.extend(new_blocks)
xml.append('</urlset>')

SITEMAP_XML.write_text('\n'.join(xml), encoding='utf-8')
print('SITEMAP_LASTMOD_UPDATED', len(urls), 'NOW', now)
