#!/usr/bin/env python3
"""
Módulo: local-content — Praia Digital.
- Identifica cidades/bairros com cobertura fraca
- Detecta conteúdo duplicado/canibalização
- Gera oportunidades de conteúdo local reversível
Nunca toca na Batch 147.
"""
import json, re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

CITIES = [
    'santos', 'guaruja', 'praia-grande', 'bertioga', 'itanhaem',
    'mongagua', 'peruibe', 'caraguatatuba', 'ilhabela', 'sao-sebastiao', 'ubatuba', 'maresias'
]

def run(context: dict) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    articles = registry.get('articles', [])
    article_by_slug = {a.get('slug'): a for a in articles if a.get('slug')}

    # Count articles per city
    city_counts = {c: 0 for c in CITIES}
    for slug, article in article_by_slug.items():
        title = (article.get('title') or '').lower()
        for city in CITIES:
            if city.replace('-', ' ') in title or city in slug:
                city_counts[city] += 1
                break

    # Detect near-duplicate titles
    titles = [(slug, (article.get('title') or '')[:80]) for slug, article in article_by_slug.items()]
    titles.sort(key=lambda x: x[1].lower())

    duplicates = []
    for i in range(len(titles) - 1):
        if titles[i][1].lower() == titles[i+1][1].lower():
            duplicates.append((titles[i][0], titles[i+1][0], titles[i][1]))

    undercovered = [c for c, count in city_counts.items() if count < 50]

    opportunities = []
    for city in undercovered[:5]:
        opportunities.append({
            'type': 'local_content',
            'city': city,
            'current_count': city_counts[city],
            'priority': 2,
        })

    if duplicates:
        opportunities.append({
            'type': 'deduplication',
            'count': len(duplicates),
            'priority': 3,
        })

    return {
        'status': 'ok',
        'actions': [],
        'city_counts': city_counts,
        'undercovered': undercovered,
        'duplicates': duplicates[:10],
        'opportunities': opportunities[:10],
        'message': f'Local content: {len(undercovered)} cidades com cobertura < 50 artigos, {len(duplicates)} duplicatas potenciais',
    }
