from pathlib import Path

img_map = {
    'santos': 'img/santos-apartamento-vista-mar.webp',
    'guaruja': 'img/gua-casa-duplex.webp',
    'praia-grande': 'img/pg-studio-moderno.webp',
    'bertioga': 'img/berta-alto-padrao.webp',
    'itanhaem': 'img/it-casa-terrea.webp',
    'mongagua': 'img/mon-ap-compacto.webp',
    'sao-vicente': 'img/sv-cobertura-duplex.webp',
    'peruibe': 'img/per-sobrado.webp',
    'caraguatatuba': 'img/default-home.jpg',
    'ilhabela': 'img/default-home.jpg',
    'sao-sebastiao': 'img/default-home.jpg',
    'ubatuba': 'img/default-home.jpg',
}

city_context = {
    'santos': 'Santos tem orla valorizada, temporada forte e perfil de comprador que exige clareza na documentação e no plano de venda.',
    'guaruja': 'Guarujá combina veraneio, temporada e liquidez concentrada em Pitangueiras, Astúrias e Enseada.',
    'praia-grande': 'Praia Grande oferece oferta diversificada em Guilhermina, Ocian e Tupi, com alta procura por moradia e temporada.',
    'bertioga': 'Bertioga une natureza, alto padrão e acessos diferenciados; atenção a área de marinha e regulamentações locais.',
    'itanhaem': 'Itanhaém cresce em oferta acessível e ambiente familiar, com destaques em Cibratel e Jardim São Fernando.',
    'mongagua': 'Mongaguá cresce como opção acessível e tranquila, com destaque para Centro, Jardim São Paulo e Balneário.',
    'sao-vicente': 'São Vicente combina história, orla e oferta econômica a médio padrão em Centro, Gonzaguinha e Itararé.',
    'peruibe': 'Peruíbe se destaca por tranquilidade, segunda residência e natureza preservada em Centro, Jardim São Paulo e Balneário.',
    'caraguatatuba': 'Caraguatatuba tem temporada forte e diversificação de oferta em Centro, Jaguaribe e Prainha.',
    'ilhabela': 'Ilhabela tem perfil exclusivo e sazonalidade forte, com atenção a área de marinha e acesso por ferry-boat.',
    'sao-sebastiao': 'São Sebastião cresce em alto padrão e temporada, com destaque para Centro Histórico, Juquehy e Maresias.',
    'ubatuba': 'Ubatuba combina natureza e temporada, com oferta em Centro, Itaguá e São Lourenço e atenção a restrições ambientais.',
}

base = Path('imoveis')
updated = 0
for p in sorted(base.glob('*.html')):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    stem = p.stem

    city_slug = None
    for c in city_context:
        if stem.endswith('-' + c):
            city_slug = c
            break
    if not city_slug:
        continue

    img = img_map.get(city_slug, 'img/default-home.jpg')
    city_name = city_slug.replace('-', ' ').title()
    context = city_context[city_slug]

    # Normalize branding
    txt = txt.replace('Litoral Prime Imóveis', 'Praia Digital')
    txt = txt.replace('Litoral Prime', 'Praia Digital')

    # Update image references
    if 'img/default-home.jpg' in txt:
        txt = txt.replace('img/default-home.jpg', img)

    # Update OG/twitter image
    txt = txt.replace('content="https://praia.digital/img/default-home.jpg"', f'content="https://praia.digital/{img}"')

    # Update title if generic
    if '<title>Apartamento' in txt or '<title>Casa' in txt:
        title_start = txt.find('<title>') + 7
        title_end = txt.find('</title>')
        if title_start > 6 and title_end > title_start:
            old_title = txt[title_start:title_end]
            # Remove "| Litoral Prime Imóveis" if present
            new_title = old_title.split(' | ')[0].strip()
            txt = txt.replace(f'<title>{old_title}</title>', f'<title>{new_title} | Praia Digital</title>')

    # Update description
    old_desc = 'litoral de São Paulo, acesso fácil. oportunidade única, bem localizado.'
    new_desc = context
    if old_desc in txt:
        txt = txt.replace(old_desc, new_desc)
    elif f'{city_name}: {city_name}: ' in txt:
        txt = txt.replace(f'{city_name}: {city_name}: ', f'{city_name}: ')

    # Add local data section if not present
    if 'Dados locais que importam' not in txt:
        marker = '<section class="servicos-section">\n      <h2>Destaques</h2>'
        local_section = f'<section class="servicos-section">\n      <h2>Dados locais que importam</h2>\n      <p>{context}</p>\n    </section>\n\n    <section class="servicos-section">\n      <h2>Destaques</h2>'
        txt = txt.replace(marker, local_section, 1)

    p.write_text(txt, encoding='utf-8')
    updated += 1

print('updated ' + str(updated) + ' property pages')
