#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor SEO rápida pós-geração: checa meta tags essenciais em HTML públicos.
Usa regex leve para title, description, canonical, og:image, keywords, viewport, charset, robots.
"""
import re
import sys
from pathlib import Path

REPO = Path('.').resolve()
PUBLIC_GLOBS = [
    'imoveis/*.html',
    'bairros/*.html',
    'hub/*.html',
    'blog/*.html',
    'cidades/*.html',
    'cidades-expansao/*.html',
    'servicos/*.html',
    'servicos/cidade-servico/*.html',
    'eventos-litoral-paulista-2026-2027/*.html',
    'cases/*.html',
    'curso/*.html',
    'landings/*.html',
    'personas/*.html',
    'propostas/*.html',
    'ferramentas/*.html',
    'anfitrioes/*.html',
    'ia/*.html',
    'investidores/*.html',
    'parcerias-norte/*.html',
    'perfis/*.html',
    'proptech/*.html',
    'subscription/*.html',
    'personas/*.html',
    'contato.html',
    'outreach/**/*.html',
    'litoral-prime-imoveis/**/*.html',
    'docs/**/*.html',
    'marketing/**/*.html',
    'newsletter/**/*.html',
]
EXCLUDE_PATTERNS = [
    r'leads/', r'dashboards/', r'backups/', r'node_modules', r'__pycache__',
    r'\.git/', r'api/', r'backend/', r'automation/', r'litoral-prime-imoveis/automation'
]

def should_exclude(rel):
    for pat in EXCLUDE_PATTERNS:
        if re.search(pat, rel):
            return True
    return False

CHECKS = [
    ('title', r'<title>\s*.+?\s*</title>', re.I),
    ('description', r'<meta\s+name="description"', re.I),
    ('canonical', r'<link\s+rel="canonical"', re.I),
    ('og:image', r'<meta\s+property="og:image"', re.I),
    ('keywords', r'<meta\s+name="keywords"', re.I),
    ('viewport', r'<meta\s+name="viewport"', re.I),
    ('charset', r'<meta\s+charset', re.I),
    ('robots', r'<meta\s+name="robots"', re.I),
]

def audit():
    files = []
    for pattern in PUBLIC_GLOBS:
        files.extend(REPO.glob(pattern))
    # filter
    public = []
    for f in files:
        rel = str(f.relative_to(REPO)).replace('\\', '/')
        if should_exclude(rel):
            continue
        if f.suffix.lower() != '.html':
            continue
        public.append((rel, f))

    issues = {name: 0 for name, _, _ in CHECKS}
    examples = {name: [] for name, _, _ in CHECKS}
    total = 0
    for rel, f in public:
        txt = f.read_text(encoding='utf-8', errors='ignore')
        if not re.search(r'<!DOCTYPE\s+html', txt, re.I):
            continue
        total += 1
        for name, pattern, flags in CHECKS:
            if not re.search(pattern, txt, flags):
                issues[name] += 1
                if len(examples[name]) < 5:
                    examples[name].append(rel)

    print(f'SEO_AUDIT total={total}')
    for name, _, _ in CHECKS:
        print(f'{name}={issues[name]}')
        for ex in examples[name]:
            print('  ', ex)
    return total, issues

if __name__ == '__main__':
    total, issues = audit()
    if any(v > 0 for v in issues.values()):
        print('SEO_AUDIT_FAIL')
        sys.exit(1)
    else:
        print('SEO_AUDIT_OK')
        sys.exit(0)
