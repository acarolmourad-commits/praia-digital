#!/usr/bin/env python3
"""
P2-10 schema type audit.
Detects schema type per page and validates against expected type.
"""
import json, re, csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

PUBLIC_GLOBS = [
    'imoveis/*.html','bairros/*.html','hub/*.html','blog/*.html','cidades/*.html',
    'servicos/*.html','servicos/cidade-servico/*.html','cases/*.html','curso/*.html',
    'landings/*.html','personas/*.html','ferramentas/*.html','anfitrioes/*.html',
    'ia/*.html','investidores/*.html','parcerias-norte/*.html','proptech/*.html',
    'contato.html',
]

# Expected schema by directory/template
EXPECTED_SCHEMA = {
    'blog': 'BlogPosting',
    'imoveis': 'RealEstateListing',
    'bairros': 'Place',
    'cidades': 'Place',
    'servicos': 'Service',
    'cases': 'CaseStudy',
    'curso': 'Course',
    'landings': 'WebPage',
    'personas': 'WebPage',
    'ferramentas': 'WebPage',
    'anfitrioes': 'WebPage',
    'ia': 'WebPage',
    'investidores': 'WebPage',
    'parcerias-norte': 'WebPage',
    'proptech': 'WebPage',
    'hub': 'WebPage',
}

html_files = []
seen = set()
for pattern in PUBLIC_GLOBS:
    for p in REPO.glob(pattern):
        rel = str(p.relative_to(REPO)).replace('\\', '/')
        if rel in seen:
            continue
        seen.add(rel)
        html_files.append((rel, p))

print(f'Total HTML files: {len(html_files)}')

results = []
for rel, path in html_files:
    txt = path.read_text(encoding='utf-8', errors='ignore')
    json_blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', txt, re.S | re.I)
    schemas = []
    valid = True
    errors = []
    for block in json_blocks:
        try:
            data = json.loads(block)
            schemas.append(data)
        except json.JSONDecodeError as e:
            valid = False
            errors.append(f'invalid_json: {e}')
    
    # Detect schema type
    schema_types = []
    for s in schemas:
        if isinstance(s, dict):
            t = s.get('@type') or s.get('@type')
            if t:
                schema_types.append(t)
            elif '@graph' in s and isinstance(s['@graph'], list):
                for item in s['@graph']:
                    if isinstance(item, dict) and item.get('@type'):
                        schema_types.append(item['@type'])
    
    cluster = rel.split('/')[0]
    expected = EXPECTED_SCHEMA.get(cluster, 'WebPage')
    
    # Determine status
    if not schemas:
        status = 'SCHEMA_MISSING'
    elif not valid:
        status = 'SCHEMA_INVALID'
    elif not schema_types:
        status = 'SCHEMA_NO_TYPE'
    elif expected in schema_types:
        status = 'SCHEMA_OK'
    elif 'BlogPosting' in schema_types and cluster == 'blog':
        status = 'SCHEMA_OK'
    elif 'WebPage' in schema_types:
        status = 'SCHEMA_GENERIC'
    else:
        status = 'SCHEMA_MISMATCH'
    
    results.append({
        'url': rel,
        'cluster': cluster,
        'schema_types': ','.join(schema_types) if schema_types else 'NONE',
        'expected': expected,
        'status': status,
        'evidence': '; '.join(errors) if errors else 'valid' if valid else 'invalid'
    })

# Summary
from collections import Counter
summary = Counter(r['status'] for r in results)
print('Schema audit summary:')
for k, v in sorted(summary.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

# Write CSV
out = REPO / 'docs/SCHEMA_TYPE_AUDIT.csv'
with out.open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['URL','CLUSTER','SCHEMA','EXPECTED_SCHEMA','STATUS','EVIDENCE'])
    for r in results:
        w.writerow([r['url'], r['cluster'], r['schema_types'], r['expected'], r['status'], r['evidence']])

print(f'Report written: {out}')
