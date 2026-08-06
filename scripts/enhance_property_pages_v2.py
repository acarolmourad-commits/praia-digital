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
    'caraguatatuba': {
        'name': 'Caraguatatuba',
        'highlights': [
            'Temporada forte e diversificação de oferta.',
            'Centro, Jaguaribe e Prainha com bons perfis.',
            'Boa infraestrutura e acesso pelo Tamoios.',
            'Perfil de comprador que valoriza lazer e serviços.'
        ]
    },
    'ilhabela': {
        'name': 'Ilhabela',
        'highlights': [
            'Perfil exclusivo e sazonalidade forte.',
            'Acesso por ferry-boat e restrições ambientais.',
            'Oferta voltada para segunda residência.',
            'Natureza preservada e valorização alta.'
        ]
    },
    'sao-sebastiao': {
        'name': 'São Sebastião',
        'highlights': [
            'Alto padrão e temporada consolidada.',
            'Centro Histórico, Juquehy e Maresias em destaque.',
            'Acesso facilitado pela Tamoios.',
            'Comprador que valoriza exclusividade e lazer.'
        ]
    },
    'ubatuba': {
        'name': 'Ubatuba',
        'highlights': [
            'Natureza e temporada como pilares.',
            'Centro, Itaguá e São Lourenço com oferta diversificada.',
            'Atenção a restrições ambientais e área de marinha.',
            'Ótima opção para quem busca tranquilidade.'
        ]
    },
}

base = Path('imoveis')
updated = 0
for p in sorted(base.glob('*.html')):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    stem = p.stem

    city_slug = None
    for c in city_data:
        if stem.endswith('-' + c):
            city_slug = c
            break
    if not city_slug:
        continue

    city = city_data[city_slug]['name']
    highlights = city_data[city_slug]['highlights']
    img = img_map.get(city_slug, 'img/default-home.jpg')

    # Ensure data section exists
    if 'Dados locais que importam' not in txt:
        marker = '</section>\n\n    <section class="servicos-section">'
        local_section = '</section>\n\n    <section class="servicos-section">\n      <h2>Dados locais que importam</h2>\n      <ul>\n'
        for h in highlights:
            local_section += f'        <li>{h}</li>\n'
        local_section += '      </ul>\n    </section>\n\n    <section class="servicos-section">'
        txt = txt.replace(marker, local_section, 1)

    # Add image before first CTA if not present
    if img not in txt:
        img_html = f'<img src="https://praia.digital/{img}" alt="{city}" style="max-width:100%;border-radius:12px;margin-top:18px;">'
        txt = txt.replace('<a class="btn-whatsapp"', img_html + '\n      <a class="btn-whatsapp"', 1)

    p.write_text(txt, encoding='utf-8')
    updated += 1

print('updated ' + str(updated) + ' property pages')
