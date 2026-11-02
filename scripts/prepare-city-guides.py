"""Prepare an isolated navigation preview and scoped sitemap rows using official builders."""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gerar_sitemaps as sitemap

spec = importlib.util.spec_from_file_location('navigation', ROOT / 'scripts/build-navigation.py')
nav = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nav)
data = json.loads((ROOT / 'data/city-guides.json').read_text(encoding='utf-8'))
pages = ['cidades/index.html'] + ['cidades/' + c['slug'] + '.html' for c in data['cities']]
preview = ROOT / '.audit/city-guides/preview'
header = (ROOT / 'partials/header.html').read_text(encoding='utf-8')
for rel in pages:
    text = (ROOT / rel).read_text(encoding='utf-8')
    rendered, ok = nav.transform(text, header)
    assert ok, rel
    target = preview / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding='utf-8')

# Apply the official discovery rules to this scoped preview. Copy robots.txt so
# the same publication restrictions apply, without scanning unrelated archives.
(preview / 'robots.txt').write_bytes((ROOT / 'robots.txt').read_bytes())
public, _ = sitemap.discover_pages(preview)
assert set(pages) <= set(public), 'City pages must satisfy official indexing rules'
generated = ROOT / '.audit/city-guides/sitemap-generated.xml'
sitemap.write(generated, pages)
rows = re.findall(r'<url>.*?</url>', generated.read_text(encoding='utf-8'), re.S)
target = ROOT / 'sitemap.xml'
original = target.read_text(encoding='utf-8')
for row in rows:
    loc = re.search(r'<loc>(.*?)</loc>', row).group(1)
    pattern = r'<url>\s*<loc>' + re.escape(loc) + r'</loc>.*?</url>'
    if re.search(pattern, original, re.S):
        original = re.sub(pattern, lambda m: row, original, flags=re.S)
    else:
        original = original.replace('</urlset>', row + '\n</urlset>')
target.write_text(original, encoding='utf-8')
print('Prepared 17 navigation previews and sitemap rows; unrelated sitemap entries preserved.')
