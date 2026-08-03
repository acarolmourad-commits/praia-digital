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
        "slug": "apartamento-garden-santos",
        "title": "Apartamento garden - Santos",
        "description": "Apartamento garden com quintal privativo, churrasqueira e vaga de garagem em Santos.",
        "city": "Santos",
        "type": "Venda",
        "price": "R$ 580.000",
        "price_raw": "580000",
        "bedrooms": "2",
        "area": "95m²",
        "image": "img/santos-garden.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Quintal privativo</p></article><article class="servico-card"><h3>✓</h3><p>Churrasqueira</p></article><article class="servico-card"><h3>✓</h3><p>Garagem</p></article>',
        "related": '<a class="servico-card" href="apartamento-2-quartos-santos.html"><h3>Apartamento 2 quartos - Santos</h3><p>Santos • Venda</p><p>R$ 450.000</p></a><a class="servico-card" href="apartamento-vista-mar-santos.html"><h3>Apartamento vista mar - Santos</h3><p>Santos • Venda</p><p>R$ 720.000</p></a><a class="servico-card" href="casa-terrea-guaruja.html"><h3>Casa térrea - Guarujá</h3><p>Guarujá • Venda</p><p>R$ 680.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20garden%20-%20Santos.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "studio-investimento-praia-grande",
        "title": "Studio investimento - Praia Grande",
        "description": "Studio com entrada facilitada e potencial de rentabilidade por temporada em Praia Grande.",
        "city": "Praia Grande",
        "type": "Venda",
        "price": "R$ 240.000",
        "price_raw": "240000",
        "bedrooms": "1",
        "area": "38m²",
        "image": "img/pg-studio-inv.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Investimento</p></article><article class="servico-card"><h3>✓</h3><p>Entrada facilitada</p></article><article class="servico-card"><h3>✓</h3><p>Temporada</p></article>',
        "related": '<a class="servico-card" href="studio-moderno-praia-grande.html"><h3>Studio moderno - Praia Grande</h3><p>Praia Grande • Venda</p><p>R$ 280.000</p></a><a class="servico-card" href="apartamento-4-quartos-praia-grande.html"><h3>Apartamento 4 quartos - Praia Grande</h3><p>Praia Grande • Venda</p><p>R$ 650.000</p></a><a class="servico-card" href="apartamento-1-quartos-mongagua.html"><h3>Apartamento 1 quartos - Mongaguá</h3><p>Mongaguá • Venda</p><p>R$ 185.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Studio%20investimento%20-%20Praia%20Grande.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "casa-condominio-fechado-santos",
        "title": "Casa condomínio fechado - Santos",
        "description": "Casa em condomínio fechado com lazer completo, segurança 24h e área verde em Santos.",
        "city": "Santos",
        "type": "Venda",
        "price": "R$ 950.000",
        "price_raw": "950000",
        "bedrooms": "3",
        "area": "160m²",
        "image": "img/santos-condominio.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Condomínio fechado</p></article><article class="servico-card"><h3>✓</h3><p>Segurança 24h</p></article><article class="servico-card"><h3>✓</h3><p>Área verde</p></article>',
        "related": '<a class="servico-card" href="apartamento-vista-mar-santos.html"><h3>Apartamento vista mar - Santos</h3><p>Santos • Venda</p><p>R$ 720.000</p></a><a class="servico-card" href="casa-terrea-guaruja.html"><h3>Casa térrea - Guarujá</h3><p>Guarujá • Venda</p><p>R$ 680.000</p></a><a class="servico-card" href="casa-condominio-fechado-praia-grande.html"><h3>Casa em condomínio fechado - Praia Grande</h3><p>Praia Grande • Venda</p><p>R$ 780.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20-%20Santos.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "apartamento-frente-mar-guaruja",
        "title": "Apartamento frente mar - Guarujá",
        "description": "Apartamento frente mar com varanda gourmet e lazer completo no Guarujá.",
        "city": "Guarujá",
        "type": "Aluguel",
        "price": "R$ 7.500/mês",
        "price_raw": "7500",
        "bedrooms": "3",
        "area": "110m²",
        "image": "img/guaruja-frente-mar.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Frente mar</p></article><article class="servico-card"><h3>✓</h3><p>Varanda gourmet</p></article><article class="servico-card"><h3>✓</h3><p>Lazer completo</p></article>',
        "related": '<a class="servico-card" href="apartamento-vista-mar-guaruja.html"><h3>Apartamento vista mar - Guarujá</h3><p>Guarujá • Aluguel</p><p>R$ 6.200/mês</p></a><a class="servico-card" href="casa-duplex-guaruja.html"><h3>Casa duplex - Guarujá</h3><p>Guarujá • Aluguel</p><p>R$ 4.500/mês</p></a><a class="servico-card" href="apartamento-vista-mar-santos.html"><h3>Apartamento vista mar - Santos</h3><p>Santos • Venda</p><p>R$ 720.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20-%20Guaruj%C3%A1.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "sobrado-guaruja",
        "title": "Sobrado - Guarujá",
        "description": "Sobrado com piscina, churrasqueira e quintal amplo em condomínio fechado no Guarujá.",
        "city": "Guarujá",
        "type": "Venda",
        "price": "R$ 780.000",
        "price_raw": "780000",
        "bedrooms": "3",
        "area": "170m²",
        "image": "img/guaruja-sobrado.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Piscina</p></article><article class="servico-card"><h3>✓</h3><p>Churrasqueira</p></article><article class="servico-card"><h3>✓</h3><p>Quintal</p></article>',
        "related": '<a class="servico-card" href="casa-duplex-guaruja.html"><h3>Casa duplex - Guarujá</h3><p>Guarujá • Aluguel</p><p>R$ 4.500/mês</p></a><a class="servico-card" href="casa-3-quartos-guaruja.html"><h3>Casa 3 quartos - Guarujá</h3><p>Guarujá • Venda</p><p>R$ 890.000</p></a><a class="servico-card" href="apartamento-frente-mar-guaruja.html"><h3>Apartamento frente mar - Guarujá</h3><p>Guarujá • Aluguel</p><p>R$ 7.500/mês</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20-%20Guaruj%C3%A1.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "apartamento-cobertura-sao-vicente",
        "title": "Cobertura duplex - São Vicente",
        "description": "Cobertura duplex com piscina privativa, vista mar e acabamento de alto padrão.",
        "city": "São Vicente",
        "type": "Venda",
        "price": "R$ 1.480.000",
        "price_raw": "1480000",
        "bedrooms": "4",
        "area": "210m²",
        "image": "img/sv-cobertura-duplex.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Piscina privativa</p></article><article class="servico-card"><h3>✓</h3><p>Vista mar</p></article><article class="servico-card"><h3>✓</h3><p>Alto padrão</p></article>',
        "related": '<a class="servico-card" href="cobertura-duplex-sao-vicente.html"><h3>Cobertura duplex - São Vicente</h3><p>São Vicente • Venda</p><p>R$ 1.250.000</p></a><a class="servico-card" href="apartamento-mobiliado-sao-vicente.html"><h3>Apartamento mobiliado - São Vicente</h3><p>São Vicente • Aluguel</p><p>R$ 3.800/mês</p></a><a class="servico-card" href="apartamento-vista-mar-santos.html"><h3>Apartamento vista mar - Santos</h3><p>Santos • Venda</p><p>R$ 720.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20duplex%20-%20S%C3%A3o%20Vicente.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "casa-ita-encontro-aguas",
        "title": "Casa encontro das águas - Itanhaém",
        "description": "Casa exclusiva no encontro das águas, com piscina e vista para o mar em Itanhaém.",
        "city": "Itanhaém",
        "type": "Venda",
        "price": "R$ 1.100.000",
        "price_raw": "1100000",
        "bedrooms": "4",
        "area": "220m²",
        "image": "img/it-encontro-aguas.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Vista mar</p></article><article class="servico-card"><h3>✓</h3><p>Piscina</p></article><article class="servico-card"><h3>✓</h3><p>Exclusiva</p></article>',
        "related": '<a class="servico-card" href="casa-terrea-itanhaem.html"><h3>Casa térrea - Itanhaém</h3><p>Itanhaém • Aluguel</p><p>R$ 3.200/mês</p></a><a class="servico-card" href="terreno-peruibe.html"><h3>Terreno - Peruíbe</h3><p>Peruíbe • Venda</p><p>R$ 190.000</p></a><a class="servico-card" href="apartamento-vista-mar-santos.html"><h3>Apartamento vista mar - Santos</h3><p>Santos • Venda</p><p>R$ 720.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20encontro%20das%20%C3%A1guas%20-%20Itanha%C3%A9m.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "apartamento-mobiliado-mongagua",
        "title": "Apartamento mobiliado - Mongaguá",
        "description": "Apartamento mobiliado para temporada, com Wi-Fi e piscina no Mongaguá.",
        "city": "Mongaguá",
        "type": "Aluguel",
        "price": "R$ 2.900/mês",
        "price_raw": "2900",
        "bedrooms": "2",
        "area": "60m²",
        "image": "img/mon-mobiliado.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Mobiliado</p></article><article class="servico-card"><h3>✓</h3><p>Temporada</p></article><article class="servico-card"><h3>✓</h3><p>Piscina</p></article>',
        "related": '<a class="servico-card" href="apartamento-compacto-mongagua.html"><h3>Apartamento compacto - Mongaguá</h3><p>Mongaguá • Venda</p><p>R$ 210.000</p></a><a class="servico-card" href="apartamento-1-quartos-mongagua.html"><h3>Apartamento 1 quartos - Mongaguá</h3><p>Mongaguá • Venda</p><p>R$ 185.000</p></a><a class="servico-card" href="studio-moderno-praia-grande.html"><h3>Studio moderno - Praia Grande</h3><p>Praia Grande • Venda</p><p>R$ 280.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20mobiliado%20-%20Mongagu%C3%A1.%20Pode%20me%20enviar%20mais%20detalhes%3F",
    },
    {
        "slug": "terreno-bertioga",
        "title": "Terreno - Bertioga",
        "description": "Terreno plano em rua asfaltada com infraestrutura pronta em Bertioga.",
        "city": "Bertioga",
        "type": "Venda",
        "price": "R$ 260.000",
        "price_raw": "260000",
        "bedrooms": "0",
        "area": "200m²",
        "image": "img/bertioga-terreno.png",
        "tags": '<article class="servico-card"><h3>✓</h3><p>Plano</p></article><article class="servico-card"><h3>✓</h3><p>Rua asfaltada</p></article><article class="servico-card"><h3>✓</h3><p>Infraestrutura pronta</p></article>',
        "related": '<a class="servico-card" href="casa-terrea-bertioga.html"><h3>Casa térrea - Bertioga</h3><p>Bertioga • Venda</p><p>R$ 520.000</p></a><a class="servico-card" href="apartamento-alto-padrao-bertioga.html"><h3>Apartamento alto padrão - Bertioga</h3><p>Bertioga • Aluguel</p><p>R$ 8.900/mês</p></a><a class="servico-card" href="terreno-santos.html"><h3>Terreno - Santos</h3><p>Santos • Venda</p><p>R$ 320.000</p></a>',
        "whatsapp_link": "https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20-%20Bertioga.%20Pode%20me%20enviar%20mais%20detalhes%3F",
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
