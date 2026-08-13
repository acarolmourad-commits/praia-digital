#!/usr/bin/env python3
"""
Módulo: notícias curadas — Praia Digital.
- Pesquisa fontes oficiais
- Classifica por relevância imobiliária/local
- Publica se houver pauta suficiente
- Senão registra sem_pauta_suficiente
Nunca toca na Batch 147.
"""
import json, re, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
NOTICIAS_HTML = REPO / 'noticias' / 'index.html'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

SOURCES = [
    'site:crecisp.gov.br', 'site:agencia.sp.gov.br',
    'site:santos.sp.gov.br', 'site:guaruja.sp.gov.br',
    'site:praiagrande.sp.gov.br', 'site:ilhabela.sp.gov.br',
    'site:ubatuba.sp.gov.br', 'site:itanhaem.sp.gov.br',
    'site:mongagua.sp.gov.br', 'site:peruibe.sp.gov.br',
    'site:caraguatatuba.sp.gov.br', 'site:sinduscon-sp.org.br',
]

KEYWORDS = [
    'mercado imobiliário', 'imóveis', 'financiamento', 'crédito imobiliário',
    'habitação', 'construção civil', 'infraestrutura', 'turismo',
    'temporada', 'aluguel', 'locação', 'CRECISP', 'IPTU', 'ITBI',
    'documentação', 'legislação', 'imobiliária', 'corretor',
    'litoral', 'santos', 'guarujá', 'praia grande', 'bertioga',
    'ilhabela', 'ubatuba', 'peruíbe', 'itanhaém', 'mongaguá',
]

def evaluate_pauta(item: dict) -> dict:
    title = (item.get('title') or '').lower()
    desc = (item.get('description') or '').lower()
    url = (item.get('url') or '').lower()
    text = title + ' ' + desc + ' ' + url

    score = 0
    reasons = []
    if any(y in text for y in ['2026', '2025']):
        score += 2; reasons.append('atualidade')
    imm = ['imóvel', 'imobiliário', 'financiamento', 'construção', 'habitação', 'crédito', 'IPTU', 'ITBI', 'aluguel', 'locação']
    if any(k in text for k in imm):
        score += 3; reasons.append('relevância imobiliária')
    coast = ['santos', 'guarujá', 'praia grande', 'bertioga', 'ilhabela', 'ubatuba', 'peruíbe', 'itanhaém', 'mongaguá', 'caraguatatuba', 'litoral']
    if any(c in text for c in coast):
        score += 2; reasons.append('impacto local')
    if any(s.replace('site:', '') in url for s in SOURCES):
        score += 2; reasons.append('fonte oficial')
    high = ['vendas', 'preço', 'financiamento', 'documentação', 'temporada', 'aluguel', 'imposto']
    if any(k in text for k in high):
        score += 1; reasons.append('potencial de busca')
    utility = ['como', 'guia', 'checklist', 'modelo', 'dicas', 'passo a passo', 'impacto']
    if any(k in text for k in utility):
        score += 1; reasons.append('utilidade prática')

    return {
        'score': score, 'sufficient': score >= 5,
        'reasons': reasons,
        'title': item.get('title'), 'url': item.get('url'),
        'description': item.get('description', '')[:300],
    }

def run(context: dict) -> dict:
    seed_file = REPO / 'docs' / 'news_seed.json'
    if not seed_file.exists():
        registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
        registry.setdefault('news_audit', []).append({
            'date': datetime.now(timezone.utc).isoformat(),
            'status': 'sem_pauta_suficiente',
            'reason': 'Nenhuma pauta encontrada na semana',
        })
        REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
        return {'status': 'sem_pauta_suficiente', 'actions': []}

    items = json.loads(seed_file.read_text(encoding='utf-8')).get('items', [])
    evaluated = [evaluate_pauta(i) for i in items]
    sufficient = [e for e in evaluated if e['sufficient']]

    if not sufficient:
        registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
        registry.setdefault('news_audit', []).append({
            'date': datetime.now(timezone.utc).isoformat(),
            'status': 'sem_pauta_suficiente',
            'reason': 'Pautas abaixo do threshold',
            'scores': [{'title': e['title'], 'score': e['score'], 'reasons': e['reasons']} for e in evaluated],
        })
        REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
        return {'status': 'sem_pauta_suficiente', 'actions': []}

    best = max(sufficient, key=lambda x: x['score'])
    # Publication logic would go here; for now, return opportunity
    return {
        'status': 'pauta_aprovada',
        'actions': [{'type': 'news_publish', 'title': best['title'], 'score': best['score']}],
        'opportunity': best,
    }
