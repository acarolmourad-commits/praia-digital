from pathlib import Path
import re

root = Path('.')

city_links = {
    'santos-imoveis-venda': [
        ('../blog/alugar-imovel-temporada-guia-proprietario-litoral-2026.html', 'Aluguel temporada', 'Guia para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-imoveis-sem-anuncios-pagos-corretores-litoral-2026.html', 'Captação orgânica', 'Sem depender só de anúncios.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'guaruja-imoveis-venda': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-leads-whatsapp-litoral-paulista-2026.html', 'Captação por WhatsApp', 'Roteiro para leads qualificados.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'praia-grande-imoveis-venda': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-leads-whatsapp-litoral-paulista-2026.html', 'Captação por WhatsApp', 'Roteiro para leads qualificados.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'bertioga-imoveis-venda': [
        ('../blog/como-escolher-imovel-litoral.html', 'Como escolher imóvel', 'Checklist e custos ocultos.'),
        ('../blog/financiamento-imovel-litoral.html', 'Financiamento', 'Passo a passo para aprovar.'),
        ('../blog/mapas-bairros-seo-imobiliarias-litoral-2026.html', 'SEO por bairro', 'Estratégia local por bairro.'),
        ('../blog/rentabilidade-imoveis-praia.html', 'Rentabilidade na praia', 'Números e cidades.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'itanhaem-imoveis-venda': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-imoveis-sem-anuncios-pagos-corretores-litoral-2026.html', 'Captação sem anúncios', 'Captação orgânica para corretores.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'mongagua-imoveis-venda': [
        ('../blog/como-escolher-imovel-litoral.html', 'Como escolher imóvel', 'Checklist e custos ocultos.'),
        ('../blog/financiamento-imovel-litoral.html', 'Financiamento', 'Passo a passo para aprovar.'),
        ('../blog/seo-local-vs-anuncios-pagos-litoral-2026.html', 'SEO local vs anúncios', 'Quando usar cada canal.'),
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'sao-vicente-imoveis-venda': [
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/temporada-verao-imovel-praia.html', 'Temporada de verão', 'Ocupação, preço e retorno.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/captacao-leads-whatsapp-litoral-paulista-2026.html', 'Captação por WhatsApp', 'Roteiro para leads qualificados.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
    'peruibe-imoveis-venda': [
        ('../blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Aluguel temporada', 'Dicas para proprietários.'),
        ('../blog/investir-imoveis-litoral-paulista-2026.html', 'Investir no litoral', 'O que analisar antes de comprar.'),
        ('../blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
        ('../blog/rentabilidade-imoveis-praia.html', 'Rentabilidade na praia', 'Números e cidades.'),
        ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ],
}

for path in sorted(root.glob('cidades/*-imoveis-venda.html')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Conteúdos recomendados' in text:
        continue
    key = path.stem
    links = city_links.get(key)
    if not links:
        print('skip', path)
        continue
    label = key.replace('-imoveis-venda', '').replace('-', ' ').title()
    cards = '\n'.join([f'        <a class="servico-card" href="{href}"><h3>{title}</h3><p>{desc}</p></a>' for href, title, desc in links])
    block = f'    <section class="servicos-section">\n      <h2>Conteúdos recomendados sobre {label}</h2>\n      <div class="servicos-grid">\n{cards}\n      </div>\n    </section>\n'
    marker = '<footer>'
    if marker not in text:
        print('no footer', path)
        continue
    new_text = text.replace(marker, block + marker, 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', path)
    else:
        print('no-insert', path)
