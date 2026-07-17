from pathlib import Path

repo = Path('.')
bairros_dir = repo/'bairros'
bairros_dir.mkdir(exist_ok=True)

# Santos bairros
bairros = {
  'santos-gonzaga': {
    'nome': 'Gonzaga',
    'preco_m2': 7600,
    'perfil_compradores': 'Famílias de renda média-alta, profissionais liberais, segunda residência',
    'potencial_airbnb': 'Médio alto - 70% temporada, diária R$ 320',
    'valorizacao': '+6.0% ao ano',
    'infraestrutura': 'Comércio movimentado, praia, transporte, bancos, cinema, farmácias'
  },
  'santos-boqueirao': {
    'nome': 'Boqueirão',
    'preco_m2': 8800,
    'perfil_compradores': 'Alta renda, investidores, turistas de temporada',
    'potencial_airbnb': 'Alto - 75-80% temporada, diária R$ 420',
    'valorizacao': '+6.8% ao ano',
    'infraestrutura': 'Orla badalada, restaurantes, hotéis, calçadão, ciclovia'
  },
  'santos-centro': {
    'nome': 'Centro Histórico',
    'preco_m2': 5800,
    'perfil_compradores': 'Investidores, comerciantes, população local',
    'potencial_airbnb': 'Médio - 58-65% temporada, diária R$ 260',
    'valorizacao': '+5.5% ao ano',
    'infraestrutura': 'Museu, teatros, comércio tradicional, mercado, transporte ferroviário'
  },
  'santos-pompeia': {
    'nome': 'Pompeia',
    'preco_m2': 6200,
    'perfil_compradores': 'Profissionais liberais, famílias, aposentados',
    'potencial_airbnb': 'Médio - 55-60% temporada, diária R$ 240',
    'valorizacao': '+5.8% ao ano',
    'infraestrutura': 'Praia tranquila, restaurantes, mercados, posto de saúde, escolas'
  },
  'santos-embare': {
    'nome': 'Embaré',
    'preco_m2': 6800,
    'perfil_compradores': 'Famílias de renda média, segunda residência, investidores conservadores',
    'potencial_airbnb': 'Médio - 60-65% temporada, diária R$ 260',
    'valorizacao': '+6.2% ao ano',
    'infraestrutura': 'Orla, mercados, padarias, supermercados, farmácia, transporte público'
  }
}

for slug, bairro in bairros.items():
    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Santos — {bairro['nome']} | Praia Digital</title>
<style>
  body{{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#1e293b;margin:0;padding:0}}
  header{{background:linear-gradient(135deg,#0a1628,#1e3a5f);color:#fff;padding:2rem 1rem;text-align:center}}
  header h1{{margin:0;font-size:2rem}}
  .container{{max-width:1000px;margin:0 auto;padding:2rem 1rem}}
  .breadcrumb{{font-size:.9rem;color:#64748b;margin-bottom:1rem}}
  .breadcrumb a{{color:#2563eb;text-decoration:none}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem;margin-bottom:2rem}}
  .card{{background:#fff;border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
  .card h3{{margin:0 0 .5rem;color:#0a1628;font-size:1.05rem}}
  .value{{font-size:1.6rem;font-weight:800;color:#2563eb}}
  .label{{font-size:.85rem;color:#64748b}}
  .section{{background:#fff;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
  .section h2{{color:#0a1628;margin:0 0 .75rem}}
  .section p{{color:#475569;line-height:1.7}}
  footer{{text-align:center;padding:2rem 1rem;color:#64748b;font-size:.85rem}}
</style>
</head>
<body>
<header>
  <h1>🏘️ Santos — {bairro['nome']}</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Santos / {bairro['nome']}</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ {bairro['preco_m2']:,}</div>
      <div class="label">Valor de entrada médio: R$ {bairro['preco_m2']*60:,}</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">{bairro['valorizacao']}</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">{bairro['potencial_airbnb'].split(' - ')[0]}</div>
      <div class="label">{bairro['potencial_airbnb'].split(' - ')[1]}</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">{bairro['potencial_airbnb'].split('R$ ')[-1] if 'R$ ' in bairro['potencial_airbnb'] else '-'}</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>{bairro['perfil_compradores']}</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>{bairro['infraestrutura']}</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Posicionamento único do bairro influencia o tipo de imóvel que converte mais. Para parceiros, destacar conveniência, reputação do entorno e identidade local costuma aumentar tempo de fechamento.</p>
  </div>
</div>
<footer>
  <p>Santos / {bairro['nome']} | Praia Digital | 2026</p>
</footer>
</body>
</html>"""
    (bairros_dir / f'{slug}.html').write_text(html, encoding='utf-8')

print('bairros de santos criados')
