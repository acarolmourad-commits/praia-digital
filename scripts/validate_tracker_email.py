import re, sys
from pathlib import Path
BLOCKED = {'exemplo.com','teste.com','domain.com','mail.com','fake.com'}
def ok(email: str) -> bool:
    if not email or '@' not in email:
        return False
    local, domain = email.rsplit('@', 1)
    if not local or not domain:
        return False
    if domain.lower() in BLOCKED:
        return False
    if re.search(r'[^a-zA-Z0-9._%+-]', local + domain):
        return False
    return True
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('docs/sales/csv-lotes-email/tracker-email-proprietarios.csv')
lines = path.read_bytes().decode('utf-8-sig').splitlines()
sep = ';' if ';' in lines[0] else ','
header = lines[0].split(sep)
idx = next((i for i,h in enumerate(header) if 'email' in h.lower() and 'nome' not in h.lower()), None)
if idx is None:
    print('No email column found')
    raise SystemExit(1)
bad=[]
for i,line in enumerate(lines[1:], start=2):
    parts=line.split(sep)
    if len(parts)<=idx:
        continue
    email=parts[idx].strip().strip('"')
    if not ok(email):
        bad.append((i,email))
print(f'Validated {len(lines)-1} rows, {len(bad)} invalid')
for row,email in bad[:20]:
    print(f'  row {row}: {email}')
