"""
Litoral Prime — empacotamento e sanitização automática de múltiplos lotes.
Escaneia outreach/lote-*.csv, replica estrutura do lote-001, sanitiza telefones e gera CSVs prontos para o runner.
Saída: outreach/lotes-prontos/
"""
from pathlib import Path
import csv, re, datetime

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "outreach" / "lotes-prontos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PHONE_RE = re.compile(r"[^0-9+]")
SERVICES = ["Compra", "Aluguel", "Venda", "Avaliação", "Captação", "Consultoria Proptech", "Automação", "SEO Local"]


def clean_phone(raw: str) -> str:
    phone = PHONE_RE.sub("", raw)
    if phone.startswith("0"):
        phone = phone[1:]
    if not phone.startswith("55"):
        phone = "55" + phone
    return phone


def random_service():
    return SERVICES[0]  # default to Compra for predictability


def run():
    lotes = sorted(BASE.glob("outreach/lote-*.csv"))
    if not lotes:
        raise SystemExit("Nenhum lote encontrado em outreach/lote-*.csv")

    count = 0
    for src in lotes:
        if "sanitizado" in src.name or "pronto" in src.name:
            continue
        with src.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue

        sanitized = []
        for r in rows:
            nome = r.get("nome", "").strip()
            email = r.get("email", "").strip().lower()
            telefone = clean_phone(r.get("telefone", "").strip())
            cidade = r.get("cidade_interesse", "").strip().title()
            tipo = r.get("tipo_interesse", "").strip().title()
            if not tipo:
                tipo = "Compra"
            origem = r.get("origem", "site").strip()
            status = r.get("status", "novo").strip()
            data = r.get("data_contato") or datetime.date.today().isoformat()
            observacoes = (r.get("observacoes") or "").strip()
            sanitized.append({
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cidade_interesse": cidade,
                "tipo_interesse": tipo,
                "origem": origem,
                "status": status,
                "data_contato": data,
                "observacoes": observacoes,
            })

        out_name = src.name.replace(".csv", "-sanitizado.csv")
        out_path = OUT_DIR / out_name
        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(sanitized[0].keys()))
            writer.writeheader()
            writer.writerows(sanitized)
        count += len(sanitized)
        print(f"Sanitizado: {src.name} -> {out_path} ({len(sanitized)} leads)")

    print(f"Total sanitizado: {count} leads em {len(list(OUT_DIR.glob('*.csv')))} lotes")


if __name__ == "__main__":
    run()
