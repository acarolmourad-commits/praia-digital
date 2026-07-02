from pathlib import Path
import csv
from datetime import datetime

praia = Path(r"C:\Users\Carolina\praia-digital")
blog = praia / "blog"
docs = praia / "docs" / "sales"
outreach = praia / "outreach"
for p in [blog, docs, outreach]:
    p.mkdir(parents=True, exist_ok=True)

SEO_PAGES = [
    {
        "path": "blog/tendencias-ia-imobiliaria-2026.html",
        "title": "Tendências de IA para imobiliária em 2026 — Praia Digital",
        "desc": "Tendências de IA para imobiliária em 2026: automação, SEO local, chatbot e captação de leads.",
        "h1": "Tendências de IA para imobiliária em 2026",
        "hero": "Tendências de IA para imobiliária em 2026 no litoral paulista: automação leve, SEO local e chatbot.",
        "pills": "🤖 IA 2026,📣 Marketing,🏖 Litoral SP,📈 Captação,📝 Conteúdo",
        "subject": "Tendências de IA para imobiliária em 2026",
        "cta1": "✉️ Quero proposta",
        "wa": "Olá! Quero IA para imobiliária em 2026"
    },
    {
        "path": "blog/ia-para-corretores-imoveis-litoral.html",
        "title": "IA para corretores de imóveis no litoral paulista — Praia Digital",
        "desc": "IA para corretores no litoral paulista: follow-up rápido, checklist e automação leve.",
        "h1": "IA para corretores de imóveis no litoral",
        "hero": "IA para corretores no litoral paulista: follow-up rápido, checklist e automação leve.",
        "pills": "🤖 Corretores,📋 Checklist,🔁 Follow-up,📈 Leads,🏖 Litoral SP",
        "subject": "IA para corretores no litoral paulista",
        "cta1": "✉️ Quero proposta",
        "wa": "Olá! Quero IA para corretores no litoral"
    },
    {
        "path": "blog/ia-generativa-marketing-imobiliario-litoral.html",
        "title": "IA generativa para marketing imobiliário no litoral — Praia Digital",
        "desc": "IA generativa para marketing imobiliário no litoral: textos, anúncios e conteúdo.",
        "h1": "IA generativa para marketing imobiliário no litoral",
        "hero": "Marketing imobiliário no litoral com IA generativa: textos, anúncios, FAQ e conteúdo otimizado.",
        "pills": "✨ IA generativa,📝 Textos,📣 Anúncios,🏖 Litoral SP,📈 Conversão",
        "subject": "IA generativa para marketing imobiliário no litoral",
        "cta1": "✉️ Quero proposta",
        "wa": "Olá! Quero IA generativa para minha imobiliaria"
    }
]

HTML_TPL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__T__</title>
<meta name="description" content="__D__">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--ocean:#0077B6;--ocean-light:#00B4D8;--sand:#F4EBD0;--white:#FFF;--dark:#023047;--accent:#90E0EF;--purple:#6B21A8;--purple-light:#A855F7}
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
.a{border-left:4px solid var(--ocean);padding:.8rem 1rem;background:var(--white);border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,.05);margin:1.5rem 0}
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
<a class="btn btn-purple" href="https://wa.me/5511954346288?text=__WA__">💬 WhatsApp</a>
</div>
</div>
__CONTENT__
<footer>© Praia Digital — Imóveis no Litoral Paulista com IA</footer>
</body>
</html>
"""

for p in SEO_PAGES:
    pills = "".join([f'<span class="pill">{x}</span>' for x in p["pills"].split(",")])
    content = (
        '<section class="section"><h2>Soluções</h2><div style="margin-top:.8rem;">'
        '<p>IA leve para imobiliárias e corretores sem taxa mínima e sem rebuild.</p>'
        '<div class="grid">'
        '<div class="card"><h3>🤖 Automação leve</h3><p>Follow-up em 5 minutos e chatbot no site.</p></div>'
        '<div class="card"><h3>📝 SEO por cidade</h3><p>Conteúdo otimizado por cidade e bairro.</p></div>'
        '<div class="card"><h3>📣 Anúncios</h3><p>Copy e oferta automática com IA.</p></div>'
        '<div class="card"><h3>📈 Relatórios</h3><p>Medição por semana e ajuste rápido.</p></div>'
        '</div>'
        '</div></section>'
        '<section class="section"><h2>Próximo passo</h2><div style="margin-top:.8rem;">'
        '<div class="a">Sem taxa mínima: piloto 30 dias com medição de leads qualificados.</div>'
        '</div></section>'
        '<section class="section"><h2>Contato</h2><div style="margin-top:.8rem;">'
        f'<p><a href="mailto:comercial@praiadigital.com?subject={p["subject"]}">✉️ E-mail</a> | <a href="https://wa.me/5511954346288?text={p["wa"]}">💬 WhatsApp</a></p>'
        '<p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>'
        '</div></section>'
    )
    html = (
        HTML_TPL.replace("__T__", p["title"])
        .replace("__D__", p["desc"])
        .replace("__H1__", p["h1"])
        .replace("__HERO__", p["hero"])
        .replace("__PILLS__", pills)
        .replace("__SUBJECT__", p["subject"])
        .replace("__CTA1__", p["cta1"])
        .replace("__WA__", p["wa"])
        .replace("__CONTENT__", content)
    )
    (praia / p["path"]).write_text(html, encoding="utf-8")
    print("OK", p["path"])

print("Done")
