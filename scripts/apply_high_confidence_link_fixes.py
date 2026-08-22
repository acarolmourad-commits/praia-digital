"""Apply only high-confidence, evidence-backed link fixes from manual audit."""
import csv
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
CSV_PATH = BASE / 'docs/editorial/link-broken-manual-2026-08-14-v3.csv'
LOG_PATH = BASE / 'docs/editorial/auto-link-fixes-2026-08-17.csv'

rows = list(csv.DictReader(CSV_PATH.open(encoding='utf-8')))
fixed = []
skipped = []
errors = []

for row in rows:
    acao = row.get('acao_recomendada', '').strip().lower()
    confianca = row.get('confianca_sugestao', '').strip().upper()
    source = row.get('arquivo_origem', '').strip()
    link = row.get('link_atual', '').strip()
    suggested = row.get('destino_sugerido', '').strip()
    if acao != 'corrigir_caminho' or confianca != 'ALTA' or not source or not link or not suggested:
        skipped.append({**row, 'motivo_skip': 'not high-confidence actionable'})
        continue
    html_path = BASE / source
    target_path = BASE / suggested.lstrip('/').replace('/', '\\')
    if not html_path.exists():
        errors.append({**row, 'erro': 'source_missing'})
        continue
    if not target_path.exists():
        errors.append({**row, 'erro': 'suggested_target_missing'})
        continue
    text = html_path.read_text(encoding='utf-8', errors='ignore')
    if link not in text:
        skipped.append({**row, 'motivo_skip': 'link_not_found_in_source'})
        continue
    new_text = text.replace(link, suggested)
    if new_text == text:
        skipped.append({**row, 'motivo_skip': 'no_change_after_replace'})
        continue
    html_path.write_text(new_text, encoding='utf-8')
    fixed.append({
        'source': source,
        'old_link': link,
        'new_link': suggested,
        'confianca': confianca,
        'motivo': row.get('motivo', ''),
    })

with LOG_PATH.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['source','old_link','new_link','confianca','motivo'])
    writer.writeheader()
    writer.writerows(fixed)

print(f'Fixed: {len(fixed)}')
for item in fixed:
    print(f"  {item['source']} :: {item['old_link']} -> {item['new_link']}")
print(f'Skipped: {len(skipped)}')
print(f'Errors: {len(errors)}')
for e in errors:
    print(' ', e['source'], e['erro'])
