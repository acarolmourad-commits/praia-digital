#!/usr/bin/env python3
"""
Módulo: SEO — Praia Digital.
- Verifica meta/h1/schema/CTA em amostras
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
    cta = any(p in html.lower() for p in ['whatsapp', 'wa.me', 'comprar', 'checkout'])

    is_redirect = (
        title and 'redirecionando' in title.group(1).lower()
    ) or bool(re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', html, re.I))

    return {
        'slug': slug,
        'has_title': bool(title),
        'has_h1': bool(h1),
        'has_meta': bool(meta),
        'has_schema': schema,
        'has_cta': cta,
        'title_len': len(title.group(1)) if title else 0,
        'h1_len': len(h1.group(1)) if h1 else 0,
        'meta_len': len(meta.group(1)) if meta else 0,
        'is_redirect': is_redirect,
    }

def run(context: dict) -> dict:
    files = sample_articles(20)
    results = [audit_article(f) for f in files]

    issues = [r for r in results if not r['is_redirect'] and (not r['has_h1'] or not r['has_meta'] or r['meta_len'] < 60 or not r['has_cta'])]
    summary = {
        'sampled': len(results),
        'issues': len(issues),
        'missing_schema': sum(1 for r in results if not r.get('has_schema') and not r.get('is_redirect')),
        'short_meta': sum(1 for r in results if r.get('meta_len', 0) < 60 and not r.get('is_redirect')),
        'short_title': sum(1 for r in results if r.get('title_len', 0) < 40 and not r.get('is_redirect')),
        'missing_h1': sum(1 for r in results if not r.get('has_h1') and not r.get('is_redirect')),
        'missing_cta': sum(1 for r in results if not r.get('has_cta') and not r.get('is_redirect')),
    }

    opportunities = []
    if summary['missing_schema'] > 0:
        opportunities.append({'type': 'seo_audit', 'message': f"{summary['missing_schema']} artigos sem schema", 'priority': 2})
    if summary['short_meta'] > 0:
        opportunities.append({'type': 'seo_audit', 'message': f"{summary['short_meta']} artigos com meta curta", 'priority': 2})
    if summary['missing_h1'] > 0:
        opportunities.append({'type': 'seo_audit', 'message': f"{summary['missing_h1']} artigos sem h1", 'priority': 3})
    if summary['missing_cta'] > 0:
        opportunities.append({'type': 'seo_audit', 'message': f"{summary['missing_cta']} artigos sem CTA/WhatsApp", 'priority': 2})

    return {
        'status': 'ok',
        'actions': [],
        'sampled': len(results),
        'issues': issues[:10],
        'summary': summary,
        'opportunities': opportunities[:10],
        'message': f"SEO audit: {len(results)} amostrados, {len(issues)} issues, {len(opportunities)} oportunidades",
    }
