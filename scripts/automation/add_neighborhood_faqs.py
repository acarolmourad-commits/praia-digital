#!/usr/bin/env python3
"""
add_neighborhood_faqs.py
Insere FAQPage JSON-LD com termos de bairro nas páginas de imóveis por cidade.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

neighborhood_faqs = {
    'litoral-prime-imoveis/cidades/santos-imoveis-venda.html': [
        ('Quais bairros de Santos têm mais oferta?', 'Gonzaga, Boqueirão, Embaré, Ponta da Praia e Pompéia concentram a maior parte dos lançamentos e ofertas.'),
        ('Vale a pena comprar no Gonzaga?', 'Sim. É um bairro com alta liquidez, infraestrutura completa e valorização consistente no litoral.'),
        ('Tem opções na orla de Santos?', 'Sim. Há apartamentos e coberturas com vista mar na orla e bairros próximos como Embaré e Ponta da Praia.'),
    ],
    'litoral-prime-imoveis/cidades/guaruja-imoveis-venda.html': [
        ('Quais bairros do Guarujá são mais procurados?', 'Pitangueiras, Enseada, Astúrias e Sorocotuba concentram a maior oferta de apartamentos e casas.'),
        ('O Guarujá é bom para temporada?', 'Sim. Pitangueiras e Enseada têm alta demanda de aluguel por temporada com boa rentabilidade.'),
        ('Tem condomínios fechados no Guarujá?', 'Sim, especialmente em Pitangueiras, Vicente de Carvalho e Pernambuco.'),
    ],
    'litoral-prime-imoveis/cidades/praia-grande-imoveis-venda.html': [
        ('Quais bairros de Praia Grande estão em alta?', 'Boqueirão, Guilhermina, Solemar, Tupi e Vila Tupi são os mais procurados para compra e temporada.'),
        ('Praia Grande é boa para investimento?', 'Sim. Valores mais acessíveis que Santos e Guarujá, com crescimento de oferta e valorização.'),
        ('Tem opções de apartamentos compactos?', 'Sim, studios e apartamentos compactos no Boqueirão, Tupi e Guilhermina são comuns.'),
    ],
    'litoral-prime-imoveis/cidades/bertioga-imoveis-venda.html': [
        ('Quais bairros de Bertioga têm oferta?', 'Boracéia, Riviera de São Lourenço, Jardim São Lourenço e Vista Linda concentram as opções.'),
        ('Bertioga é indicada para temporada?', 'Sim. Riviera e Boracéia são muito procuradas no verão, com alta ocupação.'),
        ('Tem terrenos à venda em Bertioga?', 'Sim. Terrenos em condomínios e áreas planas no centro e na Riviera.'),
    ],
    'litoral-prime-imoveis/cidades/itanhaem-imoveis-venda.html': [
        ('Quais bairros de Itanhaém são mais buscados?', 'Cibratel, Gaivotas, Nova Itanhaém, Costão e Centro concentram a maior oferta.'),
        ('Itanhaém vale a pena para temporada?', 'Sim. Cibratel e Gaivotas têm forte procura sazonal e rentabilidade alta.'),
        ('Tem casas térreas em Itanhaém?', 'Sim. Opções térreas com quintal no centro, Cibratel e Nova Itanhaém.'),
    ],
    'litoral-prime-imoveis/cidades/mongagua-imoveis-venda.html': [
        ('Quais bairros de Mongaguá são mais buscados?', 'Agenor Campos, Vera Cruz, Vila Atlântica, Centro e Balneário têm maior oferta.'),
        ('Mongaguá é boa para temporada?', 'Sim. O centro e a orla movimentam bastante na alta temporada.'),
        ('Tem casas geminadas em Mongaguá?', 'Sim, principalmente no Vera Cruz e Agenor Campos.'),
    ],
    'litoral-prime-imoveis/cidades/sao-vicente-imoveis-venda.html': [
        ('Quais bairros de São Vicente são mais buscados?', 'Gonzaguinha, Catiapoa, Itararé, Centro e Vila São Jorge concentram ofertas.'),
        ('São Vicente tem opções no centro?', 'Sim. Apartamentos compactos e casas no centro e Gonzaguinha são comuns.'),
        ('Tem coberturas em São Vicente?', 'Sim, principalmente em Gonzaguinha e Itararé.'),
    ],
    'litoral-prime-imoveis/cidades/peruibe-imoveis-venda.html': [
        ('Quais bairros de Peruíbe são mais buscados?', 'Centro, Jardim Peruíbe, Rio Preto, Trevo e São Miguel concentram a oferta.'),
        ('Peruíbe é boa para temporada?', 'Sim. Centro e Trevo são procurados por famílias na alta temporada.'),
        ('Tem terrenos em Peruíbe?', 'Sim, especialmente no Trevo e Rio Preto.'),
    ],
}

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

for relative, qas in neighborhood_faqs.items():
    path = BASE / relative
    if not path.exists():
        print('missing', path)
        continue
    text = path.read_text(encoding='utf-8')
    if 'FAQPage' in text:
        print('skip faq exists', relative)
        continue
    items = ','.join(
        item_template.format(question=q, answer=a) for q, a in qas
    )
    block = template.format(items=items)
    if '<head>' not in text:
        print('skip no head', relative)
        continue
    text = text.replace('<head>', '<head>\n' + block, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', relative)
