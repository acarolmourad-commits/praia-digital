#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador automático de artigos SEO em lote para publicação diária.
Lê templates de temas, gera títulos, H2/H3, meta description e HTML otimizado.
"""
import os
import random
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(BASE, "blog")
DUP_DIR = os.path.join(BASE, "scripts", "blog")
if os.path.exists(DUP_DIR):
    import shutil; shutil.rmtree(DUP_DIR, ignore_errors=True)
TEMPLATES = [
    {"tema": "captação", "titulos": ["Como captar imóveis no litoral em baixa temporada", "5 táticas infalíveis para captação imobiliária no litoral paulista", "Captação de imóveis offseason: roteiro prático para corretores"]},
    {"tema": "seo", "titulos": ["SEO local para imobiliárias do litoral: passo a passo", "Como aparecer no Google Maps para imobiliárias", "Checklist SEO local para corretores do litoral em 2026"]},
    {"tema": "vendas", "titulos": ["Follow-up automático: do primeiro contato ao fechamento", "3 erros que matam vendas de temporada no litoral", "WhatsApp Business para imobiliárias: automação passo a passo"]},
    {"tema": "ferramentas", "titulos": ["Ferramentas gratuitas para corretores do litoral em 2026", "IA para imobiliárias: 3 usos práticos hoje", "Avaliação automática de preço: como usar no atendimento"]},
    {"tema": "gestao", "titulos": ["Gestão de temporada sem dor de cabeça", "Indicadores que todo corretor deve medir", "Plano de ação de 30 dias para imobiliárias do litoral"]},
]

def slugify(txt):
    return "".join(c if c.isalnum() or c == " " else "" for c in txt).strip().lower().replace(" ", "-")

def build_article(item, idx):
    title = item["titulos"][idx % len(item["titulos"])]
    tema = item["tema"]
    slug = f"{slugify(title)}-lote-{datetime.now().strftime('%Y-%m-%d')}-{idx+1}"
    h2 = [
        ["Por que isso importa no litoral paulista", "Passo 1: Diagnóstico rápido", "Passo 2: Execução prática", "Passo 3: Medição de resultado", "Conclusão"],
        ["O que mudou no mercado", "Checklist essencial", "Automação que funciona", "Erros comuns e como evitar", "Próximos passos"],
        ["Contexto do mercado", "Framework de aplicação", "Exemplo prático", "Métricas de sucesso", "Ação recomendada"],
        ["Visão geral do litoral", "Plano de execução simples", "Ferramentas recomendadas", "Checklist final", "Próximo passo"]
    ][idx % 5]
    meta = title + " — guia prático para imobiliárias e corretores do litoral paulista."
    slug_safe = slug.replace("?", "").replace("&", "").replace("=", "").replace("%", "")
    body = "\n".join([f'<h2>{h}</h2><p>Conteúdo prático sobre {tema} no litoral paulista. {random.choice(["Aplicável para temporada alta e baixa.","Sem ferramentas pagas.","Foco em conversão e automação."])}</p>' for h in h2])
    keywords = f"{title}, {tema} imobiliária, litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe, imóveis litoral, temporada, aluguel temporada"
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="https://praia.digital/blog/{slug_safe}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:image" content="https://praia.digital/img/default-home.jpg">
<meta property="og:url" content="https://praia.digital/blog/{slug_safe}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta}">
<meta name="twitter:image" content="https://praia.digital/img/default-home.jpg">
<meta name="robots" content="index, follow">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title}",
  "description": "{meta}",
  "url": "https://praia.digital/blog/{slug_safe}.html",
  "author": {{"@type": "Organization", "name": "Litoral Prime Imóveis"}},
  "publisher": {{"@type": "Organization", "name": "Litoral Prime Imóveis", "url": "https://praia.digital/"}}
}}
</script>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header>
  <nav aria-label="Navegação principal">
    <div class="logo">
      <h1>🏖️ Litoral Prime Imóveis</h1>
      <p class="tagline">Conteúdo para o litoral paulista</p>
    </div>
    <ul class="nav-menu">
      <li><a href="../index.html">Início</a></li>
      <li><a href="../servicos.html">Serviços</a></li>
      <li><a href="index.html">Blog</a></li>
    </ul>
  </nav>
</header>
<main id="main">
  <article>
    <h1>{title}</h1>
    <p>{meta}</p>
    {body}
    <p><a class="btn-whatsapp" href="https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20em%20{slug_safe.replace('-', '%20')}." target="_blank" rel="noopener">Fale com um especialista</a></p>
  </article>
</main>
<footer aria-label="Rodapé">
  <p>© Litoral Prime Imóveis • comercial@praia.digital • (11) 95434-6288</p>
</footer>
</body>
</html>"""
    path = os.path.join(OUT_DIR, f"{slug}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    created = []
    for idx, template in enumerate(TEMPLATES):
        for sub in range(0, len(template["titulos"])):
            p = build_article(template, idx * 10 + sub)
            created.append(p)
    print(f"Criados {len(created)} artigos em {OUT_DIR}")
    for p in created[:5]:
        print(f"- {p}")

if __name__ == "__main__":
    main()
