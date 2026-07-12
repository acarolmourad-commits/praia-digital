#!/usr/bin/env python3
"""
gerar_seo_por_cidade.py
Gera artigos SEO unicos por cidade/tema no litoral paulista.
Uso: python scripts/automation/gerar_seo_por_cidade.py
"""

import random
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[2]
BLOG_DIR = BASE / "blog"

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

TEMPLATES = [
    "Guia rápido: {city}",
    "Checklist: temporada em {city}",
    "Follow-up automático para {city}",
    "Como captar leads em {city} sem anúncios",
    "SEO local em {city} para imóveis",
    "Métricas essenciais para corretores em {city}",
    "Reels para imobiliárias em {city}",
    "Investimento em imóveis em {city} em 2026",
    "Onboarding rápido para parceiros em {city}",
    "Negociação de imóveis em {city} sem perder o cliente",
    "Modelo de apresentação para imóveis em {city}",
    "WhatsApp para imobiliárias em {city}",
    "Case social rápido para parcerias em {city}",
    "Redes sociais para imóveis em {city}",
    "Proposta comercial para {city}",
]


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


def article_html(title, city, body):
    slug = slugify(title + "-" + city)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {city} | Praia Digital</title>
  <meta name="description" content="{body[:120]}...">
  <link rel="canonical" href="https://acarolmourad-commits.github.io/praia-digital/blog/{slug}.html">
  <style>
    :root{{bg:#f8fafc;text:#0f172a;border:#e5e7eb;primary:#2563eb;secondary:#0ea5e9}}
    body{{font:14px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text);padding:18px}}
    .wrap{{max-width:880px;margin:0 auto}}
    a{{color:var(--primary)}}
    ul{{padding-left:18px;margin:10px 0}}
    li{{margin:6px 0}}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{title}</h1>
    <p><strong>Local:</strong> {city}</p>
    {body}
    <p><a href="/praia-digital/ferramentas-gratuitas/imobiliarias/">Ferramentas gratuitas</a></p>
  </div>
</body>
</html>
"""


BODY_TEMPLATES = [
    "<p>Ação prática: use SEO local e follow-up em 3 dias.</p><ul><li>Página profissional por imóvel</li><li>WhatsApp direto</li><li>Conteúdo semanal</li></ul>",
    "<p>Checklist rápida: SEO, follow-up, visita e proposta.</p><ul><li>Defina cidade-alvo</li><li>Publique com preço</li><li>Agende follow-up</li></ul>",
    "<p>Passo a passo para {city}: captação, conteúdo, métricas.</p><ul><li>Captação sem spam</li><li>Reels curtos</li><li>Métricas simples</li></ul>",
]


def generate(n=10):
    count = 0
    used = set()
    for city in CITIES:
        for _ in range(n):
            tmpl = random.choice(TEMPLATES)
            title = tmpl.format(city=city)
            body = random.choice(BODY_TEMPLATES).format(city=city)
            slug = slugify(title + "-" + city)
            if slug in used:
                continue
            used.add(slug)
            path = BLOG_DIR / f"{slug}.html"
            path.write_text(article_html(title, city, body), encoding="utf-8")
            count += 1
    print(f"Gerados {count} artigos SEO em {BLOG_DIR}")


if __name__ == "__main__":
    generate()
