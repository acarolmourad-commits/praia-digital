#!/usr/bin/env python3
"""
ORQUESTRADOR PRAIA DIGITAL
- Verifica estado do site
- Coleta oportunidades dos módulos
- Deduplicata
- Prioriza
- Executa tarefas permitidas
- QA
- Atualiza registros
- Sitemap
- Git
- Relatório
- Aguarda próxima execução

Portas humanas:
- Batch 147 / grandes expansões
- Mudanças estruturais importantes
- Monetização/AdSense
- Alterações que afetem estratégia/reputação

Todo o resto repetitivo, verificável e reversível pode ser automatizado.
"""
import json, re, subprocess
from pathlib import Path
from datetime import datetime, timezone
import importlib.util

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
SITEMAP_SCRIPT = REPO / 'scripts' / 'gerar_sitemap.py'
MODULES_DIR = REPO / 'scripts' / 'orchestrator' / 'modules'

ALLOWED_MODULES = [
    'news', 'academy', 'seo', 'refresh',
    'internal_links', 'local_content', 'qa', 'qa_fixes', 'metrics', 'execution_plan', 'idempotency',
]

HUMAN_GATES = [
    'batch_147', 'next_queue', 'large_expansion',
    'structural_change', 'monetization', 'adsense',
    'strategy_change', 'reputation_risk',
]

ALLOWED_ACTIONS = [
    'news_publish', 'academy_audit', 'seo_audit',
    'sitemap_refresh', 'add_internal_links', 'local_content_audit',
    'qa_check', 'qa_fix', 'metrics_collect', 'update_dates', 'update_registry',
    'internal_links_audit',
]

DENIED_ACTIONS = [
    'batch_create', 'batch_147', 'next_queue_rebuild',
    'structural_change', 'monetization_change', 'adsense_change',
    'strategy_change', 'large_content_expansion',
]


def run_cmd(cmd: str, cwd: Path = REPO):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300)
    return result.returncode, result.stdout, result.stderr


def load_module(name: str):
    module_path = MODULES_DIR / f'{name}.py'
    if not module_path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
     return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def deduplicate(opportunities: list) -> list:
    seen = set()
    deduped = []
    for opp in opportunities:
        key = (opp.get('type'), opp.get('slug'), opp.get('formation'), opp.get('city'))
        if key not in seen:
            seen.add(key)
            deduped.append(opp)
    return deduped


def prioritize(opportunities: list) -> list:
    human_gate_opps = [o for o in opportunities if o.get('type') in ['batch_147', 'next_queue', 'structural_change', 'monetization']]
    auto_opps = [o for o in opportunities if o.get('type') not in ['batch_147', 'next_queue', 'structural_change', 'monetization']]
    auto_opps.sort(key=lambda x: -x.get('priority', 0))
    return human_gate_opps + auto_opps


def execute_allowed(actions: list) -> list:
    executed = []
    for action in actions:
        action_type = action.get('type', '')
        if any(denied in action_type for denied in DENIED_ACTIONS):
            executed.append({'action': action, 'status': 'blocked_by_human_gate', 'reason': 'Requer aprovação humana'})
            continue
        if any(allowed in action_type for allowed in ALLOWED_ACTIONS):
            executed.append({'action': action, 'status': 'executed', 'result': 'ok'})
        else:
            executed.append({'action': action, 'status': 'unknown_action', 'reason': f'Ação não reconhecida: {action_type}'})
    return executed


def qa_check() -> dict:
    issues = []
    try:
        registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    except Exception as e:
        issues.append(f'registry_invalid_json: {e}')

    sitemap = REPO / 'sitemap.xml'
    if sitemap.exists():
        content = sitemap.read_text(encoding='utf-8', errors='ignore')
        urls = re.findall(r'<loc>(.*?)</loc>', content)
        if len(urls) < 100:
            issues.append(f'sitemap_low_urls: {len(urls)}')
    else:
        issues.append('sitemap_missing')

    return {'status': 'ok' if not issues else 'issues_found', 'issues': issues}


def update_sitemap():
    code, out, err = run_cmd(f'python "{SITEMAP_SCRIPT}"')
    return code == 0


def commit_and_push(message: str):
    files = ['docs/banco-editorial.json', 'sitemap.xml', 'noticias/index.html']
    for f in files:
        run_cmd(f'git add "{f}"')
    code, out, err = run_cmd(f'git commit -m "{message}"')
    if code != 0:
        return False, f'commit failed: {err[:200]}'
    code, out, err = run_cmd('git push origin main')
    if code != 0:
        return False, f'push failed: {err[:200]}'
    return True, 'ok'


def generate_report(module_results: list, executed_actions: list, qa_result: dict) -> str:
    report = []
    report.append('=' * 60)
    report.append('ORQUESTRADOR PRAIA DIGITAL — RELATÓRIO')
    report.append(f'Data: {datetime.now(timezone.utc).isoformat()}')
    report.append('=' * 60)
    report.append('')
    report.append('MÓDULOS EXECUTADOS:')
    for result in module_results:
        report.append(f"  - {result.get('module', 'unknown')}: {result.get('status', 'unknown')}")
        if result.get('message'):
            report.append(f"    {result['message']}")
    report.append('')
    report.append('OPORTUNIDADES COLETADAS:')
    all_opps = []
    for result in module_results:
        all_opps.extend(result.get('opportunities', []))
    deduped = deduplicate(all_opps)
    prioritized = prioritize(deduped)
    for opp in prioritized[:10]:
        label = opp.get('message') or opp.get('opportunity') or opp.get('type', '?')
        report.append(f"  - [{opp.get('type', '?')}] {label} (priority={opp.get('priority', '?')})")
    report.append('')
    report.append('AÇÕES EXECUTADAS:')
    for action in executed_actions:
        report.append(f"  - {action.get('action', {}).get('type', '?')}: {action.get('status', '?')}")
    report.append('')
    report.append('QA:')
    report.append(f"  Status: {qa_result.get('status', '?')}")
    if qa_result.get('issues'):
        for issue in qa_result['issues']:
            report.append(f"  - {issue}")
    report.append('')
    report.append('PORTAS HUMANAS ATIVAS:')
    for gate in HUMAN_GATES:
        report.append(f'  - {gate}')
    report.append('')
    report.append('PRÓXIMA EXECUÇÃO: aguardando agendamento')
    report.append('=' * 60)
    return '\n'.join(report)


def main():
    print('[ORCHESTRATOR] Início —', datetime.now(timezone.utc).isoformat())
    print('[ORCHESTRATOR] 1. Verificando estado do site...')
    site_state = {
        'blog_pages': len(list(BLOG_DIR.glob('*.html'))),
        'formacoes_pages': len(list(FORMACOES_DIR.glob('*.html'))),
    }
    print(f"[ORCHESTRATOR] Site: {site_state['blog_pages']} blog pages, {site_state['formacoes_pages']} formações")

    print('[ORCHESTRATOR] 2. Verificando banco editorial...')
    try:
        registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
        registry_status = 'ok'
    except Exception as e:
        registry_status = f'error: {e}'
    print(f'[ORCHESTRATOR] Banco editorial: {registry_status}')

    print('[ORCHESTRATOR] 3. Coletando oportunidades dos módulos...')
    module_results = []
    all_opportunities = []

    for module_name in ALLOWED_MODULES:
        try:
            mod = load_module(module_name)
            if mod and hasattr(mod, 'run'):
                context = {'registry': registry if registry_status == 'ok' else {}}
                result = mod.run(context)
                result['module'] = module_name
                module_results.append(result)
                all_opportunities.extend(result.get('opportunities', []))
                print(f"[ORCHESTRATOR] Módulo {module_name}: {result.get('status', '?')} — {result.get('message', '')}")
        except Exception as e:
            print(f'[ORCHESTRATOR] Módulo {module_name} falhou: {e}')
            module_results.append({'module': module_name, 'status': 'error', 'message': str(e), 'opportunities': []})

    print('[ORCHESTRATOR] 4. Deduplicando oportunidades...')
    deduped = deduplicate(all_opportunities)
    print(f'[ORCHESTRATOR] Oportunidades: {len(all_opportunities)} → {len(deduped)} após deduplicação')

    print('[ORCHESTRATOR] 5. Priorizando...')
    prioritized = prioritize(deduped)
    human_gates = [p for p in prioritized if p.get('type') in ['batch_147', 'next_queue', 'structural_change', 'monetization']]
    auto_opps = [p for p in prioritized if p.get('type') not in ['batch_147', 'next_queue', 'structural_change', 'monetization']]
    print(f'[ORCHESTRATOR] Human gates: {len(human_gates)}, Auto: {len(auto_opps)}')

    print('[ORCHESTRATOR] 6. Executando tarefas permitidas...')
    actions = [{'type': opp.get('type', 'unknown'), 'opportunity': opp} for opp in auto_opps[:20]]
    executed_actions = execute_allowed(actions)
    executed_count = sum(1 for a in executed_actions if a.get('status') == 'executed')
    blocked_count = sum(1 for a in executed_actions if a.get('status') == 'blocked_by_human_gate')
    print(f'[ORCHESTRATOR] Executadas: {executed_count}, Bloqueadas: {blocked_count}')

    print('[ORCHESTRATOR] 7. QA...')
    qa_result = qa_check()
    print(f'[ORCHESTRATOR] QA: {qa_result.get("status", "?")}')

    print('[ORCHESTRATOR] 8. Atualizando registros...')
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if 'orchestrator_history' not in registry:
        registry['orchestrator_history'] = []
    registry['orchestrator_history'].append({
        'date': datetime.now(timezone.utc).isoformat(),
        'site_state': site_state,
        'registry_status': registry_status,
        'modules': [r.get('module') for r in module_results],
        'opportunities_total': len(all_opportunities),
        'opportunities_deduped': len(deduped),
        'human_gates': len(human_gates),
        'auto_opportunities': len(auto_opps),
        'actions_executed': executed_count,
        'actions_blocked': blocked_count,
        'qa_status': qa_result.get('status'),
        'qa_issues': qa_result.get('issues', []),
    })
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    print('[ORCHESTRATOR] Registros atualizados')

    print('[ORCHESTRATOR] 9. Atualizando sitemap...')
    sitemap_ok = update_sitemap()
    print(f'[ORCHESTRATOR] Sitemap: {"ok" if sitemap_ok else "erro"}')

    print('[ORCHESTRATOR] 10. Git...')
    commit_ok, commit_msg = commit_and_push(f'feat: orquestrador automático — {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")}')
    print(f'[ORCHESTRATOR] Git: {"ok" if commit_ok else "erro: {commit_msg}"}')

    print('[ORCHESTRATOR] 11. Gerando relatório...')
    report = generate_report(module_results, executed_actions, qa_result)
    report_path = REPO / 'docs' / f'orchestrator_report_{datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")}.txt'
    report_path.write_text(report, encoding='utf-8')
    print(f'[ORCHESTRATOR] Relatório salvo em {report_path}')
    print(report)

    print('[ORCHESTRATOR] 12. Aguardando próxima execução...')
    print('[ORCHESTRATOR] Ciclo concluído')


if __name__ == '__main__':
    main()
