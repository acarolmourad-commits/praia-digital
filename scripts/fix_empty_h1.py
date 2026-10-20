#!/usr/bin/env python3
"""Preenche <h1> vazios/quebrados com texto derivado do <title> da pagina.
Roda no build (deploy) e antes do SEO audit. Idempotente."""
import os, re, sys

fixed = []
for root, _, files in os.walk('.'):
    if '.git' in root:
        continue
    for fn in files:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        try:
            html = open(path, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
        if not m or m.group(1).strip() not in ('', '>'):
            continue
        t = re.search(r'<title>(.*?)</title>', html, re.S)
        title = (t.group(1).strip() if t else '') or fn.replace('.html', '').replace('-', ' ').title()
        title = title.split('|')[0].split('—')[0].strip()
        if not title:
            continue
        html = html[:m.start(1)] + title + html[m.end(1):]
        open(path, 'w', encoding='utf-8').write(html)
        fixed.append(path)

print(f'fix_empty_h1: {len(fixed)} pagina(s) corrigida(s)')
for f in fixed[:20]:
    print(' -', f)
sys.exit(0)
