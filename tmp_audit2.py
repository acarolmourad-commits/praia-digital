from pathlib import Path
import re
issues=[]
for p in list(Path('assets').glob('*.html')) + list(Path('servicos').glob('*.html')):
    text = p.read_text(encoding='utf-8', errors='ignore')
    rel = str(p.relative_to(Path('.'))).replace('\\', '/')
    m = re.search(r'</html>([\s\S]*)$', text, re.I)
    if m and m.group(1).strip():
        issues.append((rel, 'AFTER_HTML', m.group(1).strip()[:120]))
print('TOTAL', len(issues))
for rel, kind, snip in issues[:20]:
    print(rel, kind, snip)
