#!/usr/bin/env python3
"""Coleta métricas da Batch146 a partir de fontes locais/URLs."""
import json, re, csv, os
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

BASE = Path(r'C:\Users\Carolina\praia-digital')
BLOG_DIR = BASE / 'blog'
SPEC = BASE / 'docs/medicao-batch146.json'
TEMPLATE = BASE / 'docs/medicao-batch146-resultado-template.json'
OUT = BASE / 'docs/medicao-batch146-resultado.json'
SITE = 'https://praia.digital'

def fetch(url, timeout=15):
    try:
        with urlopen(url, timeout=timeout) as r:
            return r.status, r.read().decode('utf-8', errors='ignore')
    except (HTTPError, URLError, Exception) as e:
        return None, str(e)

def local_metrics(slug):
    html = BLOG_DIR / f'{slug}.html'
    if not html.exists():
        return {'exists': False}
    txt = html.read_text(encoding='utf-8', errors='ignore')
    words = len(re.findall(r'\w+', txt))
    h1 = len(re.findall(r'<h1', txt, flags=re.I))
    return {
        'exists': True,
        'chars': len(txt),
        'words': words,
        'h1_count': h1,
        'has_title': '<title>' in txt.lower(),
        'has_description': '<meta name="description"' in txt.lower()
    }

def summarize_local(items):
    total = len(items)
    exists = sum(1 for i in items if i['local'].get('exists'))
    no_title = sum(1 for i in items if i['local'].get('exists') and not i['local'].get('has_title'))
    no_desc = sum(1 for i in items if i['local'].get('exists') and not i['local'].get('has_description'))
    short = sum(1 for i in items if i['local'].get('exists') and i['local'].get('words', 0) < 300)
    return {
        'total': total,
        'exists': exists,
        'missing': total - exists,
        'no_title': no_title,
        'no_description': no_desc,
        'short_local': short
    }

def summarize_remote(results):
    total = len(results)
    remote_ok = sum(1 for r in results if r.get('remote_ok'))
    remote_fail = total - remote_ok
    statuses = {}
    for r in results:
        s = r.get('remote_status')
        statuses[s] = statuses.get(s, 0) + 1
    return {
        'total': total,
        'remote_ok': remote_ok,
        'remote_fail': remote_fail,
        'status_counts': statuses
    }

def main():
    spec = json.loads(SPEC.read_text(encoding='utf-8'))
    template = json.loads(TEMPLATE.read_text(encoding='utf-8'))
    items = spec.get('items', [])
    results = []
    for item in items:
        slug = item['slug']
        lm = local_metrics(slug)
        url = f"{SITE}/blog/{slug}.html"
        status, body = fetch(url)
        results.append({
            'slug': slug,
            'action': item['action'],
            'local': lm,
            'remote_status': status,
            'remote_ok': status == 200,
            'remote_url': url,
        })
    summary = {
        'local': summarize_local([{**item, 'local': local_metrics(item['slug'])} for item in items]),
        'remote': summarize_remote(results)
    }
    template['status'] = 'measurement_collected'
    template['collected_at'] = str(Path(__file__).stat().st_mtime)
    template['results'] = results
    template['summary'] = summary
    OUT.write_text(json.dumps(template, indent=2, ensure_ascii=False), encoding='utf-8')
    print('collected', len(results), 'items ->', OUT)
    print('summary:', json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    main()
