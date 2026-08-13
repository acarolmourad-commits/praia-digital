#!/usr/bin/env python3
"""
Módulo: Academy — Praia Digital.
- Verifica necessidades das 8 formações
- Identifica lacunas e oportunidades
- NÃO cria material automaticamente
Nunca toca na Batch 147.
"""
import json, re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

FORMACOES = [
    'formacao-corretor-imoveis-litoral', 'avaliacao-imoveis-ptam', 'financiamento-imobiliario',
    'locacao-temporada-administracao', 'captacao-imoveis', 'marketing-imobiliario',
    'documentacao-imoveis', 'mercado-imobiliario-litoral',
]

def analyze_formacao(slug: str) -> dict:
    path = FORMACOES_DIR / f'{slug}.html'
    if not path.exists():
        return {'slug': slug, 'status': 'missing', 'needs': [], 'priority': 0}

    html = path.read_text(encoding='utf-8', errors='ignore')
    needs = []
    priority = 0

    faq_match = re.search(r'<h2>\s*(Perguntas frequentes|FAQ)\s*</h2>', html, re.IGNORECASE)
    faq_count = len(re.findall(r'class="faq-item"', html))
    if not faq_match or faq_count < 3:
        needs.append('faq')
        priority += 2

    if 'Entidades' not in html and 'referências locais' not in html.lower():
        needs.append('entidades')
        priority += 1

    if 'Artigos relacionados' not in html and 'Conteúdo complementar' not in html:
        needs.append('artigos_relacionados')
        priority += 1

    if 'wa.me' not in html and 'whatsapp' not in html.lower():
        needs.append('cta')
        priority += 2

    if len(html) < 3000:
        needs.append('conteudo_base')
        priority += 1

    return {
        'slug': slug, 'status': 'ok', 'needs': needs, 'priority': priority,
        'size': len(html), 'has_faq': faq_count >= 3,
    }

def run(context: dict) -> dict:
    analyses = [analyze_formacao(s) for s in FORMACOES]
    needs = [{'formation': a['slug'], 'need': n, 'priority': a['priority']} for a in analyses for n in a['needs']]
    needs.sort(key=lambda x: -x['priority'])

    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    registry.setdefault('academy_weekly', []).append({
        'date': datetime.now(timezone.utc).isoformat(),
        'formation_analysis': analyses,
        'top_needs': needs[:10],
        'created_materials': [],
        'status': 'audited',
    })
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

    return {
        'status': 'ok',
        'actions': [],
        'analyses': analyses,
        'needs': needs[:10],
        'message': f'Academy auditada: {len(analyses)} formações, {len(needs)} necessidades identificadas',
    }
