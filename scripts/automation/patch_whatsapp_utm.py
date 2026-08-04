#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Padroniza CTAs WhatsApp com UTMs por origem em massa nas páginas públicas.
Mapeia diretórios para utm_source e ajusta links wa.me mantendo mensagens existentes.
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

def map_utm(rel: str) -> tuple[str, str]:
    rel = rel.replace('\\', '/')
    if '/imoveis/' in rel:
        return 'imoveis', 'landing-imovel'
    if '/bairros/' in rel:
        return 'bairros', 'bairro'
    if '/cidades/' in rel or '/cidades-expansao/' in rel:
        return 'cidades', 'cidade'
    if '/servicos/cidade-servico/' in rel:
        return 'cidade-servico', 'servico-cidade'
    if '/servicos/' in rel:
        return 'servicos', 'servico'
    if '/blog/' in rel:
        return 'blog', 'blog'
    if '/personas/' in rel:
        return 'personas', 'persona'
    if '/eventos-litoral-paulista-2026-2027/' in rel:
        return 'eventos', 'evento'
    if '/landings/' in rel:
        return 'landings', 'landing'
    if '/cases/' in rel:
        return 'cases', 'case'
    if '/curso/' in rel:
        return 'curso', 'curso'
    if '/propostas/' in rel:
        return 'propostas', 'proposta'
    if '/ferramentas/' in rel:
        return 'ferramentas', 'ferramenta'
    if '/anfitrioes/' in rel:
        return 'anfitrioes', 'anfitriao'
    if '/ia/' in rel:
        return 'ia', 'ia'
    if '/investidores/' in rel:
        return 'investidores', 'investidor'
    if '/parcerias-norte/' in rel:
        return 'parcerias-norte', 'parceria-norte'
    if '/perfis/' in rel:
        return 'perfis', 'perfil'
    if '/proptech/' in rel:
        return 'proptech', 'proptech'
    if '/subscription/' in rel:
        return 'subscription', 'subscription'
    if '/outreach/' in rel:
        return 'outreach', 'outreach'
    if '/litoral-prime-imoveis/' in rel:
        return 'litoral-prime', 'litoral-prime'
    if '/docs/' in rel:
        return 'docs', 'docs'
    if rel in ('contato.html', '404.html', 'sitemap.html', 'index.html'):
        return 'core', 'core'
    return 'outros', 'outros'

def process(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    rel = str(path.relative_to(REPO)).replace('\\', '/')
    source, medium = map_utm(rel)
    # Match all wa.me links
    wa_links = list(re.finditer(r'https://wa\.me/5511954346288\?text=([^"\']+)', txt, re.I))
    if not wa_links:
        return False
    changed = False
    for m in wa_links:
        link = m.group(0)
        text_param = m.group(1)
        # Se já tiver utm_source, ignora
        if 'utm_source=' in link:
            continue
        new_link = f'https://wa.me/5511954346288?text={text_param}&utm_source={source}&utm_medium={medium}&utm_campaign=site'
        txt = txt.replace(link, new_link, 1)
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
    print('WHATSAPP_UTM_PATCHED', patched)
    print('TOTAL_SCANNED', len(public))

if __name__ == '__main__':
    main()
