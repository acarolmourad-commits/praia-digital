import re, csv
from pathlib import Path

ROOT = Path('C:/Users/Carolina/praia-digital')
OUT = ROOT / 'docs/editorial/auditoria-cluster-documentacao-2026-08-17.md'

KEYWORDS = ['documentacao','documentos','escritura','registro','financiamento','avaliacao','ptam','estrangeiro','heranca','inventario','certidao','compra','venda','locacao','temporada']
PATTERNS = [re.compile(k, re.I) for k in KEYWORDS]
EXCLUDE_DIRS = {'academy','backup','.git','node_modules','__pycache__','academy/cursos'}
INCLUDE_PREFIXES = ['blog/','assets/','education/','servicos','solucoes','anfitrioes','cases','cidades','bairros']

def classify(path: Path, content: str):
    text = content[:8000]
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return None
    rel = str(path.relative_to(ROOT)).replace('\\','/')
    if not any(rel.startswith(pre) for pre in INCLUDE_PREFIXES):
        return None
    if '/cursos/' in rel.lower() or '/academy/cursos/' in rel.lower():
        return None
    matches = [p.pattern for p in PATTERNS if p.search(text) or p.search(path.name)]
    if not matches:
        return None
    lower = f"{rel} {text}".lower()
    if any(p.pattern in lower for p in PATTERNS if p.pattern in ['documentacao','documentos','escritura','registro','certidao','financiamento']):
        if 'temporada' in lower:
            return 'DOC_TEMPORADA'
        return 'DOC_COMPRA_VENDA'
    if 'avaliacao' in lower or 'ptam' in lower:
        return 'AVALIACAO'
    if 'estrangeiro' in lower:
        return 'ESTRANGEIRO'
    if 'heranca' in lower or 'inventario' in lower:
        return 'HERANCA_INVENTARIO'
    if 'locacao' in lower or 'temporada' in lower or 'aluguel' in lower:
        return 'LOCACAO_TEMPORADA'
    if 'compra' in lower or 'venda' in lower:
        return 'COMPRA_VENDA'
    return 'RELACIONADO'

def read_head(path: Path, n=4000):
    try:
        with path.open('r', encoding='utf-8', errors='ignore') as f:
            return f.read(n)
    except Exception:
        return ''

def main():
    rows = []
    seen = set()
    for ext in ('*.html','*.md'):
        for p in ROOT.rglob(ext):
            rel = str(p.relative_to(ROOT)).replace('\\','/')
            if rel in seen:
                continue
            seen.add(rel)
            content = read_head(p)
            cat = classify(p, content)
            if not cat:
                continue
            title = re.search(r'<title[^>]*>(.*?)</title>', content, re.I|re.S)
            title = title.group(1).strip() if title else ''
            meta = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.I)
            meta = meta.group(1).strip() if meta else ''
            canonical = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content, re.I)
            canonical = canonical.group(1).strip() if canonical else ''
            rows.append({'path': rel, 'title': title, 'meta': meta, 'canonical': canonical, 'category': cat})
    csv_path = ROOT / 'docs/editorial/auditoria-cluster-documentacao-2026-08-17.csv'
    with csv_path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['path','title','meta','canonical','category'])
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    c = Counter(r['category'] for r in rows)
    lines = [
        '# Auditoria cluster documentação imobiliária','Data: 2026-08-17','',
        '## Escopo','- Documentação + financiamento + escritura + registro + avaliação/PTAM + estrangeiro + inventário/herança.','- `education/cursos`/`academy/cursos`/`backup`: fora do cluster; apenas como oportunidade de link interno.','- Não publicado/alterado/removido; somente diagnóstico.','',
        '## CSV', f'- {csv_path.relative_to(ROOT)}','',
        '## Totais por categoria'
    ]
    for k,v in sorted(c.items()):
        lines += [f'- {k}: {v}']
    lines += [
        '','## Critérios','- MANTER / ATUALIZAR / EXPANDIR / FUNDIR / NOVO GAP','- FUNDIR se títulos/meta quase idênticos e mesma intenção.','','## GSC','- Cruzar com `docs/seo/gsc-improvement-plan-2026-08-17.md` e checklist pós-D2.','','## Próximos passos','- Leitura amostral por categoria.','- Arquitetura definitiva + ordem de produção.',''
    ]
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print('report', OUT)
    print('csv', csv_path)
    print('rows', len(rows))

if __name__ == '__main__':
    main()
