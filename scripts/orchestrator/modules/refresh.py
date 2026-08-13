#!/usr/bin/env python3
"""
Módulo: refresh — Praia Digital.
- Atualiza sitemap e registros básicos
- Não altera conteúdo estrutural
"""
import json, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
SITEMAP_SCRIPT = REPO / 'scripts' / 'gerar_sitemap.py'

def run(context: dict) -> dict:
    result = subprocess.run(f'python "{SITEMAP_SCRIPT}"', shell=True, cwd=REPO, capture_output=True, text=True, timeout=300)
    sitemap_ok = result.returncode == 0

    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    registry['last_refresh'] = datetime.now(timezone.utc).isoformat()
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

    return {
        'status': 'ok' if sitemap_ok else 'error',
        'actions': [{'type': 'sitemap_refresh', 'ok': sitemap_ok}],
        'message': f'Sitemap atualizado: {sitemap_ok}',
    }
