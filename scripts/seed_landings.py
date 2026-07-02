import os
from pathlib import Path

praia_root = Path(r"C:\Users\Carolina\praia-digital")
blog_dir = praia_root / "blog"
landing_dir = praia_root / "landing"
blog_dir.mkdir(exist_ok=True)
landing_dir.mkdir(exist_ok=True)

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

def cta(title,body,buttons):
    btns="".join(['<a class="btn '+b[0]+'" href="'+b[1]+'">'+b[2]+'</a>' for b in buttons])
    return s(title, '<div class="cta"><h2>Acelere seus resultados com IA</h2><p>'+body+'</p><div style="display:inline-flex;gap:1rem;flex-wrap:wrap;justify-content:center;">'+btns+'</div><p style="margin-top:1rem;opacity:.9;">Ferramentas e serviços gratuitos em: <a href="https://praia.digital" style="color:#fff;text-decoration:underline;">https://praia.digital</a></p></div>')

pages = []

pages.append(dict(
    path="blog/ia-para-administradores-imoveis-litoral.html",
    title="IA para administradores de imóveis no litoral — automatize temporada sem rebuild — Praia Digital",
    desc="IA para administradores de imóveis no litoral paulista: diminua operação, suba ocupação e melhore experiência com IA leve.",
    h1="IA para administradores de imóveis no litoral",
    hero="Administradores de imóveis no litoral ganham agilidade, reduzem custos e aumentam ocupação com automação leve por temporada.",
    pills="🤖 Automação leve,🤖 Chatbot 24h,📊 Relatórios,💬 Check-in/checkout,⭐ Avaliações automáticas",
    subject="Administradores de imóveis + IA",
    cta1="✉️ Quero automatizar",
    cta2="💬 WhatsApp",
    wa="Olá! Quero automatizar administração de imóveis no litoral",
    content="\n".join([
        s("Administradores de imóveis no litoral",
          "<p>Administradores enfrentam alta demanda em temporada, múltiplos canais e retenção clássica. IA automática melhora check-in, checkout, lembretes e avaliações SEM aumentar equipe.</p>" +
          cs([
            ("📋 Check-in/check-out","Lembretes automáticos por WhatsApp/e-mail e checklist digital."),
            ("⭐ Avaliações","Solicitações automáticas após estadia para aumentar recompra."),
            ("💸 Rentabilidade","Relatórios por temporada e por imóvel com dados de busca."),
            ("🤖 Chatbot","Responde dúvidas do hóspede 24h/7 sem equipe adicional.")
          ])),
        s("Execução sem rebuild",
          "<blockquote><strong>Implementação leve por imóvel</strong>: plano em 3 dias, sem substituir seu sistema atual. Use uma página web com automação se seu sistema atual não suportar integrações.</blockquote>"),
        cta("Quero automatizar administração de imóveis",
            "Vamos reduzir custos e aumentar avaliações e recompra no litoral.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Administradores de imóveis + IA","Quero automatizar administração"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero automatizar administração de imóveis","WhatsApp")])
    ])
))

pages.append(dict(
    path="blog/parceria-ganho-compartilhado-imobiliaria.html",
    title="Parceria com ganho compartilhado para imobiliária no litoral — Praia Digital",
    desc="Proposta de parceria com ganho compartilhado: imobiliária cresce vendas e aluguéis, Praia Digital ganha com desempenho.",
    h1="Parceria com ganho compartilhado para imobiliária no litoral",
    hero="Proposta de parceria sem taxa fixa obrigatória: cresça juntos, sem riscos, sem fidelidade longa e sem surpresas.",
    pills="🧪 Sem taxa fixa,📈 Performance por resultado,🏖 Litoral SP,🤖 IA leve,🍃 Agilidade",
    subject="Parceria ganho compartilhado imobiliaria",
    cta1="✉️ Quero negociação",
    cta2="💬 WhatsApp",
    wa="Olá! Quero negociar parceria de ganho compartilhado",
    content="\n".join([
        s("Por que ganho compartilhado faz sentido no litoral",
          "<p>Imobiliária libera recurso fixo e ganha uma parceira alinhada ao resultado. A Praia Digital ganha com crescimento real — sem taxa mínima obrigatória.</p>" +
          cs([
            ("🏁 Planejamento","Defina meta, sazonalidade, buyer persona e budget compatível."),
            ("📊 Conteúdo por cidade","SEO local e anúncios específicos por bairro para alta temporada."),
            ("🤖 Automação leve","Chatbot, follow-up, CRM básico e relatórios semanais."),
            ("💰 Repartição","Percentual por lead qualificado ou contrato, sem obrigação longa.")
          ])),
        s("Riscos e como mitigar",
          "<blockquote>Risco não é técnico, é operacional: se a imobiliária não enviar dados e fotos, o conteúdo sai genérico. Mitigamos com checklist de entrada e taxa mínima de material por semana. Zero surpresa.</blockquote>"),
        cta("Quero propor ganho compartilhado",
            "Sem taxa fixa, sem fidelidade longa: resultados primeiro.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Parceria ganho compartilhado imobiliaria","Propor ganho compartilhado"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero parceria ganho compartilhado","WhatsApp")])
    ])
))

pages.append(dict(
    path="blog/roi-ia-imobiliaria-litoral-paulista.html",
    title="ROI de IA para imobiliária no litoral paulista — cálculo prático — Praia Digital",
    desc="Calcule o ROI de IA para imobiliárias no litoral paulista com base em ticket médio, conversão e economia de anúncios.",
    h1="ROI de IA para imobiliária no litoral paulista",
    hero="Estime retorno com base em ticket médio, taxa de contato e taxa de conversão. ROI positivo costuma aparecer em 30 a 90 dias.",
    pills="📈 ROI,📊 Conversão,🧮 Cálculo,💡 Benchmark,🏖 Litoral SP",
    subject="ROI IA Imobiliária Litoral",
    cta1="✉️ Quero meu cálculo",
    cta2="💬 WhatsApp",
    wa="Olá! Quero calcular o ROI de IA para minha imobiliária",
    content="\n".join([
        s("ROI de IA no litoral paulista",
          "<p>ROI de IA depende de ticket médio, taxa de contato e taxa de conversão. Em pilotos, o retorno positivo costuma aparecer em 30 a 90 dias.</p>" +
          cs([
            ("📈 Aumento de contato","+15% a +35% com automação leve."),
            ("⏱ Menor tempo de resposta","de horas para minutos."),
            ("💵 Redução de custos","menos anúncios desperdiçados e mais fechamento."),
            ("🔁 Recompra","avaliações automáticas ajudam temporada seguinte.")
          ])),
        s("Cálculo simplificado",
          "<ul><li>Ticket médio: R$ 300k a R$ 700k para apartamentos no litoral</li><li>Custo médio de anúncio: R$ 600 a R$ 1.500/mês</li><li>Ganho com 1 venda/aluguel longo: até R$ 8.000+</li><li>Piloto com 1 ferramenta: custo baixo, upside alto</li></ul>"),
        cta("Quero calcular meu ROI",
            "Enviamos modelo pronto e benchmark por cidade para sua imobiliária.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=ROI - Imobiliaria IA litoral","Quero calcular ROI"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero calcular ROI da minha imobiliaria","WhatsApp")])
    ])
))

pages.append(dict(
    path="blog/consultoria-ia-imobiliaria-litoral-paulista-leve.html",
    title="Consultoria leve de IA para imobiliária no litoral paulista — sessão rápida e prática — Praia Digital",
    desc="Consultoria leve de IA para imobiliária no litoral: sessão prática, sem projeto longo, sem taxa fixa alta.",
    h1="Consultoria leve de IA para imobiliária no litoral paulista",
    hero="Sessão direcionada para definir ferramentas certas, prioridades e um cronograma 30 dias sem rebuild.",
    pills="🧠 Diagnóstico rápido,📋 Planejamento 30 dias,🏖 Litoral SP,🤖 IA aplicada,🚀 Execução ágil",
    subject="Consultoria leve IA imobiliaria",
    cta1="✉️ Quero uma sessão",
    cta2="💬 WhatsApp",
    wa="Olá! Quero uma sessão de consultoria leve de IA para minha imobiliária",
    content="\n".join([
        s("Consultoria leve de IA para imobiliárias",
          "<p>Alguns clientes precisam de decisão, não de projeto de 6 meses. Nossa consultoria é desenhada para desbloquear crescimento rápido no litoral.</p>" +
          cs([
            ("🔎 Mapeamento","Ferramentas que fazem sentido para sua realidade."),
            ("📋 Priorização","0 a 3 ações de maior impacto primeiro."),
            ("⚡ Execução ágil","Implementação leve, sem rebuild."),
            ("📈 Medição","KPIs claros para decidir se cresce.")
          ])),
        s("Entregáveis da sessão",
          "<ul><li>Diagnóstico por canal: site, WhatsApp, portais, anúncios</li><li>Mapa de ações rápidas: 5 melhorias startáveis em 7 dias</li><li>Lista de ferramentas gratuitas e pagas recomendadas</li><li>Plano de conteúdo por cidade/bairro para 30 dias</li></ul>"),
        cta("Quero uma sessão de consultoria",
            "Resposta em até 1 dia útil. Comece por WhatsApp ou e-mail.",
            [("btn-primary","mailto:comercial@praiadigital.com?subject=Consultoria leve IA - imobiliaria","Agendar consultoria leve"),
             ("btn-purple","https://wa.me/5511954346288?text=Quero consultoria leve de IA para imobiliaria","WhatsApp")])
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
    out = praia_root / p["path"]
    out.write_text(html, encoding="utf-8")
    print("OK", p["path"], len(html.splitlines()), "lines")
