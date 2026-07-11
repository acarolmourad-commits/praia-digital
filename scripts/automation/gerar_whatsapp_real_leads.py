#!/usr/bin/env python3
"""
Gera página de prospecção WhatsApp real a partir do CSV enriquecido.
Saída: outreach/enviar-whatsapp-real-2026-07-11.html
"""
import csv, html as html_mod
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_FILE = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTPUT = BASE / "outreach/enviar-whatsapp-real-2026-07-11.html"

TEMPLATE = ("Praia Digital: parceiro de IA para imobiliárias do litoral. "
            "Temos 4 ferramentas gratuitas + onboarding express. "
            "Quer que eu envie o passo a passo do piloto de 14 dias?")

rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8", errors="ignore")))
alvos = [r for r in rows if r.get("status","").lower() not in {"parceria_fechada","nao_interessado","cancelado"} and r.get("whatsapp","").strip()]
alvos.sort(key=lambda r: int(r.get("_score", 0)), reverse=True)

def wa_link(phone, text):
    return "https://wa.me/" + phone.replace("(","").replace(")","").replace(" ","").replace("-","") + "?text=" + text.replace(" ", "%20")

cards=[]
for r in alvos:
    lid=r.get("id","")
    nome=r.get("nome_da_imobiliaria","")
    contato=r.get("pessoa_de_contato","")
    cidade=r.get("cidade","")
    phone=r.get("whatsapp","").strip()
    txt=html_mod.escape(TEMPLATE)
    link=wa_link(phone, txt)
    cards.append(
        f'''
        <div class="card-lead">
          <strong>Lead {html_mod.escape(lid)} — {html_mod.escape(nome)}</strong>
          <div class="small">Contato: {html_mod.escape(contato)} | Cidade: {html_mod.escape(cidade)}</div>
          <div class="small">WhatsApp: {html_mod.escape(phone)}</div>
          <div class="small">Status: {html_mod.escape(r.get('status',''))}</div>
          <a class="btn" href="{link}" target="_blank" rel="noopener">Abrir conversa</a>
        </div>
        '''
    )

html=f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Enviar WhatsApp real - 2026-07-11 - Praia Digital</title>
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
    <h1>Enviar WhatsApp real</h1>
    <p class="lead">Total de alvos: {len(alvos)}. Clique em "Abrir conversa" para enviar a mensagem personalizada pelo WhatsApp.</p>
    <p class="lead">Se o número estiver incorreto, edite o campo WhatsApp no CSV e gere novamente.</p>
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
print(f"Alvos: {len(alvos)}")
