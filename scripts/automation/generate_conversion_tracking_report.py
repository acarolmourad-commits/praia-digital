from pathlib import Path
import csv
import re

root = Path('.')
exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

utm_re = re.compile(r'https://wa\.me/5511954346288\?([^"\'>\s]+)')

rows = []
for p in root.rglob('*.html'):
    rel = p.relative_to(root)
    if any(part in exclude for part in rel.parts):
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    for m in utm_re.finditer(text):
        qs = m.group(1)
        params = dict(re.findall(r'([^=&]+)=([^&]*)', qs))
        rows.append({
            'page': str(rel),
            'whatsapp_url': m.group(0),
            'utm_source': params.get('utm_source', ''),
            'utm_medium': params.get('utm_medium', ''),
            'utm_campaign': params.get('utm_campaign', ''),
            'utm_content': params.get('utm_content', ''),
        })

out = Path('conversion_tracking_report.csv')
with out.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['page','whatsapp_url','utm_source','utm_medium','utm_campaign','utm_content'])
    writer.writeheader()
    writer.writerows(rows)

print('wrote', len(rows), 'rows to', out)
