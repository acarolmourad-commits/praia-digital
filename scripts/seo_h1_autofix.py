#!/usr/bin/env python3
"""Injeta <h1> visualmente oculto (acessivel) em paginas publicas sem h1.

Regra de alta confianca: a pagina precisa ter <title> e <body>; o h1 usa
o texto do title (antes do '|') com tecnica sr-only, sem alterar o layout.
Paginas noindex/redirect e dirs internos (partials, backup, templates) sao ignoradas.

Uso: python scripts/seo_h1_autofix.py [--dry-run]
"""
import os, re, json, sys, html as H

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.isdir(os.path.join(BASE, '.git')):
    BASE = os.getcwd()
DRY = '--dry-run' in sys.argv
SKIP = ('partials/', 'backup/', 'backups/', 'templates/', '.audit/')

def strip(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

added = 0
modified = []
for root, dirs, files in os.walk(BASE):
    if '.git' in root.split(os.sep): continue
    for f in sorted(files):
        if not f.endswith('.html'): continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, BASE)
        if any(rel.startswith(d) for d in SKIP): continue
        try: c = open(p, encoding='utf-8', errors='ignore').read()
        except OSError: continue
        low = c.lower()
        if '</head>' not in low or 'noindex' in low or 'http-equiv="refresh"' in low: continue
        if '<h1' in low: continue
        m = re.search(r'<title[^>]*>(.*?)</title>', c, re.I | re.S)
        if not m: continue
        t = strip(m.group(1)).split('|')[0].strip()
        if not t: continue
        tag = ('<h1 style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
               'overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0">'
               + H.escape(t) + '</h1>')
        new = re.sub(r'(<body[^>]*>)', lambda mm: mm.group(1) + '\n' + tag, c, count=1, flags=re.I)
        if new != c:
            added += 1
            modified.append(rel)
            if not DRY:
                open(p, 'w', encoding='utf-8').write(new)

report = {'dry_run': DRY, 'h1_added': added, 'files_modified': len(modified)}
json.dump(report, open('seo_h1_report.json', 'w'), indent=2, ensure_ascii=False)
print(json.dumps(report, ensure_ascii=False))
