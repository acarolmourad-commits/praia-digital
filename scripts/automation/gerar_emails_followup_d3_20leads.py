#!/usr/bin/env python3
"""
Gera e-mails de follow-up D3 personalizados para os 20 leads.
Saída: outreach/emails-followup-d3-20prontos-2026-07-11.html
"""
import csv, html as html_mod
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
CSV = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTPUT = BASE / "outreach/emails-followup-d3-20prontos-2026-07-11.html"
TODAY = datetime.now().strftime("%Y-%m-%d")

rows = list(csv.DictReader(CSV.open(encoding="utf-8", errors="ignore")))
rows.sort(key=lambda r: int(r.get("_score", "0") or 0), reverse=True)
lote = rows[:20]

cards = []
for r in lote:
    nome = r.get("pessoa_de_contato", "")
    empresa = r.get("nome_da_imobiliaria", "")
    cidade = r.get("cidade", "")
    email = r.get("email", "")
    assunto = f"Acompanhamento Praia Digital — {empresa} ({cidade})"
    corpo = f"""Olá, {nome}!

Estou acompanhando o envio que fizemos há 3 dias sobre o piloto de IA para imobiliárias do litoral.

Minha pergunta é direta: você quer seguir com o piloto gratuito?

Se sim, eu já envio o onboarding simplificado por e-mail ou WhatsApp, para você começar em até 48 horas.

Posso também enviar um case curto de uma imobiliária parceira do litoral que já está usando as ferramentas de IA.

Aguardo um ok para eu já adiantar o primeiro passo por aqui.

Atenciosamente,
CEO — Praia Digital
comercial@praia.digital | (11) 95434-6288
https://praia.digital
"""
    mailto = f"mailto:{html_mod.escape(email)}?subject={html_mod.escape(assunto)}&body={html_mod.escape(corpo).replace(chr(10), '%0A')}"
    cards.append(f'''
    <div class="card-lead">
      <strong>Lead {r['id']} — {html_mod.escape(empresa)}</strong>
      <div class="small">Contato: {html_mod.escape(nome)} | Cidade: {html_mod.escape(cidade)}</div>
      <div class="small">E-mail: {html_mod.escape(email)}</div>
      <a class="btn" href="{mailto}">Enviar e-mail</a>
    </div>
    ''')

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>E-mails D3 prontos — 20 leads — 2026-07-11</title>
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
    <h1>E-mails D3 prontos</h1>
    <p class="lead">20 e-mails personalizados com mailto. Clique em <strong>Enviar e-mail</strong> para abrir o cliente de e-mail pré-preenchido.</p>
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
print(f"Leads: {len(lote)}")
