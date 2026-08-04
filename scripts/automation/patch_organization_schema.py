#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona Organization schema JSON-LD no footer de páginas públicas que ainda não possuem.
Idempotente: não altera páginas que já têm Organization.
"""
import json, re
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

ORG_SCRIPT = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Litoral Prime Imóveis",
  "url": "https://praia.digital/",
  "logo": "https://praia.digital/img/default-home.jpg",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+55-11-95434-6288",
    "contactType": "sales",
    "availableLanguage": ["Portuguese", "English"]
  },
  "sameAs": [
    "https://wa.me/5511954346288"
  ]
}
</script>\n'''

def should_exclude(rel):
    for pat in EXCLUDE_PATTERNS:
        if re.search(pat, rel):
            return True
    return False

def process(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if '"@type": "Organization"' in txt:
        return False
    if '</head>' not in txt:
        return False
    txt = txt.replace('</head>', ORG_SCRIPT + '</head>', 1)
    path.write_text(txt, encoding='utf-8')
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
    print('ORGANIZATION_ADDED', patched)
    print('TOTAL_SCANNED', len(public))

if __name__ == '__main__':
    main()
