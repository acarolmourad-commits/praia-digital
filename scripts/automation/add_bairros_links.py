from pathlib import Path
import re

city_name_map = {
    'santos': 'Santos',
    'guaruja': 'Guarujá',
    'guarujá': 'Guarujá',
    'praia-grande': 'Praia Grande',
    'bertioga': 'Bertioga',
    'itanhaem': 'Itanhaém',
    'itanhaém': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'mongaguá': 'Mongaguá',
    'sao-vicente': 'São Vicente',
    'são-vicente': 'São Vicente',
    'peruibe': 'Peruíbe',
    'peruíbe': 'Peruíbe',
}

default_links = [
    ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
    ('../blog/captacao-imoveis-sem-anuncios-pagos-corretores-litoral-2026.html', 'Captação orgânica', 'Sem depender só de anúncios.'),
    ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
    ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
    ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
]

city_links = {
    'santos': [
        ('../blog/alugar-imovel-temporada-guia-proprietario-litoral-2026.html', 'Aluguel temporada', 'Guia para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-imoveis-sem-anuncios-pagos-corretores-litoral-2026.html', 'Captação orgânica', 'Sem depender só de anúncios.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'guarujá': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-leads-whatsapp-litoral-paulista-2026.html', 'Captação por WhatsApp', 'Roteiro para leads qualificados.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'praia grande': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-leads-whatsapp-litoral-paulista-2026.html', 'Captação por WhatsApp', 'Roteiro para leads qualificados.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'bertioga': [
        ('../blog/como-escolher-imovel-litoral.html', 'Como escolher imóvel', 'Checklist e custos ocultos.'),
        ('../blog/financiamento-imovel-litoral.html', 'Financiamento', 'Passo a passo para aprovar.'),
        ('../blog/mapas-bairros-seo-imobiliarias-litoral-2026.html', 'SEO por bairro', 'Estratégia local por bairro.'),
        ('../blog/rentabilidade-imoveis-praia.html', 'Rentabilidade na praia', 'Números e cidades.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'itanhaém': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-imoveis-sem-anuncios-pagos-corretores-litoral-2026.html', 'Captação sem anúncios', 'Captação orgânica para corretores.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'mongaguá': [
        ('../blog/como-escolher-imovel-litoral.html', 'Como escolher imóvel', 'Checklist e custos ocultos.'),
        ('../blog/financiamento-imovel-litoral.html', 'Financiamento', 'Passo a passo para aprovar.'),
        ('../blog/seo-local-vs-anuncios-pagos-litoral-2026.html', 'SEO local vs anúncios', 'Quando usar cada canal.'),
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'são vicente': [
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/temporada-verao-imovel-praia.html', 'Temporada de verão', 'Ocupação, preço e retorno.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-leads-whatsapp-litoral-paulista-2026.html', 'Captação por WhatsApp', 'Roteiro para leads qualificados.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'peruíbe': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/rentabilidade-imoveis-praia.html', 'Rentabilidade na praia', 'Números e cidades.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
}

root = Path('.')
updated = []
skipped = []
for path in sorted(root.glob('bairros/*.html')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Conteúdos recomendados' in text:
        continue
    name = path.stem.lower()
    city_key = None
    for key in city_name_map:
        if name.startswith(key.lower()):
            city_key = city_name_map[key].lower()
            break
    links = city_links.get(city_key) or default_links
    city_label = city_name_map.get(city_key, city_key.replace('-', ' ').title()) if city_key else path.stem.replace('-', ' ').title()
    cards = ''.join([f'<a class="servico-card" href="{href}"><h3>{title}</h3><p>{desc}</p></a>' for href, title, desc in links])
    block = (
        f'    <section class="servicos-section">\n'
        f'      <h2>Conteúdos recomendados sobre {city_label}</h2>\n'
        f'      <div class="servicos-grid">\n'
        f'{cards}\n'
        f'      </div>\n'
        f'    </section>\n'
    )
    new_text = re.sub(r'\s+</div>\n\s*<footer>', '\n' + block + '  <footer>', text, count=1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        updated.append(path.name)
    else:
        skipped.append(path.name)

print('updated', len(updated))
for name in updated:
    print(name)
print('skipped', len(skipped))
for name in skipped:
    print(name)
