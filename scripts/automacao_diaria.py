import csv, os
from datetime import datetime, timedelta

REPO = "C:/Users/Carolina/praia-digital"
LEADS = f"{REPO}/docs/sales/leads-litoral-enriquecido.csv"
REGISTRO = f"{REPO}/docs/sales/followup-registro.md"
RELATORIO = f"{REPO}/docs/sales/relatorio-diario.html"

def parse_date(s):
    try:
        return datetime.strptime(s.strip(), "%d/%m/%Y")
    except Exception:
        return None

def run():
    now = datetime.now()
    rows = []
    with open(LEADS, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    alerts = []
    followups_3d = []
    followups_7d = []
    interessados_sem_call = []

    for row in rows:
        nome = row.get("nome_da_imobiliaria","").strip()
        cidade = row.get("cidade","").strip()
        email = row.get("email","").strip()
        status = row.get("status","").strip() or "novo"
        last = parse_date(row.get("last_contact",""))
        if last is None:
            alerts.append(f"{nome} ({cidade}) — sem data de último contato")
            continue
        if (now - last).days >= 7 and status != "interessado":
            followups_7d.append((nome, cidade, email, (now - last).days))
        elif (now - last).days >= 3 and status != "interessado":
            followups_3d.append((nome, cidade, email, (now - last).days))
        if status == "interessado":
            interessados_sem_call.append((nome, cidade, email))

    # atualizar registro
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(f"\n- {now.strftime('%d/%m/%Y %H:%M')}: automação diária — {len(followups_3d)} fu3d, {len(followups_7d)} fu7d, {len(alerts)} alertas\n")

    # gerar relatório HTML
    linhas = []
    def table(title, items, cols):
        linhas.append(f"<h2>{title} ({len(items)})</h2>")
        if not items:
            linhas.append("<p>Nenhum item.</p>")
            return
        linhas.append("<table><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>")
        for it in items:
            linhas.append("<tr>" + "".join(f"<td>{v}</td>" for v in it) + "</tr>")
        linhas.append("</table>")

    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><title>Relatório Diário {now:%d/%m/%Y}</title>
<style>
body {{ font-family: Arial, sans-serif; margin:20px; background:#f5f7fa; color:#222; }}
h1 {{ color:#003366; }} h2 {{ color:#0066cc; }}
table {{ width:100%; border-collapse: collapse; margin:10px 0; background:#fff; border:1px solid #ddd; }}
th, td {{ border:1px solid #ddd; padding:8px 10px; text-align:left; font-size:13px; }}
th {{ background:#003366; color:#fff; }}
</style></head><body>
<h1>Relatório Diário — {now:%d/%m/%Y}</h1>
""")
        f.write(f"<p><strong>Total leads:</strong> {len(rows)}</p>")
        table("Follow-ups 3 dias pendentes", [(n,c,e,d) for n,c,e,d in followups_3d], ["Nome","Cidade","E-mail","Dias sem contato"])
        table("Follow-ups 7 dias pendentes", [(n,c,e,d) for n,c,e,d in followups_7d], ["Nome","Cidade","E-mail","Dias sem contato"])
        table("Interessados sem call agendada", [(n,c,e) for n,c,e in interessados_sem_call], ["Nome","Cidade","E-mail"])
        table("Alertas", [(a,) for a in alerts], ["Alerta"])
        f.write("<p><small>Gerado automaticamente por automacao_diaria.py — CEO Praia Digital</small></p></body></html>")
    print(f"Relatório diário gerado: {RELATORIO}")
    print(f"Follow-ups 3d: {len(followups_3d)}, 7d: {len(followups_7d)}, alertas: {len(alerts)}")

if __name__ == "__main__":
    run()
