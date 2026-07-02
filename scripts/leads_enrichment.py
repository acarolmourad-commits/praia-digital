"""Enrich leads and prepare B2B outreach assets."""
from pathlib import Path
import csv
from datetime import datetime

praia = Path(r"C:\Users\Carolina\praia-digital")
docs = praia / "docs" / "sales"
outreach = praia / "outreach" / "por-lead"
docs.mkdir(parents=True, exist_ok=True)
outreach.mkdir(parents=True, exist_ok=True)

# 1) Rebuild richer leads CSV
leads = [
  ["1","Alpha Imóveis Praia","Santos","Carlos Lima","Gerente","contato1@exemplo.com","(13) 99999-0001","construtora","novo","atendimento","seo","Portais","40","Relatórios","R$ 0.5-2k/mês","parceiro","Santos",""],
  ["2","Região Sul Digital","Mongaguá","Ana Lima","Gerente","contato2@exemplo.com","(13) 99999-0002","construtora","novo","anuncios","anuncios","Indicação","63","Aumentar captação","R$ 0.5-2k/mês","direto","Mongaguá",""],
  ["3","Ocean Blue Digital","Santos","Maria Barros","Responsável","contato3@exemplo.com","(13) 99999-0003","gestor","novo","conversao","seo","Instagram","42","SEO local","R$ 1-3k/mês","parceiro","Santos",""],
  ["4","Norte Sul Praia","Guarujá","Ana Lima","Sócio","contato4@exemplo.com","(13) 99999-0004","gestor","novo","atendimento","seo","Portais","61","Mais conteúdo","R$ 1-3k/mês","formal","Guarujá",""],
  ["5","Beta Imóveis Praia","São Vicente","Maria Rocha","Corretor-chefe","contato5@exemplo.com","(13) 99999-0005","imobiliaria","novo","conversao","chatbot","Instagram","45","SEO local","R$ 0.5-2k/mês","formal","São Vicente",""],
  ["6","Beta Imóveis Centro","Santos","Fernanda Nunes","Corretor-chefe","contato6@exemplo.com","(13) 99999-0006","construtora","novo","conversao","seo","Indicação","90","Relatórios","R$ 0.5-2k/mês","parceiro","Santos",""],
  ["7","Região Sul Digital","Bertioga","Ricardo Mendes","Responsável","contato7@exemplo.com","(13) 99999-0007","imobiliaria","novo","anuncios","avaliacao","LinkedIn","75","Mais conteúdo","R$ 0.5-2k/mês","parceiro","Bertioga",""],
  ["8","Ocean Blue Digital","Guarujá","Maria Barros","Gerente","contato8@exemplo.com","(13) 99999-0008","construtora","novo","atendimento","chatbot","LinkedIn","84","Relatórios","R$ 1-3k/mês","direto","Guarujá",""],
  ["9","Ocean Blue Centro","Santos","Luciana Nunes","Gerente","contato9@exemplo.com","(13) 99999-0009","imobiliaria","novo","conteudo","chatbot","Portais","83","Automação","R$ 1-3k/mês","parceiro","Santos",""],
  ["10","Região Sul Praia","Peruíbe","Carlos Barros","Responsável","contato10@exemplo.com","(13) 99999-0010","construtora","novo","leads","anuncios","Google Maps","90","Automação","R$ 0.5-2k/mês","parceiro","Peruíbe",""],
  ["11","Imobiliária Litoral Litoral","Santos","Luciana Mendes","Gerente","contato11@exemplo.com","(13) 99999-0011","corretor","novo","conteudo","anuncios","Google Maps","70","Automação","R$ 1-3k/mês","formal","Santos",""],
  ["12","Norte Sul Site","São Vicente","Luciana Costa","Corretor-chefe","contato12@exemplo.com","(13) 99999-0012","gestor","novo","leads","avaliacao","Portais","64","Aumentar captação","R$ 0.5-2k/mês","formal","São Vicente",""]
]

header = ["id","nome_da_imobiliaria","cidade","pessoa_de_contato","cargo","email","whatsapp","perfil","status","dor_principal","diferencial","fonte","pontuacao_lead","objetivo_90_dias","orcamento_estimado","tom","cidade_ref","created_at"]
with (docs / "leads-litoral-enriquecido.csv").open("w", encoding="utf-8", newline="") as f:
    import csv
    w = csv.writer(f)
    w.writerow(header)
    for row in leads:
        w.writerow(row)
print("Leads CSV updated:", len(leads), "rows")

# 2) Generate outreach emails with light personalization
rows = [dict(zip(header, r)) for r in leads]
lines = []
for i, r in enumerate(rows, 1):
    nome = r.get("nome_da_imobiliaria")
    cidade = r.get("cidade")
    dor = r.get("dor_principal")
    perfil = r.get("perfil")
    contato_nome = r.get("pessoa_de_contato")
    subject = f"{nome}: proposta de IA para {dor} no litoral"
    body = f"""Olá, {contato_nome}, tudo bem?

Sou a Carol, CEO da Praia Digital. Vimos que a {nome} em {cidade} pode melhorar {dor} no litoral paulista.

Oferecemos um piloto de 30 dias sem taxa mínima:
- conteúdo por cidade/bairro
- SEO local
- chatbot 24h
- follow-up em 5 minutos

Ferramentas gratuitas para avaliar: https://praia.digital
Site: https://praia.digital
Contato: (11) 95434-6288 | comercial@praiadigital.com
"""
    lines.append(f"Lead {i}: {nome} | {cidade} | {perfil} | Contato: {contato_nome} | Dor: {dor}")
    lines.append(f"Subject: {subject}")
    lines.append(body)
    lines.append("-" * 60)
(docs / "outreach-emails.txt").write_text("\n".join(lines), encoding="utf-8")
print("Outreach emails generated:", len(rows))

# 3) Generate per-lead outreach HTML with mailto primary action
outreach_tpl = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Proposta para __NOME__ — Praia Digital</title>
<meta name="description" content="Proposta de IA para __NOME__ no litoral paulista.">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#F4EBD0;color:#023047;line-height:1.6;padding:1.4rem;margin:0}
.hero{background:linear-gradient(135deg,#0077B6 0%,#00B4D8 100%);color:#fff;padding:1.2rem 1.6rem;border-radius:16px;margin-bottom:1.2rem}
.hero h1{font-size:1.3rem}
.card{background:#fff;padding:1.1rem;border-radius:14px;box-shadow:0 6px 18px rgba(0,0,0,.05);margin-bottom:1rem}
.cta{background:linear-gradient(135deg,#6B21A8 0%,#A855F7 100%);color:#fff;text-align:center;padding:1.6rem 1.2rem;border-radius:16px}
.btn{display:inline-block;margin:.5rem;padding:.7rem 1.3rem;border-radius:50px;text-decoration:none;color:#fff;background:#0077B6;font-weight:700}
.btn-secondary{background:#A855F7}
footer{background:#023047;color:#fff;text-align:center;padding:.8rem;font-size:.8rem;opacity:.75;margin-top:2rem}
ul{padding-left:1.3rem;margin:.6rem 0}
li{margin:.25rem 0}
</style>
</head>
<body>
<div class="hero">
<h1>Olá, __NOME__ 👋</h1>
<p>Proposta de IA para __CIDADE__ com resultado primeiro.</p>
</div>
<div class="card">
<h3>🎯 Proposta direta</h3>
<p>Oferecemos um plano leve para <strong>__DOR__</strong> na <strong>__CIDADE__</strong>.</p>
<ul>
<li>conteúdo por cidade/bairro</li>
<li>SEO local</li>
<li>chatbot 24h no site</li>
<li>follow-up em até 5 minutos</li>
<li>relatório semanal simples</li>
</ul>
</div>
<div class="card">
<h3>🧪 Piloto 30 dias</h3>
<p>Sem taxa mínima e sem fidelidade longa. Você só segue se perceber leads qualificados.</p>
</div>
<div class="card">
<h3>📍 Saiba mais</h3>
<p>Ferramentas gratuitas para avaliar primeiro: <a href="https://praia.digital">https://praia.digital</a></p>
</div>
<div class="cta">
<h2>Quer conversar sobre um piloto leve?</h2>
<p>Sem taxa mínima, sem rebuild e sem fidelidade longa.</p>
<a class="btn" href="mailto:comercial@praiadigital.com?subject=__SUBJECT__">✉️ Responder por e-mail</a>
<a class="btn btn-secondary" href="https://wa.me/5511954346288?text=__WA__">💬 WhatsApp</a>
<footer>© Praia Digital — Imóveis no Litoral Paulista com IA | (11) 95434-6288 | comercial@praiadigital.com</footer>
</div>
</body>
</html>
"""

for i, r in enumerate(rows, 1):
    nome = r.get("nome_da_imobiliaria")
    cidade = r.get("cidade")
    dor = r.get("dor_principal")
    subject = f"Proposta para {nome} - captação no litoral"
    wa = f"Olá! Quero um piloto para {nome} em {cidade}"
    html = outreach_tpl.replace("__NOME__", nome).replace("__CIDADE__", cidade).replace("__DOR__", dor).replace("__SUBJECT__", subject).replace("__WA__", wa)
    out = outreach / f"lead-{i:02d}.html"
    out.write_text(html, encoding="utf-8")

print("Outreach por-lead atualizado:", len(rows), "arquivos")

print("Done leads B2B preparation")
