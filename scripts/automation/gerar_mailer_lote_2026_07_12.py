#!/usr/bin/env python3
"""
Gera outreach/mailer-lote-2026-07-12.html com 20 mailto prontos para o lote do dia.
"""
import re
from pathlib import Path
from html import escape

BASE = Path("C:/Users/Carolina/praia-digital")
LOTE_DIR = BASE / "docs/sales/lote-dia-2026-07-12"
OUTPUT = BASE / "outreach/mailer-lote-2026-07-12.html"

files = sorted(LOTE_DIR.glob("lote-2026-07-12-*.md"))

rows = []
for f in files:
    txt = f.read_text(encoding="utf-8", errors="ignore")
    to = re.search(r"\*\*Para:\*\*\s*(.+)", txt)
    subject = re.search(r"\*\*Assunto:\*\*\s*(.+)", txt)
    nome_match = re.search(r"Olá,\s*(.+)!", txt)
    lead_id = re.search(r"(\d{3})", f.stem)
    lead_id = lead_id.group(1) if lead_id else f.stem.split("-")[-1]
    to_addr = to.group(1).strip() if to else f"lead-{lead_id}@exemplo.com"
    subj = subject.group(1).strip() if subject else "Parceria Praia Digital"
    body = txt.split("---", 1)[1].strip() if "---" in txt else txt
    nome = nome_match.group(1).strip() if nome_match else "Contato"
    if "@" not in to_addr:
        continue
    body_enc = escape(body)
    mailto = f"mailto:{to_addr}?subject={escape(subj)}&body={body_enc}"
    rows.append((lead_id, nome, to_addr, subj, mailto))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
cards = "\n".join(
    f'''
    <div class="card">
      <h2>Lead {lead_id}</h2>
      <p><strong>Contato:</strong> {escape(nome)}</p>
      <p><strong>E-mail:</strong> {escape(to_addr)}</p>
      <p><strong>Assunto:</strong> {escape(subj)}</p>
      <a class="btn" href="{mailto}">Enviar e-mail</a>
    </div>
    '''
    for lead_id, nome, to_addr, subj, mailto in rows
)

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mailer Lote 2026-07-12 - Praia Digital</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Noto Sans"; background: #f7f9fb; color: #1f2937; }}
  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 40px 20px; }}
  .card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(17,24,39,0.06); }}
  h1 {{ font-size: 34px; letter-spacing: -0.5px; margin-bottom: 8px; }}
  h2 {{ font-size: 22px; margin: 24px 0 12px; color: #111827; }}
  .lead {{ color: #6b7280; margin-bottom: 20px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 18px; }}
  .btn {{ appearance: none; border: 0; background: #2563eb; color: white; padding: 12px 18px; border-radius: 12px; cursor: pointer; font-weight: 600; text-decoration: none; display: inline-block; }}
  .btn:hover {{ background: #1d4ed8; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>Mailer do lote — 2026-07-12</h1>
    <p class="lead">Clique em <strong>Enviar e-mail</strong> para abrir o cliente de e-mail pré-preenchido. Se alguns endereços estiverem ausentes, use o template em docs/sales/lote-dia-2026-07-12/.</p>
  </div>
  <div class="grid">
    {cards}
  </div>
</div>
</body>
</html>
'''

OUTPUT.write_text(html, encoding="utf-8")
print(f"Mailer gerado em: {OUTPUT}")
print(f"Total mailtos: {len(rows)}")
