from pathlib import Path
import re

root = Path('.')
exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

new_date = '2026-08-03'

# target patterns that indicate older content dates
patterns = ['2026-07', '2026-08-01', '2026-08-02']

updated = 0
for path in root.rglob('*.html'):
    rel = path.relative_to(root)
    if any(part in exclude for part in rel.parts):
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if not any(pat in text for pat in patterns):
        continue
    new_text = re.sub(r'2026-07-\d{2}|2026-08-0[12]', new_date, text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        updated += 1

print('updated', updated)
