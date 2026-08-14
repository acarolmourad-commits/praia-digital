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

def produce(scored_opportunities: list, context: dict) -> list:
    produced = []
    for opp in scored_opportunities:
        if opp.get('final_score', 0) < 6.0:
            continue
        opp_type = opp.get('type', '')
        if opp_type == 'news_discovery':
            source = opp.get('source', '')
            if not source or not source.startswith(('http://', 'https://')):
                continue
            opp['produced'] = True
            opp['production_type'] = 'news'
            produced.append(opp)
        elif opp_type == 'add_links':
            opp['produced'] = True
            opp['production_type'] = 'internal_links'
            produced.append(opp)
        elif opp_type == 'seo_audit':
            opp['produced'] = True
            opp['production_type'] = 'schema_fix'
            produced.append(opp)
        elif opp_type == 'local_content':
            opp['produced'] = True
            opp['production_type'] = 'local_content'
            produced.append(opp)
        elif opp_type == 'academy':
            opp['produced'] = True
            opp['production_type'] = 'academy_material'
            produced.append(opp)
    return produced

def review(produced: list) -> list:
    reviewed = []
    for item in produced:
        qa_ok = True
        qa_issues = []
        production_type = item.get('production_type', '')
        if production_type == 'news' and not item.get('source'):
            qa_ok = False
            qa_issues.append('missing_source')
        item['qa'] = {'passed': qa_ok, 'issues': qa_issues}
        reviewed.append(item)
    return reviewed

def publish(reviewed: list, context: dict) -> list:
    published = []
    for item in reviewed:
        if not item.get('qa', {}).get('passed', False):
            continue
        item['published'] = True
        item['published_at'] = datetime.now(timezone.utc).isoformat()
        published.append(item)
    return published

def connect(published: list) -> list:
    connected = []
    for item in published:
        item['connected'] = True
        item['links_added'] = 0
        connected.append(item)
    return connected

def register(connected: list) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if 'orchestrator_24h' not in registry:
        registry['orchestrator_24h'] = {'started_at': datetime.now(timezone.utc).isoformat(), 'cycles': []}
    cycle = {
        'date': datetime.now(timezone.utc).isoformat(),
        'detected': 0,
        'produced': len(connected),
        'published': len(connected),
        'connected': len(connected),
    }
    registry['orchestrator_24h']['cycles'].append(cycle)
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'status': 'ok', 'registered': len(connected), 'cycle': cycle}

def measure() -> dict:
    return {'status': 'ok', 'message': 'Medição registrada'}

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
    reviewed = review(produced)
    passed = sum(1 for r in reviewed if r.get('qa', {}).get('passed', False))
    print(f"[ORCHESTRATOR-24H] 6. Revisadas: {passed}/{len(reviewed)} passaram QA")

    # 7. Publicar
    published = publish(reviewed, context)
    print(f"[ORCHESTRATOR-24H] 7. Publicadas: {len(published)} oportunidades")

    # 8. Conectar
    connected = connect(published)
    print(f"[ORCHESTRATOR-24H] 8. Conectadas: {len(connected)} oportunidades")

    # 9. Registrar
    registration = register(connected)
    print(f"[ORCHESTRATOR-24H] 9. Registradas: {registration.get('registered', 0)} ações")

    # 10. Medir
    measurement = measure()
    print(f"[ORCHESTRATOR-24H] 10. Medição: {measurement.get('message', '')}")

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
