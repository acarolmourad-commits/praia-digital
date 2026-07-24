"""
Litoral Prime — sanitize do lote de leads para envio.
Entrada: outreach/lote-001-leads.csv
Saída: outreach/lote-001-sanitizado.csv
"""
from pathlib import Path
import csv, re, datetime

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "outreach" / "lote-001-leads.csv"
OUTPUT = BASE / "outreach" / "lote-001-sanitizado.csv"

PHONE_RE = re.compile(r"[^0-9+]")


def clean_phone(raw: str) -> str:
    phone = PHONE_RE.sub("", raw)
    if phone.startswith("0"):
        phone = phone[1:]
    if phone.startswith("55"):
        phone = phone
    else:
        phone = "55" + phone
    return phone


def sanitize(row: dict) -> dict:
    nome = row.get("nome", "").strip()
    email = row.get("email", "").strip().lower()
    telefone = clean_phone(row.get("telefone", "").strip())
    cidade = row.get("cidade_interesse", "").strip().title()
    tipo = row.get("tipo_interesse", "").strip().title()
    origem = row.get("origem", "site")
    status = row.get("status", "novo")
    data = row.get("data_contato") or datetime.date.today().isoformat()
    observacoes = (row.get("observacoes") or "").strip()
    return {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cidade_interesse": cidade,
        "tipo_interesse": tipo,
        "origem": origem,
        "status": status,
        "data_contato": data,
        "observacoes": observacoes,
    }


def run():
    if not INPUT.exists():
        raise SystemExit(f"Arquivo não encontrado: {INPUT}")
    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    sanitized = [sanitize(r) for r in rows]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(sanitized[0].keys()))
        writer.writeheader()
        writer.writerows(sanitized)
    print(f"Sanitizado: {len(sanitized)} registros -> {OUTPUT}")


if __name__ == "__main__":
    run()
