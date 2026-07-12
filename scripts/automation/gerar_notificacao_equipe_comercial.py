import csv
from pathlib import Path
from datetime import date, datetime

root = Path("C:/Users/Carolina/praia-digital")
source = root / "docs/sales/parcerias-leads-capturados.csv"
notification_dir = root / "docs/sales/notificacao-equipe"
notification_dir.mkdir(parents=True, exist_ok=True)

if not source.exists():
    print("Arquivo de leads não encontrado.")
    raise SystemExit(1)

# Lê template de notificação
template_path = root / "docs/sales/template-notificacao-equipe-comercial-parceria.html"
if not template_path.exists():
    print("Template de notificação não encontrado.")
    raise SystemExit(1)

template = template_path.read_text(encoding="utf-8")

with source.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Filtra apenas leads não notificados
new_rows = []
notified_count = 0
today = date.today().isoformat()

for row in rows:
    if row.get("Notificado") == "sim":
        new_rows.append(row)
        continue

    empresa = row.get("Nome da imobiliária", "").strip()
    nome = row.get("Seu nome", "").strip()
    email = row.get("E-mail comercial", "").strip()
    whatsapp = row.get("WhatsApp", "").strip()
    cidade = row.get("Cidade", "").strip()
    mensagem = row.get("Mensagem", "").strip()
    timestamp = row.get("Timestamp", "").strip()
    origem = row.get("Origem", "").strip()

    if not empresa and not nome:
        new_rows.append(row)
        continue

    # Gera notificação
    notification_text = template.replace("[EMPRESA]", empresa or "Não informado")
    notification_text = notification_text.replace("[NOME]", nome or "Não informado")
    notification_text = notification_text.replace("[EMAIL]", email or "Não informado")
    notification_text = notification_text.replace("[WHATSAPP]", whatsapp or "Não informado")
    notification_text = notification_text.replace("[CIDADE]", cidade or "Não informado")
    notification_text = notification_text.replace("[MENSAGEM]", mensagem or "Não informado")
    notification_text = notification_text.replace("[TIMESTAMP]", timestamp or today)
    notification_text = notification_text.replace("[ORIGEM]", origem or "Site")

    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"notificacao-parceria-{timestamp_file}.html"
    out_path = notification_dir / filename
    out_path.write_text(notification_text, encoding="utf-8")

    # Marca como notificado
    row["Notificado"] = "sim"
    new_rows.append(row)
    notified_count += 1

# Atualiza CSV principal
fieldnames = reader.fieldnames if 'reader' in locals() else list(rows[0].keys())
if "Notificado" not in fieldnames:
    fieldnames.append("Notificado")

with source.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

print(f"Notificações geradas: {notified_count}")
print(f"Atualizado: {source}")
print(f"Próximos passos: verificar {notification_dir} e enviar e-mails via Brevo.")
