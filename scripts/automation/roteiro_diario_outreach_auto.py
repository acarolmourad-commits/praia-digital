#!/usr/bin/env python3
"""
Roteiro diário autônomo de outreach WhatsApp.
Passos:
  1. Gera lote do dia (100 leads) sem repetir contatos já enviados.
  2. Gera página operacional com botões de envio.
  3. Bloqueia reenvios cruzando tracker + CSVs de enviados.
  4. Atualiza docs/sales/followup-registro-limpo.md com data do lote.
  5. Gera relatório diário de outreach.
Saídas:
  - docs/sales/lote-whatsapp-YYYY-MM-DD.html
  - docs/sales/relatorio-outreach-diario-YYYY-MM-DD.md
"""
import csv, re, html as html_mod
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_LEADS = BASE / "docs/sales/leads-litoral-enriquecido.csv"
TRACKER = BASE / "docs/sales/followup-registro-limpo.md"
TODAY = datetime.now().strftime("%Y-%m-%d")
OUTPUT_LOTE = BASE / f"docs/sales/lote-whatsapp-{TODAY}.html"
OUTPUT_REPORT = BASE / f"docs/sales/relatorio-outreach-diario-{TODAY}.md"
SENT_CSVS = [
    BASE / "docs/sales/whatsapp-enviados-2026-07-11.csv",
    BASE / "docs/sales/lote-whatsapp-2026-07-11.csv",
]
MAX_DAILY = 100
TEMPLATE = ("Praia Digital: parceiro de IA para imobiliárias do litoral. "
            "Temos 4 ferramentas gratuitas + onboarding express. "
            "Quer que eu envie o passo a passo do piloto de 14 dias?")


def load_csv(path: Path):
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8", errors="ignore")))


def wa_link(phone, text):
    digits = "".join(ch for ch in phone if ch.isdigit())
    return f"https://wa.me/{digits}?text={html_mod.escape(text).replace('%20','+')}"


def main():
    rows = load_csv(CSV_LEADS)
    tracker_text = TRACKER.read_text(encoding="utf-8", errors="ignore") if TRACKER.exists() else ""

    contacted = set()
    for p in SENT_CSVS:
        if p.exists():
            for r in load_csv(p):
                if r.get("id", "").strip():
                    contacted.add(r["id"].strip())
    for r in rows:
        phone = r.get("whatsapp", "").strip()
        if phone and phone in tracker_text:
            contacted.add(r.get("id", "").strip())

    alvos = [r for r in rows if r.get("whatsapp", "").strip() and r.get("id", "").strip() not in contacted]
    alvos.sort(key=lambda r: int(r.get("_score", 0) or 0), reverse=True)
    lote = alvos[:MAX_DAILY]

    # HTML lote
    cards = "\n".join(
        f'''
        <div class="card-lead">
          <strong>Lead {html_mod.escape(r['id'])} — {html_mod.escape(r['nome_da_imobiliaria'])}</strong>
          <div class="small">Contato: {html_mod.escape(r['pessoa_de_contato'])} | Cidade: {html_mod.escape(r['cidade'])} | Score: {r.get('_score','0')}</div>
          <div class="small">WhatsApp: {html_mod.escape(r['whatsapp'])}</div>
          <div class="small">Status: {html_mod.escape(r.get('status',''))}</div>
          <a class="btn" href="{wa_link(r['whatsapp'], TEMPLATE)}" target="_blank" rel="noopener">Abrir conversa</a>
        </div>
        '''
        for r in lote
    )

    city_count = Counter(r.get("cidade", "") for r in lote)
    summary = ", ".join(f"{c}: {n}" for c, n in sorted(city_count.items(), key=lambda x: -x[1]))

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lote WhatsApp — {TODAY} - Praia Digital</title>
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
    <h1>Lote WhatsApp — {TODAY}</h1>
    <p class="lead">Total no lote: {len(lote)}. Distribuição por cidade: {summary}.</p>
    <p class="lead">Após enviar, marque no rastreador: outreach/whatsapp-rastrear-envios-2026-07-11.html</p>
  </div>
  <div class="grid">{cards}</div>
</div>
</body>
</html>
'''
    OUTPUT_LOTE.write_text(html, encoding="utf-8")

    # Relatório diário
    report_lines = [
        f"# Relatório de outreach diário — {TODAY}",
        "",
        f"- Lote gerado: {len(lote)}",
        f"- Leads já contactados/bloqueados: {len(contacted)}",
        f"- Disponíveis restantes: {len(alvos) - len(lote)}",
        "",
        "## Distribuição do lote",
    ]
    for c, n in sorted(city_count.items(), key=lambda x: -x[1]):
        report_lines.append(f"- {c}: {n}")
    report_lines += [
        "",
        "## Próximos passos",
        "- Enviar mensagens pelo lote",
        "- Marcar envios no rastreador",
        "- Rodar relatório de performance",
        "- Rodar plano de ação pós-envio",
        "",
        "## Arquivos gerados",
        f"- Lote: {OUTPUT_LOTE}",
        f"- Relatório: {OUTPUT_REPORT}",
    ]
    OUTPUT_REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Lote: {OUTPUT_LOTE} ({len(lote)} leads)")
    print(f"Relatório: {OUTPUT_REPORT}")
    print("Distribuição:")
    for c, n in sorted(city_count.items(), key=lambda x: -x[1]):
        print(f"- {c}: {n}")


if __name__ == "__main__":
    main()
