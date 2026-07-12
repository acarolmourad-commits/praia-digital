import os
from pathlib import Path

REPO = Path(r'C:/Users/Carolina/praia-digital')
BLOG_DIR = REPO / 'blog'
os.makedirs(BLOG_DIR, exist_ok=True)

# Fresh SEO topics focused on conversion funnels and bot traffic
topics = [
    "funil de vendas para imobiliarias pequenas litoral paulista",
    "chatbot para imoveis primeira mensagem ideal modelo 2026",
    "captacao leads sem anuncios para corretores verao 2026",
    "checklist de visita tecnica imovel litoral corretores 2026",
    "roteiro de video imobiliario 1 minuto para redes sociais 2026",
    "avaliacao de imoveis automatizada ferramenta gratuita litoral",
    "modelo de proposta de venda imovel temporada praia 2026",
    "onboarding rapido para novos parceiros imobiliarias digitais",
    "gestao de indicadores imobiliarios sem planilha complicada 2026",
    "roteiro de follow up por whatsapp para leads frios imobiliarios"
]

cities = ["Santos","Guarujá","Praia Grande","Ubatuba","São Vicente","Bertioga","Ilhabela","Peruíbe","Mongaguá","Itanhaém"]
today = "2026-07-12"

created = []
for i, topic in enumerate(topics):
    city = cities[i % len(cities)]
    clean = topic.replace(" 2026","").replace(" para "," em ")
    title = f"{clean.capitalize()} em {city}"
    slug = title.lower().replace(' ','-').replace('–','').replace('/','')
    path = BLOG_DIR / f"{slug}-{today}.html"
    if path.exists():
        continue
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Praia Digital</title>
<meta name="description" content="Conteudo pratico sobre {topic} em {city} para corretores e imobiliarias do litoral paulista.">
<style>
body{{font-family:Arial,sans-serif;background:#f4f6f9;margin:0;color:#1f2937;}}
.container{{max-width:800px;margin:0 auto;padding:2rem;}}
.header{{background:linear-gradient(135deg,#0a1628,#1a3a5c);color:#fff;padding:2rem;border-radius:12px;margin-bottom:1.5rem;text-align:center;}}
.article{{background:#fff;border-radius:12px;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);line-height:1.7;}}
h2{{color:#0a1628;margin-top:1.5rem;}}
ul{{margin:.75rem 0;padding-left:1.25rem;}}
.cta{{margin-top:2rem;background:linear-gradient(135deg,#00d4ff,#7b2ff7);color:#fff;padding:1rem;border-radius:8px;text-align:center;font-weight:700;display:inline-block;text-decoration:none;}}
.footer{{text-align:center;color:#6b7280;font-size:.9rem;margin-top:2rem;}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div style="opacity:.8;font-size:.9rem;">Praia Digital · {today}</div>
    <h1>{title}</h1>
    <div style="opacity:.8;font-size:.9rem;">{topic} • {city}</div>
  </div>
  <article class="article">
    <p>Guia pratico sobre <strong>{topic}</strong> em <strong>{city}</strong>: ideias prontas para usar na rotina de captacao, atendimento e fechamento.</p>
    <h2>1. O que funciona no verao</h2>
    <p>Em {city}, o volume de consultas cresce mais nos fins de semana. Responder Rapido, usar canal direto e repetir mensagem curta aumenta muito a taxa de resposta.</p>
    <h2>2. Modelos prontos</h2>
    <ul>
      <li><strong>Mensagem 1:</strong> apresentacao objetiva com 1 foto e 1 diferencial.</li>
      <li><strong>Mensagem 2:</strong> follow up com proposta de visita em 3 horarios.</li>
      <li><strong>Mensagem 3:</strong> alerta de urgencia e beneficios sociais.</li>
    </ul>
    <h2>3. Checklist rapido</h2>
    <ol>
      <li>Definir 3 imoveis destaque da semana</li>
      <li>Responder todos os leads ate 2h uteis</li>
      <li>Agendar visitas em horarios comerciais + noite</li>
      <li>Registrar status no funil simples</li>
    </ol>
    <h2>4. Automacao util</h2>
    <p>Use em <a href="https://praia.digital" target="_blank">https://praia.digital</a> as ferramentas de recomendacao, avaliacao e assistente virtual para ganhar tempo.</p>
    <a class="cta" href="https://praia.digital" target="_blank">Abrir ferramentas gratuitas</a>
  </article>
  <div class="footer">
    <p>Praia Digital · Conteudo para {city}</p>
    <p><a href="https://acarolmourad-commits.github.io/praia-digital/" target="_blank" style="color:#0a1628;">Site oficial</a></p>
  </div>
</div>
</body>
</html>"""
    path.write_text(html, encoding='utf-8')
    created.append(str(path))

print(f"Criados {len(created)} artigos SEO novos")
for p in created:
    print("-", Path(p).name)

