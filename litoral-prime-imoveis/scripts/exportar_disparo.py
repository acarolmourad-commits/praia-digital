"""
Litoral Prime — gera CSV para importação manual no WhatsApp/evolutivo.
Não envia nada automaticamente.
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "outreach" / "lote-001-sanitizado.csv"
OUTPUT = BASE / "outreach" / "lote-001-pronto-disparo.csv"


def wa_link(name: str, cidade: str, tipo: str):
    msg = f"Olá, {name}! Quer opções de {tipo.lower()} no litoral de SP?"
    number_fallback = "5511954346288"
    phone = "5511954346288"
    return f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"


def run():
    if not INPUT.exists():
        raise SystemExit("Sanitize antes de exportar para disparo.")
    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "nome", "telefone", "cidade_interesse", "tipo_interesse",
                "origem", "status", "whatsapp_link", "data_geracao"
            ],
        )
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "nome": r["nome"],
                    "telefone": r["telefone"],
                    "cidade_interesse": r["cidade_interesse"],
                    "tipo_interesse": r["tipo_interesse"],
                    "origem": r["origem"],
                    "status": r["status"],
                    "whatsapp_link": wa_link(r["nome"], r["cidade_interesse"], r["tipo_interesse"]),
                    "data_geracao": datetime.date.today().isoformat(),
                }
            )
    print(f"Exportado para disparo manual: {OUTPUT}")


if __name__ == "__main__":
    run()
