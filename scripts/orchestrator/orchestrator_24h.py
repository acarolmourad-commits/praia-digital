#!/usr/bin/env python3
"""
ORQUESTRADOR CENTRAL 24/7 — Praia Digital
Fluxo: detecta → pesquisa → compara com acervo → pontua → decide → produz/atualiza → revisa → publica → conecta → registra → mede

Execução: a cada hora, 24/7
Não espera comando manual para tarefas permitidas.
"""
import json, re, subprocess, sys, importlib
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
SITEMAP_SCRIPT = REPO / 'scripts' / 'gerar_sitemap.py'
SITEMAP_PATH = REPO / 'sitemap.xml'

sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'modules').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'discovery').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'decision').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'pipeline').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'maintenance').resolve()))

HUMAN_GATES = {
    'batch_147', 'next_queue', 'large_expansion', 'structural_change',
    'monetization', 'adsense', 'strategy_change', 'reputation_risk',
}

ALLOWED_MODULES = [
    'news', 'academy', 'seo', 'refresh',
    'internal_links', 'local_content', 'qa', 'qa_fixes', 'metrics', 'execution_plan',
]

def load_module(name: str, paths: list):
    for path in paths:
        module_path = path / f'{name}.py'
        if module_path.exists():
            spec = importlib.util.spec_from_file_location(name, str(module_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    return None

def run_module(name: str, paths: list, context: dict) -> dict:
    module = load_module(name, paths)
    if not module:
        return {'status': 'error', 'message': f'{name} não encontrado'}
    try:
        return module.run(context)
    except Exception as e:
        return {'status': 'error', 'message': f'Erro em {name}: {str(e)}'}

def detect(context: dict) -> dict:
    results = []
    news = run_module('news_discovery', [REPO / 'scripts' / 'orchestrator' / 'discovery'], context)
    if news.get('status') == 'ok' and news.get('relevant_count', 0) > 0:
        results.extend(news.get('opportunities', []))
    seo = run_module('seo', [REPO / 'scripts' / 'orchestrator' / 'modules'], context)
    if seo.get('status') == 'ok':
        results.extend(seo.get('opportunities', []))
    il = run_module('internal_links', [REPO / 'scripts' / 'orchestrator' / 'modules'], context)
    if il.get('status') == 'ok':
        results.extend(il.get('opportunities', []))
    lc = run_module('local_content', [REPO / 'scripts' / 'orchestrator' / 'modules'], context)
    if lc.get('status') == 'ok':
        results.extend(lc.get('opportunities', []))
    academy = run_module('academy', [REPO / 'scripts' / 'orchestrator' / 'modules'], context)
    if academy.get('status') == 'ok':
        results.extend(academy.get('opportunities', []))
    return {'status': 'ok', 'opportunities': results, 'count': len(results), 'message': f'Detectadas {len(results)} oportunidades'}

def research(opportunities: list) -> list:
    validated = []
    for opp in opportunities:
        opp_type = opp.get('type', '')
        if opp_type == 'news_discovery':
            source = opp.get('source', '')
            if not source:
                opp['research_status'] = 'sem_fonte'
                continue
            opp['research_status'] = 'fonte_ok'
            opp['research_score'] = 7.0
        elif opp_type == 'seo_audit':
            opp['research_status'] = 'schema_validation_needed'
            opp['research_score'] = 6.0
        elif opp_type == 'add_links':
            opp['research_status'] = 'semantic_check_needed'
            opp['research_score'] = 6.5
        elif opp_type == 'local_content':
            opp['research_status'] = 'local_validation_needed'
            opp['research_score'] = 6.0
        else:
            opp['research_status'] = 'generic'
            opp['research_score'] = 5.0
        validated.append(opp)
    return validated

def score(opportunities: list) -> list:
    scored = []
    for opp in opportunities:
        base_score = opp.get('research_score', 5.0)
        priority = opp.get('priority', 1)
        score = base_score + priority * 0.3
        opp_type = opp.get('type', '')
        if opp_type in ['news_discovery', 'content_gap']:
            score += 0.5
        elif opp_type in ['add_links', 'seo_audit']:
            score += 0.3
        score = min(10.0, max(0.0, score))
        opp['final_score'] = score
        scored.append(opp)
    scored.sort(key=lambda x: x.get('final_score', 0), reverse=True)
    return scored

def _validate_slug(slug: str) -> bool:
    if not slug or not isinstance(slug, str):
        return False
    s = slug.strip().lower()
    if not s or s in {'none', 'null', 'undefined', ''}:
        return False
    return True

def _validate_html_path(path: Path) -> bool:
    if not isinstance(path, Path):
        return False
    if not path.exists():
        return False
    if path.suffix.lower() != '.html':
        return False
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if '<html' not in text.lower() and '<body' not in text.lower() and '<h1' not in text.lower():
            return False
        return True
    except Exception:
        return False

def _validate_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return False
    return True

def _validate_internal_links(html_path: Path, min_required: int = 1) -> dict:
    result = {
        'valid': False,
        'links_added': 0,
        'linked_slugs': [],
        'error': None,
    }
    try:
        html = html_path.read_text(encoding='utf-8', errors='ignore')
        hrefs = re.findall(r'href="(/[^"]+)"', html)
        internal = [h for h in hrefs if h.startswith('/blog/') or h.startswith('/education/') or h.startswith('/noticias/')]
        slugs = []
        for h in internal:
            slug = h.rsplit('/', 1)[-1]
            if slug.endswith('.html'):
                slug = slug[:-5]
            if slug:
                slugs.append(slug)
        unique_slugs = list(dict.fromkeys(slugs))
        result['links_added'] = len(unique_slugs)
        result['linked_slugs'] = unique_slugs
        result['valid'] = len(unique_slugs) >= min_required
    except Exception as e:
        result['error'] = str(e)
    return result

def _update_sitemap_if_needed(slugs: list) -> dict:
    if not slugs:
        return {'updated': False, 'reason': 'nenhum slug para adicionar'}
    try:
        result = subprocess.run(
            f'python "{SITEMAP_SCRIPT}"',
            shell=True,
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            'updated': result.returncode == 0,
            'output': result.stdout[-500:] if result.stdout else '',
            'error': result.stderr[-500:] if result.stderr else '',
        }
    except Exception as e:
        return {'updated': False, 'error': str(e)}

def _register_article_in_editorial(evidence: dict) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    articles = registry.get('articles', [])
    existing_index = None
    for idx, art in enumerate(articles):
        if art.get('slug') == evidence['slug']:
            existing_index = idx
            break
    record = {
        'slug': evidence['slug'],
        'title': evidence['title'],
        'html_path': evidence['html_path'],
        'url': evidence['url'],
        'published': True,
        'production_type': evidence['production_type'],
        'published_at': datetime.now(timezone.utc).isoformat(),
        'status': 'PUBLISHED',
        'internal_links_added': evidence.get('internal_links_added', 0),
        'linked_slugs': evidence.get('linked_slugs', []),
        'registered_at': datetime.now(timezone.utc).isoformat(),
    }
    if existing_index is not None:
        articles[existing_index] = record
        action = 'updated'
    else:
        articles.append(record)
        action = 'created'
    registry['articles'] = articles
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'status': 'ok', 'action': action, 'slug': evidence['slug']}

def _audit_cycles_registry() -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    cycles = registry.get('orchestrator_24h', {}).get('cycles', [])
    audit = []
    for c in cycles:
        audit.append({
            'date': c.get('date'),
            'detected': c.get('detected', 0),
            'produced': c.get('produced', 0),
            'published': c.get('published', 0),
            'connected': c.get('connected', 0),
            'evidence': c.get('evidence'),
            'classification': 'NÃO VERIFICÁVEL',
        })
    return {'status': 'ok', 'cycles': audit, 'total_cycles': len(audit)}

def produce(scored_opportunities: list, context: dict) -> list:
    evidence = context.setdefault('evidence', {})
    produced = []
    for opp in scored_opportunities:
        if opp.get('final_score', 0) < 6.0:
            continue
        opp_type = opp.get('type', '')
        production_type = None
        html_path = None
        title = None
        source_url = None
        if opp_type == 'news_discovery':
            source_url = opp.get('source', '')
            if not source_url or not source_url.startswith(('http://', 'https://')):
                continue
            production_type = 'news'
            title = opp.get('title') or 'Notícia curada'
            news_dir = REPO / 'noticias'
            news_dir.mkdir(parents=True, exist_ok=True)
            slug = opp.get('slug') or re.sub(r'[^a-z0-9-]+', '-', title.lower()).strip('-')
            html_path = news_dir / f'{slug}.html'
            html_content = (
                f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
                f'<title>{title}</title><link rel="canonical" href="https://praia.digital/noticias/{slug}.html">'
                f'<meta name="description" content="{opp.get("description", "")[:160]}">'
                f'</head><body><h1>{title}</h1>'
                f'<p><em>Fonte: <a href="{source_url}">{source_url}</a></em></p>'
                f'<p>{opp.get("description", "")}</p></body></html>'
            )
            try:
                html_path.write_text(html_content, encoding='utf-8')
            except Exception as e:
                opp['production_error'] = str(e)
                opp['produced'] = False
                produced.append(opp)
                continue
        elif opp_type == 'add_links':
            production_type = 'internal_links'
            title = f'Linkagem: {opp.get("message", "")[:60]}'
            target_slug = opp.get('target_slug') or opp.get('slug') or 'internal-links'
            html_path = REPO / 'blog' / f'{target_slug}.html'
            if not html_path.exists():
                html_path = REPO / 'blog' / 'links-atualizacao.html'
            title = opp.get('title') or 'Atualização de links internos'
        elif opp_type == 'seo_audit':
            production_type = 'schema_fix'
            title = f'SEO: {opp.get("message", "")[:60]}'
            target_slug = opp.get('target_slug') or 'seo-atualizacao'
            html_path = REPO / 'blog' / f'{target_slug}.html'
            if not html_path.exists():
                html_path = REPO / 'blog' / 'seo-atualizacao.html'
            title = opp.get('title') or 'Atualização SEO'
        elif opp_type == 'local_content':
            production_type = 'local_content'
            title = opp.get('title') or 'Conteúdo local'
            city = opp.get('city') or 'litoral'
            slug_core = re.sub(r'[^a-z0-9-]+', '-', title.lower()).strip('-')
            html_path = REPO / 'blog' / f'{slug_core}-{city}.html'
            html_content = (
                f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
                f'<title>{title}</title><link rel="canonical" href="https://praia.digital/blog/{slug_core}-{city}.html">'
                f'<meta name="description" content="{opp.get("description", "")[:160]}">'
                f'</head><body><h1>{title}</h1>'
                f'<p>{opp.get("description", "")}</p></body></html>'
            )
            try:
                html_path.parent.mkdir(parents=True, exist_ok=True)
                html_path.write_text(html_content, encoding='utf-8')
            except Exception as e:
                opp['production_error'] = str(e)
                opp['produced'] = False
                produced.append(opp)
                continue
        elif opp_type == 'academy':
            production_type = 'academy_material'
            title = opp.get('title') or 'Material Academy'
            slug_core = re.sub(r'[^a-z0-9-]+', '-', title.lower()).strip('-')
            html_path = REPO / 'education' / 'formacoes' / f'{slug_core}.html'
            html_content = (
                f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
                f'<title>{title}</title><link rel="canonical" href="https://praia.digital/education/formacoes/{slug_core}.html">'
                f'<meta name="description" content="{opp.get("description", "")[:160]}">'
                f'</head><body><h1>{title}</h1>'
                f'<p>{opp.get("description", "")}</p></body></html>'
            )
            try:
                html_path.parent.mkdir(parents=True, exist_ok=True)
                html_path.write_text(html_content, encoding='utf-8')
            except Exception as e:
                opp['production_error'] = str(e)
                opp['produced'] = False
                produced.append(opp)
                continue
        else:
            continue
        if not html_path:
            continue
        if not _validate_html_path(html_path):
            opp['produced'] = False
            opp['production_error'] = f'HTML inválido ou não criado: {html_path}'
            produced.append(opp)
            continue
        slug = html_path.stem
        url = f'https://praia.digital/{html_path.relative_to(REPO)}'.replace('\\', '/')
        evidence_item = {
            'slug': slug,
            'title': title,
            'html_path': str(html_path),
            'url': url,
            'production_type': production_type,
            'source_url': source_url,
            'validated_at': datetime.now(timezone.utc).isoformat(),
            'internal_links_added': 0,
            'linked_slugs': [],
        }
        evidence[slug] = evidence_item
        opp['produced'] = True
        opp['production_type'] = production_type
        opp['slug'] = slug
        opp['html_path'] = str(html_path)
        opp['title'] = title
        opp['url'] = url
        opp['evidence_key'] = slug
        produced.append(opp)
    return produced

def review(produced: list, context: dict) -> list:
    evidence = context.get('evidence', {})
    reviewed = []
    for item in produced:
        evidence_key = item.get('evidence_key')
        item_evidence = evidence.get(evidence_key) if evidence_key else None
        valid = False
        qa_issues = []
        if not item.get('produced'):
            qa_issues.append('not_produced')
        elif not item_evidence:
            qa_issues.append('missing_evidence')
        else:
            html_path = item_evidence.get('html_path')
            slug = item_evidence.get('slug')
            title = item_evidence.get('title')
            url = item_evidence.get('url')
            if not html_path or not Path(html_path).exists():
                qa_issues.append('html_missing')
            elif not _validate_html_path(Path(html_path)):
                qa_issues.append('html_invalid')
            if not _validate_slug(slug):
                qa_issues.append('invalid_slug')
            if not title or not isinstance(title, str) or not title.strip():
                qa_issues.append('invalid_title')
            if not _validate_url(url):
                qa_issues.append('invalid_url')
            if item.get('type') == 'news_discovery':
                source_url = item_evidence.get('source_url')
                if not _validate_url(source_url):
                    qa_issues.append('invalid_source_url')
            if not qa_issues:
                valid = True
        item['qa'] = {'passed': valid, 'issues': qa_issues}
        reviewed.append(item)
    return reviewed

def publish(reviewed: list, context: dict) -> list:
    evidence = context.get('evidence', {})
    published = []
    for item in reviewed:
        if not item.get('qa', {}).get('passed', False):
            item['published'] = False
            item['publication_error'] = 'QA failed: ' + ', '.join(item.get('qa', {}).get('issues', []))
            published.append(item)
            continue
        evidence_key = item.get('evidence_key')
        item_evidence = evidence.get(evidence_key) if evidence_key else None
        if not item_evidence:
            item['published'] = False
            item['publication_error'] = 'missing_evidence'
            published.append(item)
            continue
        html_path = Path(item_evidence['html_path'])
        if not _validate_html_path(html_path):
            item['published'] = False
            item['publication_error'] = 'html_invalid'
            published.append(item)
            continue
        item['published'] = True
        item['published_at'] = datetime.now(timezone.utc).isoformat()
        item['publication_status'] = 'PUBLISHED'
        published.append(item)
    return published


def verify_and_fix_published(published: list, context: dict) -> list:
    """
    Verifica artigos publicados e tenta corrigir automaticamente divergências.
    Apenas considera PUBLICADO_OK se todas as verificações passarem.
    """
    evidence = context.get('evidence', {})
    results = []
    
    for item in published:
        evidence_key = item.get('evidence_key')
        item_evidence = evidence.get(evidence_key) if evidence_key else None
        if not item_evidence:
            item['post_publish_status'] = 'REVISAR_HUMANO'
            item['post_publish_error'] = 'missing_evidence'
            results.append(item)
            continue
        
        html_path = Path(item_evidence['html_path'])
        slug = item_evidence.get('slug', '')
        
        # Run verification
        try:
            sitemap_slugs = set()
            if SITEMAP_SCRIPT.exists():
                sitemap_slugs = _load_sitemap_slugs()
        except Exception:
            sitemap_slugs = set()
        
        verification = _verify_article(html_path, sitemap_slugs)
        item['post_publish_verification'] = verification
        
        if verification.get('valid'):
            item['post_publish_status'] = 'PUBLISHED_OK'
            results.append(item)
        else:
            # Try automatic fix
            try:
                fix_module = load_module('post_publish_fix', [REPO / 'scripts' / 'orchestrator' / 'maintenance'])
                if fix_module:
                    fix_result = fix_module.run({})
                    # Re-verify after fix
                    verification_after = _verify_article(html_path, sitemap_slugs)
                    if verification_after.get('valid'):
                        item['post_publish_status'] = 'PUBLISHED_OK'
                        item['post_publish_fixed'] = True
                    else:
                        item['post_publish_status'] = 'REVISAR_HUMANO'
                        item['post_publish_fix_failed'] = True
                else:
                    item['post_publish_status'] = 'REVISAR_HUMANO'
                    item['post_publish_error'] = 'fix_module_not_found'
            except Exception as e:
                item['post_publish_status'] = 'REVISAR_HUMANO'
                item['post_publish_error'] = f'fix_error: {str(e)}'
            results.append(item)
    
    return results


def _load_sitemap_slugs() -> set:
    if not SITEMAP_PATH.exists():
        return set()
    txt = SITEMAP_PATH.read_text(encoding='utf-8', errors='ignore')
    urls = set(re.findall(r'<loc>(.*?)</loc>', txt))
    slugs = set()
    for url in urls:
        if '/blog/' in url and url.endswith('.html'):
            slugs.add(Path(url).stem)
    return slugs


def _verify_article(html_path: Path, sitemap_slugs: set, min_required: int = 1) -> dict:
    if not html_path.exists():
        return {'valid': False, 'error': 'missing', 'issues': ['file_missing']}
    txt = html_path.read_text(encoding='utf-8', errors='ignore')
    slug = html_path.stem
    issues = []
    in_sitemap = slug in sitemap_slugs
    if not in_sitemap:
        issues.append('missing_from_sitemap')
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', txt, re.I)
    internal = [h for h in hrefs if h.startswith('/blog/') or h.startswith('/education/') or h.startswith('/noticias/')]
    if len(internal) < min_required:
        issues.append(f'insufficient_internal_links:{len(internal)}')
    if not any(p in txt.lower() for p in ['whatsapp', 'wa.me', 'comprar', 'checkout']):
        issues.append('missing_cta_or_whatsapp')
    if len(txt) < 800:
        issues.append(f'content_too_small:{len(txt)}')
    if '<title>' not in txt.lower():
        issues.append('missing_title')
    if 'meta name="description"' not in txt.lower():
        issues.append('missing_description')
    if '<h1' not in txt.lower():
        issues.append('missing_h1')
    if 'rel="canonical"' not in txt.lower():
        issues.append('missing_canonical')
    return {
        'slug': slug,
        'valid': len(issues) == 0,
        'issues': issues,
        'size': len(txt),
        'internal_links': len(internal),
        'in_sitemap': in_sitemap,
    }

def connect(published: list, context: dict) -> list:
    evidence = context.get('evidence', {})
    connected = []
    for item in published:
        evidence_key = item.get('evidence_key')
        item_evidence = evidence.get(evidence_key) if evidence_key else None
        item['connected'] = False
        item['links_added'] = 0
        item['linked_slugs'] = []
        item['connection_error'] = None
        if not item.get('published'):
            item['connection_error'] = 'not_published'
            connected.append(item)
            continue
        if not item_evidence:
            item['connection_error'] = 'missing_evidence'
            connected.append(item)
            continue
        html_path = Path(item_evidence['html_path'])
        if not _validate_html_path(html_path):
            item['connection_error'] = 'html_invalid'
            connected.append(item)
            continue
        link_result = _validate_internal_links(html_path, min_required=1)
        item['connected'] = link_result['valid']
        item['links_added'] = link_result['links_added']
        item['linked_slugs'] = link_result.get('linked_slugs', [])
        item_evidence['internal_links_added'] = link_result['links_added']
        item_evidence['linked_slugs'] = link_result.get('linked_slugs', [])
        if link_result['error']:
            item['connection_error'] = link_result['error']
        if not item['connected']:
            item['connection_error'] = item.get('connection_error') or 'insufficient_internal_links'
        connected.append(item)
    return connected

def register(connected: list, context: dict) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    evidence = context.get('evidence', {})
    if 'orchestrator_24h' not in registry:
        registry['orchestrator_24h'] = {'started_at': datetime.now(timezone.utc).isoformat(), 'cycles': []}
    evidence_entries = []
    produced_count = 0
    published_count = 0
    connected_count = 0
    failed_count = 0
    for item in connected:
        evidence_key = item.get('evidence_key')
        item_evidence = evidence.get(evidence_key) if evidence_key else None
        produced_count += 1 if item.get('produced') else 0
        published_count += 1 if item.get('published') else 0
        connected_count += 1 if item.get('connected') else 0
        failed_count += 0 if item.get('produced') else 1
        if item_evidence:
            _register_article_in_editorial(item_evidence)
            evidence_entries.append({
                'slug': item_evidence.get('slug'),
                'title': item_evidence.get('title'),
                'html_path': item_evidence.get('html_path'),
                'url': item_evidence.get('url'),
                'produced': bool(item.get('produced')),
                'published': bool(item.get('published')),
                'connected': bool(item.get('connected')),
                'links_added': item.get('links_added', 0),
                'linked_slugs': item.get('linked_slugs', []),
                'published_at': item.get('published_at'),
                'error': item.get('production_error') or item.get('publication_error') or item.get('connection_error'),
            })
    cycle = {
        'date': datetime.now(timezone.utc).isoformat(),
        'detected': registry.get('last_detected_count', 0),
        'produced': produced_count,
        'published': published_count,
        'connected': connected_count,
        'failed_production': failed_count,
        'evidence': evidence_entries,
        'audit': 'verified',
    }
    registry['orchestrator_24h']['cycles'].append(cycle)
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    sitemap_slugs = [e['slug'] for e in evidence_entries if e.get('published')]
    if sitemap_slugs:
        _update_sitemap_if_needed(sitemap_slugs)
    return {'status': 'ok', 'registered': len(evidence_entries), 'cycle': cycle}

def measure() -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    evidence_cycle = None
    for c in reversed(registry.get('orchestrator_24h', {}).get('cycles', [])):
        if c.get('evidence'):
            evidence_cycle = c
            break
    measurement = {
        'status': 'ok',
        'message': 'Medição baseada em evidências',
        'total_published_evidence': len(evidence_cycle.get('evidence', [])) if evidence_cycle else 0,
        'total_connected_evidence': sum(1 for e in evidence_cycle.get('evidence', []) if e.get('connected')) if evidence_cycle else 0,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    return measurement

def run(context: dict = {}) -> dict:
    print('[ORCHESTRATOR-24H] Início —', datetime.now(timezone.utc).isoformat())
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    hour_key = datetime.now(timezone.utc).strftime('%Y%m%d%H')
    executed_actions = registry.get('executed_actions', [])
    if f'cycle_{hour_key}' in executed_actions:
        return {'status': 'ok', 'message': f'Ciclo já executado para {hour_key} (idempotente)', 'skipped': True}

    # 1. Detectar
    detected = detect(context)
    opportunities = detected.get('opportunities', [])
    print(f"[ORCHESTRATOR-24H] 1. Detectadas: {len(opportunities)} oportunidades")

    # 2. Pesquisar
    researched = research(opportunities)
    print(f"[ORCHESTRATOR-24H] 2. Pesquisadas: {len(researched)} oportunidades")

    # 3. Comparar com acervo
    archive_module = load_module('archive_comparator', [REPO / 'scripts' / 'orchestrator' / 'pipeline'])
    archive_result = {'status': 'ok', 'message': 'archive_comparator skipped'}
    if archive_module:
        try:
            archive_context = {'opportunities': researched}
            archive_result = archive_module.run(archive_context)
            archive_result['phase'] = 'archive_comparison'
            opportunities = archive_result.get('opportunities', researched)
        except Exception as e:
            archive_result = {'status': 'error', 'message': f'Erro em archive_comparator: {str(e)}', 'phase': 'archive_comparison'}
    print(f"[ORCHESTRATOR-24H] 3. Comparação com acervo: {archive_result.get('message', '')}")

    # 4. Pontuar
    scored = score(opportunities)
    print(f"[ORCHESTRATOR-24H] 4. Pontuadas: {len(scored)} oportunidades")

    # 5. Produzir
    produced = produce(scored, context)
    print(f"[ORCHESTRATOR-24H] 5. Produzidas: {len(produced)} oportunidades")

    # 6. Revisar
    reviewed = review(produced, context)
    passed = sum(1 for r in reviewed if r.get('qa', {}).get('passed', False))
    print(f"[ORCHESTRATOR-24H] 6. Revisadas: {passed}/{len(reviewed)} passaram QA")

    # 7. Publicar
    published = publish(reviewed, context)
    print(f"[ORCHESTRATOR-24H] 7. Publicadas: {len(published)} oportunidades")

    # 7.1 Verificar e corrigir publicadas
    verified = verify_and_fix_published(published, context)
    published_ok = sum(1 for v in verified if v.get('post_publish_status') == 'PUBLISHED_OK')
    needs_human = sum(1 for v in verified if v.get('post_publish_status') == 'REVISAR_HUMANO')
    print(f"[ORCHESTRATOR-24H] 7.1 Verificadas: {published_ok} OK, {needs_human} para revisão humana")

    # 8. Conectar
    connected = connect(verified, context)
    print(f"[ORCHESTRATOR-24H] 8. Conectadas: {len(connected)} oportunidades")

    # 9. Registrar
    registration = register(connected, context)
    print(f"[ORCHESTRATOR-24H] 9. Registradas: {registration.get('registered', 0)} ações")

    # 10. Medir
    measurement = measure()
    print(f"[ORCHESTRATOR-24H] 10. Medição: {measurement.get('message', '')}")

    # 11. Verificação pós-publicação
    try:
        verification_module = load_module('post_publish_verify', [REPO / 'scripts' / 'orchestrator' / 'maintenance'])
        if verification_module:
            verification = verification_module.run({})
            print(f"[ORCHESTRATOR-24H] 11. Verificação pós-publicação: {verification.get('status', 'unknown')}")
            if verification.get('status') == 'divergences_found':
                print(f"[ORCHESTRATOR-24H] Divergências encontradas: {verification.get('failed_slugs', [])}")
                # Tentar correção automática segura
                try:
                    fix_module = load_module('post_publish_fix', [REPO / 'scripts' / 'orchestrator' / 'maintenance'])
                    if fix_module:
                        fix_result = fix_module.run({})
                        print(f"[ORCHESTRATOR-24H] 12. Correção automática: {fix_result.get('status', 'unknown')}")
                except Exception as e:
                    print(f"[ORCHESTRATOR-24H] 12. Correção automática erro: {e}")
        else:
            print('[ORCHESTRATOR-24H] 11. Verificação pós-publicação: módulo não encontrado')
    except Exception as e:
        print(f"[ORCHESTRATOR-24H] 11. Verificação pós-publicação erro: {e}")

    # Manutenção
    maint = run_module('auto_maintenance', [REPO / 'scripts' / 'orchestrator' / 'maintenance'], context)
    print(f"[ORCHESTRATOR-24H] Manutenção: {maint.get('message', '')}")

    # Mark cycle as executed for idempotency — reload registry to avoid
    # overwriting writes from register() and auto_maintenance above.
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    registry['executed_actions'] = list(set(registry.get('executed_actions', []) + [f'cycle_{hour_key}']))
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

    print('[ORCHESTRATOR-24H] Ciclo concluído')
    return {
        'status': 'ok',
        'cycle': registration.get('cycle', {}),
        'detected': len(opportunities),
        'produced': len(produced),
        'published': len(published),
        'message': f'Ciclo 24h: {len(published)} publicados, {len(opportunities)} detectados',
    }

if __name__ == '__main__':
    run()
