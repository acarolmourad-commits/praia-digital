"""relatorio_diario.py — relatorio B2B consolidado a partir do tracker-master.csv.

Uso:
    python scripts/pipeline/relatorio_diario.py
"""
import csv, os
from collections import Counter
from datetime import datetime

REPO = os.environ.get("PRAIA_REPO", "C:/Users/Carolina/praia-digital")
TRACKER = f"{REPO}/docs/sales/csv-lotes-b2b/tracker-master.csv"
SAIDA = f"{REPO}/docs/sales/relatorio-diario-automacao-{datetime.now():%Y-%m-%d}.html"

def run():
    if not os.path.exists(TRACKER):
        print("tracker-master.csv nao encontrado. Rode disparar_lote.py primeiro.")
        return
    with open(TRACKER, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    por_seg = Counter(r.get("segmento", "?") for r in rows)
    por_status = Counter(r.get("status", "?") for r in rows)
    linhas = "".join(f"<tr><td>{s}</td><td>{n}</td></tr>" for s, n in por_seg.most_common())
    stats = "".join(f"<tr><td>{s}</td><td>{n}</td></tr>" for s, n in por_status.most_common())
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>Relatorio B2B {datetime.now():%d/%m/%Y}</title>
<style>body{{font-family:Arial;margin:20px}}table{{border-collapse:collapse}}td,th{{border:1px solid #ccc;padding:6px}}</style>
</head><body>
<h1>Vendas B2B — {datetime.now():%d/%m/%Y}</h1>
<p>Total de leads no tracker: <strong>{len(rows)}</strong></p>
<h2>Por segmento</h2><table><tr><th>Segmento</th><th>Leads</th></tr>{linhas}</table>
<h2>Por status</h2><table><tr><th>Status</th><th>Leads</th></tr>{stats}</table>
</body></html>""")
    print(f"Relatorio gerado: {SAIDA}")

if __name__ == "__main__":
    run()
