"""
Litoral Prime — valida preflight do CSV de pronto-disparo do dia.
Verifica colunas obrigatórias, duplicidade de telefone, campos vazios,
comprimento mínimo de número e alerta de formatação.
Uso: uv run python scripts/validar_pronto_disparo.py
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "outreach" / "do-dia" / datetime.date.today().isoformat() / "pronto-disparo.csv"
EXPECTED = {"nome","telefone","cidade_interesse","tipo_interesse","estagio","mensagem","whatsapp_link","data_acao"}


def validar(path: Path):
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("Arquivo vazio.")
        return

    errors = []
    warnings = []

    missing = EXPECTED - rows[0].keys()
    if missing:
        errors.append(f"Colunas ausentes: {sorted(missing)}")

    phones = []
    for idx, r in enumerate(rows, 1):
        if not (r.get("nome") or "").strip():
            errors.append(f"Linha {idx}: nome vazio")
        phone = (r.get("telefone") or "").strip()
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 12:
            errors.append(f"Linha {idx}: telefone curto: {phone}")
        if not phone:
            errors.append(f"Linha {idx}: telefone vazio")
        phones.append(digits)
        link = (r.get("whatsapp_link") or "").strip()
        if "wa.me/" not in link:
            warnings.append(f"Linha {idx}: link WhatsApp inválido")

    dups = sorted({p for p in phones if phones.count(p) > 1})
    if dups:
        errors.append(f"Telefones duplicados: {dups}")

    print(f"Arquivo: {path}")
    print(f"Linhas: {len(rows)}")
    if errors:
        print("ERROS:")
        for e in errors:
            print(" -", e)
    else:
        print("Nenhum erro.")
    if warnings:
        print("AVISOS:")
        for w in warnings:
            print(" -", w)


if __name__ == "__main__":
    validar(CSV)
