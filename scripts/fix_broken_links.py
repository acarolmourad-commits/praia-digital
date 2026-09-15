#!/usr/bin/env python3
"""Corrige links internos quebrados em paginas HTML.

Estrategia (somente correcoes de alta confianca):
1. Colapsa segmentos duplicados no caminho (ex.: blog/blog/x.html -> blog/x.html)
2. Se o nome do arquivo existe exatamente 1x no repo, reescreve o link
   para o caminho relativo correto.

Uso: python scripts/fix_broken_links.py [--dry-run]
Gera fix_links_report.json com o resumo.
"""
import os, re, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--dry-run' in sys.argv

all_files, basename_index = set(), {}
for root, dirs, files in os.walk(BASE):
    if '.git' in root.split(os.sep): continue
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), BASE)
        all_files.add(rel)
        basename_index.setdefault(f, []).append(rel)

href_pat = re.compile(r'((?:href|src|action)\s*=\s*)(["\'])(.*?)(\2)', re.I)

def collapse_dup(path):
    out = []
    for p in path.split('/'):
        if out and out[-1] == p: continue
        out.append(p)
    return '/'.join(out)

stats = {'dup_segments': 0, 'unique_basename': 0, 'unresolved': 0}
modified = []

for rel in sorted(f for f in all_files if f.endswith('.html')):
    p = os.path.join(BASE, rel)
    base = os.path.dirname(p)
    try: content = open(p, encoding='utf-8', errors='ignore').read()
    except OSError: continue
    state = {'changed': False}
    def repl(m):
        prefix, q, link, _ = m.groups()
        link = link.strip()
        if (not link or link.startswith(('#','mailto:','tel:','javascript:','data:'))
                or re.match(r'https?://', link) or '${' in link or '{{' in link):
            return m.group(0)
        frag = ''
        if '#' in link:
            link, f = link.split('#', 1); frag = '#' + f
        path = link.split('?')[0]
        if not path: return m.group(0)
        target = (os.path.normpath(os.path.join(BASE, path[1:])) if path.startswith('/')
                  else os.path.normpath(os.path.join(base, path)))
        if os.path.exists(target): return m.group(0)
        cand = collapse_dup(path)
        t2 = (os.path.normpath(os.path.join(BASE, cand[1:])) if cand.startswith('/')
              else os.path.normpath(os.path.join(base, cand)))
        if cand != path and os.path.exists(t2):
            stats['dup_segments'] += 1; state['changed'] = True
            return f'{prefix}{q}{cand}{frag}{q}'
        bn = os.path.basename(path)
        matches = basename_index.get(bn, [])
        if bn and len(matches) == 1:
            newlink = os.path.relpath(os.path.join(BASE, matches[0]), base)
            stats['unique_basename'] += 1; state['changed'] = True
            return f'{prefix}{q}{newlink}{frag}{q}'
        stats['unresolved'] += 1
        return m.group(0)
    new = href_pat.sub(repl, content)
    if state['changed']:
        modified.append(rel)
        if not DRY:
            open(p, 'w', encoding='utf-8').write(new)

report = {'dry_run': DRY, 'files_modified': len(modified), **stats}
json.dump(report, open('fix_links_report.json', 'w'), indent=2, ensure_ascii=False)
print(json.dumps(report, ensure_ascii=False))
