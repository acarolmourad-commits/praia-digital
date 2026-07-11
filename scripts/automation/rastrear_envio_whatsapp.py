#!/usr/bin/env python3
"""
Gera página de rastreamento de envio WhatsApp.
Usuário marca checkbox 'Enviado' e clica em salvar.
Saída: docs/sales/whatsapp-enviados-YYYY-MM-DD.csv
"""
import csv, html as html_mod, json
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_FILE = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTPUT = BASE / f"docs/sales/whatsapp-enviados-{datetime.now().strftime('%Y-%m-%d')}.csv"
HTML_OUTPUT = BASE / "outreach/whatsapp-rastrear-envios-2026-07-11.html"

TEMPLATE = ("Praia Digital: parceiro de IA para imobiliárias do litoral. "
            "Temos 4 ferramentas gratuitas + onboarding express. "
            "Quer que eu envie o passo a passo do piloto de 14 dias?")

rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8", errors="ignore")))
alvos = [r for r in rows if r.get("whatsapp", "").strip()]
alvos.sort(key=lambda r: int(r.get("_score", 0) or 0), reverse=True)

def wa_link(phone, text):
    digits = "".join(ch for ch in phone if ch.isdigit())
    return f"https://wa.me/{digits}?text={html_mod.escape(text).replace('%20','+')}"

cards = "\n".join(
    f'''
    <div class="card-lead" id="lead-{r['id']}">
      <strong>Lead {html_mod.escape(r['id'])} — {html_mod.escape(r['nome_da_imobiliaria'])}</strong>
      <div class="small">Contato: {html_mod.escape(r['pessoa_de_contato'])} | Cidade: {html_mod.escape(r['cidade'])} | Score: {r.get('_score','0')}</div>
      <div class="small">WhatsApp: {html_mod.escape(r['whatsapp'])}</div>
      <label class="check">
        <input type="checkbox" data-id="{r['id']}" onchange="toggleSent({r['id']})"> Enviado
      </label>
      <a class="btn" href="{wa_link(r['whatsapp'], TEMPLATE)}" target="_blank" rel="noopener">Abrir conversa</a>
    </div>
    '''
    for r in alvos
)

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rastrear envios WhatsApp - 2026-07-11 - Praia Digital</title>
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
  .check {{ display: inline-flex; align-items: center; gap: 8px; margin-top: 10px; color: #374151; }}
  .salvar {{ background: #16a34a; }}
  .salvar:hover {{ background: #15803d; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>Rastrear envios WhatsApp</h1>
    <p class="lead">Total: {len(alvos)} leads. Marque <strong>Enviado</strong> após cada envio e clique em Salvar CSV.</p>
    <button class="btn salvar" onclick="salvarCSV()">Salvar CSV</button>
  </div>
  <div class="grid">
    {cards}
  </div>
</div>
<script>
  const leadsData = JSON.parse('{json.dumps([{"id":r['id'], "nome":r['nome_da_imobiliaria'], "cidade":r['cidade'], "contato":r['pessoa_de_contato'], "whatsapp":r['whatsapp'], "score":r.get('_score','0'), "status":r.get('status','')} for r in alvos])}');
  function toggleSent(id) {{
    const div = document.getElementById('lead-'+id);
    if (div) div.style.borderColor = div.querySelector('input').checked ? '#16a34a' : '#e5e7eb';
  }}
  function salvarCSV() {{
    const sent = [];
    document.querySelectorAll('input[type=checkbox]:checked').forEach(cb => {{
      const id = cb.getAttribute('data-id');
      const item = leadsData.find(x => x.id === id);
      if (item) sent.push(item);
    }});
    const csv = 'id,nome,cidade,contato,whatsapp,score,status\\n' + sent.map(r => `${{r.id}},${{r.nome}},${{r.cidade}},${{r.contato}},${{r.whatsapp}},${{r.score}},${{r.status}}`).join('\\n');
    const blob = new Blob([csv], {{type: 'text/csv'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'whatsapp-enviados-{datetime.now().strftime('%Y-%m-%d')}.csv'; a.click();
  }}
</script>
</body>
</html>
'''

HTML_OUTPUT.write_text(html, encoding="utf-8")
print(f"HTML: {HTML_OUTPUT}")
print(f"CSV saída: {OUTPUT}")
print(f"Alvos: {len(alvos)}")
for r in alvos[:5]:
    print(r['id'], r['nome_da_imobiliaria'], r['whatsapp'])
