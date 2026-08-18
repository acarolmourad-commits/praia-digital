#!/usr/bin/env python3
"""
Batch article generator for Praia Digital editorial expansion.
Generates SEO-ready HTML articles in batches and updates sitemap/registry.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from editorial_expansion import load_bank, get_expansion_targets, validate_slug
from article_generator import generate_article, load_template, validate_generated_article, PublicationGateError

REPO = Path(__file__).resolve().parents[3]
BLOG_DIR = REPO / 'blog'
SITEMAP_PATH = REPO / 'sitemap.xml'
REGISTRY_PATH = REPO / 'docs' / 'editorial_registry.json'


def get_existing_paths():
    """Get set of existing article paths to avoid duplicates."""
    existing = set()
    for p in BLOG_DIR.glob('*.html'):
        existing.add(str(p.relative_to(REPO)))
    return existing


def validate_target(target, existing_paths):
    """Validate target viability."""
    city = target.get('city') or ''
    title = target.get('title') or ''
    
    if not city or not title:
        return False, 'missing city or title'
    
    slug = validate_slug(title, city)
    expected_path = f"blog/{slug}.html"
    
    if expected_path in existing_paths:
        return False, f'path already exists: {expected_path}'
    
    if not target.get('primary_keyword'):
        return False, 'missing primary_keyword'
    
    return True, slug


def update_sitemap(new_paths):
    """Append new URLs to sitemap.xml."""
    if not SITEMAP_PATH.exists():
        print('WARNING: sitemap.xml not found, skipping sitemap update')
        return
    
    sitemap = SITEMAP_PATH.read_text(encoding='utf-8')
    today = datetime.now().strftime('%Y-%m-%d')
    
    new_urls = []
    for path in new_paths:
        url = f"https://praia.digital/{path}"
        url = url.replace('\\', '/')
        entry = f"<url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq></url>"
        new_urls.append(entry)
    
    # Insert before closing </urlset>
    if '</urlset>' in sitemap:
        sitemap = sitemap.replace('</urlset>', '\n'.join(new_urls) + '\n</urlset>')
        SITEMAP_PATH.write_text(sitemap, encoding='utf-8')
        print(f'SITEMAP: added {len(new_paths)} URLs')
    else:
        print('WARNING: sitemap.xml missing </urlset>, skipping')


def update_registry(new_articles):
    """Update editorial registry with new articles."""
    if not REGISTRY_PATH.exists():
        print('WARNING: editorial_registry.json not found, skipping registry update')
        return
    
    registry = json.loads(REGISTRY_PATH.read_text(encoding='utf-8'))
    
    if 'articles' not in registry:
        registry['articles'] = []
    
    existing_ids = {a.get('id') for a in registry['articles']}
    added = 0
    for a in new_articles:
        if a.get('id') not in existing_ids:
            registry['articles'].append(a)
            added += 1
    
    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f'REGISTRY: added {added} articles')


def generate_batch(batch_size=10, dry_run=False, start_from=0):
    """
    Generate a batch of expansion articles.
    Returns dict with results.
    """
    data = load_bank()
    articles = data.get('articles', [])
    targets = get_expansion_targets(articles)
    existing_paths = get_existing_paths()
    
    written_paths = []
    written_articles = []
    skipped = []
    
    template = load_template()
    
    for i, target in enumerate(targets[start_from:], start=start_from):
        if len(written_paths) >= batch_size:
            break
        
        valid, msg = validate_target(target, existing_paths)
        if not valid:
            skipped.append({'target': target.get('title'), 'reason': msg})
            continue
        
        try:
            path, article, filename = generate_article(target, template)
            rel_path = str(path.relative_to(REPO))
            
            if dry_run:
                print(f'[DRY RUN] {rel_path}')
                written_paths.append(rel_path)
            else:
                if path.exists():
                    skipped.append({'target': target.get('title'), 'reason': 'already exists'})
                    continue
                
                validate_generated_article(article, path)
                path.write_text(article, encoding='utf-8')
                written_paths.append(rel_path)
                written_articles.append({
                    'id': target.get('id'),
                    'title': target.get('title'),
                    'path': rel_path,
                    'cluster': target.get('cluster'),
                    'city': target.get('city'),
                    'generated_at': datetime.now().isoformat(),
                })
                print(f'WRITE: {rel_path}')
        except PublicationGateError as e:
            skipped.append({'target': target.get('title'), 'reason': f'publication_gate: {e}'})
        except Exception as e:
            skipped.append({'target': target.get('title'), 'reason': str(e)})
    
    # Update sitemap and registry
    if not dry_run and written_paths:
        update_sitemap(written_paths)
        update_registry(written_articles)
    
    return {
        'written': written_paths,
        'skipped': skipped,
        'total_targets': len(targets),
        'batch_size': batch_size,
    }


if __name__ == '__main__':
    result = generate_batch(batch_size=10, dry_run=False)
    print(f"\n=== BATCH COMPLETE ===")
    print(f"Written: {len(result['written'])}")
    print(f"Skipped: {len(result['skipped'])}")
    print(f"Total targets available: {result['total_targets']}")
