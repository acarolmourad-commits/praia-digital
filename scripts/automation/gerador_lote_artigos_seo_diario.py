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
    body = "\n".join([f'<h2>{h}</h2><p>Conteúdo prático sobre {tema} no litoral paulista. {random.choice(["Aplicável para temporada alta e baixa.","Sem ferramentas pagas.","Foco em conversão e automação."])}</p>' for h in h2])
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://acarolmourad-commits.github.io/praia-digital/blog/{slug}.html">
</head>
<body>
<article>
<h1>{title}</h1>
<p>{meta}</p>
{body}
<p>Ferramentas gratuitas em <a href="https://praia.digital">praia.digital</a></p>
</article>
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
