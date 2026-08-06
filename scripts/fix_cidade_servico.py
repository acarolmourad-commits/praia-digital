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
    parts = stem.split('-', 1)
    if len(parts) != 2:
        continue
    city_slug, service_slug = parts
    city = city_names.get(city_slug, city_slug.replace('-', ' ').title())
    service = service_map.get(service_slug, service_slug.replace('-', ' ').title())
    title = f'{service} em {city} | Praia Digital'
    description = f'{service} profissional para o mercado imobiliário de {city}. Atendimento rápido e especializado pela Praia Digital.'
    canonical = f'https://praia.digital/servicos/cidade-servico/{stem}.html'
    service_name = service
    area_served = city

    # Remove ||| artifacts
    txt = re.sub(r'\s*\|\|\|\s*\n?', '', txt)

    # Fix title
    txt = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', txt, count=1, flags=re.IGNORECASE)

    # Fix description
    txt = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{description}"', txt, count=1, flags=re.IGNORECASE)

    # Fix canonical
    txt = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{canonical}"', txt, count=1, flags=re.IGNORECASE)

    # Fix og:title
    txt = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{title}"', txt, count=1, flags=re.IGNORECASE)

    # Fix og:description
    txt = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{description}"', txt, count=1, flags=re.IGNORECASE)

    # Fix og:url
    txt = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{canonical}"', txt, count=1, flags=re.IGNORECASE)

    # Fix Service schema name and description
    txt = re.sub(r'"name":\s*"[^"]*"', f'"name": "{service_name} em {city}"', txt, count=1, flags=re.IGNORECASE)
    txt = re.sub(r'"description":\s*"[^"]*"', f'"description": "{description}"', txt, count=1, flags=re.IGNORECASE)
    txt = re.sub(r'"areaServed":\s*"[^"]*"', f'"areaServed": "{area_served}"', txt, count=1, flags=re.IGNORECASE)

    # Fix provider name
    txt = txt.replace('"name": "Litoral Prime Imóveis"', '"name": "Praia Digital"')
    txt = txt.replace('"name": "Litoral Prime Imoveis"', '"name": "Praia Digital"')

    # Fix hreflang x-default
    txt = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*" />', f'<link rel="alternate" hreflang="x-default" href="{canonical}" />', txt, count=1, flags=re.IGNORECASE)

    # Fix hreflang pt-BR
    txt = re.sub(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*">', f'<link rel="alternate" hreflang="pt-BR" href="{canonical}">', txt, count=1, flags=re.IGNORECASE)

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

    p.write_text(txt, encoding='utf-8')
    print(f'updated {p}')

print('done')
