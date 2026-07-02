import os
from pathlib import Path

praia = Path(r"C:\Users\Carolina\praia-digital")
blog = praia / "blog"
assets = praia / "assets"
outreach = praia / "outreach" / "por-lead"
docs_sales = praia / "docs" / "sales"
for p in [blog, assets, outreach, docs_sales]:
    p.mkdir(parents=True, exist_ok=True)

TPL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__T__</title>
<meta name="description" content="__D__">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--ocean:#0077B6;--ocean-light:#00B4D8;--sand:#F4EBD0;--white:#FFF;--dark:#023047;--accent:#90E0EF;--purple:#6B21A8;--purple-light:#A855F7;--green:#16a34a;--amber:#d97706}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--sand);color:var(--dark);line-height:1.6}
header{background:linear-gradient(135deg,var(--ocean) 0%,var(--ocean-light) 100%);color:var(--white);padding:1.2rem 2rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;box-shadow:0 2px 18px rgba(0,0,0,.18)}
.logo{font-size:1.3rem;font-weight:700;text-decoration:none;color:var(--white)}
.hero{background:linear-gradient(180deg,var(--ocean) 0%,var(--ocean-light) 60%,var(--accent) 100%);color:var(--white);text-align:center;padding:3rem 1.2rem 1.8rem}
.hero h1{font-size:clamp(1.6rem,4vw,2.5rem);font-weight:800;margin-bottom:.6rem}
.hero p{font-size:1.05rem;max-width:820px;margin:0 auto 1.3rem;opacity:.94}
.btn{padding:.78rem 1.6rem;border-radius:50px;font-size:.98rem;font-weight:700;text-decoration:none;cursor:pointer;border:none;display:inline-block;transition:transform .2s,box-shadow .2s}
.btn-primary{background:var(--white);color:var(--ocean)}
.btn-purple{background:var(--purple);color:var(--white)}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(0,0,0,.18)}
.section{max-width:1120px;margin:2.2rem auto;padding:0 1.4rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.1rem)}
.card{background:var(--white);padding:1.4rem;border-radius:16px;box-shadow:0 6px 22px rgba(0,0,0,.05);border-top:4px solid var(--purple)}
.card h3{font-size:1.05rem;margin-bottom:.4rem}
.card p{font-size:.92rem;color:#334155}
.cta{background:linear-gradient(135deg,var(--purple) 0%,var(--purple-light) 100%);color:var(--white);text-align:center;padding:2.8rem 1.6rem;margin-top:.9rem;border-radius:18px}
.cta h2{font-size:clamp(1.5rem,3.6vw,2rem);margin-bottom:.7rem}
.cta p{max-width:720px;margin:0 auto 1.1rem;opacity:.95}
.pill-row{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin:.7rem 0 1rem}
.pill{background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);padding:.32rem .8rem;border-radius:999px;font-size:.78rem}
footer{background:var(--dark);color:var(--white);text-align:center;padding:1rem;font-size:.82rem;opacity:.75;margin-top:2rem}
blockquote{border-left:4px solid var(--ocean);padding:.8rem 1rem;background:var(--white);border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,.05);margin:1.5rem 0}
ul,ol{padding-left:1.3rem;margin:.6rem 0}
li{margin:.25rem 0}
a{color:var(--ocean)}
</style>
</head>
<body>
<header>
<a class="logo" href="/">🌊 Praia Digital</a>
<nav><a href="/" style="color:#fff;text-decoration:none;font-weight:500;">Voltar ao site</a></nav>
</header>
<div class="hero">
<h1>__H1__</h1>
<p>__HERO__</p>
<div class="pill-row">__PILLS__</div>
<div style="display:inline-flex;gap:1rem;flex-wrap:wrap;justify-content:center;">
<a class="btn btn-primary" href="mailto:comercial@praiadigital.com?subject=__SUBJECT__">__CTA1__</a>
<a class="btn btn-purple" href="https://wa.me/5511954346288?text=__WA__">__CTA2__</a>
</div>
</div>
__CONTENT__
<footer>© Praia Digital — Imóveis no Litoral Paulista com IA</footer>
</body>
</html>
"""

def s(name,body):
    return "<section class='section'><h2>"+name+"</h2><div style='margin-top:.8rem;'>"+body+"</div></section>\n"
def cs(items):
    out=["<div class='grid' style='margin-top:1rem;'>"]
    for h3,desc in items:
        out.append("<div class='card'><h3>"+h3+"</h3><p>"+desc+"</p></div>")
    out.append("</div>")
    return "\n".join(out)
def cta(title,body,buttons):
    btns="".join(['<a class="btn '+b[0]+'" href="'+b[1]+'">'+b[2]+'</a>' for b in buttons])
    return s(title, '<div class="cta"><h2>Acelere seus resultados com IA</h2><p>'+body+'</p><div style="display:inline-flex;gap:1rem;flex-wrap:wrap;justify-content:center;">'+btns+'</div><p style="margin-top:1rem;opacity:.9;">Ferramentas e serviços gratuitos em: <a href="https://praia.digital" style="color:#fff;text-decoration:underline;">https://praia.digital</a></p></div>')

pages = []
pages.append(dict(
    path="blog/piloto-30-dias-imobiliaria-ia-litoral-paulista.html",
    title="Piloto de 30 dias de IA para imobiliária no litoral paulista — Praia Digital",
    desc="Piloto de 30 dias de IA para imobiliária no litoral paulista: SEO, conteúdo, chatbot e follow-up sem taxa mínima.",
    h1="Piloto de 30 dias de IA para imobiliária no litoral paulista",
    hero="Comece por um piloto leve: sem taxa mínima, sem fidelidade longa e sem rebuild. Se não captar leads em 30 dias, não continuamos.",
    pills="🧪 Piloto 30 dias,📈 Leads qualificados,🤖 IA leve,🏖 Litoral SP,📝 Conteúdo por cidade",
    subject="Piloto 30 dias imobiliaria IA litoral",
    cta1="✉️ Quero o piloto",
    cta2="💬 WhatsApp",
    wa="Olá! Quero o piloto 30 dias de IA para minha imobiliaria",
    body="\n".join([
        s("O que é o piloto",
          "<p>É uma inicialização enxuta: diagnóstico, 1 objetivo por semana, 1 ferramenta por semana e medição. Evita desperdício e sinaliza parceiro real.</p>"+cs([
            ("Semana 1 - Diagnóstico","Site, anúncios, portais e atendimento."),
            ("Semana 2 - SEO local","Conteúdo por cidade e bairro + FAQ."),
            ("Semana 3 - Automação","Chatbot, follow-up, lead scoring."),
            ("Semana 4 - Parcerias","Indicação, administradores e construtoras.")
          ])),
        s("Compromisso","<blockquote>Sem taxa mínima, sem fidelidade longa e sem rebuild. Você só continua se perceber valor real nos leads.</blockquote>"),
        cta("Quero o piloto agora",
            "Vamos alinhar objetivo, SLA de entrega e métrica com você.",
            [('btn-primary','mailto:comercial@praiadigital.com?subject=Piloto 30 dias - imobiliaria','Quero o piloto'),
             ('btn-purple','https://wa.me/5511954346288?text=Quero piloto 30 dias para imobiliaria','WhatsApp')])
    ])
))

pages.append(dict(
    path="blog/captacao-leads-ia-litoral-paulista-30-dias.html",
    title="Captação de leads com IA no litoral paulista em 30 dias — Praia Digital",
    desc="Captação de leads com IA no litoral paulista em 30 dias: SEO, conteúdo, chatbot e follow-up sem taxa mínima.",
    h1="Captação de leads com IA no litoral paulista em 30 dias",
    hero="Plano direto de captação: SEO local, conteúdo por cidade, chatbot e follow-up leve para imobiliárias do litoral.",
    pills="📈 Captação de leads,🤖 IA,📝 Conteúdo,🏖 Litoral SP,🗓 30 dias",
    subject="Captação de leads IA litoral 30 dias",
    cta1="✉️ Quero captar leads",
    cta2="💬 WhatsApp",
    wa="Olá! Quero captar leads com IA no litoral",
    body="\n".join([
        s("Plano de captação",
          "<p>Conquiste contatos locais e qualificados com conteúdo otimizado, chatbot 24h e follow-up em 5 minutos.</p>"+cs([
            ("Semana 1 - SEO","Páginas por cidade e bairro com H1/H2 local."),
            ("Semana 2 - Chatbot","FAQ, qualificação e agendamento."),
            ("Semana 3 - Anúncios","Copy e oferta com IA por temporada."),
            ("Semana 4 - Parcerias","Indicação com administradores e construtoras.")
          ])),
        s("Métricas",
          "<ul><li>Conhecimento de marca</li><li>Contatos por semana</li><li>Contatos em até 15 min</li><li>Origem por canal/tipo</li></ul>"),
        cta("Quero executar a captação",
            "Sem taxa mínima: execute e meça o resultado comigo.",
            [('btn-primary','mailto:comercial@praiadigital.com?subject=Captação leads IA litoral','Quero captar leads'),
             ('btn-purple','https://wa.me/5511954346288?text=Quero captar leads com IA no litoral','WhatsApp')])
    ])
))

pages.append(dict(
    path="blog/modelo-parceria-ganho-compartilhado-imobiliaria-litoral-paulista.html",
    title="Modelo de parceria com ganho compartilhado para imobiliária no litoral paulista — Praia Digital",
    desc="Modelo de parceria com ganho compartilhado para imobiliária no litoral paulista: reduz risco, alinha resultados e cresce junto.",
    h1="Modelo de parceria com ganho compartilhado para imobiliária no litoral",
    hero="Parceria sem taxa fixa longa: cresça por resultado, sem riscos excessivos e com suporte de IA leve.",
    pills="🤝 Parceria,💸 Ganho compartilhado,📈 Resultado,🏖 Litoral SP,🍃 Lean",
    subject="Parceria ganho compartilhado imobiliaria litoral",
    cta1="✉️ Quero negociar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero negociar parceria com ganho compartilhado para minha imobiliaria",
    body="\n".join([
        s("Proposta de valor",
          "<p>Em vez de fee fixo, alinhamos crescimento e performance. Praia Digital ganha com mais leads qualificados, e a imobiliária ganha resultados sem taxa mínima alta.</p>"+cs([
            ("Planejamento","Metas clear por cidade, temporada e buyer persona."),
            ("Execução leve","Conteúdo, chatbot e follow-up sem rebuild."),
            ("Relatórios","Lead origin, tempo resposta e conversão."),
            ("Repartição","Percentual por lead qualificado ou contrato.")
          ])),
        s("Exemplo prático",
          "<blockquote>'Criamos 1 página SEO + 4 anúncios + follow-up para temporada 2026. Se não houver contatos qualificados, mês seguinte cortamos.'</blockquote>"),
        cta("Quero propor ganho compartilhado",
            "Sem taxa fixa, sem fidelidade longa: resultados primeiro.",
            [('btn-primary','mailto:comercial@praiadigital.com?subject=Parceria ganho compartilhado','Propor parceria'),
             ('btn-purple','https://wa.me/5511954346288?text=Quero parceria com ganho compartilhado','WhatsApp')])
    ])
))

pages.append(dict(
    path="blog/passo-a-passo-implementar-ia-imobiliaria-sem-investimento-inicial.html",
    title="Passo a passo para implementar IA em imobiliária sem investimento inicial — Praia Digital",
    desc="Implemente IA em imobiliária sem investimento inicial: use ferramentas gratuitas, conteúdo otimizado e automação leve no litoral.",
    h1="Passo a passo para implementar IA em imobiliária sem investimento inicial",
    hero="Use ferramentas gratuitas, conteúdo otimizado e automação leve para colher leads no litoral sem investir fortemente.",
    pills="🆓 Sem investimento inicial,🤖 IA gratuita,🛠 Ferramentas,🏖 Litoral SP,🚀 Execução leve",
    subject="Implementar IA imobiliaria sem investimento inicial",
    cta1="✉️ Quero executar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero passo a passo para implementar IA em minha imobiliaria sem investimento",
    body="\n".join([
        s("Mapa de execução",
          "<p>Comece por baixo custo: conteúdo SEO, FAQ estruturado, chatbot em página simples e follow-up. Depois suba para anúncios e CRM.</p>"+cs([
            ("Ferramentas gratuitas","Formulários, WhatsApp, Google Sheets, FAQ simples."),
            ("Conteúdo","Páginas por cidade/bairro com keyword local."),
            ("Automação","Lembretes, follow-up minutos e chatbot básico."),
            ("Primeiro insight","Medição semanal de contatos e origem.")
          ])),
        s("Economia de custos",
          "<ul><li>Sem taxa fixa</li><li>Sem rebuild</li><li>Sem integrações caras</li><li>Com medição clara antes de crescer</li></ul>"),
        cta("Quero executar agora",
            "Vamos primeiro testar com os recursos que você já tem.",
            [('btn-primary','mailto:comercial@praiadigital.com?subject=Implementar IA sem investimento','Quero executar'),
             ('btn-purple','https://wa.me/5511954346288?text=Quero passo a passo de IA sem investimento','WhatsApp')])
    ])
))

for p in pages:
    tpl = TPL.replace("__T__", p["title"]).replace("__D__", p["desc"]).replace("__H1__", p["h1"]).replace("__HERO__", p["hero"]).replace("__PILLS__", "".join(["<span class='pill'>"+x+"</span>" for x in p["pills"].split(",")])).replace("__SUBJECT__", p["subject"]).replace("__CTA1__", p["cta1"]).replace("__CTA2__", p["cta2"]).replace("__WA__", p["wa"]).replace("__CONTENT__", p["body"])
    out = praia / p["path"]
    out.write_text(tpl, encoding="utf-8")
    print("OK", out.relative_to(praia), len(tpl.splitlines()))

# Update sitemap lightly: append new pages from filesystem
sitemap = praia / "sitemap.xml"
existing = ""
if sitemap.exists():
    existing = sitemap.read_text(encoding="utf-8")
new_lines = []
blog_files = [p for p in blog.glob("*.html") if p.name not in ["index.html"]]
added = 0
for f in sorted(blog_files):
    url = f"https://acarolmourad-commits.github.io/praia-digital/blog/{f.name}"
    if f.name in existing:
        continue
    new_lines.append(f"<url><loc>{url}</loc><priority>0.7</priority></url>")
    added += 1
sitemap_text = existing.strip() + "\n" + "\n".join(new_lines)
sitemap.write_text(sitemap_text, encoding="utf-8")
print(f"Sitemap updated: {added} entries appended")

# Create a basic outreach email template per lead from CSV
csv_path = praia / "docs" / "sales" / "leads-litoral-enriquecido.csv"
if csv_path.exists():
    import csv
    rows = list(csv.DictReader(csv_path.open("r", encoding="utf-8")))
    out_emails = praia / "docs" / "sales" / "outreach-emails.txt"
    lines = []
    for i,r in enumerate(rows,1):
        nome = r.get("nome_da_imobiliaria")
        cidade = r.get("cidade")
        dor = r.get("dor_principal")
        perfil = r.get("perfil")
        lines.append(f"Lead {i}: {nome} | {cidade} | {perfil} | Dor: {dor}")
        subject = f"{nome}: proposta de IA para {dor} no litoral"
        body = f"""Olá, sou a Carol, CEO da Praia Digital.

Notei que {nome} pode melhorar {dor} no litoral paulista. Criamos um framework leve de captação com IA: SEO por cidade, conteúdo e automação sem taxa mínima.

Queremos apresentar um piloto 30 dias sem fidelidade: se não captar leads qualificados, não continuamos.

Site: https://praia.digital
Ferramentas gratuitas: https://praia.digital
Contato: (11) 95434-6288 | comercial@praiadigital.com
"""
        lines.append(f"Subject: {subject}")
        lines.append(body)
        lines.append("-"*60)
    out_emails.write_text("\n".join(lines), encoding="utf-8")
    print(f"Outreach emails: {len(rows)} generated -> {out_emails.relative_to(praia)}")

print("Done SEO + outreach expansion")
