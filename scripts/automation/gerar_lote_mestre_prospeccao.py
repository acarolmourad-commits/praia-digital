#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_DIR = BASE / "csv-lotes-email"
OUT = CSV_DIR / "lote-mestre-unificado-2026-07-10.csv"

FILES = [
    "batch-30-emails-2026-07-10.csv",
    "lote-consorcio-20-leads-20260709.csv",
    "lote-captacao-15leads-20260709.csv",
    "lote-envio-27-leads-2026-07-10.csv",
    "lote-envio-30-leads-2026-07-10.csv",
    "lote-envio-top5-2026-07-10.csv",
    "lote-agentes-turismo-temporada-2026-07-10.csv",
    "lote-proprietarios-luxo-20-leads-2026-07-10.csv",
]

FIELD_MAP_COMMON = {
    "nome": ["nome", "Nome", "NOME", "lead_id"],
    "email": ["email", "Email", "EMAIL", "E-mail", "e-mail"],
    "telefone": ["telefone", "Telefone", "TELEFONE", "WhatsApp", "whatsapp", "phone", "Phone"],
    "cidade": ["cidade", "Cidade", "CIDADE"],
    "assunto": ["assunto", "Assunto", "ASSUNTO"],
    "mensagem": ["mensagem", "Mensagem", "MENSSAGEM", "Menssagem", "corpo", "Corpo", "MensagemPersonalizada"],
    "origem": ["origem", "Origem", "ORIGEM"],
    "dia_envio": ["dia_envio", "DiaEnvio", "DataEnvio", "data_envio", "Data de Envio"],
    "followup_72h": ["followup_72h", "Followup72h", "follow-up 72h", "followup_72h", "Follow up 72h"],
    "followup_7d": ["followup_7d", "Followup7d", "follow-up 7d", "followup_7d", "Follow up 7d"],
    "call_15min": ["call_15min", "Call15min", "call_15min", "Call 15min", "call", "Call"],
}

def normalize(value):
    return str(value).strip().lower().replace("\n", " ").replace("\r", " ")

def find_value(row, possible_keys):
    for key in possible_keys:
        if key in row:
            return row[key]
        for actual in row.keys():
            if normalize(actual) == normalize(key):
                return row[actual]
    return ""

def map_row(row):
    mapped = {}
    for field, keys in FIELD_MAP_COMMON.items():
        mapped[field] = find_value(row, keys)
    return mapped

records = []
seen = set()
missing_count = 0

for fname in FILES:
    path = CSV_DIR / fname
    if not path.exists():
        continue
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapped = map_row(row)
                email = normalize(mapped.get("email", ""))
                if not email:
                    missing_count += 1
                    continue
                if email in seen:
                    continue
                seen.add(email)
                mapped["email"] = email
                mapped["origem"] = mapped.get("origem", "") or fname
                if not mapped.get("dia_envio"):
                    mapped["dia_envio"] = "2026-07-10"
                if not mapped.get("followup_72h"):
                    mapped["followup_72h"] = "2026-07-13"
                if not mapped.get("followup_7d"):
                    mapped["followup_7d"] = "2026-07-17"
                if not mapped.get("call_15min"):
                    mapped["call_15min"] = "Sim"
                records.append(mapped)
    except Exception as e:
        print(f"Erro em {fname}: {e}")

fields = ["nome", "email", "telefone", "cidade", "assunto", "mensagem", "origem", "dia_envio", "followup_72h", "followup_7d", "call_15min"]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for rec in records:
        writer.writerow({k: rec.get(k, "") for k in fields})

print(f"Lote mestre gerado: {OUT}")
print(f"Leads únicos: {len(records)}")
print(f"Registros sem e-mail ignorados: {missing_count}")
