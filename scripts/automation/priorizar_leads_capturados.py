import csv
from pathlib import Path
from datetime import date

root = Path("C:/Users/Carolina/praia-digital")
source = root / "docs/sales/parcerias-leads-capturados.csv"
out = root / "docs/sales/leads-priorizados-2026-07-12.csv"
out_format = root / "docs/sales/csv-lotes-email/lote-brevo-leads-capturados-2026-07-12.csv"

if not source.exists():
    print("Arquivo de leads não encontrado.")
    raise SystemExit(1)

score_map = {
    "Santos": 25,
    "Guarujá": 20,
    "Praia Grande": 20,
    "São Vicente": 15,
    "Bertioga": 15,
    "Outra": 5,
}

intent = [
    "parceria", "cliente", "venda", "recurso", "ferramenta", "ia", "seo", "automação", "leads", "imoveis", "imóveis", "agencia", "agência"
]
reject = ["revenda", "spam", "teste", "não", "sem", "fake"]

with source.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

scored = []
for row in rows:
    nome = (row.get("Seu nome") or "").strip().lower()
    empresa = (row.get("Nome da imobiliária") or "").strip().lower()
    email = (row.get("E-mail comercial") or "").strip()
    whatsapp = (row.get("WhatsApp") or "").strip()
    cidade = (row.get("Cidade") or "").strip()
    mensagem = (row.get("Mensagem") or "").strip().lower()
    timestamp = (row.get("Timestamp") or "").strip()

    if not email and not whatsapp:
        continue

    s = 0
    s += score_map.get(cidade, 0)
    s += 15 if any(k in mensagem for k in intent) else 0
    s += -20 if any(k in mensagem for k in reject) else 0
    s += 10 if whatsapp else 0
    s += 5 if email and "@" in email and "." in email.split("@")[-1] else 0
    s += 5 if len(empresa) > 2 else 0
    s += 5 if timestamp else 0

    p = "Alta" if s >= 40 else "Média" if s >= 20 else "Baixa"
    scored.append({
        "NOME": row.get("Seu nome") or row.get("Nome da imobiliária") or "",
        "EMAIL": email,
        "WHATSAPP": whatsapp,
        "CIDADE": cidade,
        "EMPRESA": row.get("Nome da imobiliária") or "",
        "ASSUNTO": f"Parceria — {cidade}",
        "LINK_EMAIL_PERSONALIZADO": f"mailto:{email}?subject=Parceria%20Praia%20Digital" if email else "",
        "ORIGEM": row.get("Origem") or "site",
        "INTERESSE": row.get("Mensagem") or "",
        "STATUS": "capturado",
        "PRIORIDADE": p,
        "SCORE": str(s),
    })

scored.sort(key=lambda x: int(x["SCORE"]), reverse=True)
fields = [
    "NOME", "EMAIL", "WHATSAPP", "CIDADE", "EMPRESA",
    "ASSUNTO", "LINK_EMAIL_PERSONALIZADO", "ORIGEM", "INTERESSE",
    "STATUS", "PRIORIDADE", "SCORE"
]

with out.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(scored)

with out_format.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(fields)
    for r in scored:
        w.writerow([r[k] for k in fields])

print(f"Leads priorizados: {len(scored)}")
print(f"Alta: {sum(1 for r in scored if r['PRIORIDADE']=='Alta')}")
print(f"Média: {sum(1 for r in scored if r['PRIORIDADE']=='Média')}")
print(f"Baixa: {sum(1 for r in scored if r['PRIORIDADE']=='Baixa')}")
print(f"Saída: {out}")
