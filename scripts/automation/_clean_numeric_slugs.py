import csv, re
from pathlib import Path

repo = Path('.').resolve()
csv_path = repo / 'imoveis' / 'landings.csv'

with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

clean = []
dropped = 0
for r in rows:
    slug = (r.get('slug') or '').strip()
    if re.fullmatch(r'\d+', slug):
        dropped += 1
        continue
    if not slug:
        dropped += 1
        continue
    clean.append(r)

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in clean:
        writer.writerow(r)

print('dropped', dropped)
print('csv_rows_now', len(clean))
