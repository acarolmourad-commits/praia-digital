import json, re, os
from collections import Counter

with open('docs/editorial/REGISTRO_EDITORIAL.json','r',encoding='utf-8') as f:
    data=json.load(f)
canonical = data.get('sitemap_plan',{}).get('canonical_urls', [])
published = data.get('published_articles', [])
pub_urls = {a.get('canonical') or a.get('url') for a in published if isinstance(a, dict) and (a.get('canonical') or a.get('url'))}

backup_slugs = []
for fname in os.listdir('backup/meta-descriptions'):
    if not fname.endswith('.html'):
        continue
    s = fname.replace('.html','')
    s = re.sub(r'-\d{4}-\d{2}-\d{2}$','',s)
    s = re.sub(r'-lote-\d+-\d+$','',s)
    s = re.sub(r'-lote-\d+$','',s)
    s = re.sub(r'-\d+$','',s)
    backup_slugs.append(s)

def norm(u):
    u = u.replace('https://praia.digital','').replace('.html','')
    u = re.sub(r'-\d{4}-\d{2}-\d{2}$','',u)
    u = re.sub(r'-lote-\d+-\d+$','',u)
    u = re.sub(r'-lote-\d+$','',u)
    u = re.sub(r'-\d+$','',u)
    return u

pub_norm = {norm(u) for u in (list(pub_urls)+canonical)}
gaps = sorted({s for s in backup_slugs if s not in pub_norm})

blog = [g for g in gaps if g.startswith('blog/')]
bairros = [g for g in gaps if g.startswith('bairros/')]
cidades = [g for g in gaps if g.startswith('cidades/')]
docs = [g for g in gaps if g.startswith('docs/')]
education = [g for g in gaps if g.startswith('education/')]
dashboards = [g for g in gaps if g.startswith('dashboards/')]
imoveis = [g for g in gaps if g.startswith('imoveis/')]
servicos = [g for g in gaps if g.startswith('servicos/')]
outreach = [g for g in gaps if g.startswith('outreach/')]
anfitrioes = [g for g in gaps if g.startswith('anfitrioes/')]
exclusivos = [g for g in gaps if g.startswith('exclusivos/')]
others = [g for g in gaps if g not in blog+bairros+cidades+docs+education+dashboards+imoveis+servicos+outreach+anfitrioes+exclusivos]

print('total_gaps', len(gaps))
print('blog', len(blog))
print('bairros', len(bairros))
print('cidades', len(cidades))
print('docs', len(docs))
print('education', len(education))
print('dashboards', len(dashboards))
print('imoveis', len(imoveis))
print('servicos', len(servicos))
print('outreach', len(outreach))
print('anfitrioes', len(anfitrioes))
print('exclusivos', len(exclusivos))
print('others', len(others))

open('.audit/gaps_categorized.txt','w',encoding='utf-8').write(
    '[BLOG]\n' + '\n'.join(blog) +
    '\n\n[BAIRROS]\n' + '\n'.join(bairros) +
    '\n\n[CIDADES]\n' + '\n'.join(cidades) +
    '\n\n[DOCS]\n' + '\n'.join(docs) +
    '\n\n[EDUCATION]\n' + '\n'.join(education) +
    '\n\n[DASHBOARDS]\n' + '\n'.join(dashboards) +
    '\n\n[IMOVEIS]\n' + '\n'.join(imoveis) +
    '\n\n[SERVICOS]\n' + '\n'.join(servicos) +
    '\n\n[OUTREACH]\n' + '\n'.join(outreach) +
    '\n\n[ANFITRIOES]\n' + '\n'.join(anfitrioes) +
    '\n\n[EXCLUSIVOS]\n' + '\n'.join(exclusivos) +
    '\n\n[OTHERS]\n' + '\n'.join(others)
)
print('wrote .audit/gaps_categorized.txt')
