import os
from pathlib import Path

REPO = Path(r'C:/Users/Carolina/praia-digital')
BLOG_DIR = REPO / 'blog'
BLOG_DIR.mkdir(exist_ok=True)

topics = [
    "guia-completo-praia-grande-familia-2026",
    "ubatuba-trilhas-praias-guia-2026",
    "santos-orla-gastronomia-passeios-2026",
    "guaruja-ilha-panqueca-fim-semana-2026",
    "bertioga-riviera-sao-francisco-guia-2026",
    "peruibe-centro-historico-praias-2026",
    "itanhaem-centro-antigo-lagoa-2026",
    "mongagua-praias-familiares-2026",
    "sao-vicente-historico-monumentos-2026",
    "cabo-frio-roteiro-casais-2026",
    "buzios-praias-famosas-guia-2026",
    "arraial-do-cabo-mergulho-2026",
    "paraty-historico-ilhas-2026",
    "angra-dos-reis-ilha-grande-2026",
    "florianopolis-praias-guia-2026",
    "balneario-camboriu-compras-praia-2026",
    "bombinhas-natureza-mergulho-2026",
    "garopaca-surf-quietude-2026",
    "itajai-porto-gastronomia-2026"
]

state_map = {
    "praia-grande": "SP", "ubatuba": "SP", "santos": "SP", "guaruja": "SP", "bertioga": "SP", "peruibe": "SP", "itanhaem": "SP", "mongagua": "SP", "sao-vicente": "SP",
    "cabo-frio": "RJ", "buzios": "RJ", "arraial-do-cabo": "RJ", "paraty": "RJ", "angra-dos-reis": "RJ",
    "florianopolis": "SC", "balneario-camboriu": "SC", "bombinhas": "SC", "garopaca": "SC", "itajai": "SC"
}

today = "2026-07-14"
created = []
for topic in topics:
    city_key = topic.split('-')[0] if '-' in topic else topic
    state = state_map.get(city_key, 'SP')
    path = REPO / 'blog' / f"{topic}-{state.lower()}-{today}.html"
    if path.exists():
        continue
    title = topic.replace('-', ' ').title()
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Praia Digital</title>
<meta name="description" content="Guia completo sobre {title} em {state}. Dicas práticas, roteiros e ferramentas gratuitas para corretores e turistas.">
<style>
body{{font-family:Arial,sans-serif;background:#f4f6f9;margin:0;color:#1f2937;}}
.container{{max-width:800px;margin:0 auto;padding:2rem;}}
.header{{background:linear-gradient(135deg,#0a1628,#1a3a5c);color:#fff;padding:2rem;border-radius:12px;margin-bottom:1.5rem;text-align:center;}}
.article{{background:#fff;border-radius:12px;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);line-height:1.7;}}
h2{{color:#0a1628;margin-top:1.5rem;}}
ul,ol{{margin:.75rem 0;padding-left:1.25rem;}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div style="opacity:.8;font-size:.9rem;">Praia Digital · {today}</div>
    <h1>{title}</h1>
    <div style="opacity:.8;font-size:.9rem;">{state} • guia completo</div>
  </div>
  <article class="article">
    <p>Guia completo sobre <strong>{title}</strong> em <strong>{state}</strong>.</p>
    <h2>1. O que esperar</h2>
    <p>Em {state}, a oferta de lazer, imoveis e servicos cresce todo ano. Quem planeja com antecedencia aproveita mais e gasta menos.</p>
    <h2>2. Roteiro rapido</h2>
    <ol>
      <li>Escolha 2-3 atividades principais do dia.</li>
      <li>Reserve hospedagem na regiao central.</li>
      <li>Use transporte local ou aplicativo.</li>
      <li>Antecipe ingressos e tours.</li>
    </ol>
    <h2>3. Dicas praticas</h2>
    <ul>
      <li>Prefira baixa temporada para precos menores.</li>
      <li>Verifique avaliacoes recentes antes de fechar.</li>
      <li>Tenha alternativa de reserva para chuvas/alta temporada.</li>
    </ul>
    <h2>4. Ferramentas uteis</h2>
    <p>Use em <a href="https://praia.digital" target="_blank">https://praia.digital</a>.</p>
  </article>
</div>
</body>
</html>"""
    path.write_text(html, encoding='utf-8')
    created.append(str(path))

print(f"Criados {len(created)} artigos SEO novos")
for p in created[:10]:
    print("-", Path(p).name)
if len(created) > 10:
    print(f"... (+{len(created)-10})")
