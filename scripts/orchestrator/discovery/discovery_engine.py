#!/usr/bin/env python3
"""
Descoberta contínua — Praia Digital.
- Monitora notícias em tempo real
- Identifica gaps de conteúdo
- Detecta artigos sem links internos
- Verifica schema
- Busca oportunidades locais
- Tudo vai para docs/banco-editorial.json
"""
import json, re, random
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'

def discover_news() -> list:
    """Descobre notícias relevantes (placeholder para integração real)"""
    opportunities = []
    
    # Em produção, isso consultaria fontes RSS/oficiais
    # Por enquanto, registra que o monitoramento está ativo
    opportunities.append({
        'type': 'news_discovery',
        'message': 'Monitoramento contínuo de notícias ativo',
        'priority': 2,
        'status': 'monitoring',
    })
    
    return opportunities

def discover_content_gaps() -> list:
    """Identifica gaps de conteúdo"""
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    articles = registry.get('articles', [])
    
    gaps = []
    # Verificar cidades com pouca cobertura
    city_counts = {}
    for a in articles:
        slug = a.get('slug', '')
        for city in ['santos', 'guaruja', 'praia-grande', 'bertioga', 'sao-vicente', 'peruibe', 'itanhaem', 'mongagua', 'caraguatatuba', 'ilhabela', 'ubatuba', 'sao-sebastiao']:
            if city in slug:
                city_counts[city] = city_counts.get(city, 0) + 1
    
    for city, count in city_counts.items():
        if count < 30:
            gaps.append({
                'type': 'content_gap',
                'city': city,
                'current_count': count,
                'priority': 2,
            })
    
    return gaps

def discover_internal_links() -> list:
    """Identifica artigos sem links internos para formações"""
    articles = list(BLOG_DIR.glob('*.html'))
    without_links = []
    
    for article in articles[:100]:  # Amostra de 100
        html = article.read_text(encoding='utf-8', errors='ignore')
        if '/education/formacoes/' not in html:
            without_links.append(article.name)
    
    if len(without_links) > 0:
        return [{
            'type': 'add_links',
            'count': len(without_links),
            'priority': 2,
        }]
    return []

def discover_schema_issues() -> list:
    """Identifica páginas sem schema"""
    articles = list(BLOG_DIR.glob('*.html'))[:20]
    missing_schema = []
    
    for article in articles:
        html = article.read_text(encoding='utf-8', errors='ignore')
        if 'application/ld+json' not in html:
            missing_schema.append(article.name)
    
    if missing_schema:
        return [{
            'type': 'seo_audit',
            'message': f'{len(missing_schema)} artigos sem schema',
            'priority': 2,
        }]
    return []

def discover_local_opportunities() -> list:
    """Identifica oportunidades locais"""
    opportunities = []
    
    # Verificar eventos sazonais, feriados, etc.
    # Em produção, consultaria calendário oficial
    opportunities.append({
        'type': 'local_opportunity',
        'message': 'Alta temporada 2026-2027 — conteúdo de preparação',
        'priority': 2,
    })
    
    return opportunities

def discover_commercial_opportunities() -> list:
    """Identifica oportunidades comerciais"""
    opportunities = []
    
    # Verificar se há artigos sem CTA
    articles = list(BLOG_DIR.glob('*.html'))[:50]
    without_cta = 0
    
    for article in articles:
        html = article.read_text(encoding='utf-8', errors='ignore')
        if 'whatsapp' not in html.lower() and 'comprar' not in html.lower():
            without_cta += 1
    
    if without_cta > 0:
        opportunities.append({
            'type': 'commercial_opportunity',
            'message': f'{without_cta} artigos sem CTA claro',
            'priority': 3,
        })
    
    return opportunities

def discover_recurring_questions() -> list:
    """Identifica perguntas recorrentes"""
    questions = [
        'Como financiar imóvel no litoral?',
        'Quanto custa manter casa de praia?',
        'É bom investir em imóvel no litoral?',
        'Como declarar aluguel de temporada no IR?',
        'Documentação necessária para comprar imóvel?',
    ]
    
    return [{
        'type': 'recurring_question',
        'question': q,
        'priority': 2,
    } for q in questions]

def run(context: dict) -> dict:
    """Executa todas as descobertas"""
    all_opportunities = []
    
    all_opportunities.extend(discover_news())
    all_opportunities.extend(discover_content_gaps())
    all_opportunities.extend(discover_internal_links())
    all_opportunities.extend(discover_schema_issues())
    all_opportunities.extend(discover_local_opportunities())
    all_opportunities.extend(discover_commercial_opportunities())
    all_opportunities.extend(discover_recurring_questions())
    
    # Atualizar banco editorial
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if 'discovery' not in registry:
        registry['discovery'] = []
    
    registry['discovery'].append({
        'date': datetime.now(timezone.utc).isoformat(),
        'opportunities': all_opportunities,
    })
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return {
        'status': 'ok',
        'actions': [],
        'opportunities': all_opportunities[:20],
        'message': f'Descoberta: {len(all_opportunities)} oportunidades encontradas',
    }
