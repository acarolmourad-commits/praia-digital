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
  'itanhaem-centro': {
    'title': 'Itanhaém — Centro | Praia Digital',
    'header': '🏘️ Itanhaém — Centro',
    'breadcrumb': 'Itanhaém / Centro',
    'preco': 'R$ 4.800',
    'entrada': 'Valor de entrada médio: R$ 288.000',
    'valorizacao': '+8,2% ao ano',
    'airbnb_level': 'Médio alto',
    'airbnb_detail': 'Ocupação estimada: 70%-74%',
    'diaria': 'R$ 260',
    'perfil': 'Jovens casais e investidores que buscam desempenho acima da média e menor custo de entrada.',
    'infra': 'Centro histórico, comércio, mercado, escolas e acesso fácil à orla.',
    'diferenciais': 'Alta valorização atrai olhares de fora; posicionamento como cidade emergente aumenta apelo.',
    'footer': 'Itanhaém / Centro | Praia Digital | 2026'
  },
  'itanhaem-gaivota': {
    'title': 'Itanhaém — Gaivota | Praia Digital',
    'header': '🏘️ Itanhaém — Gaivota',
    'breadcrumb': 'Itanhaém / Gaivota',
    'preco': 'R$ 5.200',
    'entrada': 'Valor de entrada médio: R$ 312.000',
    'valorizacao': '+8,4% ao ano',
    'airbnb_level': 'Alto',
    'airbnb_detail': 'Ocupação estimada: 72%-76%',
    'diaria': 'R$ 270',
    'perfil': 'Famílias e investidores com perfil de crescimento acelerado.',
    'infra': 'Praia ativa, mercados, padarias, escolas e transporte.',
    'diferenciais': 'Valorização acima da média com estrutura residencial consolidada.',
    'footer': 'Itanhaém / Gaivota | Praia Digital | 2026'
  },
  'itanhaem-jardim-grande': {
    'title': 'Itanhaém — Jardim Grande | Praia Digital',
    'header': '🏘️ Itanhaém — Jardim Grande',
    'breadcrumb': 'Itanhaém / Jardim Grande',
    'preco': 'R$ 5.000',
    'entrada': 'Valor de entrada médio: R$ 300.000',
    'valorizacao': '+8,1% ao ano',
    'airbnb_level': 'Médio',
    'airbnb_detail': 'Ocupação estimada: 66%-70%',
    'diaria': 'R$ 250',
    'perfil': 'População local e famílias que priorizam custo reduzido.',
    'infra': 'Praia, área residencial, mercado local, escolas.',
    'diferenciais': 'Perfil mais acessível e bom para captação contínua.',
    'footer': 'Itanhaém / Jardim Grande | Praia Digital | 2026'
  },
  'itanhaem-balneario-itapoan': {
    'title': 'Itanhaém — Balneário Itapoã | Praia Digital',
    'header': '🏘️ Itanhaém — Balneário Itapoã',
    'breadcrumb': 'Itanhaém / Balneário Itapoã',
    'preco': 'R$ 5.600',
    'entrada': 'Valor de entrada médio: R$ 336.000',
    'valorizacao': '+8,6% ao ano',
    'airbnb_level': 'Alto',
    'airbnb_detail': 'Ocupação estimada: 72%-75%',
    'diaria': 'R$ 275',
    'perfil': 'Veranistas e investidores que buscam área com potencial turístico.',
    'infra': 'Praia com serviços turísticos e incremento de comércio local.',
    'diferenciais': 'Valorização progressiva traz retorno mais rápido para imobiliárias parceiras.',
    'footer': 'Itanhaém / Balneário Itapoã | Praia Digital | 2026'
  },
  'itanhaem-avenida-pablo-neruda': {
    'title': 'Itanhaém — Avenida Pablo Neruda | Praia Digital',
    'header': '🏘️ Itanhaém — Avenida Pablo Neruda',
    'breadcrumb': 'Itanhaém / Avenida Pablo Neruda',
    'preco': 'R$ 5.400',
    'entrada': 'Valor de entrada médio: R$ 324.000',
    'valorizacao': '+8,3% ao ano',
    'airbnb_level': 'Médio alto',
    'airbnb_detail': 'Ocupação estimada: 70%-73%',
    'diaria': 'R$ 265',
    'perfil': 'Perfil emergente, jovens e profissionais liberais.',
    'infra': 'Rua movimentada, comércio próximo e acesso fácil à orla.',
    'diferenciais': 'Crescimento de procura por localização com identidade e serviços próximos.',
    'footer': 'Itanhaém / Avenida Pablo Neruda | Praia Digital | 2026'
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

print('bairros de itanhaem criados')
