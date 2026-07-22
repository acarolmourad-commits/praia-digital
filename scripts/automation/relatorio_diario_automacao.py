#!/usr/bin/env python3
"""
relatorio_diario_automacao.py
Gera relatório diário do lote de automação para imobiliárias.
Uso: python scripts/automation/relatorio_diario_automacao.py
"""

from collections import Counter
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
TRACKER = BASE / "docs/sales/csv-lotes-b2b/tracker-automacao-2026-07-22.csv"
FOLLOWUPS = BASE / "docs/sales/csv-lotes-b2b/followup-pairs-automacao-2026-07-22.csv"
SAIDA = BASE / "docs/sales/relatorio-diario-automacao-2026-07-22.html"


def esc(v):
    return str(v or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def main():
    tracker_rows = []
    if TRACKER.exists():
        import csv
        with TRACKER.open(newline="", encoding="utf-8") as f:
            tracker_rows.extend(csv.DictReader(f, delimiter=";"))
    followup_rows = []
    if FOLLOWUPS.exists():
        import csv
        with FOLLOWUPS.open(newline="", encoding="utf-8") as f:
            followup_rows.extend(csv.DictReader(f, delimiter=";"))

    status_count = Counter(r.get("status", "") for r in tracker_rows)
    followup_map = {r.get("id"): r for r in followup_rows}

    linhas = ""
    for r in tracker_rows:
        ident = r.get("id", "")
        fu = followup_map.get(ident, {})
        linhas += f"""
      <tr>
        <td>{esc(r.get('nome',''))}</td>
        <td>{esc(r.get('imobiliaria',''))}</td>
        <td>{esc(r.get('cidade',''))}</td>
        <td>{esc(r.get('telefone',''))}</td>
        <td>{esc(r.get('status',''))}</td>
        <td>{esc(fu.get('q1_em',''))}</td>
        <td>{esc(fu.get('q2_em',''))}</td>
        <td>{esc(fu.get('q3_em',''))}</td>
      </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório Diário — Automação Imobiliárias</title>
<style>
  body{{font-family:Arial,sans-serif;max-width:1100px;margin:auto;padding:18px;color:#112}}
  .card{{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:14px;margin:14px 0}}
  table{{width:100%;border-collapse:collapse;font-size:12px;margin-top:10px}}
  th{{background:#eef2ff;color:#0a58ca;text-align:left;padding:8px;border-bottom:1px solid #e5e7eb}}
  td{{padding:8px;border-bottom:1px solid #f1f5f9}}
  .kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-top:10px}}
  .kpi{{background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:10px;text-align:center}}
  .kpi strong{{display:block;font-size:18px;color:#0a58ca}}
  .muted{{color:#64748b;font-size:12px}}
</style>
</head>
<body>
  <div class="card">
    <h1>Relatório Diário — Automação para Imobiliárias</h1>
    <p class="muted">Data: {date.today().isoformat()}</p>
    <div class="kpis">
      <div class="kpi"><strong>{len(tracker_rows)}</strong><span class="muted">Leads</span></div>
      <div class="kpi"><strong>{status_count.get('pendente_q1',0)}</strong><span class="muted">Pendentes Q1</span></div>
      <div class="kpi"><strong>{status_count.get('respondido',0)}</strong><span class="muted">Respondidos</span></div>
      <div class="kpi"><strong>{status_count.get('fechado',0)}</strong><span class="muted">Fechados</span></div>
    </div>
  </div>
  <div class="card">
    <h2 style="font-size:14px;font-weight:800;margin-bottom:8px">Status dos leads</h2>
    <table>
      <tr>
        <th>Nome</th><th>Imobiliária</th><th>Cidade</th><th>Telefone</th>
        <th>Status</th><th>Q1</th><th>Q2</th><th>Q3</th>
      </tr>
      {linhas}
    </table>
    <p class="muted" style="margin-top:10px">Arquivos: tracker-automacao-2026-07-22.csv | followup-pairs-automacao-2026-07-22.csv</p>
  </div>
</body>
</html>
"""
    SAIDA.write_text(html, encoding="utf-8")
    print(f"Relatório gerado: {SAIDA}")
    print("Status:")
    for k, v in status_count.most_common():
        print(f" - {k or 'vazio'}: {v}")


if __name__ == "__main__":
    main()
