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
    txt = txt.replace('Automação Imobiliária em Guarujá | Litoral Prime Imóveis', title)
    txt = txt.replace('Automação Imobiliária em Santos | Litoral Prime Imóveis', title)
    txt = txt.replace('Automação Imobiliária em Bertioga | Litoral Prime Imóveis', title)

    # Fix description
    txt = txt.replace('Solução profissional de automação imobiliária para o mercado imobiliário de Guarujá. Atendimento rápido e especializado pela Litoral Prime.', description)
    txt = txt.replace('Solução profissional de automação imobiliária para o mercado imobiliário de Santos. Atendimento rápido e especializado pela Litoral Prime.', description)
    txt = txt.replace('Solução profissional de automação imobiliária para o mercado imobiliário de Bertioga. Atendimento rápido e especializado pela Litoral Prime.', description)

    # Fix canonical
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/santos-avaliacao.html"', f'href="{canonical}"')
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/guaruja-captacao.html"', f'href="{canonical}"')
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/bertioga-consultoria.html"', f'href="{canonical}"')

    # Fix og:title
    txt = txt.replace('content="Automação Imobiliária em Guarujá | Litoral Prime Imóveis"', f'content="{title}"')
    txt = txt.replace('content="Automação Imobiliária em Santos | Litoral Prime Imóveis"', f'content="{title}"')
    txt = txt.replace('content="Automação Imobiliária em Bertioga | Litoral Prime Imóveis"', f'content="{title}"')

    # Fix og:description
    txt = txt.replace('content="Solução profissional de automação imobiliária para o mercado imobiliário de Guarujá. Atendimento rápido e especializado pela Litoral Prime."', f'content="{description}"')
    txt = txt.replace('content="Solução profissional de automação imobiliária para o mercado imobiliário de Santos. Atendimento rápido e especializado pela Litoral Prime."', f'content="{description}"')
    txt = txt.replace('content="Solução profissional de automação imobiliária para o mercado imobiliário de Bertioga. Atendimento rápido e especializado pela Litoral Prime."', f'content="{description}"')

    # Fix og:url
    txt = txt.replace('content="https://praia.digital/servicos/cidade-servico/santos-avaliacao.html"', f'content="{canonical}"')
    txt = txt.replace('content="https://praia.digital/servicos/cidade-servico/guaruja-captacao.html"', f'content="{canonical}"')
    txt = txt.replace('content="https://praia.digital/servicos/cidade-servico/bertioga-consultoria.html"', f'content="{canonical}"')

    # Fix Service schema
    txt = txt.replace('"name": "Automação Imobiliária em Guarujá"', f'"name": "{service_name} em {city}"')
    txt = txt.replace('"name": "Automação Imobiliária em Santos"', f'"name": "{service_name} em {city}"')
    txt = txt.replace('"name": "Automação Imobiliária em Bertioga"', f'"name": "{service_name} em {city}"')
    txt = txt.replace('"description": "Solução profissional de automação imobiliária para o mercado imobiliário de Guarujá. Atendimento rápido e especializado pela Litoral Prime."', f'"description": "{description}"')
    txt = txt.replace('"description": "Solução profissional de automação imobiliária para o mercado imobiliário de Santos. Atendimento rápido e especializado pela Litoral Prime."', f'"description": "{description}"')
    txt = txt.replace('"description": "Solução profissional de automação imobiliária para o mercado imobiliário de Bertioga. Atendimento rápido e especializado pela Litoral Prime."', f'"description": "{description}"')
    txt = txt.replace('"areaServed": "Guarujá"', f'"areaServed": "{area_served}"')
    txt = txt.replace('"areaServed": "Santos"', f'"areaServed": "{area_served}"')
    txt = txt.replace('"areaServed": "Bertioga"', f'"areaServed": "{area_served}"')

    # Fix provider name
    txt = txt.replace('"provider": {"@type": "LocalBusiness", "name": "Litoral Prime Imóveis"}', '"provider": {"@type": "LocalBusiness", "name": "Praia Digital"}')

    # Fix hreflang x-default
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/santos-avaliacao.html" />', f'href="{canonical}" />')
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/guaruja-captacao.html" />', f'href="{canonical}" />')
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/bertioga-consultoria.html" />', f'href="{canonical}" />')

    # Fix hreflang pt-BR
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/guaruja-automacao.html">', f'href="{canonical}">')
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/santos-automacao.html">', f'href="{canonical}">')
    txt = txt.replace('href="https://praia.digital/servicos/cidade-servico/bertioga-automacao.html">', f'href="{canonical}">')

    # Fix Organization schema name
    txt = txt.replace('"name": "Litoral Prime Imóveis"', '"name": "Praia Digital"')
    txt = txt.replace('"name": "Litoral Prime Imoveis"', '"name": "Praia Digital"')

    # Fix hero title
    txt = txt.replace('<h2>Automação Imobiliária em Guarujá</h2>', f'<h2>{service_name} em {city}</h2>')
    txt = txt.replace('<h2>Automação Imobiliária em Santos</h2>', f'<h2>{service_name} em {city}</h2>')
    txt = txt.replace('<h2>Automação Imobiliária em Bertioga</h2>', f'<h2>{service_name} em {city}</h2>')

    # Fix price/location line
    txt = txt.replace('<p class="price">Guarujá</p>', f'<p class="price">{city}</p>')
    txt = txt.replace('<p class="price">Santos</p>', f'<p class="price">{city}</p>')
    txt = txt.replace('<p class="price">Bertioga</p>', f'<p class="price">{city}</p>')

    # Fix service description in body
    txt = txt.replace('Solução profissional de automação imobiliária para o mercado imobiliário de Guarujá. Atendimento rápido e especializado pela Litoral Prime.', description)
    txt = txt.replace('Solução profissional de automação imobiliária para o mercado imobiliário de Santos. Atendimento rápido e especializado pela Litoral Prime.', description)
    txt = txt.replace('Solução profissional de automação imobiliária para o mercado imobiliário de Bertioga. Atendimento rápido e especializado pela Litoral Prime.', description)

    # Fix footer
    txt = txt.replace('© Litoral Prime Imóveis', '© Praia Digital')
    txt = txt.replace('© Litoral Prime Imoveis', '© Praia Digital')

    # Fix breadcrumb city name
    txt = txt.replace('      <span aria-current="page">Guarujá</span>', f'      <span aria-current="page">{city}</span>')
    txt = txt.replace('      <span aria-current="page">Santos</span>', f'      <span aria-current="page">{city}</span>')
    txt = txt.replace('      <span aria-current="page">Bertioga</span>', f'      <span aria-current="page">{city}</span>')

    p.write_text(txt, encoding='utf-8')
    print(f'updated {p}')

print('done')
