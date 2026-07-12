import csv
from pathlib import Path

root = Path("C:/Users/Carolina/praia-digital")
source = root / "docs/sales/parcerias-leads-capturados.csv"
out = root / "docs/sales/csv-lotes-email/lote-brevo-leads-capturados-2026-07-12.csv"

if not source.exists():
    print("Arquivo de leads não encontrado.")
    raise SystemExit(1)

with source.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with out.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "NOME", "EMAIL", "WHATSAPP", "CIDADE", "EMPRESA",
        "ASSUNTO", "LINK_EMAIL_PERSONALIZADO", "ORIGEM", "INTERESSE", "STATUS"
    ])
    for row in rows:
        nome = row.get("Seu nome", "").strip()
        empresa = row.get("Nome da imobiliária", "").strip()
        email = row.get("E-mail comercial", "").strip()
        whatsapp = row.get("WhatsApp", "").strip()
        cidade = row.get("Cidade", "").strip()
        mensagem = row.get("Mensagem", "").strip()
        origem = row.get("Origem", "").strip()
        timestamp = row.get("Timestamp", "").strip()

        if not email and not whatsapp:
            continue

        subject = f"Parceria com Praia Digital — {empresa or 'imobiliária'} {cidade or ''}".strip()
        link_email = f"mailto:{email}?subject={subject.replace(' ', '%20')}" if email else ""
        status = "capturado"

        writer.writerow([
            nome or empresa,
            email,
            whatsapp,
            cidade,
            empresa,
            subject,
            link_email,
            origem,
            mensagem,
            status,
        ])

print(f"Processados {len(rows)} leads. CSV Brevo gerado em {out}")
