#!/usr/bin/env python3
"""
Atualiza docs/sales/leads-litoral-enriquecido.csv com status de envio.
Lê docs/sales/whatsapp-enviados-YYYY-MM-DD.csv e marca contato_inicial_enviado + data.
Gera docs/sales/leads-litoral-enriquecido-atualizado.csv
"""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
MASTER = BASE / "docs/sales/leads-litoral-enriquecido.csv"
TODAY = datetime.now().strftime("%Y-%m-%d")
SENT_CSV = BASE / f"docs/sales/whatsapp-enviados-{TODAY}.csv"
OUTPUT = BASE / "docs/sales/leads-litoral-enriquecido-atualizado.csv"

def load_csv(path: Path):
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8", errors="ignore")))

master = load_csv(MASTER)
sent = load_csv(SENT_CSV)
sent_ids = {r.get("id", "").strip() for r in sent if r.get("id", "").strip()}

updated = 0
for r in master:
    if r.get("id", "").strip() in sent_ids:
        if r.get("status", "") != "contato_inicial_enviado":
            r["status"] = "contato_inicial_enviado"
            r["last_contact"] = TODAY
            r["next_followup"] = (datetime.now() + __import__('datetime').timedelta(days=3)).strftime("%d/%m/%Y")
            updated += 1

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=master[0].keys())
    w.writeheader()
    w.writerows(master)

print(f"Atualizado: {OUTPUT}")
print(f"Leads marcados como enviados: {updated}")
print(f"Total na base: {len(master)}")
