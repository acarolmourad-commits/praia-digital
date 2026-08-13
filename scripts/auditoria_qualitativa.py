#!/usr/bin/env python3
"""Auditoria qualitativa avançada do banco editorial."""
import json, pathlib, re, collections
from datetime import datetime, timezone

REPO = pathlib.Path('.')
with open(REPO / 'docs/banco-editorial.json', 'r', encoding='utf-8') as f:
    registry = json.load(f)

articles = registry.get('articles', [])
existing_slugs = {a.get('slug') for a in articles if a.get('slug')}

TRANSACTIONAL_CLUSTERS = {'compra_venda', 'locacao_temporada', 'investimento', 'financiamento', 'juridico'}
CITY_PRIORITY = ['santos', 'guaruja', 'praia_grande', 'bertioga', 'itanhaem', 'mongagua', 'peruibe', 'caraguatatuba', 'ilhabela', 'sao_sebastiao', 'sao_vicente', 'ubatuba', 'maresias', 'litoral_paulista']

# Priority 1: Fix intent in transactional clusters
intent_fix_candidates = []
for a in articles:
    slug = a.get('slug') or ''
    cluster = a.get('cluster') or ''
    intent = a.get('intent') or ''
    city = a.get('city') or ''
    if cluster in TRANSACTIONAL_CLUSTERS and intent == 'informacional' and city in CITY_PRIORITY:
        intent_fix_candidates.append({
            'slug': slug,
            'action': 'ATUALIZAR',
            'reason': f'Corrigir intent de informacional para comercial em cluster {cluster} (alto potencial de conversão)',
            'cluster': cluster,
            'city': city,
            'article_type': a.get('article_type') or 'A',
            'score': 9,
            'fix_type': 'intent'
        })

# Priority 2: Add FAQ to transactional clusters
faq_expand_candidates = []
for a in articles:
    slug = a.get('slug') or ''
    cluster = a.get('cluster') or ''
    city = a.get('city') or ''
    if cluster not in ['cases', 'parcerias', 'financiamento', 'juridico']:
        continue
    fp = REPO / 'blog' / f'{slug}.html'
    if not fp.exists():
        continue
    text = ''
    try:
        text = fp.read_text(encoding='utf-8', errors='ignore')
    except:
        pass
    if 'FAQ' not in text and 'faq' not in text:
        faq_expand_candidates.append({
            'slug': slug,
            'action': 'EXPANDIR',
            'reason': f'Adicionar FAQ + entidades locais para {cluster} (conversão)',
            'cluster': cluster,
            'city': city,
            'article_type': a.get('article_type') or 'A',
            'score': 8,
            'fix_type': 'faq'
        })

# Priority 3: Add local context to transactional clusters
local_context_candidates = []
for a in articles:
    slug = a.get('slug') or ''
    cluster = a.get('cluster') or ''
    city = a.get('city') or ''
    title = a.get('title') or ''
    h1 = a.get('h1') or ''
    meta = a.get('meta_description') or ''
    if cluster not in TRANSACTIONAL_CLUSTERS:
        continue
    if not city or city not in CITY_PRIORITY:
        continue
    city_norm = city.replace('_', ' ')
    hay = (title + ' ' + h1 + ' ' + meta).lower()
    if city_norm not in hay and city.replace('_', ' ') not in hay:
        local_context_candidates.append({
            'slug': slug,
            'action': 'ATUALIZAR',
            'reason': f'Incluir contexto local de {city.replace("_", " ")} em {cluster} (relevância local)',
            'cluster': cluster,
            'city': city,
            'article_type': a.get('article_type') or 'A',
            'score': 7,
            'fix_type': 'local_context'
        })

# Priority 4: Long-tail high-intent CREATE opportunities
long_tail_creates = [
    {
        'slug': 'como-declarar-aluguel-temporada-ir-2026',
        'title': 'Como declarar aluguel temporada no IR 2026',
        'cluster': 'locacao_temporada',
        'city': 'litoral_paulista',
        'article_type': 'C',
        'intent': 'comercial',
        'funnel': 'Fundo',
        'reason': 'Long-tail fiscal alta intenção; ausência total no banco',
        'score': 10,
        'action': 'CRIAR'
    },
    {
        'slug': 'seguro-fianca-aluguel-temporada-2026',
        'title': 'Seguro fiança para aluguel temporada no litoral — guia 2026',
        'cluster': 'locacao_temporada',
        'city': 'litoral_paulista',
        'article_type': 'C',
        'intent': 'comercial',
        'funnel': 'Fundo',
        'reason': 'Objeção frequente de proprietários; sem conteúdo específico',
        'score': 9,
        'action': 'CRIAR'
    },
    {
        'slug': 'distrato-construtora-imoveis-litoral-2026',
        'title': 'Distrato de construtora: direitos e passos no litoral paulista',
        'cluster': 'juridico',
        'city': 'litoral_paulista',
        'article_type': 'C',
        'intent': 'comercial',
        'funnel': 'Fundo',
        'reason': 'Risco alto para compradores; lacuna editorial crítica',
        'score': 10,
        'action': 'CRIAR'
    },
    {
        'slug': 'documentacao-venda-imovel-herdado-litoral',
        'title': 'Documentação para vender imóvel herdado no litoral paulista',
        'cluster': 'juridico',
        'city': 'litoral_paulista',
        'article_type': 'C',
        'intent': 'comercial',
        'funnel': 'Fundo',
        'reason': 'Cenário comum em litoral; sem guia prático',
        'score': 9,
        'action': 'CRIAR'
    },
    {
        'slug': 'financiamento-por-idade-imoveis-litoral',
        'title': 'Financiamento por idade: como usar na compra de imóveis no litoral',
        'cluster': 'financiamento',
        'city': 'litoral_paulista',
        'article_type': 'C',
        'intent': 'comercial',
        'funnel': 'Fundo',
        'reason': 'Dúvida recorrente de aposentados; sem resposta estruturada',
        'score': 9,
        'action': 'CRIAR'
    },
    {
        'slug': 'taxa-ocupacao-media-temporada-litoral',
        'title': 'Taxa de ocupação média para temporada no litoral paulista',
        'cluster': 'locacao_temporada',
        'city': 'litoral_paulista',
        'article_type': 'C',
        'intent': 'comercial',
        'funnel': 'Fundo',
        'reason': 'Indicador fundamental para investidores; sem conteúdo estruturado',
        'score': 9,
        'action': 'CRIAR'
    }
]

# Build balanced queue
queue = []
seen_slugs = set()

# 8 ATUALIZAR: mix of intent fix + local context
for item in intent_fix_candidates + local_context_candidates:
    if item['slug'] in seen_slugs:
        continue
    at_count = len([q for q in queue if q['action'] == 'ATUALIZAR'])
    if at_count >= 8:
        break
    queue.append(item)
    seen_slugs.add(item['slug'])

# 8 EXPANDIR: FAQ gaps
for item in faq_expand_candidates:
    if item['slug'] in seen_slugs:
        continue
    ex_count = len([q for q in queue if q['action'] == 'EXPANDIR'])
    if ex_count >= 8:
        break
    queue.append(item)
    seen_slugs.add(item['slug'])

# 4 CRIAR: long-tail high-intent
for item in long_tail_creates:
    if item['slug'] in seen_slugs or item['slug'] in existing_slugs:
        continue
    cr_count = len([q for q in queue if q['action'] == 'CRIAR'])
    if cr_count >= 4:
        break
    queue.append(item)
    seen_slugs.add(item['slug'])

# Backfill if needed
if len(queue) < 20:
    for item in faq_expand_candidates:
        if item['slug'] in seen_slugs:
            continue
        queue.append(item)
        seen_slugs.add(item['slug'])
        if len(queue) >= 20:
            break

if len(queue) < 20:
    for item in intent_fix_candidates + local_context_candidates:
        if item['slug'] in seen_slugs:
            continue
        queue.append(item)
        seen_slugs.add(item['slug'])
        if len(queue) >= 20:
            break

print('next_queue size:', len(queue))
for i, item in enumerate(queue, 1):
    print(f"{i:02d}. [{item['action']}] score={item.get('score', 'N/A')} | {item['slug']} | {item['cluster']} | {item.get('city','')} | {item['article_type']} | {item['reason']}")

# Save audit results
registry['auditoria_qualitativa'] = {
    'date': datetime.now(timezone.utc).isoformat(),
    'total_articles': len(articles),
    'action_counts': {
        'MANTER': len([s for s in articles if s.get('slug') not in [i['slug'] for i in intent_fix_candidates + faq_expand_candidates + local_context_candidates]]),
        'ATUALIZAR': len(intent_fix_candidates) + len(local_context_candidates),
        'EXPANDIR': len(faq_expand_candidates),
        'CRIAR': len(long_tail_creates)
    },
    'journey_gaps': [
        {'cluster': 'juridico', 'funnel': 'Fundo', 'count': 4},
        {'cluster': 'financiamento', 'funnel': 'Fundo', 'count': 3}
    ],
    'queue_summary': {
        'total': len(queue),
        'ATUALIZAR': len([q for q in queue if q['action'] == 'ATUALIZAR']),
        'EXPANDIR': len([q for q in queue if q['action'] == 'EXPANDIR']),
        'CRIAR': len([q for q in queue if q['action'] == 'CRIAR'])
    }
}

with open(REPO / 'docs/banco-editorial.json', 'w', encoding='utf-8') as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)

print('\nAuditoria registrada em docs/banco-editorial.json')
