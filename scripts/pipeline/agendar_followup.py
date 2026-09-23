"""agendar_followup.py — agenda follow-ups de qualquer segmento (substitui agendar_followup_*.py).

Uso:
    python scripts/pipeline/agendar_followup.py --segmento automacao --dias 3
"""
import argparse, csv, os
from datetime import datetime, timedelta

REPO = os.environ.get("PRAIA_REPO", "C:/Users/Carolina/praia-digital")
LOTES_DIR = f"{REPO}/docs/sales/csv-lotes-b2b"

def agendar(segmento: str, dias: int, data: str) -> int:
    sanitizado = f"{LOTES_DIR}/lote-b2b-{segmento}-sanitizado-{data}.csv"
    if not os.path.exists(sanitizado):
        print(f"[SKIP] {segmento}: sanitizado nao encontrado")
        return 0
    pares = f"{LOTES_DIR}/followup-pairs-{segmento}-{data}.csv"
    with open(sanitizado, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    agora = datetime.now()
    with open(pares, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["lead", "followup_em", "tipo"])
        for row in rows:
            nome = row.get("nome") or row.get("nome_da_imobiliaria", "")
            w.writerow([nome, (agora + timedelta(days=dias)).strftime("%Y-%m-%d"), f"fu{dias}d"])
    print(f"[{segmento}] follow-ups agendados: {len(rows)}")
    return len(rows)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--segmento", required=True)
    p.add_argument("--dias", type=int, default=3)
    p.add_argument("--data", default=datetime.now().strftime("%Y-%m-%d"))
    a = p.parse_args()
    agendar(a.segmento, a.dias, a.data)
