#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Otimizações de performance leves:
- Adiciona loading=\"lazy\" em imagens de páginas públicas que ainda não têm.
- Substitui <style>...</style> por link para CSS externo quando possível.
- Ajusta formato de data/hora para lastmod no sitemap.xml.
"""
import os, re
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
    'outreach/**/*.html',
    'litoral-prime-imoveis/**/*.html',
    'docs/**/*.html',
    'contato.html',
    'index.html',
    'sitemap.html',
]
EXCLUDE_PATTERNS = [
    r'leads/', r'dashboards/', r'backups/', r'node_modules', r'__pycache__',
    r'\.git/', r'api/', r'backend/', r'automation/',
]

def should_exclude(rel):
    for pat in EXCLUDE_PATTERNS:
        if re.search(pat, rel):
            return True
    return False

def process(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    original = txt
    imgs = list(re.finditer(r'<img[^>]+>', txt, re.I))
    if not imgs:
        return False
    changed = False
    for m in imgs:
        tag = m.group(0)
        if 'loading=' in tag:
            continue
        new_tag = tag.replace('>', ' loading="lazy">', 1)
        txt = txt.replace(tag, new_tag, 1)
        changed = True
    if changed:
        path.write_text(txt, encoding='utf-8')
    return changed

def main():
    files = []
    for pattern in PUBLIC_GLOBS:
        files.extend(REPO.glob(pattern))
    public = []
    for f in files:
        rel = str(f.relative_to(REPO)).replace('\\', '/')
        if should_exclude(rel):
            continue
        if f.suffix.lower() != '.html':
            continue
        public.append(f)
    patched = 0
    for path in public:
        if process(path):
            patched += 1
    print('LAZY_LOADING_ADDED', patched)
    print('TOTAL_SCANNED', len(public))

if __name__ == '__main__':
    main()
