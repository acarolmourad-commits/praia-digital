#!/usr/bin/env python3
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
OUT = BASE / "cidades"
OUT.mkdir(parents=True, exist_ok=True)

cidades = [
    ("santos", "Santos"),
    ("guaruja", "Guarujá"),
    ("praia-grande", "Praia Grande"),
    ("itanhaem", "Itanhaém"),
    ("sao-vicente", "São Vicente"),
    ("mongagua", "Mongaguá"),
    ("peruibe", "Peruíbe"),
    ("bertioga", "Bertioga"),
]

features = [
    ("seguranca", "Segurança"),
    ("elevador", "Elevador"),
    ("sacada", "Sacada"),
    ("varanda", "Varanda"),
    ("pet-friendly", "Pet friendly"),
    ("academia", "Academia"),
    ("sauna", "Sauna"),
    ("comercial", "Comercial"),
    ("residencial", "Residencial"),
    ("venda-rapida", "Venda rápida"),
    ("compra-programada", "Compra programada"),
]

services = [
    ("gestao-de-imovel", "Gestão de Imóvel"),
    ("propaganda-imobiliaria", "Propaganda Imobiliária"),
    ("midia-profissional", "Mídia Profissional"),
]

copy = {
    "seguranca": "<strong>Segurança</strong> em {city}: condomínios fechados, monitoramento, portaria e proximidade de delegacias.",
    "elevador": "<strong>Elevador</strong> em {city}: conforto, acessibilidade e valorização do imóvel.",
    "sacada": "<strong>Sacada</strong> em {city}: área externa privativa integrada ao apartamento.",
    "varanda": "<strong>Varanda</strong> em {city}: ventilação, iluminação natural e visual privilegiado.",
    "pet-friendly": "<strong>Pet friendly</strong> em {city}: regras claras, áreas comuns adequadas e proximidade de serviços.",
    "academia": "<strong>Academia</strong> no condomínio em {city}: saúde, conveniência e valor agregado.",
    "sauna": "<strong>Sauna</strong> em {city}: lazer e bem-estar no mesmo condomínio.",
    "comercial": "<strong>Comercial</strong> em {city}: salas, escritórios e pontos de atendimento.",
    "residencial": "<strong>Residencial</strong> em {city}: apartamentos, casas e coberturas para moradia.",
    "venda-rapida": "<strong>Venda rápida</strong> em {city}: imóveis com liquidez, preço e localização favoráveis.",
    "compra-programada": "<strong>Compra programada</strong> em {city}: planejamento financeiro e acompanhamento especializado.",
}

copy_service = {
    "gestao-de-imovel": "<strong>Gestão de imóvel</strong> em {city}: anúncios, atendimento, agendamentos e rotina de locação/venda.",
    "propaganda-imobiliaria": "<strong>Propaganda imobiliária</strong> em {city}: anúncios, redes sociais, portais e peças digitais com foco em conversão.",
    "midia-profissional": "<strong>Mídia profissional</strong> em {city}: fotografia, vídeo, tour virtual e peças prontas para vender mais rápido.",
}

created = 0
skipped = 0

for city_slug, city_label in cidades:
    for slug, label in features:
        path = OUT / f"{city_slug}-{slug}.html"
        if path.exists():
            skipped += 1
            continue
        body = copy[slug].replace("{city}", city_label)
        title = f"{label} em {city_label}"
        subtitle = f"{label} em {city_label} — Litoral Prime Imóveis"
        wa_text = f"Olá! Tenho interesse em {label} em {city_label}."
        wa_encoded = wa_text.replace(" ", "%20")
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Litoral Prime Imóveis</title>
<meta name="description" content="{subtitle}">
<link rel="canonical" href="https://praia.digital/cidades/{city_slug}-{slug}.html">
<link rel="alternate" hreflang="x-default" href="https://praia.digital/cidades/{city_slug}-{slug}.html" />
<link rel="alternate" hreflang="pt-BR" href="https://praia.digital/cidades/{city_slug}-{slug}.html">

<link rel="preload" as="image" href="https://praia.digital/img/default-home.jpg" type="image/jpeg" fetchpriority="high">

<link rel="preload" as="image" href="https://praia.digital/img/default-home.jpg" type="image/jpeg" fetchpriority="high">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{subtitle}">
<meta property="og:url" content="https://praia.digital/cidades/{city_slug}-{slug}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{subtitle}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Quais cidades são atendidas?","acceptedAnswer":{{"@type":"Answer","text":"Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe."}}}},{{"@type":"Question","name":"Como solicitar atendimento?","acceptedAnswer":{{"@type":"Answer","text":"Pelo formulário abaixo ou diretamente pelo WhatsApp."}}}}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{title}","description":"{subtitle}","areaServed":"{city_label}","provider":{{"@type":"LocalBusiness","name":"Litoral Prime Imóveis","telephone":"+5511954346288"}}}}
</script>
</head>
<body style="font-family:Arial,sans-serif;max-width:900px;margin:auto;padding:20px;color:#222;background:#f5f7fa">
<a id="skip-link" class="skip-link" href="#main" style="position:absolute;left:-9999px;">Pular para o conteúdo</a>
<header>
  <h1 style="color:#0b4f6c">{title}</h1>
  <p>{subtitle}</p>
</header>
<main id="main">
<section>
  <h2>Sobre</h2>
  <p>{body}</p>
</section>
<section style="margin-top:18px">
  <h2>Atendimento em {city_label}</h2>
  <p>Atendimento especializado pelo WhatsApp com consultores locais, visitas presenciais e suporte digital.</p>
  <p><a href="https://wa.me/5511954346288?text={wa_encoded}" target="_blank" rel="noopener" style="background:#0b4f6c;color:#fff;padding:10px 14px;border-radius:6px;text-decoration:none;">Contato WhatsApp</a></p>
</section>
<section style="margin-top:18px">
  <h2>Veja também</h2>
  <ul>
    <li><a href="../../cidades/{city_slug}.html">Imóveis em {city_label}</a></li>
    <li><a href="../../servicos.html">Todos os serviços</a></li>
    <li><a href="../../imoveis.html">Ver todos os imóveis</a></li>
  </ul>
</section>
</main>
<section class="recommended" style="margin-top:18px">
  <h2>Outras cidades</h2>
  <ul>
    <li><a href="santos-{slug}.html">Santos</a></li>
    <li><a href="guaruja-{slug}.html">Guarujá</a></li>
    <li><a href="praia-grande-{slug}.html">Praia Grande</a></li>
    <li><a href="sao-vicente-{slug}.html">São Vicente</a></li>
    <li><a href="itanhaem-{slug}.html">Itanhaém</a></li>
    <li><a href="mongagua-{slug}.html">Mongaguá</a></li>
    <li><a href="peruibe-{slug}.html">Peruíbe</a></li>
    <li><a href="bertioga-{slug}.html">Bertioga</a></li>
  </ul>
</section>
<footer aria-label="Rodapé" style="margin-top:24px">
  <p>© Litoral Prime Imóveis • <a href="https://praia.digital" rel="noopener">https://praia.digital</a></p>
  <p><a href="../sitemap.html">Mapa do site</a></p>
</footer>
</body>
</html>
"""
        path.write_text(html, encoding="utf-8")
        created += 1

    for slug, label in services:
        path = OUT / f"{city_slug}-{slug}.html"
        if path.exists():
            skipped += 1
            continue
        body = copy_service[slug].replace("{city}", city_label)
        title = f"{label} em {city_label}"
        subtitle = f"{label} em {city_label} — Litoral Prime Imóveis"
        wa_text = f"Olá! Tenho interesse em {label} em {city_label}."
        wa_encoded = wa_text.replace(" ", "%20")
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Litoral Prime Imóveis</title>
<meta name="description" content="{subtitle}">
<link rel="canonical" href="https://praia.digital/cidades/{city_slug}-{slug}.html">
<link rel="alternate" hreflang="x-default" href="https://praia.digital/cidades/{city_slug}-{slug}.html" />
<link rel="alternate" hreflang="pt-BR" href="https://praia.digital/cidades/{city_slug}-{slug}.html">

<link rel="preload" as="image" href="https://praia.digital/img/default-home.jpg" type="image/jpeg" fetchpriority="high">

<link rel="preload" as="image" href="https://praia.digital/img/default-home.jpg" type="image/jpeg" fetchpriority="high">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{subtitle}">
<meta property="og:url" content="https://praia.digital/cidades/{city_slug}-{slug}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{subtitle}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Quais cidades são atendidas?","acceptedAnswer":{{"@type":"Answer","text":"Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe."}}}},{{"@type":"Question","name":"Como solicitar atendimento?","acceptedAnswer":{{"@type":"Answer","text":"Pelo formulário abaixo ou diretamente pelo WhatsApp."}}}}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{title}","description":"{subtitle}","areaServed":"{city_label}","provider":{{"@type":"LocalBusiness","name":"Litoral Prime Imóveis","telephone":"+5511954346288"}}}}
</script>
</head>
<body style="font-family:Arial,sans-serif;max-width:900px;margin:auto;padding:20px;color:#222;background:#f5f7fa">
<a id="skip-link" class="skip-link" href="#main" style="position:absolute;left:-9999px;">Pular para o conteúdo</a>
<header>
  <h1 style="color:#0b4f6c">{title}</h1>
  <p>{subtitle}</p>
</header>
<main id="main">
<section>
  <h2>Sobre</h2>
  <p>{body}</p>
</section>
<section style="margin-top:18px">
  <h2>Atendimento em {city_label}</h2>
  <p>Atendimento especializado pelo WhatsApp com consultores locais, visitas presenciais e suporte digital.</p>
  <p><a href="https://wa.me/5511954346288?text={wa_encoded}" target="_blank" rel="noopener" style="background:#0b4f6c;color:#fff;padding:10px 14px;border-radius:6px;text-decoration:none;">Contato WhatsApp</a></p>
</section>
<section style="margin-top:18px">
  <h2>Veja também</h2>
  <ul>
    <li><a href="../../cidades/{city_slug}.html">Imóveis em {city_label}</a></li>
    <li><a href="../../servicos.html">Todos os serviços</a></li>
    <li><a href="../../imoveis.html">Ver todos os imóveis</a></li>
  </ul>
</section>
</main>
<section class="recommended" style="margin-top:18px">
  <h2>Outras cidades</h2>
  <ul>
    <li><a href="santos-{slug}.html">Santos</a></li>
    <li><a href="guaruja-{slug}.html">Guarujá</a></li>
    <li><a href="praia-grande-{slug}.html">Praia Grande</a></li>
    <li><a href="sao-vicente-{slug}.html">São Vicente</a></li>
    <li><a href="itanhaem-{slug}.html">Itanhaém</a></li>
    <li><a href="mongagua-{slug}.html">Mongaguá</a></li>
    <li><a href="peruibe-{slug}.html">Peruíbe</a></li>
    <li><a href="bertioga-{slug}.html">Bertioga</a></li>
  </ul>
</section>
<footer aria-label="Rodapé" style="margin-top:24px">
  <p>© Litoral Prime Imóveis • <a href="https://praia.digital" rel="noopener">https://praia.digital</a></p>
  <p><a href="../sitemap.html">Mapa do site</a></p>
</footer>
</body>
</html>
"""
        path.write_text(html, encoding="utf-8")
        created += 1

print(f"Criados: {created}")
print(f"Ignorados/existentes: {skipped}")
print(f"Total alvo: {created + skipped}")
