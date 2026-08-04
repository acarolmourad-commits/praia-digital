#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expande páginas de bairros com conteúdo único e imagens categorizadas por cidade.
Usa os assets existentes em img/ como fallback por cidade.
"""
import os
import re
from pathlib import Path

REPO = Path('.').resolve()
BAIRROS_DIR = REPO / 'bairros'
IMG_DIR = REPO / 'img'

CITY_IMAGE = {
    'bertioga': 'berta-alto-padrao',
    'caraguatatuba': 'caragua-padrao',
    'guaruja': 'gua-casa-duplex',
    'itanhaem': 'it-casa-terrea',
    'mongagua': 'mon-ap-compacto',
    'peruibe': 'per-sobrado',
    'praia': 'pg-studio-moderno',
    'santos': 'santos-apartamento-vista-mar',
    'saovicente': 'sv-cobertura-duplex',
    'ubatuba': 'uba-padrao',
}

CITY_NAME = {
    'bertioga': 'Bertioga',
    'caraguatatuba': 'Caraguatatuba',
    'guaruja': 'Guarujá',
    'itanhaem': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'peruibe': 'Peruíbe',
    'praia': 'Praia Grande',
    'santos': 'Santos',
    'saovicente': 'São Vicente',
    'ubatuba': 'Ubatuba',
}

NEIGHBORHOOD_FEATURES = {
    'centro': 'comércio, serviços e acesso',
    'enseada': 'marina, restaurantes e lazer náutico',
    'boraceia': 'praia tranquila e área verde',
    'guaratuba': 'orla familiar e esportes',
    'indaiá': 'praia e gastronomia local',
    'riviera-de-sao-lourenco': 'alto padrão e segurança 24h',
    'vila-lucy': 'acesso fácil e vida local',
    'vila-maheta': 'quintas e área residencial',
    'penteado': 'vista mar e imóveis de alto padrão',
    'cocanha': 'praia preservada e natureza',
    'massaguacu': 'frente mar e temporada',
    'tabatinga': 'orla familiar e lazer',
    'avenida-pablo-neruda': 'acesso à praia e vida noturna',
    'balneario-itapoan': 'temporada e veraneio',
    'gaivota': 'família e parques',
    'jardim-grande': 'residencial e comércio local',
    'aguas-brancas': 'área verde e silêncio',
    'balneario-verde-mar': 'temporada e rentabilidade',
    'jardim-real': 'acesso à praia e estrutura completa',
    'jardim-vitoria-regia': 'imóveis compactos e alto giro',
    'sao-jose': 'orla e mercado local',
    'vila-caiçara': 'veraneio e vida simples',
    'vila-oricuri': 'acesso à orla e temporada',
    'balneario-praia-peruibe': 'temporada e rentabilidade',
    'jardim-elm-kebler': 'residencial e lazer',
    'sao-joao-batista': 'acesso à praia e lazer',
    'vila-nova-peruibe': 'orla e temporada',
    'aguas-montantes': 'natureza e tranquilidade',
    'camburi': 'surf e aventura',
    'itagua': 'acesso fácil e vida local',
    'jardim-ipe': 'residencial e lazer',
    'vila-ipiranga': 'quintas e família',
    'aguia-de-haia': 'alto padrão e vista mar',
    'boqueirao': 'orla e gastronomia',
    'gonzaga': 'nobre e vista mar',
    'macuco': 'histórico e arquitetura',
    'ponta-da-praia': 'orla e família',
    'embare': 'acesso fácil e vida local',
    'apa': 'tranquilidade e área residencial',
    'vila-mathias': 'comércio e serviços',
    'jose-menino': 'orla e famoso calçadão',
    'campo-grande': 'comércio e acesso',
    'pompeia': 'moderno e vista mar',
    'canoeiras': 'tranquilidade e família',
    'central': 'comércio e serviços',
    'itapua': 'orla e veraneio',
    'leste': 'tradição e vida local',
    'norte': 'turismo e natureza',
    'oeste': 'acesso e estrutura',
    'sul': 'orla e investimento',
}

def infer_city_slug(path: Path):
    name = path.stem
    for c in CITY_NAME:
        if name.startswith(c):
            return c
    return None

def infer_neighborhood(slug: str, city_slug: str):
    return slug[len(city_slug)+1:].replace('-', ' ').title()

def build_content(city_slug: str, neighborhood: str):
    city = CITY_NAME[city_slug]
    feature_key = neighborhood.lower().replace(' ', '-')
    feature = NEIGHBORHOOD_FEATURES.get(feature_key, 'características únicas e boa localização')
    feature2 = NEIGHBORHOOD_FEATURES.get(feature_key, 'oportunidades para compra, venda e temporada')
    return {
        'title': f'{neighborhood} | {city} — Imóveis e Oportunidades | Litoral Prime Imóveis',
        'description': f'Imóveis em {neighborhood}, {city}. Análise de valores, destaques do bairro e oportunidades de compra e temporada com a Litoral Prime.',
        'keywords': f'{neighborhood} {city}, imóveis {neighborhood}, apartamento {neighborhood}, casa {neighborhood}, litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe, comprar imóvel litoral, aluguel temporada, apartamento vista mar, casa condomínio, cobertura, investimento imobiliário',
        'feature': feature,
        'feature2': feature2,
        'city_image': CITY_IMAGE.get(city_slug, 'default-home'),
    }

def ensure_meta(txt: str, name: str, content: str):
    pat = re.compile(r'<meta\s+name="' + re.escape(name) + r'"[^>]*>', re.I)
    replacement = f'<meta name="{name}" content="{content}">'
    if pat.search(txt):
        return pat.sub(replacement, txt, count=1)
    return txt.replace('</head>', f'  {replacement}\n</head>', 1)

def ensure_og_image(txt: str, url: str):
    pat = re.compile(r'<meta\s+property="og:image"\s+content="[^"]*"', re.I)
    replacement = f'<meta property="og:image" content="{url}">'
    if pat.search(txt):
        return pat.sub(replacement, txt, count=1)
    return txt.replace('</head>', f'  {replacement}\n</head>', 1)

def ensure_twitter_image(txt: str, url: str):
    pat = re.compile(r'<meta\s+name="twitter:image"\s+content="[^"]*"', re.I)
    replacement = f'<meta name="twitter:image" content="{url}">'
    if pat.search(txt):
        return pat.sub(replacement, txt, count=1)
    return txt.replace('</head>', f'  {replacement}\n</head>', 1)

def main():
    created = []
    updated = []
    for path in sorted(BAIRROS_DIR.glob('*.html')):
        txt = path.read_text(encoding='utf-8', errors='ignore')
        city_slug = infer_city_slug(path)
        if not city_slug:
            continue
        neighborhood = infer_neighborhood(path.stem, city_slug)
        data = build_content(city_slug, neighborhood)
        original = txt
        # Update title
        txt = re.sub(r'<title>\s*.+?\s*</title>', f'<title>{data["title"]}</title>', txt, flags=re.I|re.S)
        # Update metas
        txt = ensure_meta(txt, 'description', data['description'])
        txt = ensure_meta(txt, 'keywords', data['keywords'])
        txt = ensure_meta(txt, 'robots', 'index, follow')
        # Update canonical to absolute praia.digital
        txt = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"', f'<link rel="canonical" href="https://praia.digital/bairros/{path.name}"', txt, flags=re.I)
        # Update OG/Twitter
        img_url = f'https://praia.digital/img/{data["city_image"]}.webp'
        txt = ensure_og_image(txt, img_url)
        txt = ensure_twitter_image(txt, img_url)
        txt = ensure_meta(txt, 'og:title', data['title'])
        txt = ensure_meta(txt, 'og:description', data['description'])
        txt = ensure_meta(txt, 'twitter:title', data['title'])
        txt = ensure_meta(txt, 'twitter:description', data['description'])
        # Inject hero image after h1
        hero = f'<picture><source srcset="{img_url}" type="image/webp"><img src="https://praia.digital/img/{data["city_image"]}.png" alt="{neighborhood}, {CITY_NAME[city_slug]}" loading="lazy" width="800" height="600" decoding="async"></picture>'
        if '<picture>' not in txt and '<img' not in txt:
            txt = txt.replace('<h1>', f'<h1>{hero}', 1)
        # Add CTA if missing
        if 'wa.me' not in txt:
            txt = txt.replace('</body>', '  <aside aria-label="Contato" style="background:#f6fbf7;border:1px solid #d8f3dc;border-radius:12px;padding:14px;margin:18px 0;text-align:center;"><p style="margin:0 0 8px;color:#064e3b;font-weight:bold;">Fale com um especialista</p><a href="https://wa.me/5511954346288?utm_source=site&utm_medium=whatsapp&utm_campaign=geral" style="display:inline-block;background:#25d366;color:#fff;padding:10px 14px;border-radius:8px;text-decoration:none;font-weight:bold;" rel="noopener">WhatsApp</a></aside>\n</body>', 1)
        if txt != original:
            path.write_text(txt, encoding='utf-8')
            if path.exists():
                updated.append(path.name)
        created.append(path.name)
    print('BAIRROS_UPDATED', len(updated))
    for x in updated:
        print('~', x)

if __name__ == '__main__':
    main()
