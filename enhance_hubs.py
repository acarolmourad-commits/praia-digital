import os, json
from datetime import datetime, timezone

now = datetime.now(timezone.utc).strftime('%Y-%m-%d')

hubs = {
    'bairros/ubatuba/index.html': {
        'title': 'Bairros de Ubatuba — Praia Digital',
        'description': 'Guia por bairros de Ubatuba: mercado, valorização, temporada e oportunidades de investimento no litoral norte de SP.',
        'canonical': 'https://praia.digital/bairros/ubatuba/index.html',
        'h1': 'Bairros de Ubatuba',
        'lead': 'Conteúdo e destaques por bairro de Ubatuba para investidores e proprietários no litoral norte.',
        'cards': [
            {
                'title': 'Centro',
                'url': '/bairros/ubatuba-centro.html',
                'text': 'Referência urbana com comércio, serviços e acesso direto à orla. Bom para quem valoriza conveniência e fluxo de temporada.'
            },
            {
                'title': 'Praia Grande',
                'url': '/bairros/ubatuba-praia-grande.html',
                'text': 'Balanço entre temporada e moradia, com procura crescente por ano e potencial de valorização estável.'
            },
            {
                'title': 'Toninhas',
                'url': '/bairros/ubatuba-toninhas.html',
                'text': 'Perfil residencial tranquilo e apelo para famílias e investidores que buscam sossego sem perder acessos.'
            },
            {
                'title': 'Itagua',
                'url': '/bairros/ubatuba-itagua.html',
                'text': 'Área com potencial de valorização e boa conexão com a natureza, ideal para temporada e segunda residência.'
            }
        ]
    },
    'bairros/caraguatatuba/index.html': {
        'title': 'Bairros de Caraguatatuba — Praia Digital',
        'description': 'Guia por bairros de Caraguatatuba: mercado, valorização e oportunidades de investimento no litoral norte de SP.',
        'canonical': 'https://praia.digital/bairros/caraguatatuba/index.html',
        'h1': 'Bairros de Caraguatatuba',
        'lead': 'Conteúdo e destaques por bairro de Caraguatatuba para investidores e proprietários no litoral norte.',
        'cards': [
            {
                'title': 'Centro',
                'url': '/bairros/caraguatatuba-centro.html',
                'text': 'Conveniência urbana, serviços próximos e acesso rápido à orla.'
            },
            {
                'title': 'Massaguaçu',
                'url': '/bairros/caraguatatuba-massaguacu.html',
                'text': 'Região familiar, com boa oferta residencial e potencial de temporada.'
            },
            {
                'title': 'Tabatinga',
                'url': '/bairros/caraguatatuba-tabatinga.html',
                'text': 'Ambiente tranquilo, proximidade com praias e tendência de valorização.'
            },
            {
                'title': 'Cocanha',
                'url': '/bairros/caraguatatuba-cocanha.html',
                'text': 'Área com perfil mais sossegado e oportunidades por metro quadrado.'
            }
        ]
    },
    'bairros/sao-vicente/index.html': {
        'title': 'Bairros de São Vicente — Praia Digital',
        'description': 'Conteúdo e destaques por bairro de São Vicente para investidores e proprietários no litoral paulista.',
        'canonical': 'https://praia.digital/bairros/sao-vicente/index.html',
        'h1': 'Bairros de São Vicente',
        'lead': 'Conteúdo e destaques por bairro de São Vicente para investidores e proprietários.',
        'cards': [
            {
                'title': 'Centro',
                'url': '/bairros/saovicente-centro.html',
                'text': 'Referência urbana com acesso facilitado ao comércio, serviços e orla.'
            },
            {
                'title': 'Gonzaguinha',
                'url': '/bairros/saovicente-gonzaguinha.html',
                'text': 'Bairro residencial com boas alternativas de locação e valorização estável.'
            },
            {
                'title': 'Parque Bitaru',
                'url': '/bairros/saovicente-parque-bitaru.html',
                'text': 'Perfil familiar, tranquilidade e potencial para temporada e long stay.'
            },
            {
                'title': 'Ponta da Praia',
                'url': '/bairros/saovicente-ponta-da-praia.html',
                'text': 'Vista para o mar, alta procura turística e boas oportunidades.'
            }
        ]
    }
}

cards_html = []
for hub_path, data in hubs.items():
    cards_html = []
    for card in data['cards']:
        cards_html.append(f'''
        <div class="card">
          <a href="{card['url']}">{card['title']}</a>
          <p style="opacity:.75; margin-top:6px;">{card['text']}</p>
        </div>''')
    cards_block = '\n'.join(cards_html)

    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"Bairros de {data['h1'].replace('Bairros de ', '')}",
        "url": data['canonical'],
        "numberOfItems": len(data['cards']),
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "url": "https://praia.digital" + card['url'], "name": card['title']}
            for i, card in enumerate(data['cards'])
        ]
    }

    faqs = [
        {
            "@type": "Question",
            "name": f"Quais bairros de {data['h1'].replace('Bairros de ', '')} são mais buscados?",
            "acceptedAnswer": {"@type": "Answer", "text": f"{', '.join(c['title'] for c in data['cards'])} são destaques por perfil e potencial de investimento."}
        },
        {
            "@type": "Question",
            "name": f"{data['h1'].replace('Bairros de ', '')} é boa para temporada?",
            "acceptedAnswer": {"@type": "Answer", "text": "Sim. Boa infraestrutura, acesso facilitado e demanda consistente por temporada e long stay."}
        },
        {
            "@type": "Question",
            "name": f"Como avaliar preço por m² em {data['h1'].replace('Bairros de ', '')}?",
            "acceptedAnswer": {"@type": "Answer", "text": "Compare médias por bairro, sazonalidade e oferta atual; use avaliação profissional para decisão segura."}
        }
    ]

    content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data['title']}</title>
  <meta name="description" content="{data['description']}">
  <link rel="canonical" href="{data['canonical']}">
  <meta name="robots" content="index, follow">
  <meta name="last-modified" content="{now}">
  <script type="application/ld+json">
  {json.dumps({
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": data['title'],
      "url": data['canonical'],
      "description": data['description']
  }, ensure_ascii=False)}
  </script>
  <script type="application/ld+json">
  {json.dumps(schema, ensure_ascii=False)}
  </script>
  <script type="application/ld+json">
  {json.dumps({
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": faqs
  }, ensure_ascii=False)}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <style>
    :root {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #0b1220; color: #e8ecf1; }}
    .wrap {{ max-width: 900px; margin: 0 auto; padding: 28px 22px; }}
    header nav a {{ color: #cfe3ff; text-decoration: none; margin-right: 14px; font-weight: 500; }}
    .lead {{ opacity: .85; line-height: 1.6; }}
    .grid {{ display: grid; gap: 1rem; margin-top: 1.5rem; }}
    .card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 18px 20px; }}
    .card a {{ color: #cfe3ff; font-weight: 700; text-decoration: none; }}
    footer {{ margin-top: 22px; opacity: .6; font-size: 12px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <nav aria-label="Navegação principal">
        <a href="https://praia.digital/index.html">Início</a>
        <a href="https://praia.digital/servicos.html">Serviços</a>
        <a href="https://praia.digital/bairros/index.html">Bairros</a>
      </nav>
    </header>

    <main id="main">
      <h1>{data['h1']}</h1>
      <p class="lead">{data['lead']}</p>

      <div class="grid">
        {cards_block}
      </div>
    </main>

    <footer>Praia Digital — conteúdo original, sem placeholders.</footer>
  </div>
</body>
</html>
'''

    with open(hub_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('enhanced', hub_path)

print('done')
