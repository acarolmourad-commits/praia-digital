import re, csv
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent.parent

PUBLIC_GLOBS = [
    'imoveis/*.html','bairros/*.html','hub/*.html','blog/*.html','cidades/*.html',
    'servicos/*.html','servicos/cidade-servico/*.html','cases/*.html','curso/*.html',
    'landings/*.html','personas/*.html','ferramentas/*.html','anfitrioes/*.html',
    'ia/*.html','investidores/*.html','parcerias-norte/*.html','proptech/*.html',
    'contato.html',
]

BASE_DOMAIN = 'praia.digital'
html_files = []
seen = set()
for pattern in PUBLIC_GLOBS:
    for p in REPO.glob(pattern):
        rel = str(p.relative_to(REPO)).replace('\\', '/')
        if rel in seen:
            continue
        seen.add(rel)
        html_files.append((rel, p))

print(f'Total HTML files: {len(html_files)}')
link_map = {rel: set() for rel, _ in html_files}

for rel, path in html_files:
    txt = path.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'href=["\']([^"\']+)["\']', txt):
        href = m.group(1).strip()
        if not href or href.startswith(('#','javascript:','mailto:','tel:')):
            continue
        parsed = urlparse(href)
        if parsed.netloc and BASE_DOMAIN not in parsed.netloc:
            continue
        if parsed.netloc and BASE_DOMAIN in parsed.netloc:
            path_href = parsed.path
            if path_href.startswith('/'):
                path_href = path_href[1:]
            if not path_href:
                continue
            if path_href.endswith('/'):
                path_href += 'index.html'
            elif '.' not in Path(path_href).name:
                path_href += '.html'
            norm = path_href.replace('\\', '/')
            if norm in link_map:
                link_map[rel].add(norm)
            continue
        if href.startswith('/'):
            path_href = href[1:]
        else:
            path_href = href
        if path_href.endswith('/'):
            path_href += 'index.html'
        elif '.' not in Path(path_href).name:
            path_href += '.html'
        norm = path_href.replace('\\', '/')
        if norm in link_map:
            link_map[rel].add(norm)

all_targets = set()
for targets in link_map.values():
    all_targets.update(targets)

orphans = [rel for rel, _ in html_files if rel not in all_targets and rel not in ['index.html', 'contato.html']]
print(f'Orphans: {len(orphans)}')

broken = [(src, tgt) for src, targets in link_map.items() for tgt in targets if tgt not in link_map]
print(f'Broken links: {len(broken)}')

redirects = []
for rel, path in html_files:
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if re.search(r'http-equiv=["\']refresh["\']', txt, re.I):
        redirects.append(rel)
print(f'Redirects: {len(redirects)}')

out = REPO / 'docs/INTERNAL_LINKING_REPORT.csv'
with out.open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['URL','CLUSTER','PROBLEM','OPPORTUNITY','RISK','RECOMMENDATION'])
    for rel in orphans[:500]:
        cluster = rel.split('/')[0]
        w.writerow([rel, cluster, 'ORPHAN', 'Add links from related pages', 'LOW', 'Link from cluster hub or related content'])
    for src, tgt in broken[:500]:
        cluster = src.split('/')[0]
        w.writerow([src, cluster, f'BROKEN_LINK -> {tgt}', 'Fix or remove link', 'MEDIUM', 'Verify target exists or update href'])
    for rel in redirects[:200]:
        cluster = rel.split('/')[0]
        w.writerow([rel, cluster, 'REDIRECT', 'Review redirect necessity', 'LOW', 'Ensure redirect is intentional and documented'])

print(f'Report written: {out}')
