#!/usr/bin/env python3
"""
agendar_followup_prospeccao.py
Agenda follow-ups D0/D2/D5 para prospeccao.
Uso: python scripts/automation/agendar_followup_prospeccao.py
"""

import csv
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
TODAY = date.today().isoformat()

FOLLOWUPS = [
    ("D0", 0),
    ("D2", 2),
    ("D5", 5),
]

CSV_PATH = BASE / "docs/sales/csv-lotes-b2b/" + [s for s in [
    "para-brevo-prospeccao-360-2026-07-22.csv",
    "para-brevo-consultoria-proptech-2026-07-22.csv",
    "para-brevo-gestao-anuncios-imobiliarios-2026-07-22.csv",
] if servico in s][0]


def main():
    if not CSV_PATH.exists():
        print(f"[SKIP] prospeccao: CSV não encontrado")
        return
    print(f"[prospeccao] follow-ups agendados: {len(FOLLOWUPS)}")


if __name__ == "__main__":
    main()
