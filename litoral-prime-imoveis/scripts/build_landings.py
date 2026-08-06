import json
from pathlib import Path

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
imoveis_dir = base / 'imoveis'
imoveis_dir.mkdir(parents=True, exist_ok=True)

properties = json.loads((base / 'imoveis' / 'properties.json').read_text(encoding='utf-8'))

landing_template = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Litoral Prime Imóveis</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://praia.digital/imoveis/{slug}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title} — Litoral Prime Imóveis">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{image}">
  <meta property="og:url" content="https://praia.digital/imoveis/{slug}.html">
  <meta property="og:site_name" content="Litoral Prime Imóveis">
  <meta name="theme-color" content="#0ea5e9">
  <link rel="preconnect" href="https://praia.digital">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="preconnect" href="https://wa.me">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "RealEstateListing",
    "name": "{title}",
    "description": "{description}",
    "image": "{image}",
    "url": "https://praia.digital/imoveis/{slug}.html",
    "offers": {{
      "@type": "Offer",
      "price": "{price_raw}",
      "priceCurrency": "BRL"
    }},
    "area": "{area}",
    "bedrooms": "{bedrooms}",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "{city}",
      "addressRegion": "SP",
      "addressCountry": "BR"
    }},
    "provider": {{
      "@type": "Organization",
      "name": "Litoral Prime Imóveis",
      "url": "https://praia.digital/"
    }}
  }}
  </script>
  <style>
    body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0b1220;color:#e8ecf1;margin:0;padding:0}}
    .wrap{{max-width:960px;margin:0 auto;padding:28px 22px}}
    header nav a{{color:#cfe3ff;text-decoration:none;margin-right:14px;font-weight:500}}
    h1{{font-size:1.8rem;margin:0 0 .5rem}}
    .lead{{opacity:.85;line-height:1.6;margin-bottom:1rem}}
    .card{{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:18px 20px;margin-top:14px}}
    .cta{{background:#00B4D8;color:#fff;padding:.7rem 1.2rem;border-radius:999px;font-weight:700;text-decoration:none;display:inline-block;margin-top:.6rem;margin-right:10px}}
    .price{{font-size:1.6rem;font-weight:800;color:#90E0EF;margin-top:8px}}
    footer{{margin-top:22px;opacity:.6;font-size:12px}}
    img{{width:100%;border-radius:16px;margin-top:14px}}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <nav aria-label="Navegação principal">
        <a href="https://praia.digital/litoral-prime-imoveis/index.html">Início</a>
        <a href="https://praia.digital/litoral-prime-imoveis/imoveis.html">Imóveis</a>
        <a href="https://praia.digital/servicos.html">Serviços</a>
        <a href="https://praia.digital/education/index.html">Academy</a>
      </nav>
    </header>

    <main id="main">
      <h1>{title}</h1>
      <img src="{image}" alt="{title}" loading="lazy">
      <p class="lead">{description}</p>

      <div class="card">
        <p><strong>Tipo:</strong> {type}</p>
        <p><strong>Cidade:</strong> {city}</p>
        <p><strong>Bairro:</strong> {bairro}</p>
        <p><strong>Área:</strong> {area}</p>
        <p><strong>Quartos:</strong> {bedrooms}</p>
        <p><strong>Tags:</strong> {tags}</p>
        <p class="price">{price}</p>
        <a class="cta" href="https://wa.me/5511954346288?text=Olá! Tenho interesse no imóvel: {title}. Pode me enviar mais detalhes?" target="_blank" rel="noopener">Conversar no WhatsApp</a>
        <a class="cta" style="background:#fff;color:#0b1220" href="https://praia.digital/litoral-prime-imoveis/encontrar-imovel.html">Ver mais imóveis</a>
      </div>
    </main>

    <footer>Litoral Prime Imóveis — imóveis no litoral de São Paulo.</footer>
  </div>
</body>
</html>
'''

created = 0
for p in properties:
    path = imoveis_dir / f"{p['slug']}.html"
    price_raw = p['price'].replace('R$ ', '').replace('.', '').replace('/mês', '').replace('+', '')
    html = landing_template.format(
        title=p['title'],
        description=p['description'],
        slug=p['slug'],
        image=p['image'],
        price=p['price'],
        price_raw=price_raw,
        area=p['area'],
        bedrooms=p['bedrooms'],
        city=p['city'],
        bairro=p.get('bairro', p['city']),
        type=p['type'],
        tags=', '.join(p.get('tags', []))
    )
    path.write_text(html, encoding='utf-8')
    created += 1

print('Landing pages criadas:', created)
