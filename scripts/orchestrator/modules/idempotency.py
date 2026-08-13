#!/usr/bin/env python3
"""
Módulo: idempotency — Praia Digital.
- Verifica se uma ação já foi executada
- Marca ações como concluídas
- Permite ações parciais
- Evita duplicação de trabalho em execuções repetidas
"""
import json
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

def is_completed(action_id: str) -> bool:
    """Verifica se uma ação já foi concluída"""
    if not REGISTRY.exists():
        return False
    
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    completed = registry.get('idempotency', {}).get('completed_actions', [])
    return action_id in completed

def mark_completed(action_id: str, metadata: dict = None) -> None:
    """Marca uma ação como concluída"""
    if not REGISTRY.exists():
        return
    
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if 'idempotency' not in registry:
        registry['idempotency'] = {
            'created_at': datetime.now(timezone.utc).isoformat(),
            'completed_actions': [],
            'partial_actions': [],
        }
    
    if action_id not in registry['idempotency']['completed_actions']:
        registry['idempotency']['completed_actions'].append(action_id)
    
    if metadata:
        registry['idempotency'][f'{action_id}_metadata'] = metadata
    
    registry['idempotency']['last_updated'] = datetime.now(timezone.utc).isoformat()
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

def mark_partial(action_id: str, metadata: dict) -> None:
    """Marca uma ação como parcialmente concluída"""
    if not REGISTRY.exists():
        return
    
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if 'idempotency' not in registry:
        registry['idempotency'] = {
            'created_at': datetime.now(timezone.utc).isoformat(),
            'completed_actions': [],
            'partial_actions': [],
        }
    
    registry['idempotency']['partial_actions'].append({
        'action_id': action_id,
        'metadata': metadata,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    })
    
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

def get_state(action_id: str) -> dict:
    """Obtém o estado de uma ação"""
    if not REGISTRY.exists():
        return {}
    
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    return registry.get('idempotency', {}).get(f'{action_id}_metadata', {})

def run(context: dict) -> dict:
    """Verifica idempotência para ações no contexto"""
    action_id = context.get('action_id', 'default')
    
    if is_completed(action_id):
        return {
            'status': 'ok',
            'actions': [],
            'message': f'Ação {action_id} já executada (idempotente)',
            'skip': True,
        }
    
    return {
        'status': 'ok',
        'actions': [],
        'message': f'Ação {action_id} pode prosseguir',
        'skip': False,
    }
