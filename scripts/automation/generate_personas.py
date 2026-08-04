#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera páginas de personas para diferentes perfis de comprador/investidor.
"""
from pathlib import Path

REPO = Path('.').resolve()
PERSONAS_DIR = REPO / 'personas'
PERSONAS_DIR.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        'slug': 'investidor',
        'title': 'Imóveis para Investidores no Litoral de SP | Litoral Prime Imóveis',
        'description': 'Oportunidades de investimento imobiliário no litoral de SP: apartamentos, coberturas e casas com alto potencial de valorização e rentabilidade.',
        'keywords': 'investimento imobiliário litoral, imóveis para investir litoral sp, apartamento investimento santos, cobertura investimento guarujá, casa condomínio investimento bertioga, comprar para alugar litoral, rentabilidade imóvel temporada, valorização imóvel litoral',
        'tagline': 'Para Investidores',
        'subtitle': 'Oportunidades com alto potencial de valorização e rentabilidade em temporada.',
        'cta_text': 'Ver oportunidades de investimento',
        'cta_msg': 'Olá! Tenho interesse em oportunidades de investimento imobiliário no litoral. Pode me enviar oportunidades?',
        'h2_1': 'Por que investir no litoral?',
        'cards_1': [
            ('📈 Valorização', 'Imóveis no litoral valorizam acima da média nacional.'),
            ('🏖️ Temporada', 'Alta demanda de aluguel no verão e feriados.'),
            ('💵 Rentabilidade', 'Retorno rápido com gestão profissional.'),
        ],
        'h2_2': 'Cidades com melhor retorno',
        'cards_2': [
            ('Santos', 'Mercado maduro e valorização constante.', 'cidades/santos.html'),
            ('Guarujá', 'Alta temporada e imóveis de luxo.', 'cidades/guaruja.html'),
            ('Praia Grande', 'Metrô + orla = alto giro e liquidez.', 'cidades/praia-grande.html'),
            ('Bertioga', 'Condomínios de alto padrão e segurança.', 'cidades/bertioga.html'),
        ],
        'h2_3': 'Tipos de imóvel para investir',
        'cards_3': [
            ('Apartamento 1 quarto', 'Ideal para temporada e renda fixa.', 'imoveis/apartamento-1-quartos-santos.html'),
            ('Cobertura', 'Alto valor agregado e vista mar.', 'imoveis/cobertura-santos.html'),
            ('Casa em condomínio', 'Segurança e lazer para família ou temporada.', 'imoveis/casa-condominio-santos.html'),
        ],
    },
    {
        'slug': 'familia',
        'title': 'Imóveis para Famílias no Litoral de SP | Litoral Prime Imóveis',
        'description': 'Imóveis familiares no litoral de SP: casas em condomínio, apartamentos com lazer e segurança para quem quer morar ou passar as férias com a família.',
        'keywords': 'imóveis para famílias litoral, casa condomínio litoral sp, apartamento família santos, imóvel com lazer guarujá, imóvel seguro bertioga, comprar imóvel para morar litoral, temporada família litoral',
        'tagline': 'Para Famílias',
        'subtitle': 'Casas em condomínio, apartamentos com lazer e segurança para morar ou passar as férias com a família.',
        'cta_text': 'Ver imóveis familiares',
        'cta_msg': 'Olá! Tenho interesse em imóveis para famílias no litoral. Pode me enviar oportunidades?',
        'h2_1': 'O que as famílias buscam',
        'cards_1': [
            ('🧒 Segurança', 'Condomínios fechados e monitorados para as crianças.'),
            ('🏊 Lazer', 'Piscina, playground e área verde para o dia a dia.'),
            ('📚 Escola', 'Proximidade de escolas e serviços essenciais.'),
        ],
        'h2_2': 'Cidades recomendadas',
        'cards_2': [
            ('Santos', 'Infraestrutura completa e orla segura para famílias.', 'cidades/santos.html'),
            ('Mongaguá', 'Praia calma e custo acessível para famílias.', 'cidades/mongagua.html'),
            ('Praia Grande', 'Metrô, parques e apartamentos com lazer completo.', 'cidades/praia-grande.html'),
            ('Caraguatatuba', 'Natureza, tranquilidade e espaço para famílias.', 'cidades/caraguatatuba.html'),
        ],
        'h2_3': 'Tipos de imóvel para famílias',
        'cards_3': [
            ('Apartamento 2 quartos', 'Espaço para a família com lazer completo.', 'imoveis/apartamento-2-quartos-santos.html'),
            ('Casa em condomínio', 'Segurança e privacidade para morar ou temporada.', 'imoveis/casa-condominio-santos.html'),
            ('Casa térrea', 'Acessibilidade e conforto para todas as idades.', 'imoveis/casa-terrea-santos.html'),
        ],
    },
    {
        'slug': 'temporada',
        'title': 'Imóveis para Temporada no Litoral de SP | Litoral Prime Imóveis',
        'description': 'Guia completo para aluguel de temporada no litoral de SP: imóveis em Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe.',
        'keywords': 'aluguel temporada litoral sp, imóveis temporada santos, temporada guarujá, temporada praia grande, temporada bertioga, temporada itanhaem, temporada mongaguá, temporada são vicente, temporada peruibe',
        'tagline': 'Para Temporada',
        'subtitle': 'Guia completo para aluguel de temporada no litoral de SP: dicas, cidades e tipos de imóvel.',
        'cta_text': 'Ver imóveis para temporada',
        'cta_msg': 'Olá! Tenho interesse em aluguel de temporada no litoral. Pode me enviar opções?',
        'h2_1': 'Dicas para temporada',
        'cards_1': [
            ('📅 Reserve com antecedência', 'Melhor disponibilidade e preço.'),
            ('🏠 Tipos de imóvel', 'Apartamentos, casas e coberturas para temporada.'),
            ('📝 Documentação', 'Contrato simples e seguro para ambas as partes.'),
        ],
        'h2_2': 'Cidades mais procuradas',
        'cards_2': [
            ('Santos', 'Orla movimentada e infraestrutura completa.', 'cidades/santos.html'),
            ('Guarujá', 'Praias e marinas ideais para verão.', 'cidades/guaruja.html'),
            ('Praia Grande', 'Orla ampla e alto giro de temporada.', 'cidades/praia-grande.html'),
            ('Mongaguá', 'Família e praias calmas para temporada.', 'cidades/mongagua.html'),
        ],
        'h2_3': 'Tipos de imóvel para temporada',
        'cards_3': [
            ('Apartamento 1 quarto', 'Compacto e funcional para casais.', 'imoveis/apartamento-1-quartos-santos.html'),
            ('Apartamento 2 quartos', 'Espaço para família e amigos.', 'imoveis/apartamento-2-quartos-santos.html'),
            ('Cobertura', 'Vista mar e experiência premium.', 'imoveis/cobertura-santos.html'),
        ],
    },
    {
        'slug': 'primeiro-imovel',
        'title': 'Primeiro Imóvel no Litoral de SP | Litoral Prime Imóveis',
        'description': 'Guia completo para comprar o primeiro imóvel no litoral de SP: dicas, cidades, tipos de imóvel e passos para começar com segurança.',
        'keywords': 'primeiro imóvel litoral, comprar primeiro imóvel litoral sp, primeiro apartamento litoral, financiamento imóvel litoral, entrada imóvel litoral, imóvel para iniciantes litoral',
        'tagline': 'Primeiro Imóvel',
        'subtitle': 'Guia completo para comprar o primeiro imóvel no litoral de SP: dicas, cidades e passos para começar.',
        'cta_text': 'Começar a busca',
        'cta_msg': 'Olá! Estou buscando meu primeiro imóvel no litoral. Pode me ajudar com dicas?',
        'h2_1': 'Por que comprar no litoral',
        'cards_1': [
            ('🌊 Qualidade de vida', 'Praia, ar puro e lazer todo dia.'),
            ('📈 Valorização', 'Imóveis no litoral valorizam bem com o tempo.'),
            ('🏡 Projeto de vida', 'Realize o sonho da casa própria na praia.'),
        ],
        'h2_2': 'Cidades para primeiro imóvel',
        'cards_2': [
            ('Mongaguá', 'Custo acessível e estrutura familiar.', 'cidades/mongagua.html'),
            ('Praia Grande', 'Metrô + orla e entrada facilitada.', 'cidades/praia-grande.html'),
            ('Santos', 'Mercado maduro e liquidez.', 'cidades/santos.html'),
            ('Itanhaém', 'Preço acessível e identidade de praia.', 'cidades/itanhaem.html'),
        ],
        'h2_3': 'Tipos de imóvel para começar',
        'cards_3': [
            ('Apartamento 1 quarto', 'Entrada menor e fácil manutenção.', 'imoveis/apartamento-1-quartos-santos.html'),
            ('Apartamento 2 quartos', 'Espaço para família ou hóspedes.', 'imoveis/apartamento-2-quartos-santos.html'),
            ('Studio', 'Investimento inicial e alto giro.', 'imoveis/studio-santos.html'),
        ],
    },
]


def build(persona):
    out = PERSONAS_DIR / f'{persona["slug"]}.html'
    cards_1 = '\n'.join([f'<article class="servico-card"><h3>{t}</h3><p>{d}</p></article>' for t, d in persona['cards_1']])
    cards_2 = '\n'.join([f'<article class="servico-card"><h3>{t}</h3><p>{d}</p><a href="../{u}">Ver imóveis em {t} →</a></article>' for t, d, u in persona['cards_2']])
    cards_3 = '\n'.join([f'<article class="servico-card"><h3>{t}</h3><p>{d}</p><a href="../{u}">Ver opções →</a></article>' for t, d, u in persona['cards_3']])
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{persona['title']}</title>
  <meta name="description" content="{persona['description']}">
  <meta name="keywords" content="{persona['keywords']}">
  <link rel="canonical" href="https://praia.digital/personas/{persona['slug']}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{persona['title']}">
  <meta property="og:description" content="{persona['description']}">
  <meta property="og:image" content="https://praia.digital/img/default-home.jpg">
  <meta property="og:url" content="https://praia.digital/personas/{persona['slug']}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{persona['title']}">
  <meta name="twitter:description" content="{persona['description']}">
  <meta name="twitter:image" content="https://praia.digital/img/default-home.jpg">
  <meta name="robots" content="index, follow">
  <link rel="alternate" hreflang="x-default" href="https://praia.digital/personas/{persona['slug']}.html" />
  <link rel="alternate" hreflang="pt-BR" href="https://praia.digital/personas/{persona['slug']}.html">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{persona['title'].split(' | ')[0]}",
    "description": "{persona['description']}",
    "url": "https://praia.digital/personas/{persona['slug']}.html",
    "breadcrumb": {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Início", "item": "https://praia.digital/index.html"}},
        {{"@type": "ListItem", "position": 2, "name": "{persona['tagline']}", "item": "https://praia.digital/personas/{persona['slug']}.html"}}
      ]
    }}
  }}
  </script>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <header>
    <nav aria-label="Navegação principal">
      <div class="logo">
        <h1>🏖️ Litoral Prime Imóveis</h1>
        <p class="tagline">{persona['tagline']}</p>
      </div>
      <ul class="nav-menu">
        <li><a href="../index.html">Início</a></li>
        <li><a href="../servicos.html">Serviços</a></li>
        <li><a href="../imoveis.html">Imóveis</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="hero">
      <h1>{persona['title'].split(' | ')[0]}</h1>
      <p class="subtitle">{persona['subtitle']}</p>
      <a class="btn-whatsapp" href="https://wa.me/5511954346288?text={persona['cta_msg'].replace(' ', '%20')}" target="_blank" rel="noopener">{persona['cta_text']}</a>
    </section>

    <section class="servicos-section">
      <h2>{persona['h2_1']}</h2>
      <div class="servicos-grid">
        {cards_1}
      </div>
    </section>

    <section class="servicos-section">
      <h2>{persona['h2_2']}</h2>
      <div class="servicos-grid">
        {cards_2}
      </div>
    </section>

    <section class="servicos-section">
      <h2>{persona['h2_3']}</h2>
      <div class="servicos-grid">
        {cards_3}
      </div>
    </section>
  </main>

  <footer aria-label="Rodapé">
    <p>© Litoral Prime Imóveis • comercial@praia.digital • (11) 95434-6288</p>
  </footer>
</body>
</html>'''
    out.write_text(html, encoding='utf-8')
    return out.name

def main():
    created = [build(p) for p in PERSONAS]
    print('PERSONAS_CREATED', len(created))
    for c in created:
        print('+', c)

if __name__ == '__main__':
    main()
