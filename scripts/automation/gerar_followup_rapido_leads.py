import csv
from pathlib import Path
from datetime import date, datetime

root = Path("C:/Users/Carolina/praia-digital")
source = root / "docs/sales/parcerias-leads-capturados.csv"
followup_dir = root / "docs/sales/followup-rapido"
followup_dir.mkdir(parents=True, exist_ok=True)

if not source.exists():
    print("Arquivo de leads não encontrado.")
    raise SystemExit(1)

template_path = root / "docs/sales/template-followup-rapido-leads-2026-07-12.html"
if not template_path.exists():
    print("Template de follow-up não encontrado.")
    raise SystemExit(1)

template = template_path.read_text(encoding="utf-8")

with source.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

new_rows = []
followup_count = 0
today = date.today().isoformat()

for row in rows:
    if row.get("Follow-up rápido") == "sim":
        new_rows.append(row)
        continue

    nome = row.get("Seu nome", "").strip()
    empresa = row.get("Nome da imobiliária", "").strip()
    email = row.get("E-mail comercial", "").strip()
    whatsapp = row.get("WhatsApp", "").strip()
    cidade = row.get("Cidade", "").strip()
    mensagem = row.get("Mensagem", "").strip()
    timestamp = row.get("Timestamp", "").strip()
    origem = row.get("Origem", "").strip()

    if not email and not whatsapp:
        new_rows.append(row)
        continue

    followup_text = template.replace("[NOME]", nome or "Não informado")
    followup_text = followup_text.replace("[EMPRESA]", empresa or "Não informado")
    followup_text = followup_text.replace("[EMAIL]", email or "Não informado")
    followup_text = followup_text.replace("[WHATSAPP]", whatsapp or "Não informado")
    followup_text = followup_text.replace("[CIDADE]", cidade or "Não informado")
    followup_text = followup_text.replace("[INTERESSE]", mensagem or "Não informado")
    followup_text = followup_text.replace("[ORIGEM]", origem or "Site")
    followup_text = followup_text.replace("[TIMESTAMP]", timestamp or today)

    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"followup-rapido-{timestamp_file}.html"
    out_path = followup_dir / filename
    out_path.write_text(followup_text, encoding="utf-8")

    row["Follow-up rápido"] = "sim"
    new_rows.append(row)
    followup_count += 1

fieldnames = reader.fieldnames if 'reader' in locals() else list(rows[0].keys())
if "Follow-up rápido" not in fieldnames:
    fieldnames.append("Follow-up rápido")

with source.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

print(f"Follow-ups gerados: {followup_count}")
print(f"Atualizado: {source}")
print(f"Próximos passos: verificar {followup_dir} e enviar e-mails via Brevo.")
