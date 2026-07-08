import csv
import os
from datetime import datetime, timedelta

LEADS_CSV = "docs/sales/leads-litoral-enriquecido.csv"
OUT_DIR = "outreach"
FOLLOWUP_DIR = "outreach/followups"
ROTEIRO = "docs/sales/roteiro-execucao-atual.md"

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

FOLLOWUP_3D = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Follow-up 3 dias — {nome}</title>
</head>
<body>
<h1>Follow-up 3 dias — {nome}</h1>
<p>Olá! Passando para saber se teve chance de ver nossa proposta de parceria.</p>
<p>Podemos agendar 15min esta semana para apresentar as ferramentas na prática.</p>
<p>Atenciosamente,<br>CEO — Praia Digital</p>
</body>
</html>"""

FOLLOWUP_7D = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Follow-up 7 dias — {nome}</title>
</head>
<body>
<h1>Follow-up 7 dias — {nome}</h1>
<p>Olá! Última oportunidade esta semana.</p>
<p>Se fizer sentido para {nome}, responda este e-mail com 2 horários para uma call curta.</p>
<p>Atenciosamente,<br>CEO — Praia Digital</p>
</body>
</html>"""

def gerar():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FOLLOWUP_DIR, exist_ok=True)
    roteiro_linhas = ["# Roteiro de Execução — Prossecução Automática\n", f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"]
    count = 0
    with open(LEADS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("Colunas:", reader.fieldnames)
        for row in reader:
            nome = row.get("nome_da_imobiliaria", "").strip()
            cidade = row.get("cidade", "").strip()
            email = row.get("email", "").strip()
            if not nome or not email:
                continue
            slug = nome.lower().replace(" ", "-").replace("/", "-")
            safe = "".join(c for c in slug if c.isalnum() or c in "-_")
            initial_path = os.path.join(OUT_DIR, f"envio-auto-lead-{safe}.html")
            followup3_path = os.path.join(FOLLOWUP_DIR, f"followup-3dias-{safe}.html")
            followup7_path = os.path.join(FOLLOWUP_DIR, f"followup-7dias-{safe}.html")
            data_envio = datetime.now().strftime("%d/%m/%Y")
            data3 = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")
            data7 = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
            for p, content in [
                (initial_path, EMAIL_TEMPLATE.format(nome=nome, cidade=cidade, site=SITE, ferramentas=FERRAMENTAS)),
                (followup3_path, FOLLOWUP_3D.format(nome=nome)),
                (followup7_path, FOLLOWUP_7D.format(nome=nome)),
            ]:
                with open(p, "w", encoding="utf-8") as out:
                    out.write(content)
            roteiro_linhas.append(f"- {data_envio}: enviar e-mail inicial → {email}\n")
            roteiro_linhas.append(f"  arquivo: {initial_path}\n")
            roteiro_linhas.append(f"- {data3}: follow-up 3 dias\n")
            roteiro_linhas.append(f"  arquivo: {followup3_path}\n")
            roteiro_linhas.append(f"- {data7}: follow-up 7 dias + fechamento\n")
            roteiro_linhas.append(f"  arquivo: {followup7_path}\n\n")
            count += 1
    with open(ROTEIRO, "w", encoding="utf-8") as r:
        r.writelines(roteiro_linhas)
    print(f"Gerados {count} leads com e-mails e follow-ups.")
    print(f"Roteiro salvo em: {ROTEIRO}")

if __name__ == "__main__":
    gerar()
