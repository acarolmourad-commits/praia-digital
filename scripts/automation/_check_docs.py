import re
from pathlib import Path
root=Path('.').resolve()
targets=['docs/inteligencia','docs/product','docs/sales']
issues=[]
for t in targets:
    base=root/t
    if not base.exists():
        continue
    for p in base.rglob('*.html'):
        txt=p.read_text(encoding='utf-8',errors='ignore')
        rel=str(p.relative_to(root))
        if not re.search(r'<meta\s+name="description"\s+content="[^"]+"', txt, flags=re.I):
            issues.append((rel, 'missing_meta_description'))
        if not re.search(r'<link\s+rel="canonical"\s+href="https://praia\.digital/', txt, flags=re.I):
            issues.append((rel, 'missing_canonical'))
        if 'application/ld+json' not in txt:
            issues.append((rel, 'missing_schema'))
print('issues', len(issues))
for i in issues:
    print(i)
