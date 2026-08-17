#!/usr/bin/env python3
"""
Editorial expansion module for Praia Digital.
Identifies high-intent expansion targets and generates SEO articles
aligned with the editorial database and design system.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

REPO = Path(__file__).resolve().parents[3]
BANK_PATH = REPO / 'docs' / 'banco-editorial.json'
BLOG_DIR = REPO / 'blog'
SITEMAP_PATH = REPO / 'sitemap.xml'

PRIORITY_CLUSTERS = [
    'automacao_ia',
    'locacao_temporada',
    'compra_venda',
    'bairros_cidades',
    'marketing_digital',
    'investimento',
]


def load_bank():
    if not BANK_PATH.exists():
        raise FileNotFoundError(f'Banco editorial não encontrado: {BANK_PATH}')
    return json.loads(BANK_PATH.read_text(encoding='utf-8'))


def get_expansion_targets(articles, min_score=3):
    """
    Return high-intent expansion targets from priority clusters
    that are not generic litoral_paulista.
    """
    targets = []
    for a in articles:
        cluster = a.get('cluster') or ''
        city = a.get('city') or ''
        intent = a.get('intent') or ''
        funnel = a.get('funnel') or ''
        conv = a.get('conversion_potential') or ''
        
        if cluster not in PRIORITY_CLUSTERS:
            continue
        if not city or city == 'litoral_paulista':
            continue
        
        score = 0
        if intent == 'comercial':
            score += 3
        if intent == 'navegacional_comparativo':
            score += 2
        if funnel in ('Fundo', 'Meio'):
            score += 2
        if conv in ('alta', 'muito_alta'):
            score += 2
        if a.get('hotmart_link') or a.get('product_related_id'):
            score += 1
        
        if score >= min_score:
            targets.append({
                'id': a.get('id'),
                'title': a.get('title') or a.get('titulo'),
                'cluster': cluster,
                'city': city,
                'intent': intent,
                'funnel': funnel,
                'conversion_potential': conv,
                'score': score,
                'path': a.get('path'),
                'primary_keyword': a.get('primary_keyword'),
                'keywords': a.get('keywords', []),
                'meta_description': a.get('meta_description'),
                'recommended_cta': a.get('recommended_cta'),
                'hotmart_link': a.get('hotmart_link'),
                'product_related_id': a.get('product_related_id'),
            })
    
    targets.sort(key=lambda x: x['score'], reverse=True)
    return targets


def cluster_summary(articles):
    clusters = Counter(a.get('cluster') or 'sem_cluster' for a in articles)
    return dict(clusters.most_common())


def city_summary(articles, limit=20):
    cities = Counter(a.get('city') or 'sem_cidade' for a in articles)
    return dict(cities.most_common(limit))


def intent_summary(articles):
    intents = Counter(a.get('intent') or 'sem_intent' for a in articles)
    return dict(intents.most_common())


def funnel_summary(articles):
    funnels = Counter(a.get('funnel') or 'sem_funil' for a in articles)
    return dict(funnels.most_common())


def expansion_plan(articles, batch_size=10):
    """
    Generate a batch expansion plan: select top targets grouped by cluster/city.
    Returns batches ready for generation.
    """
    targets = get_expansion_targets(articles)
    
    # Group by cluster then city
    grouped = defaultdict(list)
    for t in targets:
        grouped[(t['cluster'], t['city'])].append(t)
    
    batches = []
    current_batch = []
    
    for (cluster, city), items in sorted(grouped.items(), key=lambda x: (x[0][0], -len(x[1]))):
        for item in items[:3]:  # max 3 per cluster/city per batch
            current_batch.append(item)
            if len(current_batch) >= batch_size:
                batches.append(current_batch)
                current_batch = []
    
    if current_batch:
        batches.append(current_batch)
    
    return batches


def validate_slug(title, city):
    """Generate a URL-safe slug from title + city."""
    slug = f"{city} {title}".lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')


def validate_target(target, existing_paths):
    """
    Validate that a target is viable for expansion:
    - path not already existing
    - slug unique
    - required fields present
    """
    city = target.get('city') or ''
    title = target.get('title') or ''
    
    if not city or not title:
        return False, 'missing city or title'
    
    slug = validate_slug(title, city)
    expected_path = f"blog/{slug}.html"
    
    if expected_path in existing_paths:
        return False, f'path already exists: {expected_path}'
    
    if not target.get('primary_keyword'):
        return False, 'missing primary_keyword'
    
    return True, slug


def run_analysis():
    """Run full expansion analysis and print report."""
    data = load_bank()
    articles = data.get('articles', [])
    
    print('=== EXPANSÃO EDITORIAL - ANÁLISE ===')
    print(f'Total artigos no banco: {len(articles)}')
    print(f'Clusters prioritários: {", ".join(PRIORITY_CLUSTERS)}')
    
    targets = get_expansion_targets(articles)
    print(f'Alvos de expansão priorizada: {len(targets)}')
    
    print('\nResumo por cluster:')
    for cluster in PRIORITY_CLUSTERS:
        count = sum(1 for t in targets if t['cluster'] == cluster)
        print(f'  {cluster}: {count} alvos')
    
    print('\nTop 20 cidades:')
    city_counts = Counter(t['city'] for t in targets)
    for city, count in city_counts.most_common(20):
        print(f'  {city}: {count}')
    
    batches = expansion_plan(articles, batch_size=10)
    print(f'\nLotes de expansão planejados: {len(batches)}')
    for i, batch in enumerate(batches[:5], 1):
        print(f'  Lote {i}: {len(batch)} artigos')
    
    print('\nPronto para expansão controlada pós-D2.')


if __name__ == '__main__':
    run_analysis()
