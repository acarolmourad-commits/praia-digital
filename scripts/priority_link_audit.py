"""Priority-page link auditor: fast, bounded, classifies links."""
import re
from pathlib import Path
from urllib.parse import urlparse

BASE = Path('C:/Users/Carolina/praia-digital')

PRIORITY_PREFIXES = [
    'index.html',
    'contato.html',
    'servicos.html',
    'sobre.html',
    'cidades/',
    'servicos/',
    'blog/',
]

html_files = []
for p in BASE.rglob('*.html'):
    rel = str(p.relative_to(BASE)).replace('\\', '/')
    if any(rel == pfx or rel.startswith(pfx) for pfx in PRIORITY_PREFIXES):
        html_files.append(p)
html_files = sorted(set(html_files))
print(f'Priority pages: {len(html_files)}')

link_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
src_re = re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE)

results = []
for html_path in html_files:
    rel = html_path.relative_to(BASE)
    text = html_path.read_text(encoding='utf-8', errors='ignore')
    refs = link_re.findall(text) + src_re.findall(text)
    for ref in refs:
        if ref.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', '//', 'data:')):
            category = 'LINK_EXTERNO' if ref.startswith(('http://', 'https://')) else 'ESPECIAL'
            results.append((str(rel), ref, category, None))
            continue
        target = ref.lstrip('/').replace('/', '\\')
        exists = (BASE / target).exists()
        if exists:
            category = 'DESTINO_EXISTENTE'
        else:
            category = 'DESTINO_INEXISTENTE'
        results.append((str(rel), ref, category, target))

print('Summary:')
from collections import Counter
c = Counter(r[2] for r in results)
for k, v in c.items():
    print(f'  {k}: {v}')

print('\nBroken/suspicious:')
for source, ref, category, target in results:
    if category == 'DESTINO_INEXISTENTE':
        print(f'{source} -> {ref}')
