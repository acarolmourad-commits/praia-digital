from pathlib import Path
import re

service_names = {
    'automacao': 'Automação Imobiliária',
    'avaliacao': 'Avaliação de Imóveis',
    'captacao': 'Captação de Imóveis',
    'consultoria': 'Consultoria Imobiliária',
    'descricao-ia': 'Descrição com IA',
    'venda-imovel': 'Venda de Imóveis',
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
    }
}

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

base = Path('servicos/cidade-servico')
for p in sorted(base.glob('*.html')):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    stem = p.stem

    city_slug = None
    service_slug = None
    for c in city_data:
        if stem.startswith(c + '-'):
            city_slug = c
            service_slug = stem[len(c) + 1:]
            break
    if not city_slug or not service_slug:
        continue

    city = city_data[city_slug]['name']
    service = service_names.get(service_slug, service_slug.replace('-', ' ').title())
    highlights = city_data[city_slug]['highlights']
    img = img_map.get(city_slug)

    # Insert local highlights after service description if not present
    if 'Dados locais que importam' not in txt:
        marker = '</section>\n\n    <section class="lead-form">'
        highlights_html = '</section>\n\n    <section>\n      <h2>Dados locais que importam</h2>\n      <ul>\n'
        for h in highlights:
            highlights_html += f'        <li>{h}</li>\n'
        highlights_html += '      </ul>\n    </section>\n\n    <section class="lead-form">'
        txt = txt.replace(marker, highlights_html, 1)

    # Add image after Dados locais section if not present
    if img and img not in txt:
        marker = '</section>\n\n    <section class="lead-form">'
        img_html = f'<img src="https://praia.digital/{img}" alt="{city}" style="max-width:100%;border-radius:12px;margin-top:18px;">\n\n    <section class="lead-form">'
        txt = txt.replace(marker, img_html, 1)

    # Update OG image
    txt = txt.replace('content="https://praia.digital/img/default-home.jpg"', f'content="https://praia.digital/{img}"')

    p.write_text(txt, encoding='utf-8')
    print(f'enhanced {p}')

print('done')
