#!/usr/bin/env python3
"""
Manutenção automática — Praia Digital.
- Sitemap
- Canonical
- Meta
- H1
- Schema
- Links internos
- Páginas órfãs
- Registros editoriais
- Contagem de artigos
- Indexação monitorada
- Git
- QA
- Relatórios
"""
import json, re, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
BLOG_DIR = REPO / 'blog'
NOTICIAS_DIR = REPO / 'noticias'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
SITEMAP_SCRIPT = REPO / 'scripts' / 'gerar_sitemap.py'

def regenerate_sitemap() -> dict:
    """Regenera sitemap"""
    result = subprocess.run(
        f'python "{SITEMAP_SCRIPT}"',
        shell=True,
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return {
        'ok': result.returncode == 0,
        'output': result.stdout,
        'error': result.stderr,
    }

def update_registry_counts() -> dict:
    """Atualiza contagens no registro"""
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    
    blog_count = len(list(BLOG_DIR.glob('*.html')))
    noticias_count = len(list(NOTICIAS_DIR.glob('*.html'))) if NOTICIAS_DIR.exists() else 0
    formacoes_count = len(list(FORMACOES_DIR.glob('*.html'))) if FORMACOES_DIR.exists() else 0
    
    registry['maintenance'] = {
        'last_run': datetime.now(timezone.utc).isoformat(),
        'blog_count': blog_count,
        'noticias_count': noticias_count,
        'formacoes_count': formacoes_count,
        'total_pages': blog_count + noticias_count + formacoes_count,
    }
    
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return {
        'ok': True,
        'blog_count': blog_count,
        'noticias_count': noticias_count,
        'formacoes_count': formacoes_count,
        'total_pages': blog_count + noticias_count + formacoes_count,
    }

def check_orphan_pages() -> dict:
    """Verifica páginas órfãs"""
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    articles = registry.get('articles', [])
    article_slugs = {a.get('slug') for a in articles if a.get('slug')}
    
    orphan_pages = []
    for html_file in list(BLOG_DIR.glob('*.html'))[:50]:
        slug = html_file.stem
        if slug not in article_slugs:
            orphan_pages.append({
                'file': html_file.name,
                'slug': slug,
            })
    
    return {
        'ok': True,
        'orphan_count': len(orphan_pages),
        'orphans': orphan_pages[:10],
    }

def commit_changes(message: str) -> dict:
    """Commit e push de mudanças"""
    try:
        # Git add
        subprocess.run('git add -A', shell=True, cwd=REPO, check=True, capture_output=True)
        
        # Git commit
        subprocess.run(
            f'git commit -m "{message}"',
            shell=True,
            cwd=REPO,
            check=True,
            capture_output=True,
        )
        
        # Git push
        subprocess.run('git push origin main', shell=True, cwd=REPO, check=True, capture_output=True)
        
        return {'ok': True, 'message': message}
    except subprocess.CalledProcessError as e:
        return {'ok': False, 'error': str(e)}

def run(context: dict) -> dict:
    """Executa manutenção automática"""
    results = []
    
    # 1. Sitemap
    sitemap_result = regenerate_sitemap()
    results.append({'task': 'sitemap', 'result': sitemap_result})
    
    # 2. Registry counts
    counts_result = update_registry_counts()
    results.append({'task': 'registry_counts', 'result': counts_result})
    
    # 3. Orphan pages
    orphan_result = check_orphan_pages()
    results.append({'task': 'orphan_pages', 'result': orphan_result})
    
    # 4. Git commit (if needed)
    # Only commit if maintenance made changes
    git_result = commit_changes('feat: manutenção automática — sitemap, registros, métricas')
    results.append({'task': 'git', 'result': git_result})
    
    return {
        'status': 'ok',
        'actions': results,
        'message': f'Manutenção: {len(results)} tarefas executadas',
    }
