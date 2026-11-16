#!/usr/bin/env python3
"""Agente Site Inspector (praia.digital).
Inspeciona todas as paginas HTML do repo: links internos quebrados e conteudo
desatualizado (referencias a anos antigos). Gera relatorio e abre/atualiza uma
issue no GitHub com label 'site-inspection' para revisao contextual."""
import os, re, json, glob, datetime, urllib.request
from link_inventory import inspect_links

TOKEN = os.environ.get('GITHUB_TOKEN','')
REPO = os.environ.get('GITHUB_REPOSITORY','acarolmourad-commits/praia-digital')
TODAY = datetime.date.today().isoformat()
CURRENT_YEAR = datetime.date.today().year

HTML = [f for f in glob.glob('**/*.html', recursive=True)
        if not f.startswith(('node_modules/', '.git/', 'social/'))]

YEAR_RE = re.compile(r'\b(20(?:19|20|21|22|23|24|25))\b')

broken, outdated, external = [], [], set()
for f in HTML:
    try: txt = open(f, encoding='utf-8', errors='ignore').read()
    except Exception: continue
    page_broken, page_external = inspect_links(txt, f)
    broken.extend(page_broken)
    external.update(page_external)
    # texto visivel (fora de tags) com anos antigos
    for seg in re.findall(r'>([^<>]+)<', txt):
        for ym in YEAR_RE.finditer(seg):
            ctx = seg.strip()[max(0, ym.start()-40):ym.end()+40]
            outdated.append({'page': f, 'year': ym.group(1), 'context': ctx[:120]})

report = {
    'date': TODAY,
    'pages_scanned': len(HTML),
    'broken_links': broken[:200],
    'outdated_mentions': outdated[:200],
    'totals': {'broken': len(broken), 'outdated': len(outdated)},
    'external_links': sorted(external),
    'coverage': {'internal': 'static href/src including same-host absolute URLs',
                 'external_http_checked': False, 'external_unique': len(external),
                 'fragments_checked': False, 'rendered_javascript_checked': False},
    'status': 'needs_review' if broken or outdated else 'static_checks_passed',
}
json.dump(report, open('site_inspection_report.json','w'), ensure_ascii=False, indent=2)

def md_section(title, items, fmt):
    if not items: return f'### {title}\n\nNenhum problema encontrado. ✅\n'
    lines = [f'### {title} ({len(items)})\n']
    for it in items[:50]: lines.append(fmt(it))
    if len(items) > 50: lines.append(f'- ... e mais {len(items)-50} ocorrencias')
    return '\n'.join(lines) + '\n'

body = f"""## Relatorio de Inspecao — {TODAY}

Paginas inspecionadas: **{len(HTML)}**

Escopo: atributos HTML href/src, incluindo URLs absolutas do proprio dominio. Links externos inventariados: **{len(external)}**, sem verificacao HTTP. Fragmentos e links gerados por JavaScript nao foram validados. Execucao bem-sucedida significa relatorio gerado, nao ausencia de pendencias.

{md_section('Links internos quebrados', broken, lambda b: f"- `{b['page']}` → link `{b['link']}`")}

{md_section('Mencoes a anos anteriores — revisar contexto, sem presumir erro', outdated, lambda o: f"- `{o['page']}` menciona **{o['year']}**: \"...{o['context']}...\"")}

---
Gerado pelo **site-inspector**. Confirme cada destino e o contexto editorial antes de corrigir. O relatorio nao autoriza reescrever artigos nem trocar destinos por suposicao.
"""

def gh(method, path, payload=None):
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}{path}',
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github+json',
                 'Content-Type': 'application/json'}, method=method)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read() or b'{}')

if TOKEN and (broken or outdated):
    title = f'[Site Inspector] Relatorio {TODAY}'
    issues = gh('GET', '/issues?state=open&labels=site-inspection&per_page=5')
    existing = next((i for i in issues if i['title'].startswith('[Site Inspector]')), None)
    if existing:
        gh('PATCH', f"/issues/{existing['number']}", {'title': title, 'body': body})
        print('ISSUE ATUALIZADA:', existing['number'])
    else:
        i = gh('POST', '/issues', {'title': title, 'body': body, 'labels': ['site-inspection']})
        print('ISSUE CRIADA:', i['number'])
elif not (broken or outdated):
    print('TUDO OK - nenhum problema encontrado.')
else:
    print('SEM TOKEN - relatorio salvo em arquivo apenas.')
print(f"RESUMO: {len(HTML)} paginas | {len(broken)} links quebrados | {len(outdated)} mencoes desatualizadas")
