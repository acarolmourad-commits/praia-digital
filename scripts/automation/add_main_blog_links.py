from pathlib import Path
import re

root = Path('.')

main_posts = [
    'blog/captacao-imoveis-sem-anuncios-pagos-corretores-litoral-2026.html',
    'blog/captacao-leads-whatsapp-litoral-paulista-2026.html',
    'blog/captar-imoveis-litoral-paulista-sem-spam-2026.html',
    'blog/aluguel-por-temporada-dicas-proprietarios-2026.html',
    'blog/investir-imoveis-litoral-paulista-2026.html',
    'blog/checklist-corretor-imoveis-litoral-rotina-2026.html',
    'blog/marketing-redes-sociais-imobiliário-para-corretores-2026-07-20.html',
    'blog/gestao-carteira-imoveis-litoral-2026.html',
    'blog/reducao-custos-imobiliarias-litoral-2026.html',
    'blog/fechamento-parceria-imobiliaria-litoral-checklist-2026.html',
    'blog/distrato-imovel-planta-litoral-paulista-2026.html',
    'blog/documentacao-aluguel-temporada-litoral-checklist-2026.html',
]

links = [
    ('../cases/case-imobiliaria-porto-da-lua-35-leads-2026.html', 'Case real', '35 leads qualificados em 30 dias.'),
    ('../servicos.html', 'Serviços', 'Compra, venda, aluguel e avaliação.'),
    ('../imoveis.html', 'Imóveis', 'Oportunidades no litoral.'),
    ('blog/seo-local-imobiliaria-litoral-passo-a-passo-2026-08-11.html', 'SEO local', 'Passo a passo para imobiliárias.'),
    ('blog/captacao-imoveis-sem-anuncios-pagos-corretores-litoral-2026.html', 'Captação', 'Sem depender só de anúncios.'),
    ('blog/aluguel-por-temporada-dicas-proprietarios-2026.html', 'Temporada', 'Dicas para proprietários.'),
]
cards = '\n'.join([f'        <a class="servico-card" href="{href}"><h3>{title}</h3><p>{desc}</p></a>' for href, title, desc in links])
block = f'    <section class="servicos-section">\n      <h2>Conteúdos recomendados</h2>\n      <div class="servicos-grid">\n{cards}\n      </div>\n    </section>\n'
for rel in main_posts:
    path = root / rel
    if not path.exists():
        print('missing', path)
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Conteúdos recomendados' in text:
        continue
    marker = '</body>'
    if marker not in text:
        print('no body close', path)
        continue
    new_text = text.replace(marker, block + marker, 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', path)
    else:
        print('no-insert', path)
