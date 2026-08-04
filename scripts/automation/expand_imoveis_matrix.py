#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expande a matriz de imóveis gerando landings por cidade/tipo.
Reusa template existente e faz patch cirúrgico de title/desc/canonical/og/twitter/keywords/schema/hero.
"""
import os, re, shutil
from pathlib import Path

REPO = Path('.').resolve()
IMOVEIS_DIR = REPO / 'imoveis'
TEMPLATE_PATH = IMOVEIS_DIR / 'apartamento-vista-mar-santos.html'
TEMPLATE = TEMPLATE_PATH.read_text(encoding='utf-8', errors='ignore')

CITIES = [
    ('santos', 'Santos'),
    ('guaruja', 'Guarujá'),
    ('praia-grande', 'Praia Grande'),
    ('bertioga', 'Bertioga'),
    ('itanhaem', 'Itanhaém'),
    ('mongagua', 'Mongaguá'),
    ('sao-vicente', 'São Vicente'),
    ('peruibe', 'Peruíbe'),
]

TYPES = [
    ('apartamento-1-quartos', 'Apartamento 1 quarto', 'Apartamento compacto com ótima localização em {city}. Ideal para quem busca praticidade no litoral.'),
    ('apartamento-2-quartos', 'Apartamento 2 quartos', 'Apartamento 2 quartos em {city}, com espaço para família e lazer completo.'),
    ('studio', 'Studio', 'Studio moderno em {city}, perfeito para investimento ou temporada.'),
    ('casa-condominio', 'Casa em condomínio', 'Casa em condomínio fechado em {city}, com segurança e área de lazer.'),
    ('cobertura', 'Cobertura', 'Cobertura em {city} com vista panorâmica e amplo espaço ao ar livre.'),
    ('casa-terrea', 'Casa térrea', 'Casa térrea em {city}, ideal para famílias que buscam conforto e acessibilidade.'),
    ('frente-mar', 'Frente mar', 'Imóvel frente mar em {city} com vista privilegiada e acesso direto à praia.'),
]

CITY_IMAGE = {
    'santos': 'santos-apartamento-vista-mar',
    'guaruja': 'gua-casa-duplex',
    'praia-grande': 'pg-studio-moderno',
    'bertioga': 'berta-alto-padrao',
    'itanhaem': 'it-casa-terrea',
    'mongagua': 'mon-ap-compacto',
    'sao-vicente': 'sv-cobertura-duplex',
    'peruibe': 'per-sobrado',
}

def replace_once(txt, pattern, repl, flags=0):
    return re.sub(pattern, repl, txt, count=1, flags=flags)

def build(city_slug, city_label, type_slug, type_title, desc_tpl):
    slug = f'{type_slug}-{city_slug}'
    path = IMOVEIS_DIR / f'{slug}.html'
    if path.exists():
        return None
    description = desc_tpl.format(city=city_label)
    title = f'{type_title} em {city_label} | Litoral Prime Imóveis'
    url = f'https://praia.digital/imoveis/{slug}.html'
    img = f'https://praia.digital/img/{CITY_IMAGE[city_slug]}.webp'
    img_png = f'https://praia.digital/img/{CITY_IMAGE[city_slug]}.png'
    keywords = f'{type_title} em {city_label}, {city_label}, imóveis litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe, comprar imóvel litoral, aluguel temporada, apartamento vista mar, casa condomínio, cobertura, investimento imobiliário'

    txt = TEMPLATE
    txt = replace_once(txt, r'<title>\s*.+?\s*</title>', f'<title>{title}</title>', flags=re.I|re.S)
    txt = replace_once(txt, r'<meta\s+name="description"\s+content="[^"]*"', f'<meta name="description" content="{description}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+name="keywords"\s+content="[^"]*"', f'<meta name="keywords" content="{keywords}">', flags=re.I)
    txt = replace_once(txt, r'<link\s+rel="canonical"\s+href="[^"]*"', f'<link rel="canonical" href="{url}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+property="og:title"\s+content="[^"]*"', f'<meta property="og:title" content="{title}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+property="og:description"\s+content="[^"]*"', f'<meta property="og:description" content="{description}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+property="og:image"\s+content="[^"]*"', f'<meta property="og:image" content="{img}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+property="og:url"\s+content="[^"]*"', f'<meta property="og:url" content="{url}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+name="twitter:title"\s+content="[^"]*"', f'<meta name="twitter:title" content="{title}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+name="twitter:description"\s+content="[^"]*"', f'<meta name="twitter:description" content="{description}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+name="twitter:image"\s+content="[^"]*"', f'<meta name="twitter:image" content="{img}">', flags=re.I)
    txt = replace_once(txt, r'<h1>\s*.+?\s*</h1>', f'<h1>{type_title} - {city_label}</h1>', flags=re.I|re.S)
    txt = replace_once(txt, r'<p class="subtitle">\s*.+?\s*</p>', f'<p class="subtitle">{description}</p>', flags=re.I|re.S)
    txt = replace_once(txt, r'<a class="btn-whatsapp"[^>]*>', f'<a class="btn-whatsapp" href="https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20em%20{type_title.replace(" ", "%20")}%20em%20{city_label.replace(" ", "%20")}.%20Pode%20me%20enviar%20mais%20detalhes%3F" target="_blank" rel="noopener">Tenho interesse neste imóvel</a>', flags=re.I)
    txt = replace_once(txt, r'<picture>.*?</picture>', f'<picture><source srcset="{img}" type="image/webp"><img src="{img_png}" alt="{type_title} - {city_label}" loading="lazy" style="width:100%;height:280px;object-fit:cover;border-radius:16px;margin-bottom:16px" width="800" height="600" decoding="async" referrerpolicy="no-referrer-when-downgrade"></picture>', flags=re.I|re.S)
    path.write_text(txt, encoding='utf-8')
    return path

def main():
    created = []
    for city_slug, city_label in CITIES:
        for type_slug, type_title, desc_tpl in TYPES:
            p = build(city_slug, city_label, type_slug, type_title, desc_tpl)
            if p:
                created.append(p.name)
    print('IMOVEIS_CREATED', len(created))
    for c in created:
        print('+', c)

if __name__ == '__main__':
    main()
