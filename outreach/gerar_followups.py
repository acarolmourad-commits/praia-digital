import os, datetime, csv

repo = r"C:\Users\Carolina\praia-digital"
csv_dir = os.path.join(repo, "csv-lotes-email")
doc_dir = os.path.join(repo, "docs", "sales")
now = datetime.date.today()
data_72h = (now + datetime.timedelta(days=3)).isoformat()
data_7d = (now + datetime.timedelta(days=7)).isoformat()

csv_path = os.path.join(csv_dir, "lote-envio-30-leads-2026-07-10.csv")
with open(csv_path, newline="", encoding="utf-8") as f:
    leads = list(csv.DictReader(f))

dor_cidades = {
    "Porto da Lua": "alta temporada",
    "Praia Grande": "familiares",
    "Costa Verde": "luxo",
    "Barra Norte": "turismo",
    "Centro Hist.": "comercial",
    "Litoral Norte": "veraneio",
    "Praia Sul": "familiares",
    "Brisa do Mar": "turismo",
    "Costa Dourada": "investimento",
    "Vila Mar": "comercial",
}

followups = []
for lead in leads:
    cidade = lead["cidade"]
    dor = dor_cidades.get(cidade, "vendas")
    body_72h = f"Olá {lead['nome']}, seguindo nosso contato sobre parceria em {cidade}. Quer testar gratuitamente as ferramentas de IA da Praia Digital por 15 dias? comercial@praia.digital"
    body_7d = f"Olá {lead['nome']}, case em {cidade}: cliente aumentou leads em 35% com IA. Quer replicar esse resultado? https://praia.digital"
    followups.append({
        "lead_id": lead["lead_id"],
        "nome": lead["nome"],
        "email": lead["email"],
        "cidade": cidade,
        "data_envio": now.isoformat(),
        "followup_72h_data": data_72h,
        "followup_72h_assunto": f"Follow-up: parceria Praia Digital — {cidade}",
        "followup_72h_corpo": body_72h,
        "followup_7d_data": data_7d,
        "followup_7d_assunto": f"Case de sucesso em {cidade} — Praia Digital",
        "followup_7d_corpo": body_7d,
    })

out_csv = os.path.join(csv_dir, f"followup-30-leads-{now.isoformat()}.csv")
fieldnames = ["lead_id","nome","email","cidade","data_envio","followup_72h_data","followup_72h_assunto","followup_72h_corpo","followup_7d_data","followup_7d_assunto","followup_7d_corpo"]
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(followups)

print(f"Follow-ups gerados: {out_csv}")
print(f"72h: {data_72h} | 7d: {data_7d}")
