from pathlib import Path

REPO = Path('.').resolve()
OUT_DIR = REPO / 'imoveis'
OUT_DIR.mkdir(exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}} | Litoral Prime Imóveis</title>
  <meta name="description" content="{{description}}">
  <meta name="keywords" content="{{title}}, imóveis litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe">
  <link rel="canonical" href="https://praia.digital/imoveis/{{slug}}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{title}} | Litoral Prime Imóveis">
  <meta property="og:description" content="{{description}}">
  <meta property="og:image" content="https://praia.digital/img/default-home.jpg">
  <meta property="og:url" content="https://praia.digital/imoveis/{{slug}}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{title}} | Litoral Prime Imóveis">
  <meta name="twitter:description" content="{{description}}">
  <meta name="twitter:image" content="https://praia.digital/img/default-home.jpg">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "RealEstateListing",
    "name": "{{title}}",
    "description": "{{description}}",
    "url": "https://praia.digital/imoveis/{{slug}}.html",
    "provider": {"@type": "Organization", "name": "Litoral Prime Imóveis", "url": "https://praia.digital/"}
  }
  </script>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <header>
    <nav aria-label="Navegação principal">
      <div class="logo">
        <h1>🏖️ Litoral Prime Imóveis</h1>
        <p class="tagline">{{city}}</p>
      </div>
      <ul class="nav-menu">
        <li><a href="../index.html">Início</a></li>
        <li><a href="../servicos.html">Serviços</a></li>
        <li><a href="index.html">Imóveis</a></li>
      </ul>
    </nav>
  </header>
  <main id="main">
    <section class="hero">
      <picture>
        <source srcset="{{image}}.webp" type="image/webp">
        <img src="{{image}}" alt="{{title}}" loading="lazy" width="800" height="600" decoding="async">
      </picture>
      <h1>{{title}}</h1>
      <p class="subtitle">{{description}}</p>
      <a class="btn-whatsapp" href="{{whatsapp_link}}" target="_blank" rel="noopener">Tenho interesse neste imóvel</a>
    </section>
    <section class="servicos-section">
      <h2>Informações</h2>
      <div class="servicos-grid">
        <article class="servico-card">
          <h3>🏷️ Tipo</h3>
          <p>{{type}}</p>
        </article>
        <article class="servico-card">
          <h3>💰 Preço</h3>
          <p>{{price}}</p>
        </article>
        <article class="servico-card">
          <h3>🛏️ Quartos</h3>
          <p>{{bedrooms}}</p>
        </article>
        <article class="servico-card">
          <h3>📐 Área</h3>
          <p>{{area}}</p>
        </article>
      </div>
    </section>
    <section class="servicos-section">
      <h2>Destaques</h2>
      <div class="servicos-grid">
        {{tags}}
      </div>
    </section>
    <section class="servicos-section">
      <h2>Imóveis relacionados</h2>
      <div class="servicos-grid">
        {{related}}
      </div>
    </section>
  </main>
</body>
</html>"""

new_items = [
  {
    "slug": "apartamento-duplex-santos",
    "title": "Apartamento duplex - Santos",
    "description": "Apartamento duplex com sacada gourmet e vista parcial em Santos.",
    "city": "Santos",
    "type": "Venda",
    "price": "R$ 890.000",
    "price_raw": "890000",
    "bedrooms": "3",
    "area": "135m²",
    "image": "img/santos-duplex.png",
    "tags": '<article class="servico-card"><h3>✓</h3><p>Duplex</p></article><article class="servico-card"><h3>✓</h3><p>Sacada gourmet</p></article><article class="servico-card"><h3>✓</h3><p>Vista parcial</p></article>',
    "related": '<a class="servico-card" href="apartamento-vista-mar-santos.html"><h3>Apartamento vista mar - Santos</h3><p>Santos • Venda</p><p>R$ 720.000</p></a><a class="servico-card" href="apartamento-garden-santos.html"><h3>Apartamento garden - Santos</h3><p>Santos • Venda</p><p>R$ 580.000</p></a><a class="servico-card" href="cobertura-duplex-sao-vicente.html"><h3>Cobertura duplex - São Vicente</h3><p>São Vicente • Venda</p><p>R$ 1.250.000</p></a>',
    "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20duplex%20-%20Santos.%20Pode%20me%20enviar%20mais%20detalhes%3F",
  },
  {
    "slug": "apartamento-1-quartos-mongagua",
    "title": "Apartamento 1 quartos - Mongaguá",
    "description": "Apartamento compacto 1 quarto com piscina e lazer em Mongaguá.",
    "city": "Mongaguá",
    "type": "Venda",
    "price": "R$ 185.000",
    "price_raw": "185000",
    "bedrooms": "1",
    "area": "42m²",
    "image": "img/mon-1q.png",
    "tags": '<article class="servico-card"><h3>✓</h3><p>1 quarto</p></article><article class="servico-card"><h3>✓</h3><p>Piscina</p></article><article class="servico-card"><h3>✓</h3><p>Compacto</p></article>',
    "related": '<a class="servico-card" href="apartamento-compacto-mongagua.html"><h3>Apartamento compacto - Mongaguá</h3><p>Mongaguá • Venda</p><p>R$ 210.000</p></a><a class="servico-card" href="studio-moderno-praia-grande.html"><h3>Studio moderno - Praia Grande</h3><p>Praia Grande • Venda</p><p>R$ 280.000</p></a><a class="servico-card" href="apartamento-mobiliado-mongagua.html"><h3>Apartamento mobiliado - Mongaguá</h3><p>Mongaguá • Aluguel</p><p>R$ 2.900/mês</p></a>',
    "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%201%20quartos%20-%20Mongagu%C3%A1.%20Pode%20me%20enviar%20mais%20detalhes%3F",
  },
  {
    "slug": "apartamento-2-quartos-santos",
    "title": "Apartamento 2 quartos - Santos",
    "description": "Apartamento 2 quartos com lazer completo e vaga de garagem em Santos.",
    "city": "Santos",
    "type": "Venda",
    "price": "R$ 450.000",
    "price_raw": "450000",
    "bedrooms": "2",
    "area": "78m²",
    "image": "img/santos-2q.png",
    "tags": '<article class="servico-card"><h3>✓</h3><p>2 quartos</p></article><article class="servico-card"><h3>✓</h3><p>Lazer completo</p></article><article class="servico-card"><h3>✓</h3><p>Garagem</p></article>',
    "related": '<a class="servico-card" href="apartamento-vista-mar-santos.html"><h3>Apartamento vista mar - Santos</h3><p>Santos • Venda</p><p>R$ 720.000</p></a><a class="servico-card" href="apartamento-garden-santos.html"><h3>Apartamento garden - Santos</h3><p>Santos • Venda</p><p>R$ 580.000</p></a><a class="servico-card" href="apartamento-duplex-santos.html"><h3>Apartamento duplex - Santos</h3><p>Santos • Venda</p><p>R$ 890.000</p></a>',
    "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%202%20quartos%20-%20Santos.%20Pode%20me%20enviar%20mais%20detalhes%3F",
  },
]

created = []
for item in new_items:
    html = TEMPLATE
    for key, value in item.items():
        if key == 'slug':
            continue
        placeholder = '{{' + key + '}}'
        html = html.replace(placeholder, value)
    out = OUT_DIR / f"{item['slug']}.html"
    if out.exists():
        continue
    out.write_text(html, encoding='utf-8')
    created.append(str(out))

print('LANDINGS_CREATED', len(created))
for p in created:
    print('-', Path(p).name)
