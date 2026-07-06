#!/usr/bin/env python3
"""Gerador em lote de páginas de imóveis a partir do CSV."""
import csv
from pathlib import Path

BASE = Path(r'C:\Users\Carolina\praia-digital')
CSV = BASE / 'propriedades/cadastro-imoveis.csv'
OUT_DIR = BASE / 'imoveis'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def build_page(row):
    pid=row['id']
    tipo=row['tipo']
    cidade=row['cidade']
    bairro=row['bairro']
    preco=f"R$ {int(row['preco_rs']):,}".replace(',','.')
    cond=f"R$ {int(row['condominio_rs']):,}".replace(',','.') if int(row['condominio_rs'])>0 else 'Sem'
    diff=row['diferenciais']
    contato=row['contato_nome']
    whats=row['contato_whats']
    desc=row['descricao_curta']
    area=row['area_m2']
    dorm=row['dormitorios']
    vagas=row['vagas']
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{tipo.title()} em {bairro}, {cidade} - {diff.split(',')[0].strip()} | Praia Digital</title>
<meta name="description" content="{tipo.title()} em {bairro}, {cidade}: {area}m2, {dorm} dorm, {vagas} vaga(s). Destaques: {diff}. Contato: {contato}.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏠</text></svg>">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#F4EBD0;color:#023047;line-height:1.6;padding:2rem}}
.container{{max-width:920px;margin:0 auto}}
.card{{background:#fff;padding:1.75rem;border-radius:16px;box-shadow:0 8px 28px rgba(0,0,0,.06);margin-bottom:1rem}}
.card h1{{font-size:1.6rem;margin-bottom:.6rem}}.price{{font-size:1.5rem;font-weight:800;color:#0077B6;margin-bottom:.5rem}}
.details{{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:.75rem;font-weight:600}}
.badge{{background:#0077B6;color:#fff;padding:.25rem .6rem;border-radius:50px;font-size:.75rem;font-weight:700}}
.cta{{display:inline-block;background:#00B4D8;color:#fff;padding:.75rem 1.5rem;border-radius:999px;text-decoration:none;font-weight:700;margin-top:.75rem}}
footer{{background:#023047;color:#fff;text-align:center;padding:1rem;font-size:.85rem;opacity:.7;margin-top:2rem}}
a{{color:#0077B6}}
</style></head>
<body><div class="container">
<div class="card">
<p class="badge">{row['status'].title()}</p>
<h1>{tipo.title()} em {bairro}, {cidade}</h1>
<div class="price">{preco}</div>
<div class="details"><span>Area: {area}m2</span><span>Dorm: {dorm}</span><span>Vagas: {vagas}</span><span>Cond.: {cond}</span></div>
<p>{desc}</p>
<p><strong>Diferenciais:</strong> {diff}</p>
<a class="cta" href="https://wa.me/{''.join([c for c in whats if c.isdigit()])}?text=Ola, tenho interesse no {tipo} em {bairro}">WhatsApp</a>
<a class="cta" href="mailto:comercial@praia.digital?subject=Interesse no {tipo} {bairro}">E-mail</a>
</div>
<footer>© Praia Digital - 2026 - IA para imoveis no litoral paulista</footer>
</div></body></html>"""

def main():
    with open(CSV, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    rows = sorted(rows, key=lambda r: int(r['id']))
    existing = {p.stem for p in OUT_DIR.glob('imovel-*.html')}
    created = 0
    for row in rows:
        pid = row['id']
        if f'imovel-{pid}' in existing:
            continue
        (OUT_DIR / f'imovel-{pid}.html').write_text(build_page(row), encoding='utf-8')
        created += 1
    print(f'CREATED {created} property pages')

if __name__ == '__main__':
    main()
