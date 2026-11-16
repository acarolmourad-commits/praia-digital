#!/usr/bin/env python3
"""Render the public app directory and consistent cross-links; preserve app logic."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    'comprar': ('Comprar e planejar', 'Comece pelo orçamento, registre as premissas e compare cenários com os mesmos dados.'),
    'temporada': ('Organizar a locação', 'Compare modelos de locação e teste a sensibilidade das receitas e despesas.'),
    'anunciar': ('Preparar e revisar anúncios', 'Organize a ficha do imóvel, confira versões e registre o que ainda precisa de confirmação.'),
    'marketplaces': ('Vender em marketplaces', 'Organize os custos da venda antes de definir o preço do produto.'),
}
APPS = [
    ('comparador-cidades', 'Comparador de cidades', 'comprar', 'Compare localidades com critérios ajustados ao seu objetivo.', 'Escolha as cidades e confira as fontes antes de interpretar a classificação.'),
    ('valor-imovel', 'Valor do imóvel', 'comprar', 'Explore uma estimativa de valor a partir das características informadas.', 'Use como ponto de partida; confirme a amostra com imóveis comparáveis.'),
    ('alugar-ou-comprar', 'Alugar ou comprar', 'comprar', 'Compare cenários de patrimônio ao longo do horizonte escolhido.', 'Mantenha prazo, custos e hipóteses consistentes entre as alternativas.'),
    ('custo-de-compra', 'Custos de compra', 'comprar', 'Organize os custos de aquisição além do preço anunciado.', 'Confira taxas e condições do seu caso antes de fechar o orçamento.'),
    ('planejador-entrada', 'Planejador de entrada', 'comprar', 'Planeje o esforço mensal para alcançar uma meta de entrada.', 'Informe uma meta e um prazo que você consiga revisar periodicamente.'),
    ('calculadora-financiamento', 'Simulador de financiamento', 'comprar', 'Compare parcelas e evolução do saldo em SAC e Price.', 'Compare a simulação com as condições completas da proposta da instituição.'),
    ('renda-para-financiar', 'Renda para financiar', 'comprar', 'Explore cenários de renda e comprometimento do orçamento.', 'A simulação não representa aprovação de crédito.'),
    ('calculadora-consorcio', 'Calculadora de consórcio', 'comprar', 'Organize parcelas e hipóteses de um plano de consórcio.', 'Confira o contrato e não trate a contemplação como uma data garantida.'),
    ('calculadora-valorizacao', 'Valorização projetada', 'comprar', 'Veja como hipóteses diferentes afetam o valor projetado.', 'Teste mais de uma hipótese; projeção não é previsão de valorização.'),
    ('checklist-vistoria', 'Checklist de vistoria', 'comprar', 'Registre itens observados e pendências para uma próxima visita.', 'Use o checklist para organizar a visita e registrar o que precisa de avaliação técnica.'),
    ('simulador-roi-temporada', 'ROI de temporada', 'temporada', 'Explore receitas, despesas e resultado de uma operação de temporada.', 'Revise ocupação, diária e custos em cenários diferentes.'),
    ('temporada-ou-anual', 'Temporada ou aluguel anual', 'temporada', 'Compare os dois modelos com premissas preenchidas por você.', 'Considere o mesmo imóvel e registre as diferenças de despesas entre os modelos.'),
    ('oficina-ia-imobiliaria', 'Oficina de IA imobiliária', 'anunciar', 'Prepare briefings e modelos de comunicação para revisão humana.', 'Preencha somente informações confirmadas e revise o texto antes de usar.'),
    ('revisor-anuncios', 'Revisor de anúncios', 'anunciar', 'Compare duas versões com uma ficha conferida do imóvel.', 'Verifique divergências de área, características e condições antes de publicar.'),
    ('relatorio-imovel', 'Relatório do imóvel', 'anunciar', 'Organize informações, fontes e próximos passos em um relatório imprimível.', 'Diferencie dados comprovados de informações pendentes de confirmação.'),
    ('calculadora-precificacao-shopee', 'Precificação para marketplaces', 'marketplaces', 'Simule preço de venda a partir dos custos e parâmetros informados.', 'Confira as tarifas vigentes da plataforma antes de aplicar o resultado.'),
]

def esc(text):
    return html.escape(text, quote=True)

def app_link(app):
    return f'<a href="/apps/{app[0]}/">{esc(app[1])}</a>'

def network(current):
    app = next((a for a in APPS if a[0] == current), None)
    related = [a for a in APPS if a[0] != current and (not app or a[2] == app[2])][:3]
    if app and app[2] == 'marketplaces':
        related = [a for a in APPS if a[0] in ['oficina-ia-imobiliaria', 'revisor-anuncios', 'relatorio-imovel']]
    links = ''.join(f'<li>{app_link(a)}</li>' for a in APPS if a[0] != current)
    next_steps = ''.join(f'<li>{app_link(a)}<p>{esc(a[3])}</p></li>' for a in related)
    hint = f'<p>{esc(app[4])}</p>' if app else ''
    return f'''<section class="pd-network" aria-labelledby="pd-network-title">
<p class="pd-network-eyebrow">Rede Praia Digital</p><h2 id="pd-network-title">Continue sua análise</h2>{hint}
<ul class="pd-next-steps">{next_steps}</ul>
<details><summary>Explorar todos os aplicativos</summary><ul class="pd-network-grid">{links}</ul></details>
<p><a href="/apps/">Catálogo de aplicativos</a> · <a href="/#apps">Roteiros na página inicial</a> · <a href="/servicos.html">Apoio profissional</a></p>
<p class="pd-network-note">Os links não transferem dados automaticamente. Registre suas premissas e confira as limitações de cada ferramenta. Resultados de simulações não são garantias.</p></section>'''

def catalog():
    sections = []
    for key, (title, intro) in GROUPS.items():
        cards = ''.join(f'<article class="pd-catalog-card"><h3>{app_link(a)}</h3><p>{esc(a[3])}</p><p class="pd-catalog-hint">{esc(a[4])}</p></article>' for a in APPS if a[2] == key)
        sections.append(f'<section id="{key}" aria-labelledby="title-{key}"><h2 id="title-{key}">{title}</h2><p>{intro}</p><div class="pd-catalog-grid">{cards}</div></section>')
    nav = ''.join(f'<li><a href="#{key}">{value[0]}</a></li>' for key, value in GROUPS.items())
    schema = {'@context':'https://schema.org','@type':'ItemList','name':'Aplicativos gratuitos Praia Digital','itemListElement':[{'@type':'ListItem','position':i+1,'name':a[1],'url':'https://praia.digital/apps/'+a[0]+'/'} for i,a in enumerate(APPS)]}
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aplicativos gratuitos para imóveis e negócios | Praia Digital</title>
<meta name="description" content="Explore 16 aplicativos gratuitos da Praia Digital: planeje a compra, compare locações, revise anúncios e organize relatórios. Escolha por objetivo e siga para a próxima etapa.">
<meta name="robots" content="index, follow"><link rel="canonical" href="https://praia.digital/apps/">
<meta property="og:title" content="Aplicativos gratuitos — Praia Digital"><meta property="og:description" content="Da pesquisa à revisão do anúncio: escolha a ferramenta para sua próxima decisão."><meta property="og:url" content="https://praia.digital/apps/"><meta property="og:type" content="website">
<link rel="stylesheet" href="/css/app-network.css?v=20261116">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
</head><body class="pd-catalog" data-pd-app>
<a class="pd-skip" href="#pd-catalog-main">Pular para os aplicativos</a>
<header><nav aria-label="Navegação do catálogo"><a href="/">Praia Digital</a><a href="/ferramentas/">Ferramentas</a><a href="/servicos.html">Serviços</a></nav></header>
<section class="pd-catalog-hero" aria-labelledby="pd-app-title"><div class="pd-catalog-width">
<p class="pd-network-eyebrow">16 aplicativos gratuitos · acesso direto</p><h1 id="pd-app-title">Uma ferramenta para cada etapa.</h1><p>Pesquise, simule, confira e organize. Escolha seu objetivo e use os aplicativos em sequência, mantendo suas premissas à mão.</p><a class="pd-catalog-cta" href="#comprar">Encontrar minha ferramenta →</a></div></section>
<main id="pd-catalog-main" class="pd-catalog-width"><nav class="pd-catalog-topics" aria-label="Escolher objetivo"><ul>{nav}</ul></nav>
{''.join(sections)}
<section class="pd-catalog-method" aria-labelledby="method-title"><h2 id="method-title">Como aproveitar melhor os resultados</h2><ol><li><strong>Defina uma pergunta.</strong> Escolha o objetivo e reúna os dados necessários.</li><li><strong>Registre as premissas.</strong> Guarde a data, a origem e as hipóteses de cada simulação.</li><li><strong>Compare cenários.</strong> Mude uma variável por vez para entender seu efeito.</li><li><strong>Confira antes de decidir.</strong> Revise documentos, condições e informações com o profissional adequado.</li></ol><p><a href="/apps/relatorio-imovel/">Organizar os próximos passos em um relatório →</a></p></section>
</main>{network(None)}<footer class="pd-catalog-footer"><a href="/">Praia Digital</a> · <a href="/metodologia.html">Fontes e metodologia</a> · <a href="/contato.html">Fale com a equipe</a></footer></body></html>
'''

def build(root=ROOT):
    for app in APPS:
        path = root / 'apps' / app[0] / 'index.html'
        text = path.read_text()
        text = re.sub(r'\s*<section class="pd-network"[\s\S]*?</section>\s*', '\n', text)
        text = re.sub(r'<link[^>]*href=["\']/css/app-network\.css(?:\?[^"\']*)?["\'][^>]*>\s*', '', text)
        text = text.replace('</head>', '<link rel="stylesheet" href="/css/app-network.css?v=20261116">\n</head>')
        text = text.replace('</body>', network(app[0])+'\n</body>')
        path.write_text(text)
    (root/'apps/index.html').write_text(catalog())

if __name__ == '__main__':
    build()
