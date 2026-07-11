#!/usr/bin/env python3
"""
Gera página de priorização dos leads a partir de docs/sales/leads-litoral-enriquecido.csv.
Saída: docs/sales/priorizacao-leads-120-praia-digital-2026.html
"""
import csv, html as html_mod
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_FILE = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTPUT = BASE / "docs/sales/priorizacao-leads-120-praia-digital-2026.html"

rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8", errors="ignore")))
rows.sort(key=lambda r: int(r.get("_score", 0)), reverse=True)

cards = []
for r in rows:
    lid = r.get("id", "")
    nome = r.get("nome_da_imobiliaria", "")
    cidade = r.get("cidade", "")
    email = r.get("email", "")
    contato = r.get("pessoa_de_contato", "")
    score = r.get("_score", "0")
    status = r.get("status", "")
    profile = r.get("perfil", "")
    cards.append(
        f'''
        <div class="card-lead">
          <strong>Lead {html_mod.escape(lid)} — {html_mod.escape(nome)}</strong>
          <div class="small">Contato: {html_mod.escape(contato)} | Score: {score}</div>
          <div class="small">Cidade: {html_mod.escape(cidade)} | Perfil: {html_mod.escape(profile)}</div>
          <div class="small">Status: {html_mod.escape(status)}</div>
          <a class="btn" href="mailto:{html_mod.escape(email)}">Enviar e-mail</a>
        </div>
        '''
    )

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Priorização de leads - Praia Digital</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Noto Sans"; background: #f7f9fb; color: #1f2937; }}
  .wrap {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
  .card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(17,24,39,0.06); }}
  h1 {{ font-size: 34px; letter-spacing: -0.5px; margin-bottom: 8px; }}
  .lead {{ color: #6b7280; margin-bottom: 20px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 18px; }}
  .card-lead {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; }}
  .card-lead strong {{ display: block; font-size: 16px; margin-bottom: 4px; }}
  .small {{ font-size: 13px; color: #6b7280; }}
  .btn {{ appearance: none; border: 0; background: #2563eb; color: white; padding: 10px 14px; border-radius: 10px; cursor: pointer; font-weight: 600; text-decoration: none; display: inline-block; margin-top: 10px; }}
  .btn:hover {{ background: #1d4ed8; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>Priorização de leads</h1>
    <p class="lead">Total de leads: {len(rows)}. Ordenados por score decrescente.</p>
  </div>
  <div class="grid">
    {''.join(cards)}
  </div>
</div>
</body>
</html>
'''

OUTPUT.write_text(html, encoding="utf-8")
print(f"Gerado: {OUTPUT}")
print(f"Leads: {len(rows)}")
print("Top 5:")
for r in rows[:5]:
    print(r["id"], r["nome_da_imobiliaria"], r["cidade"], r["_score"], r["status"])
