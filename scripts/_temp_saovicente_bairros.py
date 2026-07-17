from pathlib import Path

repo = Path('.')
bairros_dir = repo/'bairros'

template = """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TITLE | Praia Digital</title>
<style>
  body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#1e293b;margin:0;padding:0}
  header{background:linear-gradient(135deg,#0a1628,#1e3a5f);color:#fff;padding:2rem 1rem;text-align:center}
  header h1{margin:0;font-size:2rem}
  .container{max-width:1000px;margin:0 auto;padding:2rem 1rem}
  .breadcrumb{font-size:.9rem;color:#64748b;margin-bottom:1rem}
  .breadcrumb a{color:#2563eb;text-decoration:none}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem;margin-bottom:2rem}
  .card{background:#fff;border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}
  .card h3{margin:0 0 .5rem;color:#0a1628;font-size:1.05rem}
  .value{font-size:1.6rem;font-weight:800;color:#2563eb}
  .label{font-size:.85rem;color:#64748b}
  .section{background:#fff;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}
  .section h2{color:#0a1628;margin:0 0 .75rem}
  .section p{color:#475569;line-height:1.7}
  footer{text-align:center;padding:2rem 1rem;color:#64748b;font-size:.85rem}
</style>
</head>
<body>
<header>
  <h1>TITLE_HEADER</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / BREADCRUMB</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">PRECO</div>
      <div class="label">ENTRADA</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">VALORIZACAO</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">AIRBNB_LEVEL</div>
      <div class="label">AIRBNB_DETAIL</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">DIARIA</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>PERFIL</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>INFRA</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>DIFERENCIAIS</p>
  </div>
</div>
<footer>
  <p>FOOTER</p>
</footer>
</body>
</html>"""

bairros = {
  'saovicente-centro': {
    'title': 'São Vicente — Centro | Praia Digital',
    'header': '🏘️ São Vicente — Centro',
    'breadcrumb': 'São Vicente / Centro',
    'preco': 'R$ 5.400',
    'entrada': 'Valor de entrada médio: R$ 324.000',
    'valorizacao': '+6,7% ao ano',
    'airbnb_level': 'Médio',
    'airbnb_detail': 'Ocupação estimada: 62%-68%',
    'diaria': 'R$ 280',
    'perfil': 'Moradores locais, comerciantes e investidores.',
    'infra': 'Centro comercial, bancos, supermercados e acessos.',
    'diferenciais': 'Perfil prático com fluxo regular de serviços.',
    'footer': 'São Vicente / Centro | Praia Digital | 2026'
  },
  'saovicente-gonzaguinha': {
    'title': 'São Vicente — Gonzaguinha | Praia Digital',
    'header': '🏘️ São Vicente — Gonzaguinha',
    'breadcrumb': 'São Vicente / Gonzaguinha',
    'preco': 'R$ 5.900',
    'entrada': 'Valor de entrada médio: R$ 354.000',
    'valorizacao': '+6,9% ao ano',
    'airbnb_level': 'Médio alto',
    'airbnb_detail': 'Ocupação estimada: 66%-70%',
    'diaria': 'R$ 290',
    'perfil': 'Famílias e jovens casais.',
    'infra': 'Praia acessível, transporte e comércio.',
    'diferenciais': 'Atende perf
