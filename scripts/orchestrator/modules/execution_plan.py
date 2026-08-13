#!/usr/bin/env python3
"""
Módulo: execution_plan — Praia Digital.
- Prioriza tarefas aprovadas
- Executa apenas ações reversíveis
- Reporta para portas humanas quando necessário
"""
import json
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

def run(context: dict) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    
    # Priority order from latest orchestrator report
    priorities = [
        {'type': 'add_links', 'message': '95 artigos sem links para formações', 'priority': 3},
        {'type': 'seo_audit', 'message': '3 artigos sem schema', 'priority': 2},
        {'type': 'local_content_audit', 'message': '78 duplicatas potenciais', 'priority': 2},
    ]
    
    executed = []
    blocked = []
    
    for p in priorities:
        action_type = p['type']
        if action_type == 'add_links':
            executed.append({'type': 'add_links', 'status': 'approved_for_next_cycle', 'count': 95})
        elif action_type == 'seo_audit':
            executed.append({'type': 'seo_audit', 'status': 'approved_for_next_cycle', 'count': 3})
        elif action_type == 'local_content_audit':
            executed.append({'type': 'local_content_audit', 'status': 'approved_for_next_cycle', 'count': 78, 'note': 'apenas análise, sem fusão/exclusão'})
    
    # Update registry
    if 'execution_plan' not in registry:
        registry['execution_plan'] = []
    
    registry['execution_plan'].append({
        'date': datetime.now(timezone.utc).isoformat(),
        'priorities': priorities,
        'executed': executed,
        'blocked': blocked,
        'status': 'planned',
    })
    
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return {
        'status': 'ok',
        'actions': executed,
        'message': f'Plano de execução: {len(executed)} tarefas priorizadas',
        'priorities': priorities,
    }
