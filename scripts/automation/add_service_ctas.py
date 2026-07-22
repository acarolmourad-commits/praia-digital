#!/usr/bin/env python3
"""
add_service_ctas.py
Add cross-sell CTA blocks to service pages.
Skipped pages:
- solucao-proptech-unificada.html
- planos-proptech-2026.html
- servicos-ia-imobiliarias.html
- ia/index.html
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
pages = [
    'automacao-imobiliarias.html',
    'captacao-imoveis-litoral.html',
    'descricao-imoveis-ia.html',
    'seo-local-imobiliarias.html',
    'avaliacao-preco-imoveis.html',
]

cta_block = '''
        <a class="cta" href="/praia-digital/planos-proptech-2026.html">Ver planos</a>
        <a class="cta" href="/praia-digital/captacao-imoveis-litoral.html">Captação Digital</a>
        <a class="cta" href="/praia-digital/automacao-imobiliarias.html">Automação para imobiliárias</a>
        <a class="cta" href="/praia-digital/descricao-imoveis-ia.html">Geração de descrições com IA</a>
        <a class="cta" href="/praia-digital/seo-local-imobiliarias.html">SEO Local</a>
'''

anchor = '        <p class="disclaimer">Aceitamos agendas rápidas de 15 minutos para entender seu cenário atual.</p>\n'

for page in pages:
    path = BASE / page
    text = path.read_text(encoding='utf-8')
    if 'planos-proptech-2026.html' in text and 'Aceitamos agendas' in text:
        snippet = anchor + cta_block
        if snippet not in text:
            text = text.replace(anchor, snippet, 1)
            path.write_text(text, encoding='utf-8')
            print('updated', page)
        else:
            print('skip', page)
    else:
        print('skip-no-anchor', page)
