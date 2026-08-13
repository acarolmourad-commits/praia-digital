#!/usr/bin/env python3
"""
Módulo: qa-fixes — Praia Digital.
- Corrige issues QA reversíveis e seguros
- Não altera conteúdo estrutural
- Não toca na Batch 147
"""
import json, re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

def fix_missing_h1(path: Path) -> bool:
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<h1' in html.lower():
        return False
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.S|re.I)
    if not title:
        return False
    title_text = title.group(1).strip()
    if not title_text:
        return False
    # Insert h1 after </title>
    insertion = f'<h1>{title_text}</h1>'
    html = html.replace('</title>', f'</title>{insertion}', 1)
    path.write_text(html, encoding='utf-8')
    return True

def fix_missing_title(path: Path) -> bool:
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<title' in html.lower():
        return False
    # derive from filename
    title_text = path.stem.replace('-', ' ').replace('_', ' ').title()
    insertion = f'<title>{title_text}</title>'
    html = html.replace('</head>', f'{insertion}\n</head>', 1)
    path.write_text(html, encoding='utf-8')
    return True

def run(context: dict) -> dict:
    fixed = []
    
    # Idempotency: check if already completed
    registry_path = REPO / 'docs' / 'banco-editorial.json'
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding='utf-8'))
        completed = registry.get('idempotency', {}).get('completed_actions', [])
        if 'qa_fixes' in completed:
            return {
                'status': 'ok',
                'actions': [],
                'fixed': fixed,
                'message': 'QA fixes: já executado anteriormente (idempotente)',
            }
    # Check a small sample of blog files
    files = list(BLOG_DIR.glob('*.html'))[:20] + list(FORMACOES_DIR.glob('*.html'))[:8]
    for f in files:
        try:
            html = f.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue

        needs_title = '<title' not in html.lower()
        needs_h1 = '<h1' not in html.lower()

        if needs_title:
            if fix_missing_title(f):
                fixed.append({'file': str(f.relative_to(REPO)), 'fix': 'add_title'})
        if needs_h1:
            if fix_missing_h1(f):
                fixed.append({'file': str(f.relative_to(REPO)), 'fix': 'add_h1'})

    # Update registry with fixes applied
    if fixed:
        registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
        if 'qa_fixes' not in registry:
            registry['qa_fixes'] = []
        registry['qa_fixes'].append({
            'date': datetime.now(timezone.utc).isoformat(),
            'fixed': fixed,
        })
        REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

    return {
        'status': 'ok',
        'actions': [{'type': 'qa_fix', 'file': x['file'], 'fix': x['fix']} for x in fixed],
        'fixed': fixed,
        'message': f'QA fixes: {len(fixed)} arquivos corrigidos',
    }
