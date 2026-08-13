#!/usr/bin/env python3
"""
Módulo: metrics — Praia Digital.
- Coleta métricas de desempenho do site
- Identifica tendências e anomalias
- Não altera nada, só registra dados
"""
import json, re, random
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

def run(context: dict) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))

    # Site metrics
    blog_count = len(list(BLOG_DIR.glob('*.html')))
    formacoes_count = len(list(FORMACOES_DIR.glob('*.html')))
    total_articles = len(registry.get('articles', []))
    next_queue = len(registry.get('next_queue', []))

    # Batch 146 measurement status
    batch146 = registry.get('batch_history', [{}])[0] if registry.get('batch_history') else {}
    measurement_pending = batch146.get('measurement_pending', False)

    metrics = {
        'blog_pages': blog_count,
        'formacoes_pages': formacoes_count,
        'registry_articles': total_articles,
        'next_queue': next_queue,
        'batch146_measurement_pending': measurement_pending,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }

    # Identify trends/opportunities
    opportunities = []
    if blog_count > 2000:
        opportunities.append({
            'type': 'content_maturation',
            'message': 'Site tem mais de 2000 páginas — foco em atualização e links internos',
            'priority': 2,
        })

    if next_queue == 0 and not measurement_pending:
        opportunities.append({
            'type': 'next_queue_empty',
            'message': 'next_queue zerada — aguardando nova auditoria qualitativa',
            'priority': 1,
        })

    if measurement_pending:
        opportunities.append({
            'type': 'measurement_window',
            'message': 'Batch 146 em medição — não criar novas batches',
            'priority': 3,
        })

    return {
        'status': 'ok',
        'actions': [],
        'metrics': metrics,
        'opportunities': opportunities,
        'message': f'Métricas coletadas: {blog_count} blog pages, {formacoes_count} formações, {total_articles} artigos',
    }
