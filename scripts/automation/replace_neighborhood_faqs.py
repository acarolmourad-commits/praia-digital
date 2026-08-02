#!/usr/bin/env python3
"""
replace_neighborhood_faqs.py
Substitui FAQPage JSON-LD genérica nas páginas de bairro por conteúdo específico da cidade.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]

neighborhood_faqs = {
    'santos': [
        ('Quais bairros de Santos são mais valorizados?', 'Gonzaga, Pompeia, Boqueirão, Embaré e Centro Historic concentram imóveis mais valorizados e alta procura.'),
        ('Santos é bom para moradia ou temporada?', 'Ótimo para ambos. Há opções de moradia permanente e temporada com alta demanda no verão.'),
        ('Qual a infraestrutura de Santos?', 'Orla, ferry, metrô, ciclovia, shoppings,mercado municipal e bons restaurantes.'),
        ('Como é o preço por m² em Santos?', 'Gonzaga/Pompeia: R$ 8.000–12.000/m²; Boqueirão/Embaré: R$ 6.500–9.000/m²; Centro: R$ 5.500–8.000/m².'),
    ],
    'guaruja': [
        ('Quais bairros do Guarujá são mais buscados?', 'Enseada, Guarujá Mirim, Penteado, Vila Lucy e Vila Maheta concentram ofertas e demanda.'),
        ('Guarujá é bom para temporada?', 'Sim. A orla e as praias atraem turistas no verão; alta taxa de ocupação.'),
        ('Qual a infraestrutura do Guarujá?', 'Orla, ferry,mercados, restaurantes e acesso fácil a Santos e SP.'),
        ('Como é o preço por m² no Guarujá?', 'Enseada/Orla: R$ 6.000–9.000/m²; Guarujá Mirim/Penteado: R$ 5.000–7.500/m²; interior: R$ 4.000–6.000/m².'),
    ],
    'praia-grande': [
        ('Quais bairros de Praia Grande são mais buscados?', 'Ocian, Guartuba, Samambaia, Solemar e Vila Caiçara concentram ofertas.'),
        ('Praia Grande é boa para temporada?', 'Sim. Boa infraestrutura, praias calmas e preços acessíveis atraem turistas.'),
        ('Qual a infraestrutura de Praia Grande?', 'Orla, mercados, farmácias, escolas e fácil acesso à BR-101.'),
        ('Como é o preço por m² em Praia Grande?', 'Ocian/Guartuba: R$ 4.500–7.000/m²; Solemar/Samambaia: R$ 4.000–6.500/m²; interior: R$ 3.500–5.500/m².'),
    ],
    'itanhaem': [
        ('Quais bairros de Itanhaém são mais buscados?', 'Centro, Balneário Itapoan, Gaivota, Jardim Grande e Avenida Pablo Neruda concentram ofertas.'),
        ('Itanhaém é boa para temporada?', 'Sim. Praias tranquilas e preços acessíveis atraem turistas e famílias.'),
        ('Qual a infraestrutura de Itanhaém?', 'Orla, centro comercial,mercado, restaurantes e acesso fácil à BR-101.'),
        ('Como é o preço por m² em Itanhaém?', 'Centro/Orla: R$ 4.000–6.500/m²; Balneário/Jardim Grande: R$ 3.500–5.500/m²; interior: R$ 3.000–4.500/m².'),
    ],
    'mongagua': [
        ('Quais bairros de Mongaguá são mais buscados?', 'Centro, Balneário, Jardim Veneza e Águas Brancas concentram ofertas.'),
        ('Mongaguá é boa para temporada?', 'Sim. Praias calmas e preços acessíveis atraem turistas e famílias.'),
        ('Qual a infraestrutura de Mongaguá?', 'Orla, mercados, farmácias e acesso fácil à BR-101.'),
        ('Como é o preço por m² em Mongaguá?', 'Centro/Orla: R$ 3.800–6.000/m²; Jardim Veneza/Águas Brancas: R$ 3.200–5.500/m²; interior: R$ 2.800–4.500/m².'),
    ],
    'saovicente': [
        ('Quais bairros de São Vicente são mais buscados?', 'Centro, Gonzaguinha, Parque Bitaru e Ponta da Praia concentram ofertas.'),
        ('São Vicente é boa para temporada?', 'Sim. Orla histórica, praias e preços acessíveis atraem turistas.'),
        ('Qual a infraestrutura de São Vicente?', 'Orla, centro histórico, ferry,mercados e fácil acesso a Santos e Guarujá.'),
        ('Como é o preço por m² em São Vicente?', 'Centro/Orla: R$ 4.000–6.500/m²; Gonzaguinha/Ponta da Praia: R$ 3.500–5.500/m²; interior: R$ 3.000–4.500/m².'),
    ],
    'peruibe': [
        ('Quais bairros de Peruíbe são mais buscados?', 'Centro, Balneário, Indaiá e Jardim Peruíbe concentram ofertas.'),
        ('Peruíbe é boa para temporada?', 'Sim. Praias preservadas e preços acessíveis atraem turistas em busca de tranquilidade.'),
        ('Qual a infraestrutura de Peruíbe?', 'Orla,mercados, restaurantes e acesso fácil à BR-101.'),
        ('Como é o preço por m² em Peruíbe?', 'Centro/Orla: R$ 3.500–5.500/m²; Balneário/Indaiá: R$ 3.000–4.800/m²; interior: R$ 2.500–4.000/m².'),
    ],
    'bertioga': [
        ('Quais bairros de Bertioga são mais buscados?', 'Centro, Boracéia, Guaratuba, Indaiá e Riviera de São Lourenço concentram ofertas.'),
        ('Bertioga é boa para temporada?', 'Sim. Praias selvagens e condomínios de alto padrão atraem turistas e investidores.'),
        ('Qual a infraestrutura de Bertioga?', 'Orla, condomínios,mercados e acesso fácil à BR-101.'),
        ('Como é o preço por m² em Bertioga?', 'Riviera/Orla: R$ 7.000–11.000/m²; Centro/Boracéia: R$ 4.500–7.000/m²; interior: R$ 3.500–5.500/m².'),
    ],
    'ubatuba': [
        ('Quais bairros de Ubatuba são mais buscados?', 'Centro, Itaguá, Maranduba, Praia Grande e Ponta da Praia concentram ofertas.'),
        ('Ubatuba é boa para temporada?', 'Sim. Praias paradisíacas e natureza preservada atraem turistas de todo o país.'),
        ('Qual a infraestrutura de Ubatuba?', 'Orla,mercados, restaurantes e fácil acesso às praias.'),
        ('Como é o preço por m² em Ubatuba?', 'Centro/Orla: R$ 5.000–8.500/m²; Itaguá/Maranduba: R$ 4.000–6.500/m²; interior: R$ 3.000–5.000/m².'),
    ],
    'caraguatatuba': [
        ('Quais bairros de Caraguatatuba são mais buscados?', 'Centro, Cocanha, Massaguaçu e Tabatinga concentram ofertas.'),
        ('Caraguatatuba é boa para temporada?', 'Sim. Praias calmas e infraestrutura turística atraem famílias e turistas.'),
        ('Qual a infraestrutura de Caraguatatuba?', 'Orla,mercados, restaurantes e acesso fácil à SP-055.'),
        ('Como é o preço por m² em Caraguatatuba?', 'Centro/Orla: R$ 4.500–7.500/m²; Cocanha/Tabatinga: R$ 3.800–6.000/m²; interior: R$ 3.000–5.000/m².'),
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

files = list((BASE / 'bairros').rglob('*.html'))
updated = 0
skipped = 0
errors = 0
for path in sorted(files):
    rel = path.relative_to(BASE)
    name = path.name
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        errors += 1
        continue
    if 'FAQPage' not in text:
        skipped += 1
        continue
    city = None
    for key in neighborhood_faqs:
        if name.startswith(key):
            city = key
            break
    if city is None:
        for key in neighborhood_faqs:
            if key in rel.parts:
                city = key
                break
    qas = neighborhood_faqs[city]['faqs'] if city else None
    if not qas:
        skipped += 1
        continue
    items = ','.join(item_template.format(question=q, answer=a) for q, a in qas)
    block = template.format(items=items)
    # Replace existing FAQPage block
    m = re.search(r'<script type="application/ld\+json">.*?</script>\s*', text, re.S)
    if not m:
        skipped += 1
        continue
    text = text[:m.start()] + block + text[m.end():]
    try:
        path.write_text(text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    except Exception as e:
        print('write error', rel, e)
        errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
