#!/usr/bin/env python3
"""
Módulo: SEO — Praia Digital.
- Verifica meta/h1/schema em amostras
- Identifica oportunidades de ajuste
- Não altera nada sem porta humana, exceto quando explicitamente permitido
"""
import json, re, random
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'

def sample_articles(n=20):
    files = list(BLOG_DIR.glob('*.html'))
    return random.sample(files, min(n, len(files)))

def audit_article(path: Path) -> dict:
    html = path.read_text(encoding='utf-8', errors='ignore')
    slug = path.stem
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.S|re.I)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S|re.I)
    meta = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', html, re.I)
    schema = 'schema.org' in html or 'application/ld+json' in html

    return {
        'slug': slug,
        'has_title': bool(title),
        'has_h1': bool(h1),
        'has_meta': bool(meta),
        'has_schema': schema,
        'title_len': len(title.group(1)) if title else 0,
        'h1_len': len(h1.group(1)) if h1 else 0,
        'meta_len': len(meta.group(1)) if meta else 0,
    }

def run(context: dict) -> dict:
    files = sample_articles(20)
    results = [audit_article(f) for f in files]

    issues = [r for r in results if not r['has_h1'] or not r['has_meta'] or r['meta_len'] < 60]
    opportunities = [r for r in results if r['has_h1'] and r['has_meta'] and r['meta_len'] < 120 and r['title_len'] < 60]

    return {
        'status': 'ok',
        'actions': [],
        'sampled': len(results),
        'issues': issues[:10],
        'opportunities': opportunities[:10],
        'message': f'SEO audit: {len(results)} artigos amostrados, {len(issues)} issues, {len(opportunities)} oportunidades',
    }
