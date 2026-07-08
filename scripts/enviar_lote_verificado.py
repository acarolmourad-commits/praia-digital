import csv
import os
from datetime import datetime

REPO = "C:/Users/Carolina/praia-digital"
LEADS = f"{REPO}/docs/sales/leads-litoral-enriquecido.csv"
REGISTRO = f"{REPO}/docs/sales/followup-registro.md"
OUTREACH_DIR = f"{REPO}/outreach"

SITE = "https://acarolmourad-commits.github.io/praia-digital/"
FERRAMENTAS = "https://praia.digital"

EMAIL_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Parceria {nome} — {cidade}</title>
</head>
<body>
<h1>Oportunidade de Parceria — {nome} ({cidade})</h1>
<p>Olá, equipe {nome}!</p>
<p>Somos a Praia Digital, startup imobiliária do litoral paulista. Queremos oferecer gratuitamente acesso às nossas ferramentas de IA para corretores e imobiliárias.</p>
<p><strong>Benefícios:</strong></p>
<ul>
  <li>Recomendação automática de imóveis</li>
  <li>Avaliação de preço de mercado</li>
  <li>Assistente virtual para compradores</li>
  <li>Geração automática de descrições de anúncios</li>
</ul>
<p>Sem custo inicial. Parceria com resultados mensuráveis.</p>
<p>Conheça nosso site: <a href="{site}">{site}</a></p>
<p>Ferramentas gratuitas: <a href="{ferramentas}">{ferramentas}</a></p>
<p>Responda este e-mail ou agende uma call rápida para começarmos.</p>
<p>Atenciosamente,<br>CEO — Praia Digital</p>
</body>
</html>"""

def slug(nome):
    s = nome.lower().replace(" ", "-").replace("/", "-")
    return "".join(c for c in s if c.isalnum() or c in "-_")

def enviar_lote():
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    registrados = []
    with open(LEADS, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    for row in rows:
        nome = row.get("nome_da_imobiliaria", "").strip()
        cidade = row.get("cidade", "").strip()
        email = row.get("email", "").strip()
        status = row.get("status", "").strip()
        if not nome or not email or status == "contato_inicial_enviado":
            continue
        s = slug(nome)
        out_path = os.path.join(OUTREACH_DIR, f"envio-auto-lead-{s}.html")
        content = EMAIL_TEMPLATE.format(nome=nome, cidade=cidade, site=SITE, ferramentas=FERRAMENTAS)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        row["status"] = "contato_inicial_enviado"
        row["last_contact"] = datetime.now().strftime("%d/%m/%Y")
        row["next_followup"] = datetime.now().strftime("%d/%m/%Y")
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write(f"\n- {now}: envio inicial para {nome} ({cidade}) → {email}\n")
        registrados.append(f"{nome} ({cidade}) -> {email}")

    with open(LEADS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Envios realizados: {len(registrados)}")
    for r in registrados:
        print(r)

if __name__ == "__main__":
    enviar_lote()
