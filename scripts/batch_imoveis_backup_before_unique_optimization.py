#!/usr/bin/env python3
"""Gerador em lote de páginas de imóveis a partir do CSV."""
import csv
from pathlib import Path

BASE = Path(r'C:\Users\Carolina\praia-digital')
CSV = BASE / 'propriedades/cadastro-imoveis.csv'
OUT_DIR = BASE / 'imoveis'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def build_page(row):
    pid = row.get('id', '').strip()
    titulo = row.get('titulo', '').strip()
    cidade = row.get('cidade', 'Litoral Paulista').strip()
    tipo = row.get('tipo', 'Imóvel').strip()
    preco_raw = row.get('preco', '0').strip()
    try:
        preco_valor = int(float(preco_raw))
    except Exception:
        preco_valor = 0
    preco = f"R$ {preco_valor:,}".replace(',', '.')
    dormitorios = row.get('dormitorios', '').strip()
    area = row.get('area', '').strip()
    descricao = row.get('descricao', '').strip()
    bairro = titulo.split(' em ', 1)[1] if ' em ' in titulo else cidade
    diferenciais = row.get('diferenciais', 'Destaque no litoral paulista').strip()
    contato_nome = row.get('contato_nome', 'Praia Digital').strip()
    contato_whats = row.get('contato_whats', '').strip()
    vagas = row.get('vagas', '').strip()
    condominio_raw = row.get('condominio_rs', '0').strip()
    try:
        cond_valor = int(float(condominio_raw))
    except Exception:
        cond_valor = 0
    cond = f"R$ {cond_valor:,}".replace(',', '.') if cond_valor > 0 else 'Sem'

    whats_digits = ''.join(ch for ch in contato_whats if ch.isdigit())
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{tipo.title()} em {bairro}, {cidade} | Praia Digital</title>
<meta name="description" content="{tipo.title()} em {bairro}, {cidade}: {area}m², {dormitorios} dorm, {vagas} vaga(s). Destaques: {diferenciais}. Contato: {contato_nome}.">
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
<p class="badge">{tipo.title()}</p>
<h1>{tipo.title()} em {bairro}, {cidade}</h1>
<div class="price">{preco}</div>
<div class="details"><span>Área: {area}m²</span><span>Dorm.: {dormitorios}</span><span>Vagas: {vagas}</span><span>Cond.: {cond}</span></div>
<p>{descricao}</p>
<p><strong>Diferenciais:</strong> {diferenciais}</p>
{'<a class="cta" href="https://wa.me/' + whats_digits + '?text=Ol%C3%A1,%20tenho%20interesse%20no%20' + tipo + '%20em%20' + cidade.replace(' ', '%20') + '">WhatsApp</a>' if whats_digits else ''}
<a class="cta" href="mailto:comercial@praia.digital?subject=Interesse%20no%20{tipo}%20{bairro}">E-mail</a>
</div>
<footer>© Praia Digital - 2026 - IA para imóveis no litoral paulista</footer>
</div></body></html>"""

def main():
    with open(CSV, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    rows = sorted(rows, key=lambda r: r.get('id', '0'))
    existing = {p.stem for p in OUT_DIR.glob('imovel-*.html')}
    created = 0
    for row in rows:
        pid = row.get('id', '').strip()
        if not pid.isdigit():
            continue
        name = f'imovel-{pid}'
        if name in existing:
            continue
        page = build_page(row)
        (OUT_DIR / f'{name}.html').write_text(page, encoding='utf-8')
        created += 1
    print(f'CREATED {created} property pages')

if __name__ == '__main__':
    main()
