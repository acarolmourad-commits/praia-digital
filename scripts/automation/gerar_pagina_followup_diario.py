#!/usr/bin/env python3
"""
Gera a página operacional de follow-ups do dia a partir de docs/sales/followup-diario-YYYY-MM-DD.md.
Saída: docs/sales/followup-diario-operacional-YYYY-MM-DD.html
"""
import re, html as html_mod
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
TODAY = datetime.now().strftime("%Y-%m-%d")
MD_FILE = BASE / f"docs/sales/followup-diario-{TODAY}.md"
OUTPUT = BASE / f"docs/sales/followup-diario-operacional-{TODAY}.html"


def parse_followups(texto: str):
    followups = []
    blocks = re.findall(r"## Lead (\d+) — ([^(]+) \(([^)]+)\)(.*?)---", texto, re.S)
    for lead_id, nome, cidade, body in blocks:
        email_m = re.search(r"- E-mail: ([^\s]+)", body)
        email = email_m.group(1).strip() if email_m else ""
        followups.append({"lead_id": lead_id, "nome": nome.strip(), "cidade": cidade.strip(), "email": email})
    return followups


def gerar_html(followups):
    cards = "\n".join(
        f'''
        <div class="card-lead">
          <strong>Lead {f["lead_id"]} — {html_mod.escape(f["nome"])}</strong>
          <div class="small">{html_mod.escape(f["cidade"])}</div>
          <a class="btn" href="mailto:{html_mod.escape(f["email"])}?subject=Acompanhamento%20Praia%20Digital&body={html_mod.escape("Olá, tudo bem? Estou acompanhando nosso envio de há 3 dias.%0A%0A1) Quer seguir com o piloto gratuito?%0A2) Posso enviar o onboarding?%0A3) Agendamos uma demo de 15min.%0A%0AAguardo um ok.")}">Enviar e-mail</a>
        </div>
        '''
        for f in followups
    )

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Follow-ups do dia — {TODAY} - Praia Digital</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Noto Sans"; background: #f7f9fb; color: #1f2937; }}
  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 40px 20px; }}
  .card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(17,24,39,0.06); }}
  h1 {{ font-size: 34px; letter-spacing: -0.5px; margin-bottom: 8px; }}
  .lead {{ color: #6b7280; margin-bottom: 20px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 18px; }}
  .card-lead {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; }}
  .card-lead strong {{ display: block; font-size: 16px; margin-bottom: 4px; }}
  .small {{ font-size: 13px; color: #6b7280; }}
  .btn {{ appearance: none; border: 0; background: #2563eb; color: white; padding: 10px 14px; border-radius: 10px; cursor: pointer; font-weight: 600; text-decoration: none; display: inline-block; margin-top: 10px; }}
  .btn:hover {{ background: #1d4ed8; }}
  .count {{ font-size: 18px; font-weight: 700; color: #111827; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>Follow-ups do dia — {TODAY}</h1>
    <p class="lead">Total: <span class="count">{len(followups)}</span> follow-ups prontos para envio.</p>
  </div>
  <div class="grid">
    {cards}
  </div>
</div>
</body>
</html>
'''
    return html


def main():
    if not MD_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {MD_FILE}")
    texto = MD_FILE.read_text(encoding="utf-8", errors="ignore")
    followups = parse_followups(texto)
    OUTPUT.write_text(gerar_html(followups), encoding="utf-8")
    print(f"Gerado: {OUTPUT}")
    print(f"Follow-ups: {len(followups)}")


if __name__ == "__main__":
    main()
