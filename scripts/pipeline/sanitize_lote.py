"""sanitize_lote.py — sanitiza lote B2B de qualquer segmento (substitui sanitize_lote_*.py).

Uso:
    python scripts/pipeline/sanitize_lote.py --segmento automacao
    python scripts/pipeline/sanitize_lote.py --segmento consultoria --data 2026-09-23

Substitui os 7 scripts sanitize_lote_<segmento>.py por um unico parametrizado.
"""
import argparse, csv, os, sys
from datetime import datetime

REPO = os.environ.get("PRAIA_REPO", "C:/Users/Carolina/praia-digital")
LOTES_DIR = f"{REPO}/docs/sales/csv-lotes-b2b"

def sanitize(segmento: str, data: str) -> int:
    entrada = f"{LOTES_DIR}/lote-b2b-{segmento}-{data}.csv"
    saida = f"{LOTES_DIR}/lote-b2b-{segmento}-sanitizado-{data}.csv"
    if not os.path.exists(entrada):
        print(f"[SKIP] {segmento}: lote de entrada nao encontrado: {entrada}")
        return 0
    with open(entrada, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []
    vistos, limpos = set(), []
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        whats = "".join(c for c in (row.get("whatsapp") or "") if c.isdigit())
        chave = email or whats
        if not chave or chave in vistos:
            continue
        vistos.add(chave)
        row["email"], row["whatsapp"] = email, whats
        row.setdefault("status", "pendente_msg1")
        limpos.append(row)
    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames or ["nome", "email", "whatsapp", "status"])
        w.writeheader(); w.writerows(limpos)
    print(f"Entrada: {entrada}\nSaida: {saida}\nLeads: {len(limpos)}\nDuplicatas bloqueadas: {len(rows)-len(limpos)}")
    return len(limpos)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--segmento", required=True)
    p.add_argument("--data", default=datetime.now().strftime("%Y-%m-%d"))
    a = p.parse_args()
    sys.exit(0 if sanitize(a.segmento, a.data) >= 0 else 1)
