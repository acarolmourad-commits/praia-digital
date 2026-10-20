import os, re, json, sys, html
sys.path.insert(0, 'tools/kb')
from kb_part1 import KB as K1
from kb_part2 import KB2
from kb_part3 import KB3
from kb_part4 import KB4
from kb_part5 import KB5

FAMS = {}
FAMS.update(K1)
VENDAS_EXTRA = KB2.pop('VENDAS_M')
FAMS['VENDAS']['modulos'] = (FAMS['VENDAS']['modulos'] + VENDAS_EXTRA)[:4]
FAMS.update(KB2); FAMS.update(KB3); FAMS.update(KB4); FAMS.update(KB5)
from editorial_corrections import apply_corrections
FAMS = apply_corrections(FAMS)

RULES = [
 (['financiamento'], 'FINANCIAMENTO'),
 (['flipping','investidor','investindo','patrimonio','rentabilidade','primeiro-imovel','comprar','casa-ou-apartamento','analise'], 'INVESTIMENTO'),
 (['locacao','temporada','airbnb','booking','pricelabs'], 'TEMPORADA'),
 (['captacao','prospeccao','networking'], 'CAPTACAO'),
 (['fechamento','negociacao','venda','vendas','funil','propostas','rotinas','recuperacao','especialista'], 'VENDAS'),
 (['atendimento','comunicacao','conflitos','emocional','pos-venda','lideranca','equipes'], 'ATENDIMENTO'),
 (['instagram','marketing','storytelling'], 'MARKETING'),
 (['ia-','crm','tecnologia','agentes','hermes','ptam'], 'TECNOLOGIA'),
 (['documentacao','avaliacao','visita','apresentacao'], 'DOCUMENTACAO'),
 (['tempo','produtividade','oratoria','planejamento'], 'PRODUTIVIDADE'),
]

def family_of(slug):
    for keys, fam in RULES:
        if any(k in slug for k in keys): return fam
    return 'VENDAS'

def display_name(slug, ipath):
    try:
        t = open(ipath, encoding='utf-8').read()
        m = re.search(r'<title>([^<]+)', t)
        if m: return m.group(1).split('—')[0].split('|')[0].strip()
    except Exception: pass
    return slug.replace('-', ' ').title()

def esc(s): return html.escape(s)

# Fail closed: require an explicit, reviewed curriculum for every course.
course_payload_path = 'tools/kb/course_content_by_slug.json'
if not os.path.isfile(course_payload_path):
    raise RuntimeError('Missing course-specific curricula. Family-wide rewriting is disabled.')
with open(course_payload_path, encoding='utf-8') as course_file:
    COURSE_CONTENT = json.load(course_file)
required_slugs = [s for s in os.listdir('education/cursos')
    if not s.startswith('_archive')
    and os.path.isdir(f'education/cursos/{s}/curso-completo')
    and os.path.isfile(f'education/cursos/{s}/index.html')]
missing = [s for s in required_slugs if s not in COURSE_CONTENT]
if missing:
    raise RuntimeError('Missing curricula: ' + ', '.join(sorted(missing)))
fingerprints = {}
for s in required_slugs:
    payload = COURSE_CONTENT[s]
    if not isinstance(payload, dict) or not payload.get('familia') or len(payload.get('modulos', [])) != 4:
        raise RuntimeError('Invalid curriculum structure: ' + s)
    for module in payload['modulos']:
        if not all(k in module for k in ('t', 'obj', 'aulas')) or not module['aulas']:
            raise RuntimeError('Incomplete module: ' + s)
        for lesson in module['aulas']:
            if not all(k in lesson for k in ('t', 'c', 'p')) or not lesson['c'].strip():
                raise RuntimeError('Incomplete lesson: ' + s)
    fingerprint = json.dumps(payload['modulos'], sort_keys=True, ensure_ascii=False)
    if fingerprint in fingerprints:
        raise RuntimeError('Duplicate curriculum: ' + fingerprints[fingerprint] + ' / ' + s)
    fingerprints[fingerprint] = s

report = {'rewritten': 0, 'catalog': 0, 'skipped': []}
catalog = []

for slug in sorted(os.listdir('education/cursos')):
    if slug.startswith('_archive'): report['skipped'].append(slug); continue
    base = f'education/cursos/{slug}'
    cdir = f'{base}/curso-completo'
    ipath = f'{base}/index.html'
    if not os.path.isdir(cdir) or not os.path.isfile(ipath):
        report['skipped'].append(slug); continue
    fam = COURSE_CONTENT[slug]
    nome = display_name(slug, ipath)
    mods = fam['modulos'][:4]
    sumario = [f'# Sumário do Curso: {nome}', '']
    for i, mod in enumerate(mods, 1):
        sumario.append(f"- Módulo {i}: {mod['t']}")
        lines = [f"# Módulo {i} — {mod['t']}", '', '## Objetivo do módulo', mod['obj'], '']
        for j, aula in enumerate(mod['aulas'], 1):
            lines.append(f"## Aula {i}.{j} — {aula['t']}")
            lines.append(aula['c'])
            lines.append('')
            lines.append('**Prática:**')
            for p in aula['p']:
                lines.append(f'- {p}')
            lines.append('')
        open(f'{cdir}/modulo-{i}.md', 'w', encoding='utf-8').write('\n'.join(lines))
    open(f'{cdir}/sumario.md', 'w', encoding='utf-8').write('\n'.join(sumario) + '\n')
    # Atualiza tabela de conteudo programatico no index.html com os nomes reais dos modulos
    t = open(ipath, encoding='utf-8').read()
    m = re.search(r'(<h2>Conteúdo programático</h2>\s*<table>).*?</table>', t, flags=re.S)
    if m:
        rows = ''.join(
            f"<tr><td>{i}</td><td><strong>{esc(mod['t'])}</strong></td><td>{'<br>'.join('• '+esc(a['t']) for a in mod['aulas'])}</td><td>{len(mod['aulas'])}</td></tr>"
            for i, mod in enumerate(mods, 1))
        table = m.group(1) + rows + '</table>'
        t = t[:m.start()] + table + t[t.index('</table>', m.start()) + len('</table>'):]
        open(ipath, 'w', encoding='utf-8').write(t)
    report['rewritten'] += 1
    # catalogo hotmart
    price_m = re.search(r'<div class="price"[^>]*>([^<]+)</div>', open(ipath, encoding='utf-8').read())
    desc_m = re.search(r'name="description" content="([^"]+)"', open(ipath, encoding='utf-8').read())
    catalog.append({
        'curso': nome,
        'familia': fam['familia'],
        'preco_atual': price_m.group(1) if price_m else '',
        'url_pagina_vendas': f'https://praia.digital/education/cursos/{slug}/index.html',
        'descricao': desc_m.group(1) if desc_m else '',
        'modulos': len(mods),
        'aulas': sum(len(mo['aulas']) for mo in mods),
    })

import csv
os.makedirs('docs', exist_ok=True)
with open('docs/hotmart-catalogo-cursos.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['curso','familia','preco_atual','url_pagina_vendas','descricao','modulos','aulas'])
    w.writeheader()
    w.writerows(catalog)
report['catalog'] = len(catalog)
print(json.dumps(report, ensure_ascii=False))

# trigger: rerun after kb_part4 fix
