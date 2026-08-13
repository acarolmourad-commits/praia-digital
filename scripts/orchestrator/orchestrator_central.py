#!/usr/bin/env python3
"""
ORQUESTRADOR CENTRAL — Praia Digital
Ciclo: descobrir → avaliar → priorizar → executar → validar → publicar → medir → aprender → repetir

Módulos:
- discovery: descoberta contínua de oportunidades
- decision: motor de decisão com scoring
- pipeline: produção automática
- maintenance: manutenção automática
- modules: módulos legados (news, academy, seo, etc.)

Regras:
- Batch 147: BLOQUEADA
- Batch 146: em medição
- Portas humanas: batch_147, next_queue, large_expansion, structural_change, monetization, adsense, strategy_change, reputation_risk
- Idempotência: evita duplicação de ações
- followup-email-geral: DESATIVADO
"""
import json, re, subprocess, sys, importlib
from pathlib import Path
from datetime import datetime, timezone
from importlib import import_module

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
SITEMAP_SCRIPT = REPO / 'scripts' / 'gerar_sitemap.py'

# Add module paths
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'modules').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'discovery').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'decision').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'pipeline').resolve()))
sys.path.insert(0, str((REPO / 'scripts' / 'orchestrator' / 'maintenance').resolve()))

# Human gates
HUMAN_GATES = {
    'batch_147', 'next_queue', 'large_expansion', 'structural_change',
    'monetization', 'adsense', 'strategy_change', 'reputation_risk',
}

# Allowed legacy modules
ALLOWED_MODULES = [
    'news', 'academy', 'seo', 'refresh',
    'internal_links', 'local_content', 'qa', 'qa_fixes', 'metrics', 'execution_plan',
]

# Allowed new modules
ALLOWED_DISCOVERY = ['discovery_engine']
ALLOWED_DECISION = ['decision_engine']
ALLOWED_PIPELINE = ['production_pipeline']
ALLOWED_MAINTENANCE = ['auto_maintenance']

def load_module(name: str, paths: list):
    """Carrega módulo de forma segura"""
    for path in paths:
        module_path = path / f'{name}.py'
        if module_path.exists():
            spec = importlib.util.spec_from_file_location(name, str(module_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    return None

def run_legacy_module(name: str, context: dict) -> dict:
    """Executa módulo legado"""
    module = load_module(name, [REPO / 'scripts' / 'orchestrator' / 'modules'])
    if not module:
        return {'status': 'error', 'message': f'Módulo {name} não encontrado'}
    
    try:
        return module.run(context)
    except Exception as e:
        return {'status': 'error', 'message': f'Erro em {name}: {str(e)}'}

def run_discovery(context: dict) -> dict:
    """Executa descoberta"""
    module = load_module('discovery_engine', [REPO / 'scripts' / 'orchestrator' / 'discovery'])
    if not module:
        return {'status': 'error', 'message': 'discovery_engine não encontrado'}
    
    try:
        return module.run(context)
    except Exception as e:
        return {'status': 'error', 'message': f'Erro em discovery: {str(e)}'}

def run_decision(context: dict) -> dict:
    """Executa motor de decisão"""
    module = load_module('decision_engine', [REPO / 'scripts' / 'orchestrator' / 'decision'])
    if not module:
        return {'status': 'error', 'message': 'decision_engine não encontrado'}
    
    try:
        return module.run(context)
    except Exception as e:
        return {'status': 'error', 'message': f'Erro em decision: {str(e)}'}

def run_pipeline(context: dict) -> dict:
    """Executa pipeline de produção"""
    module = load_module('production_pipeline', [REPO / 'scripts' / 'orchestrator' / 'pipeline'])
    if not module:
        return {'status': 'error', 'message': 'production_pipeline não encontrado'}
    
    try:
        return module.run(context)
    except Exception as e:
        return {'status': 'error', 'message': f'Erro em pipeline: {str(e)}'}

def run_maintenance(context: dict) -> dict:
    """Executa manutenção automática"""
    module = load_module('auto_maintenance', [REPO / 'scripts' / 'orchestrator' / 'maintenance'])
    if not module:
        return {'status': 'error', 'message': 'auto_maintenance não encontrado'}
    
    try:
        return module.run(context)
    except Exception as e:
        return {'status': 'error', 'message': f'Erro em maintenance: {str(e)}'}

def update_sitemap() -> None:
    """Atualiza sitemap"""
    result = subprocess.run(
        f'python "{SITEMAP_SCRIPT}"',
        shell=True,
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        print(f'[ORCHESTRATOR] Aviso: sitemap retornou {result.returncode}')
        print(result.stderr[:500])

def git_commit_and_push(message: str) -> None:
    """Commit e push"""
    try:
        subprocess.run('git add -A', shell=True, cwd=REPO, check=True, capture_output=True)
        subprocess.run(f'git commit -m "{message}"', shell=True, cwd=REPO, check=True, capture_output=True)
        subprocess.run('git push origin main', shell=True, cwd=REPO, check=True, capture_output=True)
        print(f'[ORCHESTRATOR] Git: {message}')
    except subprocess.CalledProcessError as e:
        print(f'[ORCHESTRATOR] Aviso: git retornou erro {e.returncode}')

def generate_report(module_results: list, pipeline_results: dict, maintenance_results: dict) -> str:
    """Gera relatório"""
    report = []
    report.append('=' * 60)
    report.append('ORQUESTRADOR CENTRAL — RELATÓRIO')
    report.append(f'Data: {datetime.now(timezone.utc).isoformat()}')
    report.append('=' * 60)
    report.append('')
    
    report.append('DESCOBERTA:')
    for result in module_results:
        if result.get('module') == 'discovery':
            report.append(f"  - {result.get('status', 'unknown')}: {result.get('message', '')}")
            if result.get('opportunities'):
                for opp in result['opportunities'][:5]:
                    report.append(f"    * [{opp.get('type', '?')}] {opp.get('message', opp.get('question', '?'))}")
    report.append('')
    
    report.append('DECISÕES:')
    for result in module_results:
        if result.get('module') == 'decision':
            report.append(f"  - {result.get('status', 'unknown')}: {result.get('message', '')}")
            report.append(f"    Aprovadas: {result.get('approved_count', 0)}, Ignoradas: {result.get('ignored_count', 0)}")
    report.append('')
    
    report.append('PIPELINE:')
    report.append(f"  - {pipeline_results.get('message', 'N/A')}")
    report.append('')
    
    report.append('MANUTENÇÃO:')
    report.append(f"  - {maintenance_results.get('message', 'N/A')}")
    if maintenance_results.get('actions'):
        for action in maintenance_results['actions']:
            task = action.get('task', '?')
            result = action.get('result', {})
            report.append(f"    * {task}: {result.get('ok', '?')}")
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
    
    context = {
        'date': datetime.now(timezone.utc).isoformat(),
        'human_gates': list(HUMAN_GATES),
    }
    
    # Phase 1: Descoberta
    print('[ORCHESTRATOR] 1. Descoberta...')
    discovery_result = run_discovery(context)
    discovery_result['module'] = 'discovery'
    print(f"[ORCHESTRATOR] Descoberta: {discovery_result.get('message', '')}")
    
    # Phase 2: Decisão
    print('[ORCHESTRATOR] 2. Decisão...')
    decision_result = run_decision(context)
    decision_result['module'] = 'decision'
    print(f"[ORCHESTRATOR] Decisão: {decision_result.get('message', '')}")
    
    # Phase 3: Pipeline
    print('[ORCHESTRATOR] 3. Pipeline...')
    pipeline_result = run_pipeline(context)
    print(f"[ORCHESTRATOR] Pipeline: {pipeline_result.get('message', '')}")
    
    # Phase 4: Manutenção
    print('[ORCHESTRATOR] 4. Manutenção...')
    maintenance_result = run_maintenance(context)
    print(f"[ORCHESTRATOR] Manutenção: {maintenance_result.get('message', '')}")
    
    # Phase 5: Relatório
    print('[ORCHESTRATOR] 5. Relatório...')
    module_results = [discovery_result, decision_result]
    report = generate_report(module_results, pipeline_result, maintenance_result)
    
    report_path = REPO / 'docs' / f'orchestrator_report_{datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")}.txt'
    report_path.write_text(report, encoding='utf-8')
    
    print(report)
    print(f'[ORCHESTRATOR] Relatório salvo em {report_path}')
    print('[ORCHESTRATOR] Ciclo concluído')

if __name__ == '__main__':
    main()
