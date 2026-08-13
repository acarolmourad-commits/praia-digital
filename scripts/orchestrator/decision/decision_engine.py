#!/usr/bin/env python3
"""
Motor de decisão — Praia Digital.
- Recebe oportunidades da descoberta
- Aplica scoring automático
- Decide ação: CRIAR, ATUALIZAR, EXPANDIR, LINKAR, CORRIGIR, MONITORAR, IGNORAR
- Sem depender de nova instrução humana para cada item
"""
import json
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

ACTION_CREATE = 'CRIAR'
ACTION_UPDATE = 'ATUALIZAR'
ACTION_EXPAND = 'EXPANDIR'
ACTION_LINK = 'LINKAR'
ACTION_FIX = 'CORRIGIR'
ACTION_MONITOR = 'MONITORAR'
ACTION_IGNORE = 'IGNORAR'

def score_opportunity(opp: dict) -> float:
    """Calcula score de 0 a 10 para uma oportunidade"""
    score = 5.0
    
    # Fatores de score
    priority = opp.get('priority', 1)
    score += priority * 0.5
    
    # Tipo de oportunidade
    opp_type = opp.get('type', '')
    if opp_type in ['news_discovery', 'content_gap']:
        score += 1.0
    elif opp_type in ['add_links', 'seo_audit']:
        score += 0.5
    elif opp_type in ['commercial_opportunity', 'recurring_question']:
        score += 1.5
    
    # Mensagem específica
    message = opp.get('message', '').lower()
    if 'alta temporada' in message or 'preparação' in message:
        score += 1.0
    if 'cta' in message:
        score += 0.5
    if 'schema' in message:
        score += 0.5
    
    return min(10.0, max(0.0, score))

def decide_action(opp: dict, context: dict) -> dict:
    """Decide ação baseada no tipo e score"""
    opp_type = opp.get('type', '')
    score = score_opportunity(opp)
    
    # Decisão baseada no tipo
    if opp_type == 'news_discovery':
        if score >= 7.0:
            return {'action': ACTION_CREATE, 'target': 'noticias/index.html', 'score': score}
        else:
            return {'action': ACTION_MONITOR, 'target': 'noticias', 'score': score}
    
    elif opp_type == 'content_gap':
        if score >= 7.0:
            return {'action': ACTION_CREATE, 'target': 'blog', 'score': score}
        else:
            return {'action': ACTION_MONITOR, 'target': 'blog', 'score': score}
    
    elif opp_type == 'add_links':
        return {'action': ACTION_LINK, 'target': 'blog_to_formacoes', 'score': score}
    
    elif opp_type == 'seo_audit':
        if score >= 6.0:
            return {'action': ACTION_FIX, 'target': 'schema', 'score': score}
        else:
            return {'action': ACTION_MONITOR, 'target': 'seo', 'score': score}
    
    elif opp_type == 'local_opportunity':
        if score >= 7.0:
            return {'action': ACTION_CREATE, 'target': 'blog', 'score': score}
        else:
            return {'action': ACTION_MONITOR, 'target': 'local_content', 'score': score}
    
    elif opp_type == 'commercial_opportunity':
        return {'action': ACTION_FIX, 'target': 'cta', 'score': score}
    
    elif opp_type == 'recurring_question':
        if score >= 7.0:
            return {'action': ACTION_EXPAND, 'target': 'faq', 'score': score}
        else:
            return {'action': ACTION_MONITOR, 'target': 'questions', 'score': score}
    
    else:
        return {'action': ACTION_IGNORE, 'target': 'unknown', 'score': score}

def run(context: dict) -> dict:
    """Processa oportunidades e decide ações"""
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    
    # Buscar oportunidades da descoberta
    opportunities = []
    if 'discovery' in registry and registry['discovery']:
        latest_discovery = registry['discovery'][-1]
        opportunities = latest_discovery.get('opportunities', [])
    
    # Processar cada oportunidade
    decisions = []
    for opp in opportunities:
        decision = decide_action(opp, context)
        decisions.append({
            'opportunity': opp,
            'decision': decision,
            'approved': decision['score'] >= 6.0 and decision['action'] != ACTION_IGNORE,
        })
    
    # Salvar decisões
    if 'decisions' not in registry:
        registry['decisions'] = []
    
    registry['decisions'].append({
        'date': datetime.now(timezone.utc).isoformat(),
        'decisions': decisions,
    })
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    
    approved = [d for d in decisions if d['approved']]
    ignored = [d for d in decisions if not d['approved']]
    
    return {
        'status': 'ok',
        'actions': [],
        'decisions': decisions[:10],
        'approved_count': len(approved),
        'ignored_count': len(ignored),
        'message': f'Decisões: {len(approved)} aprovadas, {len(ignored)} ignoradas',
    }
