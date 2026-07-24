"""
Litoral Prime — watcher simples para automação de novos lotes.
Monitora a pasta outreach/ por arquivos novos e sanitiza automaticamente.
Requisito: rode manualmente ou via cron.
"""
from pathlib import Path
import time, csv, datetime, re

BASE = Path(__file__).resolve().parent.parent
WATCH_DIR = BASE / "outreach"
OUT_DIR = BASE / "outreach" / "lotes-prontos"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED = BASE / "outreach" / ".processed"

PHONE_RE = re.compile(r"[^0-9+]")


def clean_phone(raw: str) -> str:
    phone = PHONE_RE.sub("", raw)
    if phone.startswith("0"):
        phone = phone[1:]
    if not phone.startswith("55"):
        phone = "55" + phone
    return phone


def already_processed(name: str) -> bool:
    if not PROCESSED.exists():
        return False
    return name in PROCESSED.read_text(encoding="utf-8").splitlines()


def mark_processed(name: str):
    with PROCESSED.open("a", encoding="utf-8") as f:
        f.write(name + "\n")


def sanitize_file(path: Path):
    if already_processed(path.name):
        return
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return
    sanitized = []
    for r in rows:
        nome = r.get("nome", "").strip()
        email = r.get("email", "").strip().lower()
        telefone = clean_phone(r.get("telefone", "").strip())
        cidade = r.get("cidade_interesse", "").strip().title()
        tipo = r.get("tipo_interesse", "").strip().title() or "Compra"
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
    out_path = OUT_DIR / path.name.replace(".csv", "-sanitizado.csv")
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(sanitized[0].keys()))
        writer.writeheader()
        writer.writerows(sanitized)
    mark_processed(path.name)
    print(f"Auto-sanitizado: {path.name} -> {out_path} ({len(sanitized)} leads)")


def run_once():
    for path in sorted(WATCH_DIR.glob("lote-*.csv")):
        if path.name.endswith("-sanitizado.csv"):
            continue
        sanitize_file(path)


if __name__ == "__main__":
    run_once()
