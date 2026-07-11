#!/usr/bin/env python3
"""
Gera plano sequencial de outreach WhatsApp de 30 dias.
Entrada: docs/sales/leads-litoral-enriquecido.csv
Saída: docs/sales/plano-sequencial-30-dias-whatsapp.md
"""
import csv, collections
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_FILE = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTPUT = BASE / "docs/sales/plano-sequencial-30-dias-whatsapp.md"

rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8", errors="ignore")))
alvos = [r for r in rows if r.get("whatsapp", "").strip()]
alvos.sort(key=lambda r: int(r.get("_score", 0) or 0), reverse=True)

LOTE = 100
DIAS = 30
cidades_ord = sorted({r.get("cidade", "") for r in alvos})

linhas = [
    "# Plano sequencial de outreach WhatsApp — 30 dias",
    "",
    f"- Data de início: {datetime.now().strftime('%Y-%m-%d')}",
    f"- Total de alvos: {len(alvos)}",
    f"- Lote por dia útil: {LOTE}",
    f"- Dias úteis no plano: {DIAS}",
    "",
    "## Distribuição",
    "",
]

# round-robin by city for variety
batches = []
for i in range(0, len(alvos), LOTE):
    batch = alvos[i:i+LOTE]
    batches.append(batch)

for idx, batch in enumerate(batches[:DIAS]):
    data = (datetime.now() + timedelta(days=idx)).strftime("%d/%m/%Y")
    cc = collections.Counter(r.get("cidade", "") for r in batch)
    distribuicao = ", ".join(f"{c}: {n}" for c, n in sorted(cc.items(), key=lambda x: -x[1]))
    linhas.append(f"### Dia {idx+1} — {data} — {len(batch)} leads")
    linhas.append(f"- Distribuição: {distribuicao}")
    linhas.append("- Leads:")
    for r in batch:
        linhas.append(f"  - Lead {r['id']} | {r['nome_da_imobiliaria']} | {r['pessoa_de_contato']} | {r['whatsapp']} | Score {r.get('_score','0')} | {r.get('status','')}")
    linhas.append("")

OUTPUT.write_text("\n".join(linhas), encoding="utf-8")
print(f"Plano: {OUTPUT}")
print(f"Lotes: {len(batches[:DIAS])}")
print("Distribuição por cidade:")
for c, n in sorted(collections.Counter(r.get("cidade","") for r in alvos).items(), key=lambda x: -x[1]):
    print(f"- {c}: {n}")
