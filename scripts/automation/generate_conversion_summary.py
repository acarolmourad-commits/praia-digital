from pathlib import Path
import csv
from collections import defaultdict, Counter

root = Path('.')
exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

rows = []
for p in root.rglob('*.html'):
    rel = p.relative_to(root)
    if any(part in exclude for part in rel.parts):
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    cta_count = text.lower().count('https://wa.me/5511954346288')
    if cta_count == 0:
        continue
    has_utm = 'utm_source=site' in text
    utm_count = text.lower().count('utm_source=site')
    category = 'outro'
    parts = rel.parts
    if parts[0] == 'blog':
        category = 'blog'
    elif parts[0] == 'cidades':
        category = 'cidade'
    elif parts[0] == 'bairros':
        category = 'bairro'
    elif parts[0] == 'imoveis':
        category = 'imovel'
    elif parts[0] == 'servicos':
        if 'cidade-servico' in str(rel):
            category = 'servico_cidade'
        else:
            category = 'servico'
    elif parts[0] == 'litoral-prime-imoveis':
        if len(parts) > 1 and parts[1] == 'servicos':
            category = 'servico_lp'
        else:
            category = 'hub_lp'
    elif str(rel) in {'index.html', 'servicos.html', 'imoveis.html', 'cases.html'}:
        category = 'hub'
    elif 'landing' in str(rel) or 'parceria' in str(rel):
        category = 'landing'
    elif str(rel).startswith('guia-'):
        category = 'guia'
    rows.append({
        'page': str(rel),
        'category': category,
        'cta_count': cta_count,
        'has_utm': 'sim' if has_utm else 'nao',
        'utm_count': utm_count,
    })

# summary
summary = defaultdict(lambda: {'pages': 0, 'ctas': 0, 'with_utm': 0})
for r in rows:
    s = summary[r['category']]
    s['pages'] += 1
    s['ctas'] += r['cta_count']
    s['with_utm'] += r['utm_count']

out = Path('conversion_summary.csv')
with out.open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['categoria','paginas_com_cta','total_ctas','ctas_com_utm','pct_utm'])
    for cat in sorted(summary):
        s = summary[cat]
        pct = round(s['with_utm'] / s['ctas'] * 100, 1) if s['ctas'] else 0
        writer.writerow([cat, s['pages'], s['ctas'], s['with_utm'], pct])

print('rows', len(rows), 'categories', len(summary))
print('summary written to', out)
