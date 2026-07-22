#!/usr/bin/env python3
"""
add_canonical_and_description.py
Adiciona/atualiza canonical e meta description nas páginas B2B.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
pages = [
    ('automacao-imobiliarias.html', 'Automação para imobiliárias — Praia Digital', 'Automação de e-mails, atendimento e prospecção para imobiliárias do litoral de SP.'),
    ('captacao-imoveis-litoral.html', 'Captação Digital — Praia Digital', 'Captação de leads qualificados para imobiliárias do litoral de SP.'),
    ('solucao-proptech-unificada.html', 'Solução Proptech Unificada — Praia Digital', 'Plataforma unificada de atendimento, captação, gestão e IA para imobiliárias.'),
    ('descricao-imoveis-ia.html', 'Geração de Descrição de Imóveis com IA — Praia Digital', 'Geração de descrições de imóveis com IA para portais e redes.'),
    ('seo-local-imobiliarias.html', 'SEO Local para Imobiliárias — Praia Digital', 'SEO local para imobiliárias do litoral de SP.'),
    ('avaliacao-preco-imoveis.html', 'Avaliação de Preço de Imóvel com IA — Praia Digital', 'Avaliação de preço de imóvel com dados de mercado.'),
    ('consultoria-transformacao-digital-imobiliarias.html', 'Consultoria de Transformação Digital — Praia Digital', 'Consultoria de transformação digital para imobiliárias do litoral de SP.'),
    ('planos-proptech-2026.html', 'Planos Proptech — Praia Digital', 'Planos modulares de IA e automação para imobiliárias do litoral de SP.'),
]

canonical_tpl = '<link rel="canonical" href="https://acarolmourad-commits.github.io/praia-digital/{page}">'
desc_tpl = '<meta name="description" content="{desc}">'

for page, title, desc in pages:
    path = BASE / page
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    changed = False

    # Ensure meta charset + viewport + description in head, before </head>
    if desc_tpl.format(desc=desc) not in text:
        text = text.replace('</head>', f'  {desc_tpl.format(desc=desc)}\n</head>', 1)
        changed = True

    # Ensure canonical before </head>
    canonical = canonical_tpl.format(page=page)
    if canonical not in text:
        text = text.replace('</head>', f'  {canonical}\n</head>', 1)
        changed = True

    if changed:
        path.write_text(text, encoding='utf-8')
        print('updated', page)
    else:
        print('skip', page)
