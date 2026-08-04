#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona/ajusta alt text em massa nas imagens de páginas públicas.
Gera alt descritivo baseado em slug/título quando ausente ou genérico.
"""
import os
import re
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

def slug_to_title(slug: str) -> str:
    return slug.replace('-', ' ').title()

def build_alt(path: Path, txt: str) -> str:
    slug = path.stem
    title_m = re.search(r'<title>\s*(.+?)\s*</title>', txt, re.I|re.S)
    title = title_m.group(1) if title_m else slug_to_title(slug)
    # Remove site name suffix
    title = re.split(r'\s*[|–-]\s*Litoral Prime', title)[0].strip()
    if not title:
        title = slug_to_title(slug)
    return title

def is_good_alt(val: str) -> bool:
    if not val:
        return False
    low = val.lower()
    if low in ['', 'image', 'img', 'photo', 'foto', 'imagem']:
        return False
    words = val.split()
    if len(words) >= 4:
        return True
    # treat slug-like text as bad even if 2-3 words
    if re.search(r'[a-z]+-[a-z]+', low):
        return False
    return True

def process(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    original = txt
    imgs = list(re.finditer(r'<img[^>]+>', txt, re.I))
    if not imgs:
        return False
    changed = False
    for m in imgs:
        tag = m.group(0)
        alt_m = re.search(r'\balt="([^"]*)"', tag, re.I)
        if alt_m:
            alt_val = alt_m.group(1).strip()
            if is_good_alt(alt_val):
                continue
            new_alt = build_alt(path, txt)
            new_tag = tag.replace(f'alt="{alt_val}"', f'alt="{new_alt}"', 1)
            txt = txt.replace(tag, new_tag, 1)
            changed = True
        else:
            new_alt = build_alt(path, txt)
            new_tag = tag.replace('>', f' alt="{new_alt}">', 1)
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
    print('ALT_TEXT_PATCHED', patched)
    print('TOTAL_SCANNED', len(public))

if __name__ == '__main__':
    main()
