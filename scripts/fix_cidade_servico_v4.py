from pathlib import Path
import re

service_map = {
    'automacao': 'Automação Imobiliária',
    'avaliacao': 'Avaliação de Imóveis',
    'captacao': 'Captação de Imóveis',
    'consultoria': 'Consultoria Imobiliária',
    'descricao-ia': 'Descrição com IA',
    'venda-imovel': 'Venda de Imóveis',
}

city_names = {
    'santos': 'Santos',
    'guaruja': 'Guarujá',
    'praia-grande': 'Praia Grande',
    'bertioga': 'Bertioga',
    'itanhaem': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'sao-vicente': 'São Vicente',
    'peruibe': 'Peruíbe',
}

base = Path('servicos/cidade-servico')
for p in sorted(base.glob('*.html')):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    stem = p.stem

    # find city prefix
    city_slug = None
    service_slug = None
    for c in city_names:
        if stem.startswith(c + '-'):
            city_slug = c
            service_slug = stem[len(c) + 1:]
            break
    if not city_slug or not service_slug:
        print(f'skip {p}: cannot parse city/service')
        continue

    city = city_names[city_slug]
    service = service_map.get(service_slug, service_slug.replace('-', ' ').title())
    title = f'{service} em {city} | Praia Digital'
    description = f'{service} profissional para o mercado imobiliário de {city}. Atendimento rápido e especializado pela Praia Digital.'
    canonical = f'https://praia.digital/servicos/cidade-servico/{stem}.html'
    service_name = service
    area_served = city

    # Remove ||| artifacts
    txt = re.sub(r'\s*\|\|\|\s*\n?', '', txt)

    # Fix all title/og/twitter patterns that might contain service in city
    for old_city, new_city in city_names.items():
        old_service = 'Automação Imobiliária'
        new_title = f'{service_name} em {city}'
        old_title = f'{old_service} em {old_city}'
        txt = txt.replace(f'{old_title} | Litoral Prime Imóveis', f'{new_title} | Praia Digital')
        txt = txt.replace(f'{old_title} | Praia Digital', f'{new_title} | Praia Digital')
        txt = txt.replace(f'content="{old_title} | Litoral Prime Imóveis"', f'content="{new_title} | Praia Digital"')
        txt = txt.replace(f'content="{old_title} | Praia Digital"', f'content="{new_title} | Praia Digital"')

    # Fix keywords
    old_keywords = re.search(r'<meta name="keywords" content="[^"]*"', txt)
    if old_keywords:
        old_kw = old_keywords.group(0)
        new_kw = f'<meta name="keywords" content="{title}, {description}, imóveis litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe, comprar imóvel litoral, aluguel temporada, apartamento vista mar, casa condomínio, cobertura, investimento imobiliário">'
        txt = txt.replace(old_kw, new_kw)

    # Fix canonical
    txt = re.sub(r'<link rel="canonical" href="https://praia\.digital/servicos/cidade-servico/[^"]*"', f'<link rel="canonical" href="{canonical}"', txt)

    # Fix og:url
    txt = re.sub(r'<meta property="og:url" content="https://praia\.digital/servicos/cidade-servico/[^"]*"', f'<meta property="og:url" content="{canonical}"', txt)

    # Fix Service schema
    txt = re.sub(r'"name":\s*"[^"]*"', f'"name": "{service_name} em {city}"', txt, count=1, flags=re.IGNORECASE)
    txt = re.sub(r'"description":\s*"[^"]*"', f'"description": "{description}"', txt, count=1, flags=re.IGNORECASE)
    txt = re.sub(r'"areaServed":\s*"[^"]*"', f'"areaServed": "{area_served}"', txt, count=1, flags=re.IGNORECASE)

    # Fix provider name
    txt = txt.replace('"provider": {"@type": "LocalBusiness", "name": "Litoral Prime Imóveis"}', '"provider": {"@type": "LocalBusiness", "name": "Praia Digital"}')

    # Fix hreflang
    txt = re.sub(r'<link rel="alternate" hreflang="x-default" href="https://praia\.digital/servicos/cidade-servico/[^"]*" />', f'<link rel="alternate" hreflang="x-default" href="{canonical}" />', txt)
    txt = re.sub(r'<link rel="alternate" hreflang="pt-BR" href="https://praia\.digital/servicos/cidade-servico/[^"]*">', f'<link rel="alternate" hreflang="pt-BR" href="{canonical}">', txt)

    # Fix Organization schema name
    txt = txt.replace('"name": "Litoral Prime Imóveis"', '"name": "Praia Digital"')
    txt = txt.replace('"name": "Litoral Prime Imoveis"', '"name": "Praia Digital"')

    # Fix hero title
    txt = re.sub(r'<h2>Automação Imobiliária em [^<]+</h2>', f'<h2>{service_name} em {city}</h2>', txt, count=1, flags=re.IGNORECASE)

    # Fix price/location line
    txt = re.sub(r'<p class="price">[^<]+</p>', f'<p class="price">{city}</p>', txt, count=1, flags=re.IGNORECASE)

    # Fix service description in body
    txt = re.sub(r'<p>Solução profissional de automação imobiliária para o mercado imobiliário de [^<]+\. Atendimento rápido e especializado pela Litoral Prime\.</p>', f'<p>{description}</p>', txt, count=1, flags=re.IGNORECASE)

    # Fix footer
    txt = txt.replace('© Litoral Prime Imóveis', '© Praia Digital')
    txt = txt.replace('© Litoral Prime Imoveis', '© Praia Digital')

    # Fix breadcrumb city name - replace any known city in breadcrumb span
    for old_city, new_city in city_names.items():
        txt = txt.replace(f'      <span aria-current="page">{old_city}</span>', f'      <span aria-current="page">{new_city}</span>')

    # Fix body city references that might be wrong
    for old_city, new_city in city_names.items():
        # Only replace if it's a different city to avoid unnecessary changes
        if old_city != city_slug:
            txt = txt.replace(f'Atendimento especializado em {old_city}', f'Atendimento especializado em {city}')
            txt = txt.replace(f'Equipe local com conhecimento do mercado de {old_city}', f'Equipe local com conhecimento do mercado de {city}')
            txt = txt.replace(f'Tenho interesse em {service} em {old_city}', f'Tenho interesse em {service} em {city}')

    p.write_text(txt, encoding='utf-8')
    print(f'updated {p}')

print('done')
