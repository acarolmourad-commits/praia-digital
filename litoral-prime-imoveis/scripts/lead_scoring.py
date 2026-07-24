"""
Litoral Prime — lead scoring automático: classifica leads por temperatura para priorizar dispatches.
Fatores:
  - tipo_interesse: venda/avaliação = ticket alto; compra/aluguel = busca ativa
  - cidade_interesse: Santos, Guarujá, PG, Bertioga = peso maior
  - origem: site = mais qualificado
Saída: outreach/do-dia/<data>/priorizados.csv
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent

HIGH_TICKET = {"venda", "avaliação", "consultoria proptech"}
HIGH_VALUE_CITIES = {"santos", "guarujá", "praia grande", "bertioga"}


def score_row(r: dict) -> int:
    score = 0
    tipo = (r.get("tipo_interesse", "") or "").strip().lower()
    cidade = (r.get("cidade_interesse", "") or "").strip().lower()
    origem = (r.get("origem", "") or "").strip().lower()
    if tipo in HIGH_TICKET:
        score += 30
    if cidade in HIGH_VALUE_CITIES:
        score += 20
    if origem == "site":
        score += 10
    if r.get("telefone"):
        score += 10
    if r.get("email"):
        score += 5
    return score


def run():
    today = datetime.date.today().isoformat()
    sanitized_dir = BASE / "outreach" / "lotes-prontos"
    out_dir = BASE / "outreach" / "do-dia" / today
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "priorizados.csv"

    candidates = sorted(sanitized_dir.glob("*-sanitizado.csv"), key=lambda p: p.stat().st_size, reverse=True)
    if not candidates:
        raise SystemExit("Nenhum lote sanitizado encontrado.")
    src = candidates[0]
    with src.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        r["score"] = score_row(r)
    rows.sort(key=lambda r: r["score"], reverse=True)

    fieldnames = list(rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Gerado: {out} ({len(rows)} leads priorizados)")


if __name__ == "__main__":
    run()
