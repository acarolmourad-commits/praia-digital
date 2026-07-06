#!/usr/bin/env python3
"""Gerador de Dashboard do Corretor com métricas simuladas e relatório PDF."""
import csv, random, os
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(r'C:\Users\Carolina\praia-digital')
CSV = BASE / 'docs/sales/mail-merge.csv'
OUT = BASE / 'dashboards'
random.seed(123)

def make_dashboard(row):
    cid = row['id']
    name = row['nome_da_imobiliaria']
    city = row['cidade']
    views = random.randint(120, 1800)
    whats = random.randint(20, 220)
    leads = random.randint(10, 90)
    avg = random.randint(8, 90)
    days = 30
    pdf_name = f'relatorio-{cid}-{datetime.now().strftime("%m-%Y")}.pdf'
    items = []
    tipos = ['apartamento','casa','cobertura','studio','lote','comercial']
    bairros_extra = ['Gonzaga','Boqueirão','Aparecida','Ponta da Praia','Enseada','Pernambuco','Balneário','Vila Tupi','Centro','Real']
    for i in range(1,6):
        items.append({
            'rank': i,
            'tipo': random.choice(tipos),
            'bairro': random.choice(bairros_extra),
            'cidade': city,
            'views': random.randint(30, views-20),
            'cliques': random.randint(5, whats-5),
        })

    # PDF path placeholder link
    pdf_path = f'/dashboards/{cid}/{pdf_name}'

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard do Corretor - {name} | Praia Digital</title>
<meta name="description" content="Painel de desempenho de {name} em {city}.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📊</text></svg>">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#F4EBD0;color:#023047;line-height:1.6;padding:2rem}}
.container{{max-width:980px;margin:0 auto}}
.header{{background:#fff;padding:1.5rem;border-radius:16px;box-shadow:0 8px 28px rgba(0,0,0,.06);margin-bottom:1rem}}
.header h1{{font-size:1.6rem;margin-bottom:.4rem}}
.kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:1rem}}
.card{{background:#fff;padding:1.25rem;border-radius:14px;border:1px solid #e5e7eb}}
.card .label{{font-size:.8rem;color:#475569}}
.card .value{{font-size:1.6rem;font-weight:800;color:#0077B6}}
.rank{{background:#fff;padding:1.25rem;border-radius:14px;border:1px solid #e5e7eb;margin-bottom:1rem}}
.rank table{{width:100%;border-collapse:collapse;margin-top:.5rem}}
.rank th,.rank td{{text-align:left;padding:.5rem;border-bottom:1px solid #f1f5f9;font-size:.9rem}}
.rank th{{color:#64748b;font-weight:600}}
.cta{{display:inline-block;background:#00B4D8;color:#fff;padding:.75rem 1.5rem;border-radius:999px;text-decoration:none;font-weight:700;margin-top:1rem}}
footer{{background:#023047;color:#fff;text-align:center;padding:1rem;font-size:.85rem;opacity:.7;margin-top:2rem}}
a{{color:#0077B6}}
</style></head>
<body><div class="container">
<div class="header">
<h1>Dashboard do Corretor</h1>
<p>{name} — {city}</p>
<p>Periodo: ultimos {days} dias | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
</div>
<div class="kpi">
  <div class="card"><div class="label">Visualizacoes</div><div class="value">{views}</div></div>
  <div class="card"><div class="label">Cliques WhatsApp</div><div class="value">{whats}</div></div>
  <div class="card"><div class="label">Leads</div><div class="value">{leads}</div></div>
  <div class="card"><div class="label">Tempo medio contato</div><div class="value">{avg} min</div></div>
</div>
<div class="rank">
  <h2>Ranking dos imoveis mais procurados</h2>
  <table>
    <tr><th>#</th><th>Tipo</th><th>Bairro</th><th>Cidade</th><th>Views</th><th>Cliques</th></tr>
"""
    for it in items:
        html += f"<tr><td>{it['rank']}</td><td>{it['tipo']}</td><td>{it['bairro']}</td><td>{it['cidade']}</td><td>{it['views']}</td><td>{it['cliques']}</td></tr>\n"
    html += f"""</table>
  <a class="cta" href="{pdf_path}">Baixar relatorio mensal em PDF</a>
</div>
<footer>© Praia Digital - 2026 - IA para imoveis no litoral paulista</footer>
</div></body></html>"""
    return cid, name, html, pdf_path

def main():
    if not CSV.exists():
        print('Missing CSV:', CSV)
        return
    rows = list(csv.DictReader(CSV.open('r', encoding='utf-8')))
    rows = sorted(rows, key=lambda r: int(r['id']))
    created = []
    for row in rows:
        d = OUT / str(row['id'])
        d.mkdir(parents=True, exist_ok=True)
        cid, name, html, pdf_path = make_dashboard(row)
        (d / 'index.html').write_text(html, encoding='utf-8')
        # placeholder PDF manifest
        (d / f'relatorio-{cid}-{datetime.now().strftime("%m-%Y")}.pdf.txt').write_text(f'PDF placeholder for {name}', encoding='utf-8')
        created.append((row['id'], name))
    print('CREATED', len(created), 'dashboards')

if __name__ == '__main__':
    main()
