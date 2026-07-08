import csv, os

LEADS = "C:/Users/Carolina/praia-digital/docs/sales/leads-litoral-enriquecido.csv"
OUTREACH_DIR = "C:/Users/Carolina/praia-digital/outreach"
FOLLOWUP_DIR = "C:/Users/Carolina/praia-digital/outreach/followups"
OUT = "C:/Users/Carolina/praia-digital/docs/sales/dashboard-prospeccao.html"

leads = []
with open(LEADS, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nome = row.get("nome_da_imobiliaria","").strip()
        cidade = row.get("cidade","").strip()
        email = row.get("email","").strip()
        score = row.get("pontuacao_lead","").strip() or "0"
        if nome and email:
            leads.append({"nome":nome,"cidade":cidade,"email":email,"score":score})

existing = set(os.listdir(OUTREACH_DIR)) if os.path.isdir(OUTREACH_DIR) else set()
followups = set(os.listdir(FOLLOWUP_DIR)) if os.path.isdir(FOLLOWUP_DIR) else set()

def base_slug(nome):
    s = nome.lower().replace(" ","-").replace("/","-")
    return "".join(c for c in s if c.isalnum() or c in "-_")

def has_initial(lead):
    slug = base_slug(lead["nome"])
    return f"envio-auto-lead-{slug}.html" in existing

def has_followup(lead, days):
    slug = base_slug(lead["nome"])
    return f"followup-{days}-{slug}.html" in followups

rows = []
for lead in leads:
    ini = "Sim" if has_initial(lead) else "Não"
    fu3 = "Sim" if has_followup(lead,"3dias") else "Não"
    fu7 = "Sim" if has_followup(lead,"7dias") else "Não"
    btn = f"<a class='button' href='mailto:{lead['email']}?subject=Parceria%20Praia%20Digital&body=Ol%C3%A1%2C%20equipe%20{lead['nome'].replace(' ','%20')}%21'>Responder</a>"
    rows.append(f"<tr><td>{lead['nome']}</td><td>{lead['cidade']}</td><td>{lead['email']}</td><td>{lead['score']}</td><td>{ini}</td><td>{fu3}</td><td>{fu7}</td><td>{btn}</td></tr>")

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Dashboard Prospecção Praia Digital</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f7fa; color: #222; }}
h1 {{ color: #003366; }}
.stats {{ display:flex; gap:20px; margin-top:15px; }}
.card {{ background:#fff; border:1px solid #ddd; border-radius:8px; padding:15px 25px; box-shadow:0 2px 6px rgba(0,0,0,0.06); }}
table {{ width:100%; border-collapse: collapse; margin-top:20px; background:#fff; border:1px solid #ddd; }}
th, td {{ border:1px solid #ddd; padding:8px 10px; text-align:left; font-size:13px; }}
th {{ background:#003366; color:#fff; }}
tr:nth-child(even) {{ background:#fafafa; }}
a.button {{ background:#0066cc; color:#fff; padding:6px 12px; border-radius:4px; text-decoration:none; font-size:12px; }}
</style>
</head>
<body>
<h1>Dashboard de Prospecção — Praia Digital</h1>
<div class='stats'>
  <div class='card'><strong>Total leads</strong><br>{len(leads)}</div>
  <div class='card'><strong>Com e-mail inicial</strong><br>{sum(1 for r in leads if has_initial(r))}</div>
  <div class='card'><strong>Follow-up 3d</strong><br>{sum(1 for r in leads if has_followup(r,'3dias'))}</div>
  <div class='card'><strong>Follow-up 7d</strong><br>{sum(1 for r in leads if has_followup(r,'7dias'))}</div>
</div>
<table>
<tr><th>Nome</th><th>Cidade</th><th>E-mail</th><th>Score</th><th>Inicial</th><th>3d</th><th>7d</th><th>Ação</th></tr>
{''.join(rows)}
</table>
<p><small>Gerado automaticamente. Clique em Responder para abrir o e-mail de follow-up ou fechamento.</small></p>
</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Dashboard salvo em {OUT}")
