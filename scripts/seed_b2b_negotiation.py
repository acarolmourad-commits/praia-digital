import os
from pathlib import Path
from datetime import datetime

praia = Path(r"C:\Users\Carolina\praia-digital")
blog = praia / "blog"
assets = praia / "assets"
docs_sales = praia / "docs" / "sales"
outreach = praia / "outreach" / "por-lead"
for p in [blog, assets, docs_sales, outreach]:
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

# Shared helpers inline:
def section(name, body):
    return "<section class='section'><h2>" + name + "</h2><div style='margin-top:.8rem;'>" + body + "</div></section>\n"
def cards(items):
    out=["<div class='grid' style='margin-top:1rem;'>"]
    for h3,desc in items:
        out.append("<div class='card'><h3>"+h3+"</h3><p>"+desc+"</p></div>")
    out.append("</div>")
    return "\n".join(out)
def cta_block(title,body,buttons,extra=False):
    btns="".join(['<a class="btn '+b[0]+'" href="'+b[1]+'">'+b[2]+'</a>' for b in buttons])
    extra_html = '<p style="margin-top:1rem;opacity:.9;">Ferramentas e serviços gratuitos em: <a href="https://praia.digital" style="color:#fff;text-decoration:underline;">https://praia.digital</a></p>' if extra else "<p style='margin-top:1rem;opacity:.9;'>Conheça mais: <a href='https://praia.digital' style='color:#fff;text-decoration:underline;'>https://praia.digital</a></p>"
    return section(title, '<div class="cta"><h2>Acelere sua captação de leads no litoral</h2><p>'+body+'</p><div style="display:inline-flex;gap:1rem;flex-wrap:wrap;justify-content:center;">'+btns+'</div>'+extra_html+'</div>')

def page(*, path,title,desc,h1,hero,pills,subject,cta1,cta2,wa,content):
    html = TPL.replace('__T__', title).replace('__D__', desc).replace('__H1__', h1).replace('__HERO__', hero).replace('__PILLS__', "".join(['<span class="pill">'+x+'</span>' for x in pills.split(",")])).replace('__SUBJECT__', subject).replace('__CTA1__', cta1).replace('__CTA2__', cta2).replace('__WA__', wa).replace('__CONTENT__', content)
    out = praia / path
    out.write_text(html, encoding="utf-8")
    print("OK", path, len(html.splitlines()))

page(
  path="blog/quanto-vale-terreno-litoral-paulista.html",
  title="Quanto vale um terreno no litoral paulista — avaliação e comparação — Praia Digital",
  desc="Quanto vale um terreno no litoral paulista: fatores, avaliação automática e cidades com maior valorização em 2026.",
  h1="Quanto vale um terreno no litoral paulista",
  hero="Descubra valor de mercado e saiba por que regiões do litoral paulista valorizam mais em temporada e em médio prazo.",
  pills="📊 Valorização,🏖 Litoral SP,📈 Mercado,🤖 Avaliação IA,🧭 Bairros",
  subject="Quanto vale terreno litoral paulista",
  cta1="✉️ Quero uma avaliação orientada",
  cta2="💬 WhatsApp",
  wa="Olá! Quero uma orientação de avaliação de imóvel no litoral",
  content="\n".join([
    section("Fatores de valor",
            "<p>Valor depende de localização, temporada, proximidade da praia, estrutura e demanda local. Conteúdo específico por cidade ajuda o lead a entender melhor o preço.</p>"+cards([
              ("🏖 Proximidade da praia","Menor distância = maior valor médio."),
              ("🗓 Temporada","Alta temporada aumenta preço e ocupação."),
              ("🧱 Estrutura","Área, vagas e acabamentos guiam avaliação."),
              ("🤖 Avaliação IA","Modelos estimam preço com dados locais.")
            ])),
    section("Serviço de avaliação leve",
            "<blockquote>Oferecemos relatórios por cidade/bairro com base em dados de busca e anúncios locais. Evite avaliação genérica: dê ao cliente um comparativo útil.</blockquote>"),
    cta_block("Quero uma orientação de avaliação no litoral",
              "Sem taxa mínima: primeiro insight rápido, depois relatório detalhado por cidade.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Avaliação de terreno litoral','Quero avaliação orientada'),('btn-purple','https://wa.me/5511954346288?text=Quero avaliação de terreno no litoral','WhatsApp')])
  ])
)

page(
  path="blog/investimento-no-litoral-bertioga.html",
  title="Investimento no litoral em Bertioga — avaliação, tendências e dicas — Praia Digital",
  desc="Investimento no litoral em Bertioga: tendências, avaliação, temporada, mercado e como usar IA para crescer.",
  h1="Investimento no litoral em Bertioga",
  hero="Tendências de investimento no litoral em Bertioga em 2026: temporada, valorização e captação de leads com IA.",
  pills="🏖 Bertioga,📈 Valorização,🏨 Temporada,📊 Mercado,🤖 IA",
  subject="Investimento Bertioga litoral",
  cta1="✉️ Quero orientação",
  cta2="💬 WhatsApp",
  wa="Olá! Quero orientação de investimento imobiliário em Bertioga",
  content="\n".join([
    section("Por que Bertioga","<p>Bertioga é um dos destinos mais competitivos do litoral paulista. Com SEO local e chatbot 24h, imobiliárias ganham reconhecimento e contatos no entorno de praia e marina.</p>"+cards([
      ("🏄 Acessibilidade","Rodovia e ferryboat melhoram fluxo."),
      ("🏅 Temporada","Alta ocupação em janeiro e julho."),
      ("🏗 Novos empreendimentos","Construtoras impulsionam leads.Bertioga tem alto tráfego."),
      ("📈 Valorização","Região cresce com infra e demanda por temporada.")
    ])),
    section("Next step","<blockquote>Conteúdo por bairro, temporada e buyer persona melhora captação. Quer um piloto 30 dias em Bertioga?</blockquote>"),
    cta_block("Quero orientação para investir no litoral",
              "Vamos alinhar conteúdo, SEO local e automação para captar leads qualificados.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Investimento Bertioga','Quero orientação de investimento'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero orientação para investimento em Bertioga','WhatsApp')])
  ])
)

page(
  path="blog/guia-imoveis-frente-mar-bertioga.html",
  title="Guia de imóveis frente mar em Bertioga — oportunidades e dicas — Praia Digital",
  desc="Guia de imóveis frente mar em Bertioga: tipos, preços, temporada, avaliação e dicas de SEO para corretores.",
  h1="Guia de imóveis frente mar em Bertioga",
  hero="Conheça oportunidades de imóveis frente mar em Bertioga: temporada, avaliação, SEO local e automação para captar leads.",
  pills="🌊 Frente mar,🏖 Bertioga,🏨 Temporada,📈 Valorização,🤖 Chatbot",
  subject="Guia imoveis frente mar Bertioga",
  cta1="✉️ Quero orientação",
  cta2="💬 WhatsApp",
  wa="Olá! Quero orientação para imóveis frente mar em Bertioga",
  content="\n".join([
    section("Imóveis frente mar em Bertioga",
            "<p>Oportunidades tem alta temporada, valorização e tipo de cliente específico. Com conteúdo detalhado e SEO local, corretores captam leads qualificados sem taxa mínima.</p>"+cards([
              ("🏖 Tipologia","Apartamento, casa, duplex e pousada."),
              ("📈 Valorização","Alta quando temporada + SEO local."),
              ("🤖 Atendimento","Chatbot e follow-up reduzem atrito."),
              ("📣 Anúncios","Copy e imagens com IA por temporada.")
            ])),
    section("Plano rápido",
            "<ul><li>SEO por bairro: centro, Riviera, etc.</li><li>FAQ estruturado: preço, temporada e estadia.</li><li>Chatbot: agendamento de visita rápido.</li><li>Follow-up: 5, 15 e 60 minutos.</li></ul>"),
    cta_block("Quero orientação para imóveis frente mar",
              "Sem taxa mínima: primeiro conteúdo por bairro e temporada.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Guia imoveis frente mar Bertioga','Quero guia de imóveis frente mar'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero orientação para imóveis frente mar em Bertioga','WhatsApp')])
  ])
)

page(
  path="blog/ia-para-imobiliaria-tradicional-litoral-paulista.html",
  title="IA para imobiliária tradicional no litoral paulista — transformação leve — Praia Digital",
  desc="IA para imobiliária tradicional no litoral paulista: transformação leve, sem rebuild e sem taxa fixa alta.",
  h1="IA para imobiliária tradicional no litoral paulista",
  hero="Seja tradicional: use IA leve para responder mais rápido, vender mais e reduzir perdas no litoral paulista.",
  pills="🏛 Tradicional,🤖 IA leve,📈 Crescimento,🧪 Piloto 30 dias,🏖 Litoral SP",
  subject="IA para imobiliaria tradicional litoral",
  cta1="✉️ Quero transformar",
  cta2="💬 WhatsApp",
  wa="Olá! Quero aplicar IA em minha imobiliaria tradicional no litoral",
  content="\n".join([
    section("Transformação respeitando o modelo atual",
            "<p>Não precisa rebuild. Comece por 1 ferramenta: chatbot, SEO ou follow-up. Em 30 dias você mede mudança sem surpresa.</p>"+cards([
              ("🔁 Atendimento","Resposta mais rápida e menos leads perdidos."),
              ("📸 Conteúdo","Local por cidade/bairro com SEO."),
              ("🧪 Piloto","30 dias, sem taxa mínima, sem fidelidade longa."),
              ("📈 Crescimento","Mais leads, mais vendas, menos custo fixo.")
            ])),
    section("Riscos e como evitar",
            "<blockquote>Risco técnico é baixo: integração leve e SaaS. Risco operacional existe se a equipe não seguir checklist. Mitigamos com treinamento curto e SLA semanal.</blockquote>"),
    cta_block("Quero transformar minha imobiliaria tradicional",
              "Sem rebuild, sem taxa alta e sem fidelidade longa: outcomes first.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=IA para imobiliaria tradicional','Quero transformar'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero IA para minha imobiliaria tradicional','WhatsApp')])
  ])
)

page(
  path="blog/ia-para-corretores-autonomos-litoral-paulista.html",
  title="IA para corretores autônomos no litoral paulista — ferramentas gratuitas — Praia Digital",
  desc="IA para corretores autônomos no litoral paulista: ferramentas gratuitas e conteúdo para vender mais sem taxa alta.",
  h1="IA para corretores autônomos no litoral paulista",
  hero="Ferramentas gratuitas, conteúdo por cidade e automação leve para corretores autônomos do litoral paulista.",
  pills="🛠 Ferramentas gratuitas,📝 Conteúdo local,🧭 Corretor autônomo,🏖 Litoral SP,📈 Leads",
  subject="IA para corretores autonomos litoral",
  cta1="✉️ Quero usar",
  cta2="💬 WhatsApp",
  wa="Olá! Quero as ferramentas gratuitas para corretor autônomo no litoral",
  content="\n".join([
    section("Ferramentas gratuitas para corretores autônomos",
            "<p>Use as ferramentas gratuitas da Praia Digital: checklist, templates de anúncio, follow-up simplificado e geração de posts para redes.</p>"+cards([
              ("📋 Checklist","Lead scoring e follow-up simplificado."),
              ("📝 Templates","Anúncios por temporada e cidade."),
              ("🤖 Chatbot","FAQ e agendamento em página simples."),
              ("📊 Diagnóstico","Descubra onde aplicar IA primeiro.")
            ])),
    section("Conteúdo por cidade",
            "<p>Artigos por cidade/bairro para captar leads locais. Publique um por semana e apareça no Google Maps primeiro.</p>"),
    cta_block("Quero começar sem investimento",
              "Comece pelas ferramentas gratuitas em https://praia.digital e depois converse com a gente.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=IA para corretores autonomos','Quero começar sem investimento'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero ferramentas gratuitas para corretor autônomo','WhatsApp')],
              extra=True)
  ])
)

page(
  path="blog/corretores-autonomos-ia-competir-imobiliarias.html",
  title="Corretores autônomos usam IA para competir com imobiliárias no litoral — Praia Digital",
  desc="Corretores autônomos usam IA para competir com imobiliárias no litoral: SEO, conteúdo e automação leve.",
  h1="Corretores autônomos usam IA para competir com imobiliárias no litoral",
  hero="Com IA leve, corretores autônomos do litoral competem com imobiliárias grandes por SEO, agilidade e conteúdo.",
  pills="⚔ Competição,📝 Conteúdo local,📈 SEO,🤖 Automação leve,🏖 Litoral SP",
  subject="Corretores autonomos competir com imobiliarias",
  cta1="✉️ Quero começar",
  cta2="💬 WhatsApp",
  wa="Olá! Quero usar IA para competir com imobiliárias no litoral",
  content="\n".join([
    section("O jogo mudou",
            "<p>Você não precisa de estrutura grande para aparecer no Google Maps. Conteúdo por cidade, SEO local e follow-up rápido são diferenciais para corretores autônomos.</p>"+cards([
              ("📈 SEO","Páginas por cidade/bairro com keyword local."),
              ("🤖 Chatbot","Atendimento 24h sem equipe."),
              ("🔁 Follow-up","Em 5 minutos, menos perda."),
              ("🛠 Ferramentas gratuitas","Modelos de anúncio e posts.")
            ])),
    section("Exemplo",
            "<blockquote>Corretor autônomo em Santos criou 3 páginas de SEO, um FAQ e chatbot leve e dobrou contatos em 60 dias sem taxa fixa.</blockquote>"),
    cta_block("Quero competir melhor",
              "Use ferramentas gratuitas primeiro e depois um piloto leve para crescer.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Corretores autonomos IA','Quero competir melhor'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero usar IA para competir com imobiliarias','WhatsApp')])
  ])
)

page(
  path="blog/consultoria-ia-imobiliaria-litoral-personalizado.html",
  title="Consultoria de IA personalizada para imobiliária no litoral paulista — Praia Digital",
  desc="Consultoria de IA personalizada para imobiliária no litoral paulista: sessão direcionada, sem taxa fixa alta e sem rebuild.",
  h1="Consultoria de IA personalizada para imobiliária no litoral",
  hero="Sessão direcionada para a sua imobiliária no litoral: cidades, temporada, perfil e ferramentas recomendadas em 1 encontro.",
  pills="🧠 Consultoria personalizada,📋 Planejamento,🤖 IA,🏖 Litoral SP,🚀 Execução",
  subject="Consultoria personalizada IA imobiliaria",
  cta1="✉️ Quero agendar",
  cta2="💬 WhatsApp",
  wa="Olá! Quero uma consultoria personalizada de IA para minha imobiliaria",
  content="\n".join([
    section("Como funciona",
            "<p>Sessão de 30 a 60 minutos para mapear gargalos, oportunidades e um plano 30 dias personalizado para cidade, temporada e perfil.</p>"+cards([
              ("🔎 Diagnóstico","Site, SEO, anúncios, portais e atendimento."),
              ("📋 Priorização","Ações por impacto e esforço."),
              ("🧪 Piloto","30 dias com medição semanal."),
              ("📈 Follow-up","Ajuste semanal e relatório de outcome.")
            ])),
    section("Resultado",
            "<blockquote>Você tem um plano priorizado por objetivo, sem taxa fixa longa. Execute com ou sem a gente: o plano continua seu.</blockquote>"),
    cta_block("Quero uma sessão personalizada",
              "Resposta em até 1 dia útil e alinhamento rápido por WhatsApp.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Consultoria personalizada IA','Quero agendar consultoria'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero consultoria personalizada de IA','WhatsApp')])
  ])
)

page(
  path="blog/dossie-conquista-pequenas-imobiliarias-litoral-paulista.html",
  title="Dossiê de conquista para pequenas imobiliárias no litoral paulista — Praia Digital",
  desc="Dossiê de conquista para pequenas imobiliárias no litoral paulista: linguagem, proposta, pilotos e argumentos b2b.",
  h1="Dossiê de conquista para pequenas imobiliárias no litoral paulista",
  hero="Dossiê comercial para pequenas imobiliárias no litoral: argumentos, proposta, ganho compartilhado e follow-up.",
  pills="📑 Dossiê,🧲 Conquista,🤝 B2B,🏖 Litoral SP,📈 Resultados",
  subject="Dossiê conquista pequenas imobiliarias litoral",
  cta1="✉️ Quero o dossiê",
  cta2="💬 WhatsApp",
  wa="Olá! Quero o dossiê de conquista para pequenas imobiliárias no litoral",
  content="\n".join([
    section("Conteúdo",
            "<p>Prepare um dossiê leve para pequenas imobiliárias do litoral com problema, solução, entrega e lista de perguntas frequentes. Use na primeira reunião ou follow-up.</p>"+cards([
              ("1. Problema","Contato demorado, SEO fraco, fraca captação."),
              ("2. Solução","IA leve: SEO, chatbot, follow-up."),
              ("3. Entrega","Piloto 30 dias sem taxa mínima."),
              ("4. Follow-up","1 e-mail + 1 WhatsApp por semana.")
            ])),
    section("Follow-up",
            "<ul><li>Resumo curto: objetivo + entrega + próximo passo</li><li>Perguntas para desbloquear orçamento e timing</li><li>Checklist mínimo de dados para iniciar</li><li>Proposta light por 3 opções: starter/growth/premium</li></ul>"),
    cta_block("Quero o dossiê de conquista",
              "Envie sua lista e geramos um dossiê personalizado por lead.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Dossiê pequenas imobiliarias','Quero o dossiê'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero dossiê de conquista para pequenas imobiliarias','WhatsApp')])
  ])
)

page(
  path="blog/dossie-conquista-corretores-autonomos-litoral-paulista.html",
  title="Dossiê de conquista para corretores autônomos no litoral paulista — Praia Digital",
  desc="Dossiê de conquista para corretores autônomos no litoral paulista: abordagem, scripts, oferta e follow-up.",
  h1="Dossiê de conquista para corretores autônomos no litoral paulista",
  hero="Abordagem comercial para corretores autônomos do litoral: script, follow-up, proposta light e ferramentas gratuitas.",
  pills="📑 Dossiê,🧲 Conquista,📸 Leads,🏖 Litoral SP,📈 Crescimento",
  subject="Dossiê conquista corretores autonomos litoral",
  cta1="✉️ Quero o dossiê",
  cta2="💬 WhatsApp",
  wa="Olá! Quero o dossiê de conquista para corretores autônomos",
  content="\n".join([
    section("Abordagem",
            "<p>Usar o dossiê para apresentar problema e solução claros. Destaque ferramentas gratuitas primeiro, depois o piloto leve.</p>"+cards([
              ("🎯 Problema","SEO e atendimento ruins no litoral."),
              ("🛠 Solução","IA leve com ferramentas gratuitas."),
              ("📈 Resultado","Leads locais e sem taxa alta."),
              ("🤝 Follow-up","E-mail + WhatsApp em 2 passos.")
            ])),
    section("Script rápido",
            "<blockquote>'Se você quer captar mais leads locais no litoral, começamos pelas ferramentas gratuitas e um piloto de 30 dias. Sem taxa mínima. Vamos?'</blockquote>"),
    cta_block("Quero o dossiê para corretores",
              "Geramos dossiê por cidade e nicho para primeiro contato.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Dossiê corretores autônomos litoral','Quero dossiê para corretores'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero dossiê corretores autônomos litoral','WhatsApp')])
  ])
)

page(
  path="blog/marketing-digital-imobiliaria-litoral-paulista.html",
  title="Marketing digital para imobiliária no litoral paulista — guia completo — Praia Digital",
  desc="Marketing digital para imobiliária no litoral paulista: SEO, conteúdo, redes sociais, automação e parcerias.",
  h1="Marketing digital para imobiliária no litoral paulista",
  hero="Guia completo de marketing digital para imobiliária no litoral paulista: SEO, conteúdo, anúncios e automação leve.",
  pills="📣 Marketing digital,🌐 SEO local,📝 Conteúdo,🎯 Anúncios,🤖 Automação leve",
  subject="Marketing digital imobiliaria litoral",
  cta1="✉️ Quero o guia",
  cta2="💬 WhatsApp",
  wa="Olá! Quero o guia de marketing digital para minha imobiliaria no litoral",
  content="\n".join([
    section("Pilares",
            "<p>Combine SEO, conteúdo e automação para anunciar e vender mais no litoral com performance mensurável.</p>"+cards([
              ("🔍 SEO","Páginas por cidade + FAQ estruturado."),
              ("📝 Conteúdo","Bairro, temporada, avaliação."),
              ("💸 Anúncios","Copy, foco e CTA por temporada."),
              ("🤖 CRM","Follow-up, origem e status em 1 lugar.")
            ])),
    section("Orçamento sugerido",
            "<ul><li>Starter: ferramentas gratuitas + conteúdo semanal</li><li>Growth: SEO, chatbot e follow-up assistido</li><li>Premium: temporada inteira com anúncios e automação</li></ul>"),
    cta_block("Quero o guia de marketing digital",
              "Execute primeiro e depois cresça com IA.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Marketing digital imobiliaria','Quero o guia'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero marketing digital para minha imobiliaria','WhatsApp')])
  ])
)

page(
  path="blog/ia-para-investidores-litoral-paulista.html",
  title="IA para investidores no litoral paulista — dados, avaliação e ROI — Praia Digital",
  desc="IA para investidores no litoral paulista: avaliação automática, ROI, temporada e dados locais para decisão.",
  h1="IA para investidores no litoral paulista",
  hero="Decida melhor com dados: avaliação automática, projeção de temporada, ROI e relatórios loc prontos.",
  pills="📊 Dados,📈 ROI,🏖 Litoral SP,🏨 Temporada,🤖 Avaliação IA",
  subject="IA para investidores litoral paulista",
  cta1="✉️ Quero dados para decisão",
  cta2="💬 WhatsApp",
  wa="Olá! Quero dados e IA para investir no litoral paulista",
  content="\n".join([
    section("Decisão com dados",
            "<p>Com IA leve, investidores ganham clareza por cidade, bairro e temporada. Relatórios simples, sem taxa fixa.</p>"+cards([
              ("📊 Avaliação","Estimativa por cidade/bairro."),
              ("📈 ROI","Comparação por temporada e perfil."),
              ("🏨 Temporada","Projeção de preço e ocupação."),
              ("🧾 Relatórios","PDF pronto para decisão.")
            ])),
    section("Cenário",
            "<blockquote>Se você investe em imóveis para temporada, precisa de dados locais atualizados e conteúdo claro. IA leve entrega isso sem projeto longo.</blockquote>"),
    cta_block("Quero dados de decisão",
              "Sem taxa alta: primeiro insight rápido, depois relatório detalhado.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=IA para investidores litoral','Quero dados para decisão'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero dados e IA para investir no litoral','WhatsApp')])
  ])
)

page(
  path="blog/quero-crescer-com-ia.html",
  title="Quero crescer com IA no litoral paulista — começo rápido — Praia Digital",
  desc="Quero crescer com IA no litoral paulista: comece em 3 passos, sem taxa alta e sem rebuild.",
  h1="Quero crescer com IA no litoral paulista",
  hero="Comece em 3 passos: SEO por cidade, chatbot e follow-up. Sem rebuild, sem taxa alta e sem fidelidade longa.",
  pills="🚀 Crescimento,🤖 IA,📝 SEO,🏖 Litoral SP,⚡ Começo rápido",
  subject="Quero crescer com IA no litoral",
  cta1="✉️ Quero começar",
  cta2="💬 WhatsApp",
  wa="Olá! Quero crescer com IA no litoral",
  content="\n".join([
    section("3 passos",
            "<p>Comece por conteúdo, depois chatbot e depois follow-up. Em 30 dias você vê resultado e decide se cresce.</p>"+cards([
              ("1. Conteúdo","Página por cidade/bairro com keyword local."),
              ("2. Chatbot","FAQ, qualificação e agendamento rápido."),
              ("3. Follow-up","Automação leve em 5 minutos."),
              ("4. Parcerias","Indicação com administradores e construtoras.")
            ])),
    section("Suporte",
            "<ul><li>Checklist gratuito</li><li>Piloto 30 dias</li><li>Ajuste semanal</li><li>Sem taxa mínima</li></ul>"),
    cta_block("Quero começar agora",
              "Comece leve e meça antes de crescer.",
              [('btn-primary','mailto:comercial@praiadigital.com?subject=Quero crescer com IA - litoral','Quero começar'),
               ('btn-purple','https://wa.me/5511954346288?text=Quero crescer com IA no litoral','WhatsApp')])
  ])
)

# Extra outreach email templates
outreach_templates = {
  "email-follow-up-b2b-litoral.md": """\
# Follow-up B2B para imobiliárias do litoral

Assunto: Segue aqui o próximo passo para crescer no litoral paulista com IA

Olá,

Tudo bem? Estava revisitando o mercado de imóveis no litoral e identifiquei uma oportunidade rápida para vocês:
- conteúdo por cidade/bairro para Google Maps
- chatbot 24h no site/residencial
- follow-up em 5 minutos

Proponho um piloto de 30 dias sem taxa mínima e sem fidelidade longa. Se não captar leads qualificados, não continuamos.

Site: https://praia.digital
Contato: (11) 95434-6288 | comercial@praiadigital.com
""",
  "email-proposta-compra-leve-imobiliaria-litoral.md": """\
# Proposta de compra leve para imobiliária no litoral

Assunto: Proposta prática: estre em SEO e chatbot sem taxa alta

Olá,

Fiz uma proposta simples para imobiliárias no litoral paulista que querem crescer rápido:
- Starter: conteúdo + SEO local + chatbot leve
- Growth: starter + automação + relatório semanal
- Premium: temporada inteira com anúncios com IA

Sem taxa mínima. Queremos resultados primeiro.

Contato: (11) 95434-6288 | comercial@praiadigital.com
""",
  "email-negociacao-renda-compartilhada-litoral.md": """\
# Negociação de ganho compartilhado no litoral

Assunto: Ganho compartilhado sem taxa fixa — proposta sem risco

Olá,

Podemos trabalhar juntos por ganho compartilhado:
- Praia Digital entrega conteúdo, SEO, chatbot e follow-up.
- Imobiliária fornece dados e aprova.
- Repartimos por leads qualificados ou contratos.

Sem taxa fixa obrigatória. Queremos resultados reais.

Contato: (11) 95434-6288 | comercial@praiadigital.com
""",
  "email-first-contact-imobiliaria-litoral.md": """\
# E-mail primeiro contato para imobiliária no litoral

Assunto: Captação de leads para imobiliária no litoral sem taxa mínima

Olá,

Sou a Carol, CEO da Praia Digital.

Ajudo imobiliárias e corretores do litoral paulista a captar mais leads com SEO local, conteúdo e automação leve. Quero propor um piloto de 30 dias para você: crescimento por resultado, sem taxa mínima e sem fidelidade longa.

Site: https://praia.digital

Queremos crescer juntos.

Contato: (11) 95434-6288 | comercial@praiadigital.com
""",
  "email-temporada-alta-litoral.md": """\
# E-mail para temporada alta no litoral

Assunto: Temporada alta no litoral — vamos captar leads?

Olá,

Temporada aproxima e leads somem por tempo de resposta lento. Vamos usar IA leve para antecipar captação e ocupação no litoral paulista:
- SEO por cidade e bairro
- Chatbot 24h
- Follow-up em 5 minutos

Sem taxa alta: primeiro piloto de 30 dias.

Site: https://praia.digital
Contato: (11) 95434-6288 | comercial@praiadigital.com
"""
}

for name, body in outreach_templates.items():
    p = docs_sales / name
    p.write_text(body, encoding="utf-8")
    print("OK", p.relative_to(praia))

print("Done B2B negotiation expansion")
