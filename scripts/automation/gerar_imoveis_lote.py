#!/usr/bin/env python3
"""
gerar_imoveis_lote.py
Gera páginas de imóveis em massa para o litoral paulista.
Uso: python scripts/automation/gerar_imoveis_lote.py
"""

import random
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[2]
IMOVEIS_DIR = BASE / "imoveis"

TITLES = [
    "Apartamento Vista Mar",
    "Casa com Piscina",
    "Cobertura Duplex",
    "Studio para Temporada",
    "Loft Moderno",
    "Casa Geminada",
    "Apartamento Beira-Mar",
    "Casa em Condomínio",
    "Sobrado Geminado",
    "Casa Rural",
]
CITIES = [
    "Praia Grande",
    "Caraguatatuba",
    "Ilhabela",
    "Ubatuba",
    "São Sebastião",
    "Bertioga",
    "Maresias",
    "Guarujá",
    "Iguape",
    "Cananéia",
]
PRICES = [290000, 520000, 610000, 640000, 740000, 760000, 790000, 870000, 980000, 1050000, 1200000, 1450000]


def slugify(text):
    return (
        text.lower()
        .replace(" ", "-")
        .replace("ç", "c")
        .replace("ã", "a")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("â", "a")
        .replace("ê", "e")
        .replace("ô", "o")
        .replace("ü", "u")
    )


def generate(start=370, count=20):
    count_file = 0
    for i in range(start, start + count):
        title = random.choice(TITLES)
        city = random.choice(CITIES)
        price = random.choice(PRICES)
        slug = slugify(f"{title}-{city}") + f"-{i}"
        path = IMOVEIS_DIR / f"imovel-{i}.html"
        if path.exists():
            continue
        bedrooms = random.randint(1, 5)
        bathrooms = random.randint(1, 4)
        area = random.randint(45, 280)
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} em {city} | Praia Digital</title>
  <meta name="description" content="{title} em {city} com ótimo custo-benefício.">
  <link rel="canonical" href="https://acarolmourad-commits.github.io/praia-digital/imoveis/imovel-{i}.html">
  <style>
    :root{{color:#0d1b2a;primary:#4f46e5;secondary:#0ea5e9;accent:#10b981;bg:#f8fafc;text:#0f172a;muted:#475569;border:#e5e7eb}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
    .wrap{{max-width:1000px;margin:0 auto;padding:16px}}
    header{{background:linear-gradient(135deg,var(--color),var(--primary));color:white;padding:18px 0}}
    header a{{color:#fbffaa;text-decoration:none}}
    .tag{{background:#eef2ff;color:#312e81;border:1px solid #c7d2fe;padding:4px 10px;border-radius:999px;font-size:12px;display:inline-block;margin:4px 0 10px}}
    .price{{font-size:22px;font-weight:800;color:var(--color)}}
    .features{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));margin:14px 0}}
    .chip{{background:white;border:1px solid var(--border);border-radius:12px;padding:10px;text-align:center;box-shadow:0 1px 0 rgba(0,0,0,.04)}}
    .cta{{background:var(--primary);color:white;padding:14px 18px;border-radius:14px;display:inline-block;text-decoration:none;font-weight:700}}
    footer{{color:var(--muted);font-size:12px;text-align:center;padding:18px 0}}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <a href="/praia-digital/"><h1>Praia Digital</h1></a>
      <p>Inteligencia imobiliaria no litoral paulista</p>
    </div>
  </header>
  <main class="wrap">
    <span class="tag">{title} · {city}</span>
    <h2>{title} em {city}</h2>
    <p class="price">R$ {price:,.0f}</p>
    <div class="features">
      <div class="chip"><strong>{bedrooms}</strong><br>quartos</div>
      <div class="chip"><strong>{bathrooms}</strong><br>banheiros</div>
      <div class="chip"><strong>{area}</strong><br>m²</div>
    </div>
    <p>Oportunidade em {city}.</p>
    <a class="cta" href="mailto:comercial@praia.digital?subject=Interesse%20no%20{title}%20em%20{city}">Tenho interesse</a>
    <p><a href="/praia-digital/ferramentas-gratuitas/imobiliarias/">Ferramentas gratuitas</a></p>
  </main>
  <footer>© Praia Digital</footer>
</body>
</html>
"""
        path.write_text(html, encoding="utf-8")
        count_file += 1
    print(f"Gerados {count_file} imóveis em {IMOVEIS_DIR}")


if __name__ == "__main__":
    generate()
