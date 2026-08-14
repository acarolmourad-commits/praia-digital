#!/usr/bin/env python3
"""
Comparação com acervo — Praia Digital.
- Compara oportunidades com todo o acervo editorial
- Verifica sobreposição de intenção, assunto, entidade, localização, palavra-chave
- Identifica: novo conteúdo, atualização, melhoria, fortalecimento de links ou descarte
- Nunca cria página redundante quando página existente atende a intenção
"""
import json, re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

# Cities for local matching
CITIES = [
    'santos', 'guarujá', 'praia grande', 'bertioga', 'são vicente',
    'peruíbe', 'itanhaém', 'mongaguá', 'caraguatatuba', 'ilhabela', 'ubatuba',
    'baixada santista', 'litoral paulista', 'litoral norte', 'litoral sul',
]

def load_archive() -> list:
    """Carrega acervo editorial para comparação"""
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    articles = registry.get('articles', [])
    # Also load existing HTML files
    existing_files = []
    for p in BLOG_DIR.glob('*.html'):
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
            existing_files.append({
                'path': str(p),
                'slug': p.stem,
                'text': txt[:5000],  # First 5KB for matching
            })
        except Exception:
            pass
    return articles, existing_files

def normalize(text: str) -> str:
    """Normaliza texto para comparação"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_cities(text: str) -> list:
    """Extrai cidades mencionadas no texto"""
    text_lower = text.lower()
    found = []
    for city in CITIES:
        if city in text_lower:
            found.append(city)
    return found

def check_overlap(opp: dict, articles: list, existing_files: list) -> dict:
    """
    Verifica sobreposição da oportunidade com o acervo.
    Retorna decisão: novo, atualizar, melhorar, linkar, descartar
    """
    opp_title = normalize(opp.get('title', opp.get('message', '')))
    opp_type = opp.get('type', '')
    opp_source = opp.get('source', '')
    
    # Extract entities from opportunity
    opp_cities = extract_cities(opp.get('title', '') + ' ' + opp.get('message', ''))
    
    best_match = None
    best_score = 0.0
    
    # Check against registry articles
    for article in articles:
        art_title = normalize(article.get('title', ''))
        art_slug = article.get('slug', '')
        art_cities = article.get('cities', [])
        
        # Calculate overlap
        title_overlap = len(set(opp_title.split()) & set(art_title.split())) / max(len(set(opp_title.split())), 1)
        city_overlap = len(set(opp_cities) & set(art_cities)) / max(len(set(opp_cities)), 1)
        
        overlap_score = title_overlap * 0.7 + city_overlap * 0.3
        
        if overlap_score > best_score:
            best_score = overlap_score
            best_match = {
                'type': 'registry',
                'article': article,
                'overlap': overlap_score,
            }
    
    # Check against existing HTML files
    for existing in existing_files:
        existing_text = normalize(existing.get('text', ''))
        existing_cities = extract_cities(existing.get('text', ''))
        
        title_overlap = len(set(opp_title.split()) & set(existing_text.split()[:20])) / max(len(set(opp_title.split())), 1)
        city_overlap = len(set(opp_cities) & set(existing_cities)) / max(len(set(opp_cities)), 1)
        
        overlap_score = title_overlap * 0.6 + city_overlap * 0.4
        
        if overlap_score > best_score:
            best_score = overlap_score
            best_match = {
                'type': 'html',
                'path': existing.get('path'),
                'slug': existing.get('slug'),
                'overlap': overlap_score,
            }
    
    # Decision logic
    if best_match and best_score >= 0.7:
        # High overlap - update or improve existing
        if opp_type in ['seo_audit', 'add_links', 'schema_fix']:
            return {
                'decision': 'melhorar',
                'reason': 'Conteúdo existente com sobreposição alta',
                'match': best_match,
                'overlap': best_score,
            }
        else:
            return {
                'decision': 'atualizar',
                'reason': 'Conteúdo existente que pode ser atualizado',
                'match': best_match,
                'overlap': best_score,
            }
    elif best_match and best_score >= 0.4:
        # Medium overlap - strengthen links or improve
        if opp_type == 'add_links':
            return {
                'decision': 'linkar',
                'reason': 'Conteúdo relacionado para linkar',
                'match': best_match,
                'overlap': best_score,
            }
        else:
            return {
                'decision': 'melhorar',
                'reason': 'Sobreposição média - melhorar existente',
                'match': best_match,
                'overlap': best_score,
            }
    else:
        # Low overlap - new content
        return {
            'decision': 'novo',
            'reason': 'Sem sobreposição significativa',
            'match': None,
            'overlap': best_score,
        }

def run(context: dict) -> dict:
    """Compara oportunidades com acervo editorial"""
    articles, existing_files = load_archive()
    
    # Get opportunities from context or registry
    opportunities = context.get('opportunities', [])
    if not opportunities:
        # Try to get from latest discovery
        registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
        news_disc = registry.get('news_discovery', [])
        if news_disc:
            latest = news_disc[-1]
            opportunities = latest.get('opportunities', [])
    
    results = []
    for opp in opportunities:
        comparison = check_overlap(opp, articles, existing_files)
        opp['comparison'] = comparison
        opp['decision'] = comparison.get('decision', 'novo')
        results.append(opp)
    
    # Count decisions
    decisions = {}
    for r in results:
        dec = r.get('decision', 'novo')
        decisions[dec] = decisions.get(dec, 0) + 1
    
    return {
        'status': 'ok',
        'opportunities': results,
        'decisions': decisions,
        'total_compared': len(results),
        'message': f'Comparadas {len(results)} oportunidades: {decisions}',
    }
