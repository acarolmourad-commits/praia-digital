import csv
from pathlib import Path

root = Path("C:/Users/Carolina/praia-digital")
source = root / "docs/sales/leads-priorizados-2026-07-12.csv"
out = root / "docs/sales/top-leads-prontas-2026-07-12.html"

if not source.exists():
    print("Arquivo de leads não encontrado.")
    raise SystemExit(1)

with source.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

rows.sort(key=lambda r: int(r.get("SCORE", "0")), reverse=True)
top = rows[:10]

html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Top leads prontas — Praia Digital</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#1f2937;line-height:1.6;padding:1.5rem}
.container{max-width:1100px;margin:0 auto}
h1{font-size:1.8rem;margin-bottom:.5rem;text-align:center}
table{width:100%;border-collapse:collapse;margin-top:1rem;background:#fff;border-radius:16px;overflow:hidden;border:1px solid #e5e7eb}
th,td{padding:.7rem;text-align:left;border-bottom:1px solid #e5e7eb;font-size:.95rem}
th{background:#f9fafb;font-weight:700}
tr:hover{background:#f8fafc}
a{color:#2563eb;text-decoration:none}
</style>
</head>
<body>
<div class="container">
<h1>Top leads prontas — contato rápido</h1>
<table>
<thead>
<tr><th>#</th><th>Nome</th><th>E-mail</th><th>WhatsApp</th><th>Cidade</th><th>Prioridade</th><th>Score</th><th>Ação</th></tr>
</thead>
<tbody>
"""

for i, row in enumerate(top, 1):
    nome = row.get("NOME", "—")
    email = row.get("EMAIL", "—")
    whatsapp = row.get("WHATSAPP", "—")
    cidade = row.get("CIDADE", "—")
    prioridade = row.get("PRIORIDADE", "—")
    score = row.get("SCORE", "—")
    link = row.get("LINK_EMAIL_PERSONALIZADO", "#")
    html += f"<tr><td>{i}</td><td>{nome}</td><td>{email}</td><td>{whatsapp}</td><td>{cidade}</td><td>{prioridade}</td><td>{score}</td><td><a href=\"{link}\">E-mail</a></td></tr>\n"

html += """
</tbody>
</table>
<p style="text-align:center;margin-top:1.5rem;font-size:.85rem;color:#6b7280">Gerado automaticamente a partir de docs/sales/leads-priorizados-2026-07-12.csv</p>
</div>
</body>
</html>"""

out.write_text(html, encoding="utf-8")
print(f"Top leads prontas gerado: {out}")
print(f"Total listado: {len(top)}")
