#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de checklist de revisão SEO para Praia Digital.
Varre páginas .html e gera checklist consolidada por página.
"""

import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'docs/materiais/checklist-revisao-seo-gerada-praia-digital-2026.md')


def pages():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'scripts']
        for name in files:
            if not name.endswith('.html'):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, ROOT)
            if rel.startswith('scripts/') or rel.startswith('docs/startup-proptech/'):
                continue
            yield rel.replace('\\', '/')


def audit(path):
    issues = []
    full = os.path.join(ROOT, path)
    txt = ''
    try:
        txt = open(full, 'r', encoding='utf-8', errors='ignore').read()
    except Exception:
        issues.append('erro-leitura')
        return issues
    if '<title>' not in txt.lower():
        issues.append('sem-title')
    if '<meta name="description"' not in txt.lower():
        issues.append('sem-meta-description')
    if '<h1>' not in txt.lower():
        issues.append('sem-h1')
    if 'rel="canonical"' not in txt.lower():
        issues.append('sem-canonical')
    if 'www.' not in txt.lower() and 'http' not in txt.lower():
        issues.append('links-internos-recomendado')
    return issues


def build(seq):
    today = datetime.now().strftime('%d/%m/%Y %H:%M')
    lines = ['# Checklist de Revisão SEO — Praia Digital\n', f'Gerado em {today}\n', 'Revisar e marcar conforme publicação/ajuste.\n']
    total = 0
    with_issues = 0
    for path in seq:
        total += 1
        issues = audit(path)
        if issues:
            with_issues += 1
            lines.append(f'- [ ] {path} | {", ".join(issues)}')
        else:
            lines.append(f'- [x] {path} | ok')
    lines += ['', f'Total de páginas: {total}', f'Páginas com ajustes pendentes: {with_issues}']
    return '\n'.join(lines)


def main():
    seq = sorted(set(pages()))
    md = build(seq)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(md)
    print('Checklist gerado:', OUT)
    print('Páginas auditadas:', len(seq))


if __name__ == '__main__':
    main()
