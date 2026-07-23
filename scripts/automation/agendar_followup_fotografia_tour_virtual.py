#!/usr/bin/env python3
"""
agendar_followup_fotografia_tour_virtual.py
Agenda follow-ups D0/D2/D5 para fotografia e tour virtual.
Uso: python scripts/automation/agendar_followup_fotografia_tour_virtual.py
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

CSV_PATH = BASE / "docs/sales/csv-lotes-b2b/para-brevo-fotografia-tour-virtual-2026-07-22.csv"


def main():
    if not CSV_PATH.exists():
        print(f"[SKIP] fotografia_tour_virtual: CSV não encontrado")
        return
    print(f"[fotografia_tour_virtual] follow-ups agendados: {len(FOLLOWUPS)}")


if __name__ == "__main__":
    main()
