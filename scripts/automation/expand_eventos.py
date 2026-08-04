#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expande a matriz de eventos em eventos-litoral-paulista-2026-2027/ com páginas de alta intenção.
Reusa template existente e faz patch cirúrgico.
"""
import os, re
from pathlib import Path

REPO = Path('.').resolve()
EVENTOS_DIR = REPO / 'eventos-litoral-paulista-2026-2027'
TEMPLATE_PATH = EVENTOS_DIR / 'santos.html'
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

EVENT_TYPES = [
    ('reveillon', 'Réveillon', 'Réveillon na orla com shows e queima de fogos.'),
    ('carnaval', 'Carnaval', 'Carnaval com blocos, shows e movimento na orla.'),
    ('festivais-verao', 'Festivais de Verão', 'Festivais, feiras gastronômicas e eventos de verão.'),
    ('temporada-alta', 'Temporada Alta', 'Alta temporada: fluxo intenso de turistas e rentabilidade.'),
    ('feriados-prolongados', 'Feriados Prolongados', 'Feriados prolongados movimentam temporada e preços.'),
    ('eventos-culturais', 'Eventos Culturais', 'Shows, exposições e eventos culturais na cidade.'),
    ('festas-tradicionais', 'Festas Tradicionais', 'Festas tradicionais do litoral: patrimônio e movimento.'),
    ('agenda-eventos', 'Agenda de Eventos', 'Agenda completa de eventos da cidade por período.'),
]

def replace_once(txt, pattern, repl, flags=0):
    return re.sub(pattern, repl, txt, count=1, flags=flags)

def build(city_slug, city_label, event_slug, event_title, event_desc):
    slug = f'{event_slug}-{city_slug}'
    path = EVENTOS_DIR / f'{slug}.html'
    if path.exists():
        return None
    title = f'Eventos em {city_label}: {event_title} 2026/2027 | Litoral Prime'
    description = f'{event_desc} em {city_label}. Veja datas, dicas e oportunidades de imóvel para temporada e eventos.'
    keywords = f'eventos {city_label}, {event_title} {city_label}, temporada {city_label}, réveillon {city_label}, carnaval {city_label}, festivais {city_label}, aluguel temporada {city_label}, imóveis {city_label}'
    url = f'https://praia.digital/eventos-litoral-paulista-2026-2027/{slug}.html'
    img = f'https://praia.digital/img/default-home.jpg'
    txt = TEMPLATE
    txt = replace_once(txt, r'<title>\s*.+?\s*</title>', f'<title>{title}</title>', flags=re.I|re.S)
    txt = replace_once(txt, r'<meta\s+name="description"\s+content="[^"]*"', f'<meta name="description" content="{description}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+name="keywords"\s+content="[^"]*"', f'<meta name="keywords" content="{keywords}">', flags=re.I)
    txt = replace_once(txt, r'<link\s+rel="canonical"\s+href="[^"]*"', f'<link rel="canonical" href="{url}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+property="og:title"\s+content="[^"]*"', f'<meta property="og:title" content="{title}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+property="og:description"\s+content="[^"]*"', f'<meta property="og:description" content="{description}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+property="og:url"\s+content="[^"]*"', f'<meta property="og:url" content="{url}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+name="twitter:title"\s+content="[^"]*"', f'<meta name="twitter:title" content="{title}">', flags=re.I)
    txt = replace_once(txt, r'<meta\s+name="twitter:description"\s+content="[^"]*"', f'<meta name="twitter:description" content="{description}">', flags=re.I)
    txt = replace_once(txt, r'<h1>\s*.+?\s*</h1>', f'<h1>Eventos em {city_label}: {event_title} 2026/2027</h1>', flags=re.I|re.S)
    path.write_text(txt, encoding='utf-8')
    return path

def main():
    created = []
    for city_slug, city_label in CITIES:
        for event_slug, event_title, event_desc in EVENT_TYPES:
            p = build(city_slug, city_label, event_slug, event_title, event_desc)
            if p:
                created.append(p.name)
    print('EVENTOS_CREATED', len(created))
    for c in created:
        print('+', c)

if __name__ == '__main__':
    main()
