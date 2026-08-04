#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Padroniza footer em massa nas páginas públicas com:
- © Litoral Prime Imóveis
- WhatsApp, e-mail, telefone
- Links: sitemap.xml, sitemap.html
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
    'sitemap.html',
    '404.html',
    'index.html',
    'litoral-norte.html',
    'litoral-sul.html',
    'eventos-litoral-paulista-2026-2027/*.html',
]
EXCLUDE_PATTERNS = [
    r'leads/', r'dashboards/', r'backups/', r'node_modules', r'__pycache__',
    r'\.git/', r'api/', r'backend/', r'automation/',
]

FOOTER_NEW = '''<footer aria-label="Rodapé">
  <p>© Litoral Prime Imóveis • <a href="https://wa.me/5511954346288">WhatsApp</a> • <a href="mailto:comercial@praia.digital">comercial@praia.digital</a> • (11) 95434-6288</p>
  <p><a href="sitemap.xml">Sitemap</a> · <a href="sitemap.html">Mapa do site</a></p>
</footer>'''

def should_exclude(rel):
    for pat in EXCLUDE_PATTERNS:
        if re.search(pat, rel):
            return True
    return False

def process(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if FOOTER_NEW in txt:
        return False
    # Replace from <footer ...> to </footer>
    new_txt = re.sub(r'<footer\b[^>]*>.*?</footer>', FOOTER_NEW, txt, count=1, flags=re.I|re.S)
    if new_txt == txt:
        return False
    path.write_text(new_txt, encoding='utf-8')
    return True

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
    print('FOOTER_PATCHED', patched)
    print('TOTAL_SCANNED', len(public))

if __name__ == '__main__':
    main()
