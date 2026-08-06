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

city_data = {
    'santos': {
        'name': 'Santos',
        'highlights': [
            'Valorização histórica consistente com liquidez elevada.',
            'Alta temporada e demanda por moradia e temporada.',
            'Acessos rápidos por Imigrantes e Anchieta.',
            'Orla com imóveis com vista mar valorizada.'
        ]
    },
    'guaruja': {
        'name': 'Guarujá',
        'highlights': [
            'Veraneio forte e alta procura por temporada.',
            'Pitangueiras e Astúrias com liquidez alta.',
            'Acesso direto pela Imigrantes/Anchieta.',
            'Condomínios e imóveis com área de lazer.'
        ]
    },
    'praia-grande': {
        'name': 'Praia Grande',
        'highlights': [
            'Alta demanda por imóveis econômicos e médio padrão.',
            'Boa conectividade com São Paulo e Baixada.',
            'Expansão urbana recente e valorização.',
            'Ocian e Tupi com oferta diversificada.'
        ]
    },
    'bertioga': {
        'name': 'Bertioga',
        'highlights': [
            'Mercado com foco em tranquilidade e natureza.',
            'Riviera e Guaratuba com alto padrão.',
            'Acesso por estrada e ferry-boat.',
            'Oportunidades para investimento sustentável.'
        ]
    },
    'itanhaem': {
        'name': 'Itanhaém',
        'highlights': [
            'Crescimento constante e oferta acessível.',
            'Regiões como Cibratel e Jardim São Fernando.',
            'Ambiente familiar e tranquilo.',
            'Boa relação custo-benefício no Litoral Sul.'
        ]
    },
    'mongagua': {
        'name': 'Mongaguá',
        'highlights': [
            'Mercado acessível com demanda crescente.',
            'Regiões como Centro, Jardim São Paulo e Balneário.',
            'Ambiente tranquilo e infraestrutura em expansão.',
            'Ótima opção para primeira moradia no litoral.'
        ]
    },
    'sao-vicente': {
        'name': 'São Vicente',
        'highlights': [
            'História e infraestrutura consolidadas.',
            'Boa oferta em Centro, Gonzaguinha e Itararé.',
            'Acesso fácil por transporte público.',
            'Mercado versátil: econômico a médio padrão.'
        ]
    },
    'peruibe': {
        'name': 'Peruíbe',
        'highlights': [
            'Natureza preservada e tranquilidade.',
            'Oferta focada em segunda moradia e temporada.',
            'Regiões como Centro, Jardim São Paulo e Balneário.',
            'Valorização gradual com demanda crescente.'
        ]
    },
}

base = Path('cidades')
updated = 0
for p in sorted(base.glob('*.html')):
    if p.name in ('index.html', 'sitemap.html'):
        continue
    txt = p.read_text(encoding='utf-8', errors='ignore')
    stem = p.stem

    city_slug = None
    feature = None
    for c in city_data:
        if stem == c:
            city_slug = c
            feature = 'hub'
            break
        elif stem.startswith(c + '-'):
            city_slug = c
            feature = stem[len(c) + 1:]
            break
    if not city_slug:
        continue

    city = city_data[city_slug]['name']
    highlights = city_data[city_slug]['highlights']
    img = img_map.get(city_slug, 'img/default-home.jpg')

    # Normalize branding
    txt = txt.replace('Litoral Prime Imóveis', 'Praia Digital')
    txt = txt.replace('Litoral Prime', 'Praia Digital')

    # Update image references
    if 'img/default-home.jpg' in txt:
        txt = txt.replace('img/default-home.jpg', img)
    if 'img/logo.png' in txt:
        txt = txt.replace('img/logo.png', img)

    # Update OG/twitter image
    txt = txt.replace('content="https://praia.digital/img/default-home.jpg"', f'content="https://praia.digital/{img}"')
    txt = txt.replace('content="https://praia.digital/img/logo.png"', f'content="https://praia.digital/{img}"')

    # Update title if generic
    if 'Litoral Prime Imóveis' in txt:
        txt = txt.replace('Litoral Prime Imóveis', 'Praia Digital')

    # Add local data section if not present
    if 'Dados locais que importam' not in txt:
        if feature == 'hub':
            marker = '</section>\n\n    <h2>Bairros e regiões em destaque</h2>'
            local_section = '</section>\n\n    <h2>Dados locais que importam</h2>\n    <div class="card">\n      <ul class="ticks">\n'
            for h in highlights:
                local_section += f'          <li>{h}</li>\n'
            local_section += '      </ul>\n    </div>\n\n    <h2>Bairros e regiões em destaque</h2>'
            txt = txt.replace(marker, local_section, 1)
        else:
            marker = '<section style="margin-top:18px">'
            local_section = f'<section style="margin-top:18px">\n  <h2>Dados locais que importam</h2>\n  <ul>\n'
            for h in highlights:
                local_section += f'    <li>{h}</li>\n'
            local_section += '  </ul>\n</section>\n\n<section style="margin-top:18px">'
            txt = txt.replace(marker, local_section, 1)

    # Add image before first CTA if not present
    if img not in txt:
        img_html = f'<img src="https://praia.digital/{img}" alt="{city}" style="max-width:100%;border-radius:12px;margin-top:18px;">'
        if feature == 'hub':
            txt = txt.replace('<a class="cta" href="https://wa.me/', img_html + '\n      <a class="cta" href="https://wa.me/', 1)
        else:
            txt = txt.replace('<p><a href="https://wa.me/', img_html + '\n  <p><a href="https://wa.me/', 1)

    p.write_text(txt, encoding='utf-8')
    updated += 1

print('updated ' + str(updated) + ' city pages')
