#!/usr/bin/env python3
"""
add_neighborhood_faqs_imoveis.py
Insere FAQPage JSON-LD nas páginas públicas imoveis/*.html usando city do nome,
com fallback no corpo do HTML e FAQ genérica quando não for possível inferir.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

faq_map = {
    'santos': [
        ('Quais bairros de Santos têm mais oferta?', 'Gonzaga, Boqueirão, Embaré, Ponta da Praia e Pompéia concentram a maior parte dos lançamentos e ofertas.'),
        ('Vale a pena comprar no Gonzaga?', 'Sim. É um bairro com alta liquidez, infraestrutura completa e valorização consistente no litoral.'),
        ('Tem opções na orla de Santos?', 'Sim. Há apartamentos e coberturas com vista mar na orla e bairros próximos como Embaré e Ponta da Praia.'),
    ],
    'guaruja': [
        ('Quais bairros do Guarujá são mais procurados?', 'Pitangueiras, Enseada, Astúrias e Sorocotuba concentram a maior oferta de apartamentos e casas.'),
        ('O Guarujá é bom para temporada?', 'Sim. Pitangueiras e Enseada têm alta demanda de aluguel por temporada com boa rentabilidade.'),
        ('Tem condomínios fechados no Guarujá?', 'Sim, especialmente em Pitangueiras, Vicente de Carvalho e Pernambuco.'),
    ],
    'guarujá': [
        ('Quais bairros do Guarujá são mais procurados?', 'Pitangueiras, Enseada, Astúrias e Sorocotuba concentram a maior oferta de apartamentos e casas.'),
        ('O Guarujá é bom para temporada?', 'Sim. Pitangueiras e Enseada têm alta demanda de aluguel por temporada com boa rentabilidade.'),
        ('Tem condomínios fechados no Guarujá?', 'Sim, especialmente em Pitangueiras, Vicente de Carvalho e Pernambuco.'),
    ],
    'praia-grande': [
        ('Quais bairros de Praia Grande estão em alta?', 'Boqueirão, Guilhermina, Solemar, Tupi e Vila Tupi são os mais procurados para compra e temporada.'),
        ('Praia Grande é boa para investimento?', 'Sim. Valores mais acessíveis que Santos e Guarujá, com crescimento de oferta e valorização.'),
        ('Tem opções de apartamentos compactos?', 'Sim, studios e apartamentos compactos no Boqueirão, Tupi e Guilhermina são comuns.'),
    ],
    'bertioga': [
        ('Quais bairros de Bertioga têm oferta?', 'Boracéia, Riviera de São Lourenço, Jardim São Lourenço e Vista Linda concentram as opções.'),
        ('Bertioga é indicada para temporada?', 'Sim. Riviera e Boracéia são muito procuradas no verão, com alta ocupação.'),
        ('Tem terrenos à venda em Bertioga?', 'Sim. Terrenos em condomínios e áreas planas no centro e na Riviera.'),
    ],
    'itanhaem': [
        ('Quais bairros de Itanhaém são mais buscados?', 'Cibratel, Gaivotas, Nova Itanhaém, Costão e Centro concentram a maior oferta.'),
        ('Itanhaém vale a pena para temporada?', 'Sim. Cibratel e Gaivotas têm forte procura sazonal e rentabilidade alta.'),
        ('Tem casas térreas em Itanhaém?', 'Sim. Opções térreas com quintal no centro, Cibratel e Nova Itanhaém.'),
    ],
    'itanhaém': [
        ('Quais bairros de Itanhaém são mais buscados?', 'Cibratel, Gaivotas, Nova Itanhaém, Costão e Centro concentram a maior oferta.'),
        ('Itanhaém vale a pena para temporada?', 'Sim. Cibratel e Gaivotas têm forte procura sazonal e rentabilidade alta.'),
        ('Tem casas térreas em Itanhaém?', 'Sim. Opções térreas com quintal no centro, Cibratel e Nova Itanhaém.'),
    ],
    'mongagua': [
        ('Quais bairros de Mongaguá são mais buscados?', 'Agenor Campos, Vera Cruz, Vila Atlântica, Centro e Balneário têm maior oferta.'),
        ('Mongaguá é boa para temporada?', 'Sim. O centro e a orla movimentam bastante na alta temporada.'),
        ('Tem casas geminadas em Mongaguá?', 'Sim, principalmente no Vera Cruz e Agenor Campos.'),
    ],
    'mongaguá': [
        ('Quais bairros de Mongaguá são mais buscados?', 'Agenor Campos, Vera Cruz, Vila Atlântica, Centro e Balneário têm maior oferta.'),
        ('Mongaguá é boa para temporada?', 'Sim. O centro e a orla movimentam bastante na alta temporada.'),
        ('Tem casas geminadas em Mongaguá?', 'Sim, principalmente no Vera Cruz e Agenor Campos.'),
    ],
    'sao-vicente': [
        ('Quais bairros de São Vicente são mais buscados?', 'Gonzaguinha, Catiapoa, Itararé, Centro e Vila São Jorge concentram ofertas.'),
        ('São Vicente tem opções no centro?', 'Sim. Apartamentos compactos e casas no centro e Gonzaguinha são comuns.'),
        ('Tem coberturas em São Vicente?', 'Sim, principalmente em Gonzaguinha e Itararé.'),
    ],
    'são-vicente': [
        ('Quais bairros de São Vicente são mais buscados?', 'Gonzaguinha, Catiapoa, Itararé, Centro e Vila São Jorge concentram ofertas.'),
        ('São Vicente tem opções no centro?', 'Sim. Apartamentos compactos e casas no centro e Gonzaguinha são comuns.'),
        ('Tem coberturas em São Vicente?', 'Sim, principalmente em Gonzaguinha e Itararé.'),
    ],
    'peruibe': [
        ('Quais bairros de Peruíbe são mais buscados?', 'Centro, Jardim Peruíbe, Rio Preto, Trevo e São Miguel concentram a oferta.'),
        ('Peruíbe é boa para temporada?', 'Sim. Centro e Trevo são procurados por famílias na alta temporada.'),
        ('Tem terrenos em Peruíbe?', 'Sim, especialmente no Trevo e Rio Preto.'),
    ],
    'peruíbe': [
        ('Quais bairros de Peruíbe são mais buscados?', 'Centro, Jardim Peruíbe, Rio Preto, Trevo e São Miguel concentram a oferta.'),
        ('Peruíbe é boa para temporada?', 'Sim. Centro e Trevo são procurados por famílias na alta temporada.'),
        ('Tem terrenos em Peruíbe?', 'Sim, especialmente no Trevo e Rio Preto.'),
    ],
    'ubatuba': [
        ('Quais bairros de Ubatuba são mais buscados?', 'Centro, Itaguá, Maranduba, Praia Grande e Ponta da Praia concentram ofertas.'),
        ('Ubatuba é boa para temporada?', 'Sim. Alta demanda no verão, especialmente praias da região norte.'),
        ('Tem opções de temporada?', 'Sim. Casas e apartamentos para aluguel temporada em toda a orla.'),
    ],
    'ilhabela': [
        ('Quais bairros de Ilhabela são mais buscados?', 'Centro, Barra Velha, Itaguá e Praia Grande concentram ofertas.'),
        ('Ilhabela é boa para temporada?', 'Sim. Alta procura no verão, com opções para temporada e moradia.'),
        ('Tem casas na orla?', 'Sim. Há opções na orla e bairros próximos.'),
    ],
    'caraguatatuba': [
        ('Quais bairros de Caraguatatuba são mais buscados?', 'Centro, Indaiá, Porto Novo e Praia Grande concentram ofertas.'),
        ('Caraguatatuba é boa para temporada?', 'Sim. Movimento forte no verão e opções para temporada.'),
        ('Tem apartamentos compactos?', 'Sim, studios e apartamentos compactos são comuns no centro.'),
    ],
}

generic = [
    ('Quais tipos de imóveis vocês oferecem?', 'Apartamentos, casas, coberturas, studios e terrenos no litoral de SP.'),
    ('Como encontrar um imóvel?', 'Use a busca por cidade ou WhatsApp para um atendimento personalizado.'),
    ('Vocês ajudam na negociação?', 'Sim. A equipe acompanha proposta, contrato e fechamento.'),
]

template = '''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {items}
  ]
}}
</script>
'''

item_template = '''    {{
      "@type": "Question",
      "name": "{question}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{answer}"
      }}
    }}'''

def pick_city(name: str, body: str):
    lower = name.lower()
    slugs = [
        'santos', 'guaruja', 'guarujá', 'guaruja', 'praia-grande',
        'bertioga', 'itanhaem', 'itanhaém', 'mongagua', 'mongaguá',
        'sao-vicente', 'são-vicente', 'peruibe', 'peruíbe', 'ubatuba', 'ilhabela'
    ]
    for slug in slugs:
        if slug in lower:
            return slug
    snippet = body.lower()
    for slug in slugs:
        if slug in snippet:
            return slug
    for key in faq_map:
        if key in lower or key in snippet:
            return key
    return None

root = BASE / 'imoveis'
updated = 0
skipped = 0
no_city = 0
for path in sorted(root.glob('*.html')):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print('read error', path, e)
        continue
    if 'FAQPage' in text:
        skipped += 1
        continue
    city = pick_city(path.name, text[:4000])
    if not city:
        qas = generic
        no_city += 1
        flag = 'generic'
    else:
        qas = faq_map[city]
        flag = city
    items = ','.join(item_template.format(question=q, answer=a) for q, a in qas)
    block = template.format(items=items)
    if '<head>' not in text:
        print('skip no head', path.name)
        continue
    text = text.replace('<head>', '<head>\n' + block, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', flag, path.name)
    updated += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'generic=', no_city)
