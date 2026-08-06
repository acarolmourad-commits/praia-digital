import re, requests
from pathlib import Path

checks = [
    ('docs/render-academy-deploy.md', ['Web Service', 'DATABASE_URL', 'ALLOWED_ORIGINS', 'BASE_URL', 'check_academy_deploy.py', 'frontend_health_check.py']),
    ('docs/render-academy-manual-steps.md', ['Web Service', 'PostgreSQL nomeado `academy-db`', 'ALLOWED_ORIGINS', 'academy.praia.digital', 'rollback']),
]

ok = True
for path, needles in checks:
    txt = Path(path).read_text(encoding='utf-8', errors='ignore')
    for n in needles:
        if n.lower() not in txt.lower():
            print(f'MISSING {n} in {path}')
            ok = False

if ok:
    print('deploy docs checks passed')
