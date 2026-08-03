#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera páginas cidade-servico faltantes para servicos/cidade-servico/.
Usa template canônico e deduplica blocos duplicados no <head>.
"""
import re
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
OUT_DIR = REPO / 'servicos' / 'cidade-servico'
OUT_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATE_PATH = REPO / 'servicos' / 'cidade-servico' / 'guaruja-automacao.html'
if not TEMPLATE_PATH.exists():
    raise SystemExit('Template servicos/cidade-servico/guaruja-automacao.html not found')

TEMPLATE = TEMPLATE_PATH.read_text(encoding='utf-8', errors='ignore')

CITIES = {
    'santos': 'Santos',
    'guaruja': 'Guarujá',
    'praia-grande': 'Praia Grande',
    'bertioga': 'Bertioga',
    'itanhaem': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'sao-vicente': 'São Vicente',
    'peruibe': 'Peruíbe',
}

SERVICES = [
    ('automacao', 'Automação Imobiliária', 'Solução profissional de automação imobiliária para o mercado de {city}. Atendimento rápido e especializado pela Litoral Prime.'),
    ('avaliacao', 'Avaliação de Imóveis', 'Avaliação profissional de imóveis para {city} com dados de mercado e experiência local.'),
    ('captacao', 'Captação de Imóveis', 'Captação profissional de imóveis em {city}. Equipe local, processo rápido e transparente.'),
    ('consultoria', 'Consultoria Imobiliária', 'Consultoria especializada para imobiliárias e proprietários em {city}.'),
    ('descricao-ia', 'Descrição de Imóveis com IA', 'Descrições profissionais de imóveis geradas com IA para {city}.'),
    ('venda-imovel', 'Venda de Imóvel', 'Venda de imóvel em {city} com atendimento especializado e marketing profissional.'),
]

def dedup_head(text):
    patterns = [
        r'<meta name="viewport"[^>]*>',
        r'<meta name="description"[^>]*>',
        r'<meta name="keywords"[^>]*>',
        r'<link rel="canonical"[^>]*>',
        r'<meta property="og:type"[^>]*>',
        r'<meta property="og:title"[^>]*>',
        r'<meta property="og:description"[^>]*>',
        r'<meta property="og:image"[^>]*>',
        r'<meta property="og:url"[^>]*>',
        r'<meta name="twitter:card"[^>]*>',
        r'<meta name="twitter:title"[^>]*>',
        r'<meta name="twitter:description"[^>]*>',
        r'<meta name="twitter:image"[^>]*>',
        r'<meta name="robots"[^>]*>',
    ]
    for pat in patterns:
        matches = list(re.finditer(pat, text, re.I))
        if len(matches) > 1:
            text = text[:matches[1].start()] + text[matches[1].end():]
    return text

def replace_placeholders(html, city_slug, service_slug, service_title, description_tpl):
    city_label = CITIES[city_slug]
    description = description_tpl.format(city=city_label)
    url = f'https://praia.digital/servicos/cidade-servico/{city_slug}-{service_slug}.html'
    replacements = {
        '{{city}}': city_label,
        '{{service_title}}': service_title,
        '{{description}}': description,
        '{{url}}': url,
        '{{title}}': f'{service_title} em {city_label} | Litoral Prime Imóveis',
        '{{og_title}}': f'{service_title} em {city_label} | Litoral Prime Imóveis',
        '{{canonical}}': url,
        '{{og_url}}': url,
        '{{keywords}}': f'{service_title} em {city_label}, {city_label}, imóveis litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe, comprar imóvel litoral, aluguel temporada, apartamento vista mar, casa condomínio, cobertura, investimento imobiliário',
        '{{breadcrumb_city}}': city_label,
        '{{breadcrumb_service}}': service_title,
        '{{lead_button}}': f'Solicitar {service_title}',
        '{{lead_subtitle}}': f'Envie seus dados e um especialista entra em contato pelo WhatsApp para {service_title.lower()} em {city_label}.',
        '{{page_heading}}': f'{service_title} em {city_label}',
        '{{price}}': city_label,
        '{{about_title}}': 'Sobre este serviço',
        '{{about_text}}': description,
        '{{about_items}}': '\n'.join([
            f'<li>Atendimento especializado em {city_label}</li>',
            '<li>Equipe local com conhecimento do mercado</li>',
            '<li>Processo rápido e transparente</li>',
            '<li>Acompanhamento completo</li>',
        ]),
        '{{related_title}}': 'Páginas relacionadas',
        '{{related_hub}}': f'../../cidades/{city_slug}.html',
        '{{related_hub_label}}': f'Hub {city_label}',
        '{{related_services}}': '../servicos.html',
        '{{related_services_label}}': 'Todos os serviços',
        '{{related_listings}}': '../../imoveis.html',
        '{{related_listings_label}}': 'Ver todos os imóveis',
        '{{cities_title}}': 'Por cidade',
        '{{operation_title}}': 'Operação rápida',
    }
    for key, value in replacements.items():
        html = html.replace(key, value)
    return html

created = []
updated = []
skipped = []
for city_slug, city_label in CITIES.items():
    for service_slug, service_title, description_tpl in SERVICES:
        slug = f'{city_slug}-{service_slug}'
        out = OUT_DIR / f'{slug}.html'
        html = TEMPLATE
        html = replace_placeholders(html, city_slug, service_slug, service_title, description_tpl)
        html = dedup_head(html)
        if out.exists():
            updated.append(slug)
        else:
            created.append(slug)
        out.write_text(html, encoding='utf-8')

print('CITY_SERVICE_CREATED', len(created))
for s in created:
    print('-', s)
print('CITY_SERVICE_UPDATED', len(updated))
for s in updated:
    print('~', s)
