from pathlib import Path
import re
issues = []
for p in Path('.').glob('**/*.html'):
    try:
        text = p.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    rel = str(p.relative_to(Path('.'))).replace('\\', '/')
    # content after </html>
    m = re.search(r'</html>([\s\S]*)$', text, re.I)
    if m:
        after = m.group(1).strip()
        if after:
            issues.append((rel, 'AFTER_HTML', after[:120]))
    # duplicate viewport meta
    if rel.startswith('assets/analise-retorno-aluguel-temporada-ia.html'):
        if text.count('<meta name="viewport"') > 1:
            issues.append((rel, 'DUP_VIEWPORT', ''))
    # missing </body> before </html>
    if '<body>' in text and '</body>' not in text:
        issues.append((rel, 'MISSING_BODY_CLOSE', ''))
print('TOTAL_ISSUES', len(issues))
for rel, kind, snip in issues[:50]:
    print(rel, kind, snip)
