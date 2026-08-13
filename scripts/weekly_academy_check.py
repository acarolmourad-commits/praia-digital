#!/usr/bin/env python3
"""
Verificação semanal da Academy — Praia Digital.
- Identifica quais formações têm maior necessidade de material complementar
- Verifica quais artigos estão levando tráfego para cada formação
- Identifica lacunas de conteúdo e oportunidades
- NÃO cria material automaticamente — só registra necessidades
Nunca toca na Batch 147.
"""
import json, re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.')
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
LINK_MAP = REPO / 'docs' / 'link_map.json'

FORMACOES = [
    'formacao-corretor-imoveis-litoral',
    'avaliacao-imoveis-ptam',
    'financiamento-imobiliario',
    'locacao-temporada-administracao',
    'captacao-imoveis',
    'marketing-imobiliario',
    'documentacao-imoveis',
    'mercado-imobiliario-litoral',
]

def analyze_formacao(slug: str) -> dict:
    """Analisa uma formação para identificar necessidades de material complementar."""
    path = FORMACOES_DIR / f'{slug}.html'
    if not path.exists():
        return {'slug': slug, 'status': 'missing', 'needs': []}

    html = path.read_text(encoding='utf-8', errors='ignore')

    needs = []
    priority = 0

    # Check FAQ
    faq_match = re.search(r'<h2>\s*(Perguntas frequentes|FAQ)\s*</h2>', html, re.IGNORECASE)
    faq_count = len(re.findall(r'class="faq-item"', html))
    if not faq_match or faq_count < 3:
        needs.append('faq')
        priority += 2

    # Check entidades
    has_entities = 'Entidades' in html or 'referências locais' in html.lower()
    if not has_entities:
        needs.append('entidades')
        priority += 1

    # Check related articles
    has_articles = 'Artigos relacionados' in html or 'Conteúdo complementar' in html
    if not has_articles:
        needs.append('artigos_relacionados')
        priority += 1

    # Check CTA
    has_cta = 'wa.me' in html or 'whatsapp' in html.lower()
    if not has_cta:
        needs.append('cta')
        priority += 2

    # Check size/complexity
    content_size = len(html)
    if content_size < 3000:
        needs.append('conteudo_base')
        priority += 1

    return {
        'slug': slug,
        'status': 'ok',
        'needs': needs,
        'priority': priority,
        'size': content_size,
        'has_faq': faq_count >= 3,
        'has_entities': has_entities,
        'has_articles': has_articles,
        'has_cta': has_cta,
    }

def analyze_link_map() -> dict:
    """Analisa o mapa de links para identificar formações com pouco tráfego."""
    if not LINK_MAP.exists():
        return {}

    with open(LINK_MAP, 'r', encoding='utf-8') as f:
        link_map = json.load(f)

    article_to_formations = link_map.get('article_to_formations', {})

    # Count articles per formation
    formation_article_count = {}
    for slug, formations in article_to_formations.items():
        for formation in formations:
            formation_article_count[formation] = formation_article_count.get(formation, 0) + 1

    return formation_article_count

def main():
    # 1. Analyze each formation
    formation_analysis = []
    for slug in FORMACOES:
        analysis = analyze_formacao(slug)
        formation_analysis.append(analysis)

    # 2. Analyze link map
    formation_traffic = analyze_link_map()

    # 3. Identify top needs
    top_needs = []
    for analysis in formation_analysis:
        if analysis['status'] == 'missing':
            top_needs.append({
                'formation': analysis['slug'],
                'need': 'pagina_ausente',
                'priority': 5,
                'justificativa': 'Página de formação não existe',
            })
            continue

        for need in analysis['needs']:
            top_needs.append({
                'formation': analysis['slug'],
                'need': need,
                'priority': analysis['priority'],
                'justificativa': f'Formação {analysis["slug"]} precisa de {need}',
            })

    # Sort by priority
    top_needs.sort(key=lambda x: -x['priority'])

    # 4. Identify content opportunities
    opportunities = []
    for analysis in formation_analysis:
        if analysis['status'] == 'ok':
            if 'exercicios_praticos' not in analysis['needs']:
                opportunities.append({
                    'formation': analysis['slug'],
                    'opportunity': 'exercicios_praticos',
                    'justificativa': 'Criar exercícios práticos para aplicar conteúdo',
                })
            if 'checklists' not in analysis['needs']:
                opportunities.append({
                    'formation': analysis['slug'],
                    'opportunity': 'checklists',
                    'justificativa': 'Criar checklists operacionais para corretores',
                })
            if 'modelos' not in analysis['needs']:
                opportunities.append({
                    'formation': analysis['slug'],
                    'opportunity': 'modelos',
                    'justificativa': 'Criar modelos/documentos editáveis',
                })

    # 5. Save analysis
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if 'academy_weekly' not in registry:
        registry['academy_weekly'] = []

    registry['academy_weekly'].append({
        'date': datetime.now(timezone.utc).isoformat(),
        'formation_analysis': formation_analysis,
        'formation_traffic': formation_traffic,
        'top_needs': top_needs[:10],
        'opportunities': opportunities[:10],
        'created_materials': [],  # Only populated when material is actually created
        'status': 'audited',
    })

    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

    print('[ACADEMY] Verificação semanal concluída')
    print(f'[ACADEMY] Formações auditadas: {len(formation_analysis)}')
    print(f'[ACADEMY] Necessidades identificadas: {len(top_needs)}')
    print(f'[ACADEMY] Oportunidades: {len(opportunities)}')

    # Print summary
    print('\n=== RESUMO ===')
    for analysis in formation_analysis:
        if analysis['status'] == 'ok':
            print(f"{analysis['slug']}: priority={analysis['priority']}, needs={analysis['needs']}")
        else:
            print(f"{analysis['slug']}: {analysis['status']}")

    if top_needs:
        print('\nTop necessidades:')
        for need in top_needs[:5]:
            print(f"  - {need['formation']}: {need['need']} (priority={need['priority']})")

    print('\n[ACADEMY] Nenhum material criado automaticamente — aguardando justificativa concreta')

if __name__ == '__main__':
    main()
