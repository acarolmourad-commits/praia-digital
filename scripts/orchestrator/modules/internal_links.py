#!/usr/bin/env python3
"""
Módulo: internal-links — Praia Digital.
- Mapeia artigos ↔ formações Academy
- Identifica páginas com poucos links internos
- Gera oportunidades de linkagem contextual
Nunca toca na Batch 147.
"""
import json, re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
LINK_MAP = REPO / 'docs' / 'link_map.json'

FORMATION_KEYWORDS = {
    'formacao-corretor-imoveis-litoral': ['captacao', 'exclusividade', 'prospeccao', 'corretor', 'vendas', 'atendimento', 'fechamento'],
    'avaliacao-imoveis-ptam': ['avaliacao', 'avaliação', 'preco', 'preço', 'ptam', 'laudo', 'mercado'],
    'financiamento-imobiliario': ['financiamento', 'financiar', 'banco', 'entrada', 'parcela', 'aprova', 'credito', 'crédito'],
    'locacao-temporada-administracao': ['temporada', 'aluguel', 'locacao', 'locação', 'airbnb', 'booking', 'ocupacao', 'ocupação'],
    'captacao-imoveis': ['captacao', 'captação', 'exclusividade', 'lead', 'prospeccao', 'prospecção', 'whatsapp'],
    'marketing-imobiliario': ['marketing', 'anuncio', 'anúncio', 'instagram', 'redes', 'seo', 'google', 'ads'],
    'documentacao-imoveis': ['documentacao', 'documentação', 'contrato', 'escritura', 'itbi', 'registro', 'certidao', 'certidão'],
    'mercado-imobiliario-litoral': ['mercado', 'tendencia', 'tendência', 'valorizacao', 'valorização', 'preco', 'preço', 'investimento'],
}

def run(context: dict) -> dict:
    # Load registry
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    articles = registry.get('articles', [])
    article_by_slug = {a.get('slug'): a for a in articles if a.get('slug')}

    # Map formations to articles
    formation_articles = {}
    for formation, keywords in FORMATION_KEYWORDS.items():
        matched = []
        for slug, article in article_by_slug.items():
            title = (article.get('title') or '').lower()
            cluster = (article.get('cluster') or '').lower()
            haystack = title + ' ' + cluster
            if any(k in haystack for k in keywords):
                score = sum(1 for k in keywords if k in haystack)
                matched.append((slug, score))
        matched.sort(key=lambda x: -x[1])
        formation_articles[formation] = matched[:5]

    # Count articles per formation
    formation_counts = {f: len(m) for f, m in formation_articles.items()}

    # Identify underlinked formations
    avg_count = sum(formation_counts.values()) / max(len(formation_counts), 1)
    underlinked = [f for f, c in formation_counts.items() if c < avg_count]

    # Count articles without formation links
    blog_files = list(BLOG_DIR.glob('*.html'))
    without_links = 0
    for f in blog_files[:100]:  # sample
        html = f.read_text(encoding='utf-8', errors='ignore')
        if 'education/formacoes' not in html:
            without_links += 1

    opportunities = []
    for formation, count in formation_counts.items():
        if count < 3:
            opportunities.append({
                'type': 'add_links',
                'message': f"{formation}: {count} artigos relacionados",
                'priority': 3,
            })

    if without_links > 50:
        opportunities.append({
            'type': 'add_links',
            'message': f"{without_links} artigos sem links para formações",
            'priority': 2,
        })

    return {
        'status': 'ok',
        'actions': [],
        'formation_counts': formation_counts,
        'underlinked': underlinked,
        'opportunities': opportunities[:10],
        'message': f'Links internos: {len(blog_files)} artigos, {len(underlinked)} formações com poucos artigos',
    }
