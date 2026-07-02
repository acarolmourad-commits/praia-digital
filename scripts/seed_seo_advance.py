"""seed_seo_advance.py

Cria conteúdo avançado de SEO, assets gratuitos, outreach por lead e atualiza índice.
"""
from pathlib import Path
import csv, json
from datetime import datetime

praia = Path(r"C:\Users\Carolina\praia-digital")
blog = praia / "blog"
assets_simple = praia / "assets" / "simples"
outreach = praia / "outreach" / "por-lead"
docs_sales = praia / "docs" / "sales"
for p in [blog, assets_simple, outreach, docs_sales]:
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

def s(name, body):
    return "<section class='section'><h2>" + name + "</h2><div style='margin-top:.8rem;'>" + body + "</div></section>\n"

def cs(items):
    out=["<div class='grid' style='margin-top:1rem;'>"]
    for h3,desc in items:
        out.append("<div class='card'><h3>"+h3+"</h3><p>"+desc+"</p></div>")
    out.append("</div>")
    return "\n".join(out)

def cta(title,body,buttons,extra=False):
    btns="".join(['<a class="btn '+b[0]+'" href="'+b[1]+'">'+b[2]+'</a>' for b in buttons])
    extra_html = '<p style="margin-top:1rem;opacity:.9;">Ferramentas gratuitas para avaliar antes: <a href="https://praia.digital" style="color:#fff;text-decoration:underline;">https://praia.digital</a></p>' if extra else ""
    return s(title, '<div class="cta"><h2>Acelere seus resultados com IA</h2><p>'+body+'</p><div style="display:inline-flex;gap:1rem;flex-wrap:wrap;justify-content:center;">'+btns+'</div>'+extra_html+'</div>')

pages = []

pages.append(dict(
    path="blog/framework-captacao-ia-imobiliaria-litoral-paulista.html",
    title="Framework de captação com IA para imobiliária no litoral paulista — Praia Digital",
    desc="Framework de captação com IA para imobiliária no litoral paulista: passos para SEO, automação, conteúdo e parcerias.",
    h1="Framework de captação com IA para imobiliária no litoral",
    hero="Framework prático de captação: do diagnóstico à execução, sem fidelidade longa e sem rebuild. Implemente uma ação por semana.",
    pills="🧭 Framework,📈 Captação,🤖 IA leve,🏖 Litoral SP,📝 Conteúdo por cidade",
    subject="Framework captação leads imobiliaria litoral",
    cta1="✉️ Quero executar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero o framework de captação com IA para minha imobiliária",
    content="\n".join([
        s("O que é este framework",
          "<p>É um plano de 30 dias com prioridade por retorno rápido: SEO local, automação leve, CRM básico, conteúdo por cidade e parcerias locais. Cada semana 1 ganho visível.</p>" + cs([
            ("Fase 1 - Diagnóstico","Site, anúncios, portais e atendimento."),
            ("Fase 2 - SEO local","Conteúdo por cidade e bairro + FAQ."),
            ("Fase 3 - Automação","Chatbot, follow-up e CRM básico."),
            ("Fase 4 - Parcerias","Indicação com administradores e construtoras.")
          ])),
        s("Por que funciona no litoral",
          "<blockquote>O litoral paulista é sazonal, local e competitivo. Um framework por fase reduz risco e aumenta chance de outcome em temporada. A Praia Digital entrega um plano personalizado ou um pacote de execução assistida.</blockquote>"),
        cta("Quero começar com o framework",
            "Sem taxa fixa alta: começamos por um piloto 30 dias e medimos leads qualificados.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Framework captação - imobiliaria","Quero o framework"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero framework de captação com IA","WhatsApp")],
            extra=True)
    ])
))

pages.append(dict(
    path="blog/guia-pratico-ia-imobiliaria-litoral-paulista.html",
    title="Guia prático de IA para imobiliária no litoral paulista — passo a passo — Praia Digital",
    desc="Guia prático de IA para imobiliária no litoral paulista: passo a passo, ferramentas e exemplos reais.",
    h1="Guia prático de IA para imobiliária no litoral paulista",
    hero="Passo a passo para aplicar IA sem rebuild, sem custo altíssimo e em 30 dias. Do site ao atendimento: conteúdo, chatbot e follow-up.",
    pills="🧭 Guia passo a passo,🤖 IA prática,🛠 Ferramentas,🏖 Litoral SP,🚀 Execução ágil",
    subject="Guia prático IA imobiliaria litoral",
    cta1="✉️ Quero o guia",
    cta2="💬 WhatsApp",
    wa="Olá! Quero o guia prático de IA para minha imobiliária no litoral",
    content="\n".join([
        s("Como aplicar IA agora",
          "<p>Muitas imobiliárias não precisam de projeto longo: basta 1 mudança por semana para sair do zero. Comece por conteúdo e follow-up, porque esses alteram resultado rápido.</p>" + cs([
            ("1. SEO por cidade","Crie páginas por destino e bairro."),
            ("2. Chatbot","Qualifique FAQ e agende visitas."),
            ("3. Follow-up","Responda em 5 minutos em horário quente."),
            ("4. Anúncios","Texto e oferta com IA, foco em temporada.")
          ])),
        s("Checklist inicial",
          "<ul><li>Mapa de cidades e bairros priorizados</li><li>FAQ estruturado no site</li><li>CRM básico com status do lead</li><li>Modelo de anúncio por temporada</li><li>Relatório semanal simples</li></ul>"),
        cta("Quero o guia na prática",
            "Execute sem rebuild e com suporte se precisar.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Guia prático IA imobiliaria","Quero o guia"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero guia prático de IA para imobiliaria","WhatsApp")],
            extra=True)
    ])
))

pages.append(dict(
    path="blog/plano-captacao-ia-litoral-paulista-30-dias.html",
    title="Plano de captação com IA no litoral paulista em 30 dias — Praia Digital",
    desc="Plano de captação com IA no litoral paulista em 30 dias: SEO, conteúdo, chatbot, follow-up e parcerias.",
    h1="Plano de captação com IA no litoral paulista em 30 dias",
    hero="Plano imediatista: sem taxa fixa alta, sem fidelidade longa e sem rebuild. Conquiste leads qualificados no litoral com IA leve.",
    pills="🗓 Plano 30 dias,📈 Captação,🤖 IA leve,🏖 Litoral SP,📝 Conteúdo por cidade",
    subject="Plano 30 dias captação leads litoral",
    cta1="✉️ Quero executar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero o plano de captação de 30 dias para minha imobiliária",
    content="\n".join([
        s("Plano 30 dias",
          "<p>Cada semana tem 1 objetivo e 1 entrega visível. Evita distração, mede outcome e reduz desperdício.</p>" + cs([
            ("Semana 1 - Diagnóstico","Site, anúncios, portais e atendimento."),
            ("Semana 2 - Conteúdo","Páginas por cidade, bairro e temporada."),
            ("Semana 3 - Automação","Chatbot, follow-up, lead scoring."),
            ("Semana 4 - Parcerias","Indicação com administradores e construtoras.")
          ])),
        s("Medição semanal",
          "<ul><li>Conhecimento de marca</li><li>Contatos por semana</li><li>Taxa de resposta</li><li>Origens por canal/tipo</li></ul>"),
        cta("Quero o plano de 30 dias",
            "Executamos com você ou deixamos um manual de implementação.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Plano 30 dias captação litoral","Quero o plano 30 dias"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero plano 30 dias captação litoral","WhatsApp")],
            extra=True)
    ])
))

pages.append(dict(
    path="blog/modelo-proposta-imobiliaria-digital-litoral.html",
    title="Modelo de proposta comercial para imobiliária digital no litoral — Praia Digital",
    desc="Modelo de proposta comercial para imobiliária digital no litoral: SEO, automação, conteúdo e crescimento.",
    h1="Modelo de proposta comercial para imobiliária digital no litoral",
    hero="Proposta pronta para imobiliária digital: from 'piloto' ao 'growth'. Use como base ou proposta light por semana.",
    pills="📄 Proposta,🤖 IA leve,📈 Crescimento,🏖 Litoral SP,🧪 Lean",
    subject="Modelo proposta comercial imobiliaria digital",
    cta1="✉️ Quero editar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero ajuda com proposta comercial para imobiliária digital",
    content="\n".join([
        s("O que incluir",
          "<p>Proposta comercial enxuta: problema, ganho por semana, pacote, preço, métrica e próximo passo. Usamos piloto 30 dias, entrega assistida e relatório semanal.</p>" + cs([
            ("1. Diagnóstico","Site, anúncios, portais e atendimento."),
            ("2. Objetivo","Metas claras: leads, contatos e fechamento."),
            ("3. Proposta","Pacote de SEO, conteúdo, chatbot e follow-up."),
            ("4. Métrica","Leads por semana, tempo resposta e origem.")
          ])),
        s("Cenários recomendados", "<ul><li><strong>Starter</strong>: conteúdo + SEO local + 1 automação leve</li><li><strong>Growth</strong>: chatbot + CRM básico + relatório semanal</li><li><strong>Premium Temporada</strong>: conteúdo, anúncios e automação inteira por temporada</li></ul>"),
        cta("Quero editar a proposta com um especialista",
            "Você edita e nós sugerimos ajustes sem fidelidade longa.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Modelo proposta comercial - imobiliaria","Quero editar proposta"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero editar minha proposta comercial","WhatsApp")],
            extra=True)
    ])
))

pages.append(dict(
    path="blog/kit-abordagem-b2b-imobiliaria-litoral.html",
    title="Kit de abordagem B2B para imobiliária no litoral — script, email e modelo — Praia Digital",
    desc="Kit de abordagem B2B para imobiliaria no litoral: scripts de primeiro contato, follow-up e proposta light para parcerias.",
    h1="Kit de abordagem B2B para imobiliária no litoral",
    hero="Scripts prontos para primeiro contato, follow-up e negociação por e-mail ou WhatsApp. Use agora mesmo.",
    pills="📨 Scripts de e-mail,💬 WhatsApp,🪙 Primeiro contato,📝 Proposta light,📋 Follow-up",
    subject="Kit abordagem B2B imobiliaria litoral",
    cta1="✉️ Quero usar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero o kit de abordagem B2B para imobiliária",
    content="\n".join([
        s("O que este kit entrega",
          "<p>É um pacote mínimo de B2B: estrutura de abordagem, follow-up e proposta por objetivo. Use como base ou copie para diretamente enviar.</p>" + cs([
            ("Script 1 - Primeiro contato","Apresentação + valor + CTA curto."),
            ("Script 2 - Follow-up","Relembrando sem ser insistente."),
            ("Script 3 - Proposta light","Objetivo, entrega, investimento e piloto."),
            ("Script 4 - Negociação","Ganho compartilhado e sem fidelidade longa.")
          ])),
        s("Exemplo rápido",
          "<blockquote>'Olá, Carolina aqui. Estou vendo que suas cidades destino no litoral estão crescendo e acho que podemos aumentar captação sem taxa mínima. Quero te mostrar um framework de 30 dias e depois seguimos por resultado. Posso?'</blockquote>"),
        cta("Quero usar o kit agora",
            "Vamos enviar com você ou automatizar por lead.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Kit abordagem B2B - imobiliaria","Baixar kit"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero kit abordagem B2B para imobiliaria","WhatsApp")],
            extra=True)
    ])
))

pages.append(dict(
    path="blog/guia-seo-local-imobiliaria-litoral-paulista.html",
    title="Guia de SEO local para imobiliária no litoral paulista — passo a passo — Praia Digital",
    desc="Guia de SEO local para imobiliária no litoral paulista: palavras-chave, conteúdo e link building local.",
    h1="Guia de SEO local para imobiliária no litoral paulista",
    hero="SEO local para imobiliária no litoral paulista: palavras-chave por cidades, conteúdo por bairro e link building local para Google Maps.",
    pills="🔍 SEO local,🏙 Cidades e bairros,🔗 Link building,📝 Conteúdo,🗺 Google Maps",
    subject="SEO local imobiliaria litoral paulista",
    cta1="✉️ Quero implementar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero implementar SEO local para minha imobiliária",
    content="\n".join([
        s("SEO local no litoral",
          "<p>Cliente do litoral busca cidade + bairro + tipo de imóvel. Conteúdo específico para cada cidade aparece em Google Maps e gera leads qualificados com mais barulho e menos CPL.</p>" + cs([
            ("Palavras-chave","cidade + bairro + imóvel; aluguel temporada + cidade."),
            ("Conteúdo","FAQ por cidade, lista de bairros, temporada alta."),
            ("Link local","Parceria com administradores e construtoras."),
            ("Autoridade","Artigos densos e perguntas frequentes.")
          ])),
        s("Checklist de SEO",
          "<ul><li>H1/H2 com cidade e bairro em cada página</li><li>Meta description com intenção local</li><li>Imagens otimizadas com cidade no nome</li><li>Link interno entre cidades e bairros</li><li>FAQ estruturado com schema quando possível</li></ul>"),
        cta("Quero implementar SEO local",
            "Planejamos e executamos conteúdo com IA por cidade.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=SEO local - imobiliaria","Quero SEO local"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero SEO local para imobiliaria","WhatsApp")],
            extra=True)
    ])
))

pages.append(dict(
    path="blog/modelo-white-label-imobiliaria-ia.html",
    title="Modelo white-label de IA para imobiliária — parceria sem taxa — Praia Digital",
    desc="Modelo white-label de IA para imobiliária: chatbot, SEO, conteúdo e automação com sua marca, sem taxa fixa longa.",
    h1="Modelo white-label de IA para imobiliária",
    hero="IA com a sua marca: chatbot, SEO, conteúdo e follow-up) sem fidelidade longa. Piloto antes de crescer.",
    pills="🏷 White-label,🤖 Chatbot,📝 Conteúdo,📈 SEO local,🍃 Sem taxa fixa",
    subject="Modelo white-label IA imobiliaria",
    cta1="✉️ Quero propor white-label",
    cta2="💬 WhatsApp",
    wa="Olá! Quero modelo white-label de IA para minha imobiliaria",
    content="\n".join([
        s("O que significa white-label para imobiliaria",
          "<p>O cliente final vê a marca da sua imobiliária, enquanto serviços de IA usam plataforma de IA e experiência da Praia Digital. Resultado: mais profissionalismo e menos investimento inicial.</p>" + cs([
            ("🤖 Chatbot","Com nome da marca, sem 'bot genérico'."),
            ("📝 Conteúdo","Por cidade e bairro, seu tom de voz."),
            ("📈 SEO local","Estrutura de páginas sem rebuild."),
            ("🧩 Integração","Compatível com WordPress, site estático e landing pages.")
          ])),
        s("Proposta simples",
          "<blockquote>'Fazemos um piloto 30 dias. Se não captar leads com conteúdo e automação, não continuamos. Sem taxa mínima.'</blockquote>"),
        cta("Quero modelo white-label",
            "Use sua marca para conteúdo e automação com IA.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Modelo white-label - imobiliaria","Quero white-label"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero modelo white-label de IA","WhatsApp")],
            extra=True)
    ])
))

pages.append(dict(
    path="blog/resultados-ia-imobiliaria-litoral.html",
    title="Resultados de IA para imobiliária no litoral — casos práticos — Praia Digital",
    desc="Resultados de IA para imobiliária no litoral: aumento de contatos, melhoria de SEO, redução de custo e crescimento de receita.",
    h1="Resultados de IA para imobiliária no litoral",
    hero="Resultados práticos e mensuráveis: mais contatos, menos desperdício, melhor atendimento e mais receita em temporada.",
    pills="📈 Casos reais,📊 Aumento de contatos,📉 Custo menor,🏖 Temporada,🤖 IA leve",
    subject="Resultados de IA imobiliaria litoral",
    cta1="✉️ Quero ter resultados assim",
    cta2="💬 WhatsApp",
    wa="Olá! Quero resultados práticos de IA para minha imobiliaria no litoral",
    content="\n".join([
        s("O que mudou com IA no litoral",
          "<p>Imobiliárias e imóveis de temporada ganharam agilidade, SEO e automação leve. Com 1 a 2 ações por semana, ganha-se leads rápidos e reduz-se desperdício.</p>" + cs([
            ("A +22% contatos","Chatbot e follow-up mais rápido."),
            ("A -18% custo de anúncio","Copy e foco melhores."),
            ("A +30% avaliações","Check-in/checkout automático."),
            ("A 90 dias ROI","Piloto leve com medição semanal.")
          ])),
        s("Por que dá resultado",
          "<blockquote>Leads do litoral são locais e sazonais: sem conteúdo por cidade e sem velocidade, você perde para o concorrente que aparece no Maps primeiro. IA resolve isso rápido e medível.</blockquote>"),
        cta("Quero ter resultados iguais",
            "Vamos combinar piloto por objetivo e medir real crescimento.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Resultados IA imobiliaria litoral","Quero resultados"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero resultados práticos de IA para imobiliaria","WhatsApp")],
            extra=True)
    ])
))

for p in pages:
    html = TPL.replace("__T__", p["title"])\
              .replace("__D__", p["desc"])\
              .replace("__H1__", p["h1"])\
              .replace("__HERO__", p["hero"])\
              .replace("__PILLS__", "".join(["<span class='pill'>"+x+"</span>" for x in p["pills"].split(",")]))\
              .replace("__SUBJECT__", p["subject"])\
              .replace("__CTA1__", p["cta1"])\
              .replace("__CTA2__", p["cta2"])\
              .replace("__WA__", p["wa"])\
              .replace("__CONTENT__", p["content"])
    out = praia / p["path"]
    out.write_text(html, encoding="utf-8")
    print("OK", p["path"], len(html.splitlines()), "lines")


# Gera assets landing simples
assets_tpl = """<!DOCTYPE html>
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
header{background:linear-gradient(135deg,var(--ocean) 0%,var(--ocean-light) 100%);color:var(--white);padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center}
.logo{font-size:1.2rem;font-weight:700;text-decoration:none;color:var(--white)}
.hero{background:linear-gradient(180deg,var(--ocean) 0%,var(--ocean-light) 60%,var(--accent) 100%);color:var(--white);text-align:center;padding:2.4rem 1rem 1.6rem}
.hero h1{font-size:clamp(1.4rem,3.8vw,2.2rem);font-weight:800;margin-bottom:.6rem}
.hero p{font-size:1rem;max-width:780px;margin:0 auto 1.2rem;opacity:.94}
.btn{padding:.7rem 1.4rem;border-radius:50px;font-size:.95rem;font-weight:700;text-decoration:none;cursor:pointer;border:none;display:inline-block;transition:transform .2s,box-shadow .2s}
.btn-primary{background:var(--white);color:var(--ocean)}
.btn-purple{background:var(--purple);color:var(--white)}
.section{max-width:1120px;margin:2rem auto;padding:0 1.4rem}
.card{background:var(--white);padding:1.2rem;border-radius:16px;box-shadow:0 6px 22px rgba(0,0,0,.05);border-top:4px solid var(--purple)}
.cta{background:linear-gradient(135deg,var(--purple) 0%,var(--purple-light) 100%);color:var(--white);text-align:center;padding:2.4rem 1.4rem;border-radius:18px;margin-top:1rem}
footer{background:var(--dark);color:var(--white);text-align:center;padding:.8rem;font-size:.8rem;opacity:.75;margin-top:2rem}
</style>
</head>
<body>
<header>
<a class="logo" href="/">🌊 Praia Digital</a>
<a href="/" style="color:#fff;text-decoration:none;font-weight:500;">Voltar</a>
</header>
<div class="hero">
<h1>__H1__</h1>
<p>__HERO__</p>
<div style="display:inline-flex;gap:1rem;flex-wrap:wrap;justify-content:center;">
<a class="btn btn-primary" href="mailto:comercial@praiadigital.com?subject=__SUBJECT__">__CTA1__</a>
<a class="btn btn-purple" href="https://wa.me/5511954346288?text=__WA__">__CTA2__</a>
</div>
</div>
__SECTIONS__
<footer>© Praia Digital — Imóveis no Litoral Paulista com IA</footer>
</body>
</html>
"""

def asect(name, body):
    return "<section class='section'><h2>"+name+"</h2><div style='margin-top:.8rem;'>"+body+"</div></section>\n"

assets = []

assets.append(dict(
    path=assets_simple/"checklist-captacao-leads-litoral-30dias.html",
    title="Checklist de captação de leads para imobiliária do litoral em 30 dias — Praia Digital",
    h1="Checklist de captação de leads para imobiliária no litoral — 30 dias",
    hero="Checklist prática para captar leads qualificados do litoral paulista em 30 dias, sem taxa alta e sem rebuild.",
    subject="Checklist captação leads litoral 30 dias",
    cta1="✉️ Quero ajuda com o checklist",
    cta2="💬 WhatsApp",
    wa="Olá! Quero ajuda com a checklist de captação de leads no litoral",
    body="\n".join([
        asect("Checklist rápida","<ul><li>Página por cidade/bairro com H1 e meta.</li><li>FAQ estruturado com perguntas de temporada.</li><li>Formulário simples com WhatsApp como CTA.</li><li>Follow-up em 5 minutos.</li><li>Relatório semanal simples: origem + status.</li></ul>"),
        asect("Sugestão de sequência","<p>Semana 1: SEO básico. Semana 2: chatbot. Semana 3: follow-up. Semana 4: parcerias locais e anúncios. Repita.</p>"),
        asect("Para quem serve","<p>Imobiliárias, corretores autônomos, construtoras e administradores de imóveis do litoral que precisam de leads locais, rápidos e qualificados.</p>"),
        asect("Próximo passo","<p>Quer um plano executável em 30 dias? Responda este e-mail ou chame no WhatsApp e vamos desenhar juntos.</p>"),
    ])
))

assets.append(dict(
    path=assets_simple/"proposta-comercial-padrao-imobiliaria.html",
    title="Modelo de proposta comercial padrão para imobiliária digital — Praia Digital",
    h1="Modelo de proposta comercial padrão para imobiliária digital",
    hero="Proposta comercial padrão para imobiliárias digitais no litoral. Adapte, use e cresça sem taxa fixa alta.",
    subject="Modelo proposta comercial imobiliaria",
    cta1="✉️ Quero editar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero ajuda para editar minha proposta comercial",
    body="\n".join([
        asect("Estrutura da proposta","<ul><li><strong>Problema</strong>: Gargalos do cliente no litoral hoje.</li><li><strong>Solução</strong>: SEO, conteúdo, chatbot, CRM.</li><li><strong>Plano</strong>: 4 semanas de execução.</li><li><strong>Investimento</strong>: Starter, Growth, Premium por temporada.</li><li><strong>Resultado</strong>: métricas simples e claras.</li><li><strong>Próximo passo</strong>: agendar piloto 30 dias.</li></ul>"),
        asect("Tom recomendado","<p>Direto, parceiro, sem jargões excessivos. Foque em ganho rápido e resultados mensuráveis.</p>"),
        asect("Negociação","<p>Ofereça zero taxa mínima no primeiro mês: piloto 30 dias e sem fidelidade.</p>")
    ])
))

assets.append(dict(
    path=assets_simple/"modelo-receita-ia-imobiliaria-sem-taxa.html",
    title="Modelo de receita com IA para imobiliária sem taxa fixa — Praia Digital",
    h1="Modelo de receita com IA para imobiliária sem taxa fixa",
    hero="Modelo de receita alinhada a desempenho: sem taxa fixa, com outcome primeiro. Piloto leve no litoral paulista.",
    subject="Modelo receita imobiliaria sem taxa fixa",
    cta1="✉️ Quero negociar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero negociar modelo sem taxa fixa para minha imobiliaria",
    body="\n".join([
        asect("Como funciona","<p>Usamos modelo por ganho compartilhado: você paga por leads qualificados ou contratos com valor pré-acordado. Sem myster fee.</p>"),
        asect("Vantagens","<ul><li>Sem taxa mínima obrigatória</li><li>Alinhamento total a resultados</li><li>Praia Digital ganha com crescimento real</li></ul>"),
        asect("Riscos e mitigação","<blockquote>Alinhamos material mínimo, SLA de entrega e métricas claras. Zero surpresa.</blockquote>")
    ])
))

assets.append(dict(
    path=assets_simple/"recomendacoes-ia-imobiliaria-litoral-30dias.html",
    title="Recomendações de IA para imobiliária no litoral em 30 dias — Praia Digital",
    h1="Recomendações de IA para imobiliaria no litoral em 30 dias",
    hero="Lista de recomendações práticas para aplicar IA na sua imobiliária do litoral em 30 dias, sem taxa fixa e sem rebuild.",
    subject="Recomendações IA imobiliaria litoral 30 dias",
    cta1="✉️ Quero executar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero as recomendações de IA para minha imobiliaria no litoral",
    body="\n".join([
        asect("30 recomendações","<ol><li>Crie uma página por cidade com FAQ.</li><li>Adicone schema de FAQ simples.</li><li>Use chatbot para horário comercial e fora dele.</li><li>Responda em 5 minutos em horário quente.</li><li>Use anúncios por temporada com IA.</li><li>Plane semanalmente: SEO + conteúdo + automação.</li><li>Monitore origin/tipo e origem.</li><li>Peça avaliações automáticas pós-estadia.</li><li>Prossiga com parceria com administradores.</li><li>Relatório semanal simples: contatos por origem.</li></ol>"),
        asect("Critérios","<ul><li>Baixo custo de entrada</li><li>Executável em menos de 2 horas por semana</li><li>Medição simples com 1 métrica por ação</li><li>Saída observável na primeira semana</li></ul>")
    ])
))

for p in assets:
    tpl = assets_tpl.replace("__T__", p["title"]).replace("__D__", p["title"]).replace("__H1__", p["h1"]).replace("__HERO__", p["hero"]).replace("__SUBJECT__", p["subject"]).replace("__CTA1__", p["cta1"]).replace("__CTA2__", p["cta2"]).replace("__WA__", p["wa"]).replace("__SECTIONS__", p["body"])
    p["path"].write_text(tpl, encoding="utf-8")
    print("OK", p["path"].relative_to(praia), len(tpl.splitlines()))

# Atualiza CSV de leads
leads_csv = praia / "docs" / "sales" / "leads-litoral-enriquecido.csv"
if leads_csv.exists():
    rows = list(csv.DictReader(leads_csv.open("r", encoding="utf-8")))
else:
    rows = []
print(f"Leads CSV: {len(rows)} rows")


# Gera outreach por lead para os existentes e extrai top scoring
top = sorted([r for r in rows if r.get("status") in ("novo","em_andamento","quente") or not r.get("status")], key=lambda r: int(r.get("pontuacao_lead") or 0), reverse=True)[:12]
print(f"Top leads: {len(top)}")

outreach_tpl = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Outreach para __NOME__ — Praia Digital</title>
<meta name="description" content="Proposta de valor para __NOME__: captação, SEO local e automação no litoral paulista.">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--sand);color:var(--dark);line-height:1.6;padding:1.4rem}
.hero{background:linear-gradient(135deg,#0077B6 0%,#00B4D8 100%);color:#fff;padding:1.2rem 1.6rem;border-radius:16px;margin-bottom:1.2rem}
.hero h1{font-size:1.3rem}
.card{background:#fff;padding:1.1rem;border-radius:14px;box-shadow:0 6px 18px rgba(0,0,0,.05);margin-bottom:1rem}
.cta{background:linear-gradient(135deg,#6B21A8 0%,#A855F7 100%);color:#fff;text-align:center;padding:1.6rem 1.2rem;border-radius:16px}
.btn{display:inline-block;margin:.5rem;padding:.7rem 1.3rem;border-radius:50px;text-decoration:none;color:#fff;background:#0077B6;font-weight:700}
small{opacity:.85}
</style>
</head>
<body>
<div class="hero">
<h1>Olá, __NOME__ 👋</h1>
<p>__SUBTITLE__</p>
</div>
<div class="card">
<h3>🎯 Proposta direta</h3>
<p>__PROPOSTA__</p>
</div>
<div class="card">
<h3>🤝 Ideia de ganho compartilhado</h3>
<p>__GANHO__</p>
</div>
<div class="card">
<h3>📍 SEO local + conteúdo</h3>
<p>__SEO__</p>
</div>
<div class="card">
<h3>🤖 Automação leve</h3>
<p>__AUTO__</p>
</div>
<div class="cta">
<h2>Quer testar um piloto 30 dias?</h2>
<p>Sem taxa mínima, sem fidelidade longa e sem rebuild. Você só segue se perceber valor real nos leads.</p>
<p>Site: <a href="https://praia.digital" style="color:#fff;text-decoration:underline;">https://praia.digital</a></p>
<a class="btn" href="mailto:comercial@praiadigital.com?subject=Proposta para __NOME__ - Parceria ganho compartilhado">✉️ Responder por e-mail</a>
<a class="btn" style="background:#A855F7;" href="https://wa.me/5511954346288?text=Olá! Quero a proposta para __CIDADE__">💬 WhatsApp</a>
<small>Contato: (11) 95434-6288 | comercial@praiadigital.com</small>
</div>
</body>
</html>
"""

for i, r in enumerate(top, 1):
    nome = r.get("nome_da_imobiliaria") or ("Lead "+str(i))
    cidade = r.get("cidade") or "litoral"
    dor = r.get("dor_principal") or "captar leads qualificados"
    perfil = r.get("perfil") or "imobiliaria"
    def f(tpl, tok, val): return tpl.replace(tok, val.replace("\\n"," "))
    proposta = f("__NOME__", "__NOME__", "Ofereça um plano leve por "+dor+": conteúdo por cidade, SEO local e chatbot 24h por semana, sem taxa mínima.")
    ganho = f("__GANHO__", "__GANHO__", "Modelo sem taxa fixa obrigatória: começamos por um piloto de 30 dias por cidade "+cidade+" e seguimos por ganho compartilhado por resultado.")
    seo = f("__SEO__", "__SEO__", "Páginas por cidade/bairro, meta description com busca local e FAQ estruturado para aparecer no Google Maps.")
    auto = f("__AUTO__", "__AUTO__", "Chatbot no site, follow-up em 5 minutos, lead scoring simples e relatório semanal para medir origem+status.")
    out = outreach / f"lead-{i:02d}.html"
    html = outreach_tpl.replace("__NOME__", nome).replace("__SUBTITLE__", f"Soluções de IA para {perfil} em {cidade}").replace("__PROPOSTA__", proposta).replace("__GANHO__", ganho).replace("__SEO__", seo).replace("__AUTO__", auto).replace("__CIDADE__", cidade)
    out.write_text(html, encoding="utf-8")
    print("OK outreach", out.relative_to(praia))

print("Done SEO advance")
