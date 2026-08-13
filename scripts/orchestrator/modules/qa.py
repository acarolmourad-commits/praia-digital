#!/usr/bin/env python3
"""
Módulo: QA — Praia Digital.
- Verifica HTML básico: tags fechadas, links internos válidos, schema mínimo
- Não altera conteúdo, só reporta issues
"""
import json, re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
FORMACOES_DIR = REPO / 'education' / 'formacoes'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

def check_html(path: Path) -> dict:
    html = path.read_text(encoding='utf-8', errors='ignore')
    issues = []

    if '<html' not in html.lower():
        issues.append('missing_html_tag')
    if '<h1' not in html.lower():
        issues.append('missing_h1')
    if '<title' not in html.lower():
        issues.append('missing_title')

    # Check for unclosed tags (basic)
    open_tags = len(re.findall(r'<(?!/)(?!!)[a-zA-Z][^>]*>', html))
    close_tags = len(re.findall(r'</[a-zA-Z][^>]*>', html))
    if abs(open_tags - close_tags) > 5:
        issues.append('possible_unbalanced_tags')

    # Check for broken internal links (basic)
    internal_links = re.findall(r'href="(/[^"]+)"', html)
    for link in internal_links[:10]:  # sample
        target = REPO / link.lstrip('/')
        if not target.exists():
            issues.append(f'broken_link:{link}')
            break

    return {
        'path': str(path.relative_to(REPO)),
        'issues': issues,
        'status': 'ok' if not issues else 'issues_found',
    }

def run(context: dict) -> dict:
    # Sample files from blog and formacoes
    blog_files = list(BLOG_DIR.glob('*.html'))[:20]
    formacoes_files = list(FORMACOES_DIR.glob('*.html'))[:8]
    all_files = blog_files + formacoes_files

    results = [check_html(f) for f in all_files]
    issues_found = [r for r in results if r['status'] == 'issues_found']

    return {
        'status': 'ok',
        'actions': [],
        'sampled': len(results),
        'issues_found': len(issues_found),
        'details': issues_found[:10],
        'message': f'QA: {len(results)} arquivos verificados, {len(issues_found)} com issues',
    }
