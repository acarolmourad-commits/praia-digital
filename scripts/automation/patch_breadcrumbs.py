#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona BreadcrumbList JSON-LD em massa para páginas públicas que ainda não possuem breadcrumbs.
"""
import os, re, json
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

def get_title(txt):
    m = re.search(r'<title>\s*(.+?)\s*</title>', txt, re.I|re.S)
    return m.group(1) if m else 'Página'

def build_breadcrumbs(path: Path, txt: str):
    title = get_title(txt)
    rel = str(path.relative_to(REPO)).replace('\\', '/')
    parts = rel.split('/')
    items = [{"@type": "ListItem", "position": 1, "name": "Início", "item": "https://praia.digital/index.html"}]
    pos = 2
    cum = []
    for part in parts[:-1]:
        cum.append(part)
        slug = part.replace('.html', '')
        url = f'https://praia.digital/{"/".join(cum)}/'
        name = slug.replace('-', ' ').title()
        if name.lower() == 'litoral-prime-imoveis':
            name = 'Litoral Prime'
        items.append({"@type": "ListItem", "position": pos, "name": name, "item": url})
        pos += 1
    # last item = current page
    current = parts[-1].replace('.html', '').replace('-', ' ').title()
    url = f'https://praia.digital/{rel}'
    items.append({"@type": "ListItem", "position": pos, "name": current, "item": url})
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }

def process(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if 'BreadcrumbList' in txt:
        return False
    data = build_breadcrumbs(path, txt)
    script = f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>\n'
    txt = txt.replace('</head>', script + '</head>', 1)
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
    print('BREADCRUMB_ADDED', patched)
    print('TOTAL_SCANNED', len(public))

if __name__ == '__main__':
    main()
