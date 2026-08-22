"""Fix high-confidence broken internal links from the manual audit CSV."""
import csv
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
CSV_PATH = BASE / 'docs/editorial/link-broken-manual-2026-08-14-v3.csv'

rows = list(csv.DictReader(CSV_PATH.open(encoding='utf-8')))
fixed = []
skipped = []
errors = []

for row in rows:
    acao = row.get('acao_recomendada', '').strip().lower()
    source = row.get('arquivo_origem', '').strip()
    link = row.get('link_atual', '').strip()
    suggested = row.get('destino_sugerido', '').strip()
    confianca = row.get('confianca_sugestao', '').strip().upper()
    if acao != 'corrigir_caminho' or not source or not link or not suggested:
        skipped.append(row)
        continue
    html_path = BASE / source
    if not html_path.exists():
        errors.append({'source': source, 'error': 'source missing'})
        continue
    text = html_path.read_text(encoding='utf-8', errors='ignore')
    if link not in text:
        # try normalized variants
        skipped.append(row)
        continue
    new_text = text.replace(link, suggested)
    if new_text == text:
        skipped.append(row)
        continue
    html_path.write_text(new_text, encoding='utf-8')
    fixed.append({'source': source, 'old': link, 'new': suggested, 'confianca': confianca})

print(f'Fixed: {len(fixed)}')
for item in fixed:
    print(f"  {item['source']} :: {item['old']} -> {item['new']} ({item['confianca']})")
print(f'Skipped: {len(skipped)}')
print(f'Errors: {len(errors)}')
if errors:
    for e in errors:
        print(' ', e)
