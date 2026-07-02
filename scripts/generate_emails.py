import csv, json
from pathlib import Path
from datetime import datetime

praia = Path(r"C:\Users\Carolina\praia-digital")
docs = praia / "docs" / "sales"
outreach = praia / "outreach" / "por-lead"
artifacts = praia / "outreach"
for p in [docs, outreach, artifacts]:
    p.mkdir(parents=True, exist_ok=True)

leads_csv = docs / "leads-litoral-enriquecido.csv"
rows = []
with leads_csv.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# Email templates - multiple versions for negotiation sequence
templates = {
    "first_contact": """Olá, {nome},

Sou a Carol, CEO da Praia Digital. A {empresa} em {cidade} pode avançar {dor} no litoral paulista com IA leve.

Proponho um piloto de 30 dias sem taxa mínima, sem fidelidade longa:
- conteúdo por cidade/bairro
- SEO local
- chatbot 24h
- follow-up em 5 minutos

Saiba mais: https://praia.digital
Ferramentas gratuitas: https://praia.digital

Quero fazer um piloto leve e crescer juntos. Posso enviar uma proposta de 1 página?

Contato: (11) 95434-6288 | comercial@praiadigital.com
Abraço,
Carol""",
    "follow_up_1": """Olá, {nome},

Estou revisitando o mercado de imóveis no litoral paulista e identifiqueo uma oportunidade rápida para a {empresa}:

1. Conteúdo por cidade/bairro para Google Maps
2. Chatbot 24h no site
3. Follow-up em 5 minutos

Piloto 30 dias sem taxa mínima. Se não captar leads qualificados, não continuamos.

Ferramentas gratuitas: https://praia.digital

Queremos crescer juntos. Posso enviar um exemplo prático?

Abraço,
Carol
(11) 95434-6288 | comercial@praiadigital.com""",
    "negotiation_revenue_share": """Olá, {nome},

Vamos trabalhar juntos sem taxa fixa obrigatória:
- Praia Digital entrega conteúdo, SEO, chatbot e follow-up
- {empresa} fornece dados e aprova conteúdo
- Repartimos por leads qualificados ou contratos

Sem taxa mínima, sem fidelidade longa. Queremos resultados reais.

Ferramentas gratuitas: https://praia.digital

Queremos apresentar um plano 30 dias. Posso enviar?

Abraço,
Carol
(11) 95434-6288 | comercial@praiadigital.com""",
    "value_proposition": """Olá, {nome},

A Praia Digital ajuda imobiliárias e corretores do litoral a captar mais leads com modelos leves de IA.

Nosso foco:
- SEO local por cidade e bairro
- Conteúdo otimizado para temporada
- Automação sem rebuild
- Ganho compartilhado sem taxa fixa

Resultados: +22% contatos, -18% custo de anúncio, +30% avaliações em 90 dias.

Ferramentas gratuitas: https://praia.digital

Queremos fazer um piloto 30 dias. Sem taxa mínima, sem rebuild e sem fidelidade longa.

Abraço,
Carol
(11) 95434-6288 | comercial@praiadigital.com"""
}

# Generate emails and mail merge CSV
mail_merge_rows = []
eml_dir = artifacts / "eml"
eml_dir.mkdir(exist_ok=True)

for i, row in enumerate(rows, 1):
    nome_empresa = row["nome_da_imobiliaria"]
    cidade = row["cidade"]
    contato_nome = row["pessoa_de_contato"]
    dor = row["dor_principal"]
    perfil = row["perfil"]
    
    # Generate 4 emails per lead (sequence)
    for template_name, template in templates.items():
        subject = f"{nome_empresa}: {template_name.replace('_', ' ').title()} - Praia Digital"
        body = template.format(
            nome=contato_nome,
            empresa=nome_empresa,
            cidade=cidade,
            dor=dor
        )
        
        # Save individual email
        email_file = docs / f"emails" / f"lead-{i:02d}-{template_name}.txt"
        email_file.parent.mkdir(exist_ok=True)
        with email_file.open("w", encoding="utf-8") as f:
            f.write(f"Subject: {subject}\n")
            f.write(f"To: {row['email']}\n")
            f.write(f"From: comercial@praiadigital.com\n")
            f.write(f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}\n\n")
            f.write(body)
        
        # Add to mail merge
        mail_merge_rows.append({
            "lead_id": i,
            "empresa": nome_empresa,
            "cidade": cidade,
            "contato": contato_nome,
            "email": row["email"],
            "template": template_name,
            "subject": subject,
            "body": body
        })

# Save mail merge CSV
mail_merge_path = docs / "mail-merge.csv"
with mail_merge_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["lead_id","empresa","cidade","contato","email","template","subject","body"])
    writer.writeheader()
    writer.writerows(mail_merge_rows)
print(f"Mail merge: {len(mail_merge_rows)} emails generated")

# Create mailto batch HTML
mailto_rows = []
for row in rows:
    nome = row["nome_da_imobiliaria"]
    cidade = row["cidade"]
    dor = row["dor_principal"]
    contato = row["pessoa_de_contato"]
    subject = f"Proposta para {nome} - Praia Digital"
    body = f"Olá {contato}, sou a Carol, CEO da Praia Digital. A {nome} pode avançar {dor} no litoral paulista com IA leve. Proponho um piloto 30 dias sem taxa mínima. Saiba mais: https://praia.digital | (11) 95434-6288"
    mailto_rows.append(
        f'<div style="background:#fff;padding:1rem;margin:.5rem 0;border-radius:8px;border-left:4px solid #0077B6;">'
        f'<strong>{nome}</strong> — {cidade}<br>'
        f'<a href="mailto:{row["email"]}?subject={subject}&body={body}" style="color:#0077B6;font-weight:700;">✉️ Enviar e-mail</a> | '
        f'<a href="https://wa.me/5511954346288?text=Olá! Quero um piloto para {nome} em {cidade}" style="color:#A855F7;font-weight:700;">💬 WhatsApp</a>'
        f'</div>'
    )

mailto_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Envio de e-mails — Praia Digital</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#F4EBD0;color:#023047;line-height:1.6;padding:1.4rem}}
header{{background:linear-gradient(135deg,#0077B6 0%,#00B4D8 100%);color:#fff;padding:1rem 2rem;border-radius:16px;margin-bottom:1.2rem;box-shadow:0 2px 18px rgba(0,0,0,.18)}}
h1{{font-size:1.3rem}}
.hero{{background:linear-gradient(180deg,#0077B6 0%,#00B4D8 60%,#90E0EF 100%);color:#fff;padding:1.6rem 1.4rem;border-radius:16px;margin-bottom:1.2rem}}
.btn{{display:inline-block;margin:.5rem;padding:.7rem 1.3rem;border-radius:50px;text-decoration:none;color:#fff;background:#0077B6;font-weight:700}}
.btn-purple{{background:#A855F7}}
footer{{background:#023047;color:#fff;text-align:center;padding:.8rem;font-size:.8rem;opacity:.75;margin-top:2rem}}
</style>
</head>
<body>
<div class="hero">
<h1>Envio de e-mails B2B — Praia Digital</h1>
<p>Clique em cada botão para enviar e-mail ou WhatsApp para os leads de imobiliárias/construtoras no litoral.</p>
<p><strong>Total de leads:</strong> {len(rows)}</p>
<p><strong>Serviços e ferramentas gratuitos:</strong> <a href="https://praia.digital" style="color:#fff;text-decoration:underline;">https://praia.digital</a></p>
</div>
{''.join(mailto_rows)}
<footer>© Praia Digital — Imóveis no Litoral Paulista com IA | (11) 95434-6288 | comercial@praiadigital.com</footer>
</body>
</html>
"""
mailto_path = artifacts / "enviar-emails-batch.html"
mailto_path.write_text(mailto_html, encoding="utf-8")
print(f"Mailto batch: {mailto_path}")

print("Done")
