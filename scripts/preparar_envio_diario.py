#!/usr/bin/env python3
"""Prepara o lote de envio diário a partir do CSV mestre, sem repetidos."""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
MASTER = BASE / 'csv-lotes-email' / 'lote-mestre-unificado-2026-07-10.csv'
OUT_DIR = BASE / 'csv-lotes-email'
OUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_DAILY = 15


def load_master(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def main():
    today = datetime.now().strftime('%Y-%m-%d')
    rows = load_master(MASTER)
    # dedupe by email/nome
    seen = set()
    unique = []
    for r in rows:
        key = (r.get('email', '').strip().lower(), r.get('nome', '').strip().lower())
        if not key[0]:
            continue
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    batch = unique[:MAX_DAILY]
    out_path = OUT_DIR / f'lote-diario-{today}.csv'
    if batch:
        with open(out_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(batch[0].keys()))
            writer.writeheader()
            writer.writerows(batch)
    print(f'DATE={today} | MASTER={len(rows)} | UNIQUE={len(unique)} | BATCH={len(batch)} | OUT={out_path}')


if __name__ == '__main__':
    main()
