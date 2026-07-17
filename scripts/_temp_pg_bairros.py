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
  'praia-grande-guartuba': {
    'title': 'Praia Grande — Guaratuba | Praia Digital',
    'header': '🏘️ Praia Grande — Guaratuba',
    'breadcrumb': 'Praia Grande / Guaratuba',
    'preco': 'R$ 5.200',
    'entrada': 'Valor de entrada médio: R$ 312.000',
    'valorizacao': '+7,8% ao ano',
    'airbnb_level': 'Alto',
    'airbnb_detail': 'Ocupação estimada: 72%-76%',
    'diaria': 'R$ 270',
    'perfil': 'Famílias de classe média, jovens casais e pequenos investidores.',
    'infra': 'Praia ampla, comércio de bairro, escolas, posto de saúde e conectividade viária em expansão.',
    'diferenciais': 'Volume alto de turistas de verão com procura por imóveis compactos e funcionais.',
    'footer': 'Praia Grande / Guaratuba | Praia Digital | 2026'
  },
  'praia-grande-ocian': {
    'title': 'Praia Grande — Ocian | Praia Digital',
    'header': '🏘️ Praia Grande — Ocian',
    'breadcrumb': 'Praia Grande / Ocian',
    'preco': 'R$ 5.600',
    'entrada': 'Valor de entrada médio: R$ 336.000',
    'valorizacao': '+7,5% ao ano',
    'airbnb_level': 'Alto',
    'airbnb_detail': 'Ocupação estimada: 70%-75%',
    'diaria': 'R$ 290',
    'perfil': 'População residente em crescimento, famílias e investidores de entrada.',
    'infra': 'Orla ativa, supermercados, escolas, transporte e ciclovia.',
    'diferenciais': 'Boa combinação entre custo e densidade de services, com rotatividade elevada.',
    'footer': 'Praia Grande / Ocian | Praia Digital | 2026'
  },
  'praia-grande-vila-caiçara': {
    'title': 'Praia Grande — Vila Caiçara | Praia Digital',
    'header': '🏘️ Praia Grande — Vila Caiçara',
    'breadcrumb': 'Praia Grande / Vila Caiçara',
    'preco': 'R$ 5.900',
    'entrada': 'Valor de entrada médio: R$ 354.000',
    'valorizacao': '+7,6% ao ano',
    'airbnb_level': 'Médio alto',
    'airbnb_detail': 'Ocupação estimada: 68%-72%',
    'diaria': 'R$ 285',
    'perfil': 'Famílias de renda média que buscam tranquilidade sem se afastar da infraestrutura.',
    'infra': 'Praia, área de lazer, comércio local e transporte.',
    'diferenciais': 'Perfil estável e boa retenção de compradores para corretores locais.',
    'footer': 'Praia Grande / Vila Caiçara | Praia Digital | 2026'
  },
  'praia-grande-solemar': {
    'title': 'Praia Grande — Solemar | Praia Digital',
    'header': '🏘️ Praia Grande — Solemar',
    'breadcrumb': 'Praia Grande / Solemar',
    'preco': 'R$ 6.100',
    'entrada': 'Valor de entrada médio: R$ 366.000',
    'valorizacao': '+7,3% ao ano',
    'airbnb_level': 'Alto',
    'airbnb_detail': 'Ocupação estimada: 70%-74%',
    'diaria': 'R$ 300',
    'perfil': 'Famílias e pequenos investidores em busca de estabilidade e valorização.',
    'infra': 'Praia, Mercado Extra, padarias, escolas e acesso rodoviário.',
    'diferenciais': 'Crescimento de oferta imobiliária com foco em liquidez.',
    'footer': 'Praia Grande / Solemar | Praia Digital | 2026'
  },
  'praia-grande-samambaia': {
    'title': 'Praia Grande — Samambaia | Praia Digital',
    'header': '🏘️ Praia Grande — Samambaia',
    'breadcrumb': 'Praia Grande / Samambaia',
    'preco': 'R$ 5.400',
    'entrada': 'Valor de entrada médio: R$ 324.000',
    'valorizacao': '+7,1% ao ano',
    'airbnb_level': 'Médio',
    'airbnb_detail': 'Ocupação estimada: 64%-68%',
    'diaria': 'R$ 260',
    'perfil': 'População local, jovens e famílias pequenas.',
    'infra': 'Praia, comércio popular, mercados e transporte local.',
    'diferenciais': 'Ótimo para captação recorrente por custo reduzido e demanda contínua.',
    'footer': 'Praia Grande / Samambaia | Praia Digital | 2026'
  }
}

for slug, data in bairros.items():
    text = (
        template
        .replace('TITLE', data['title'])
        .replace('TITLE_HEADER', data['header'])
        .replace('BREADCRUMB', data['breadcrumb'])
        .replace('PRECO', data['preco'])
        .replace('ENTRADA', data['entrada'])
        .replace('VALORIZACAO', data['valorizacao'])
        .replace('AIRBNB_LEVEL', data['airbnb_level'])
        .replace('AIRBNB_DETAIL', data['airbnb_detail'])
        .replace('DIARIA', data['diaria'])
        .replace('PERFIL', data['perfil'])
        .replace('INFRA', data['infra'])
        .replace('DIFERENCIAIS', data['diferenciais'])
        .replace('FOOTER', data['footer'])
    )
    (bairros_dir / f'{slug}.html').write_text(text, encoding='utf-8')

print('bairros de praia grande criados')
