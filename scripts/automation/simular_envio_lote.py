#!/usr/bin/env python3
"""
simular_envio_lote.py
Simula envio de e-mail em lote e registra no tracker sem SMTP real.
Uso: python scripts/automation/simular_envio_lote.py --lote 35 --dry-run
"""

import csv
import argparse
import time
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[2]
TRACKER_CSV = BASE / "docs/sales/tracker_envios.csv"
LOG_CSV = BASE / "docs/sales/log_envios.csv"


def load_tracker(path):
    rows = []
    if not path.exists():
        return rows
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def save_tracker(path, rows):
    headers = [
        "nome",
        "email",
        "cidade",
        "imovel_url",
        "fonte",
        "data_captura",
        "status",
        "ultimo_contato",
        "proxima_acao",
        "observacoes",
        "lote",
        "ferramenta",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def append_log(path, rows):
    headers = [
        "data",
        "lead",
        "email",
        "cidade",
        "subject",
        "status",
        "lote",
        "observacoes",
    ]
    file_exists = path.exists() and path.stat().st_size > 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def simulate(lote, dry_run=True):
    tracker = load_tracker(TRACKER_CSV)
    log_rows = []
    updated = False

    for row in tracker:
        if row.get("lote") == str(lote) and row.get("status") == "novo":
            row["status"] = "simulado" if dry_run else "enviado"
            row["ultimo_contato"] = datetime.now().isoformat()
            row["proxima_acao"] = "follow-up 3 dias"
            log_rows.append(
                {
                    "data": datetime.now().isoformat(),
                    "lead": row.get("nome"),
                    "email": row.get("email"),
                    "cidade": row.get("cidade"),
                    "subject": f"Ferramentas gratuitas e parceria para imobiliária em {row.get('cidade')}",
                    "status": "simulado (dry-run)" if dry_run else "enviado",
                    "lote": str(lote),
                    "observacoes": "Simulacao automatica",
                }
            )
            updated = True

    if updated:
        save_tracker(TRACKER_CSV, tracker)
        append_log(LOG_CSV, log_rows)
        print(f"Simulação concluída para lote {lote}. {len(log_rows)} leads atualizados.")
    else:
        print(f"Nenhum lead novo encontrado no lote {lote}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lote", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    simulate(args.lote, args.dry_run)
