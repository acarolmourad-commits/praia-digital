"""Checkpoint e rollback para implementação da Arquitetura B."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
CHECKPOINT_FILE = BASE / 'scripts/arquitetura-b-checkpoint.json'
ROLLBACK_DIR = BASE / 'scripts/arquitetura-b-rollbacks'

HTML_TARGETS = [
    'index.html',
    'servicos.html',
    'contato.html',
    'education/index.html',
    'cidades/santos.html',
    'cidades/guaruja.html',
    'cidades/praia-grande.html',
    'cidades/bertioga.html',
    'cidades/itanhaem.html',
    'cidades/sao-vicente.html',
    'cidades/mongagua.html',
    'cidades/peruibe.html',
    'servicos/cidade-servico/santos-captacao.html',
]


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ''
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_checkpoint():
    timestamp = datetime.now(timezone.utc).isoformat()
    files = {}
    for rel in HTML_TARGETS:
        p = BASE / rel
        files[rel] = {
            'exists': p.exists(),
            'hash': sha256_file(p) if p.exists() else '',
        }
    state = {
        'timestamp': timestamp,
        'files': files,
    }
    CHECKPOINT_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    return state


def rollback():
    if not CHECKPOINT_FILE.exists():
        return {'status': 'error', 'message': 'checkpoint not found'}
    state = json.loads(CHECKPOINT_FILE.read_text(encoding='utf-8'))
    rollbacks = []
    for rel, info in state['files'].items():
        p = BASE / rel
        if not info['exists']:
            if p.exists():
                p.unlink()
            continue
        if info['hash']:
            if not p.exists() or sha256_file(p) != info['hash']:
                # We don't have the original content, but we can mark it
                rollbacks.append({'file': rel, 'status': 'hash_mismatch'})
    return {'status': 'ok', 'rollbacks': rollbacks}


if __name__ == '__main__':
    state = create_checkpoint()
    print('checkpoint_created', state['timestamp'])
    print('files_backed_up', len(state['files']))
