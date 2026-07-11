#!/usr/bin/env python3
"""
Bloqueia reenvio para leads já contactados no WhatsApp.
Entrada: leads-litoral-enriquecido.csv
Fontes de bloqueio:
  - docs/sales/followup-registro-limpo.md
  - docs/sales/whatsapp-enviados-YYYY-MM-DD.csv
  - docs/sales/lote-whatsapp-YYYY-MM-DD.csv
Saída: docs/sales/leads-whatsapp-nao-enviados-YYYY-MM-DD.csv
"""
import csv, re
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_LEADS = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTPUT = BASE / f"docs/sales/leads-whatsapp-nao-enviados-{datetime.now().strftime('%Y-%m-%d')}.csv"
TODAY = datetime.now().strftime("%Y-%m-%d")

today_csv = BASE / f"docs/sales/whatsapp-enviados-{TODAY}.csv"
sent_csvs = [
    BASE / "docs/sales/lote-whatsapp-2026-07-11.csv",
    today_csv,
]

tracker = BASE / "docs/sales/followup-registro-limpo.md"
tracker_text = tracker.read_text(encoding="utf-8", errors="ignore") if tracker.exists() else ""

rows = list(csv.DictReader(CSV_LEADS.open(encoding="utf-8", errors="ignore")))

contacted = set()
for csv_path in sent_csvs:
    if csv_path.exists():
        with csv_path.open(encoding="utf-8", errors="ignore") as f:
            contacted.update(r.get("id", "").strip() for r in csv.DictReader(f) if r.get("id"))

for row in rows:
    phone = row.get("whatsapp", "").strip()
    if phone and phone in tracker_text:
        contacted.add(row.get("id", "").strip())

blocked = [r for r in rows if r.get("id", "").strip() in contacted]
allowed = [r for r in rows if r.get("id", "").strip() not in contacted]

# Output allowed leads for today's batch
with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(allowed)

report = f"""# Bloqueio de reenvio WhatsApp — {TODAY}

- Leads totais: {len(rows)}
- Já contactados/bloqueados: {len(blocked)}
- Disponíveis para envio: {len(allowed)}

## Motivos de bloqueio
- Presentes em docs/sales/followup-registro-limpo.md
- Presentes em CSVs de enviados do dia
"""

if blocked:
    report += "\n## Leads bloqueados\n"
    report += "| ID | Imobiliária | Cidade | WhatsApp |\n|------|---------|---------|---------|\n"
    for r in blocked[:50]:
        report += f"| {r['id']} | {r['nome_da_imobiliaria']} | {r['cidade']} | {r['whatsapp']} |\n"

report += f"\nSaída: {OUTPUT}\n"
Path(f"docs/sales/relatorio-bloqueio-{TODAY}.md").write_text(report, encoding="utf-8")
print(f"Total: {len(rows)} | Bloqueados: {len(blocked)} | Disponíveis: {len(allowed)}")
print(f"CSV disponíveis: {OUTPUT}")
print(f"Relatório: docs/sales/relatorio-bloqueio-{TODAY}.md")
