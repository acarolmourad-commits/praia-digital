#!/usr/bin/env python3
import csv
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
MASTER = BASE / "csv-lotes-email" / "lote-mestre-unificado-2026-07-10.csv"
OUT = BASE / "csv-lotes-email" / "lote-brevo-30-2026-07-10.csv"

with open(MASTER, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

rows = rows[:30]

FIELDS = [
    "NOME",
    "EMAIL",
    "TELEFONE",
    "CIDADE",
    "ASSUNTO",
    "MENSAGEM",
    "REMETENTE",
    "RESPOSTA_PARA",
    "PREHEADER",
    "NOME_EMPRESA",
]

with open(OUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    for r in rows:
        writer.writerow({
            "NOME": r.get("nome", ""),
            "EMAIL": r.get("email", ""),
            "TELEFONE": r.get("telefone", ""),
            "CIDADE": r.get("cidade", ""),
            "ASSUNTO": r.get("assunto", "") or f"Proposta de parceria — {r.get('cidade','Litoral')}",
            "MENSAGEM": r.get("mensagem", ""),
            "REMETENTE": "Carolina Moura | CEO Praia Digital",
            "RESPOSTA_PARA": "comercial@praia.digital",
            "PREHEADER": "Parceria com ferramentas de IA e captação no litoral.",
            "NOME_EMPRESA": "Praia Digital",
        })

print(f"Gerado: {OUT}")
print(f"Linhas: {len(rows)}")
