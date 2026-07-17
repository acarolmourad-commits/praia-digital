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
  'guaruja-enseada': {
    'title': 'Guarujá — Enseada | Praia Digital',
    'header': '🏘️ Guarujá — Enseada',
    'breadcrumb': 'Guarujá / Enseada',
    'preco': 'R$ 7.200',
    'entrada': 'Valor de entrada médio: R$ 432.000',
    'valorizacao': '+7,0% ao ano',
    'airbnb_level': 'Alto',
    'airbnb_detail': 'Ocupação estimada: 75%-80% na temporada',
    'diaria': 'R$ 400',
    'perfil': 'Turistas e famílias de renda média-alta em busca de segunda residência na orla.',
    'infra': 'Orla movimentada, restaurantes, mercados, hotéis e centro comercial com fácil acesso à navegação.',
    'diferenciais': 'A Enseada combina visibilidade turística com estrutura urbana consolidada. Corretor: valorize proximidade do mar e conveniência. Investidor: temporada forte com fluxo alto de hóspedes.',
    'footer': 'Guarujá / Enseada | Praia Digital | 2026'
  },
  'guaruja-guaruja-mirim': {
    'title': 'Guarujá — Guarujá Mirim | Praia Digital',
    'header': '🏘️ Guarujá — Guarujá Mirim',
    'breadcrumb': 'Guarujá / Guarujá Mirim',
    'preco': 'R$ 6.500',
    'entrada': 'Valor de entrada médio: R$ 390.000',
    'valorizacao': '+6,5% ao ano',
    'airbnb_level': 'Médio',
    'airbnb_detail': 'Ocupação estimada: 60%-65%',
    'diaria': 'R$ 280',
    'perfil': 'Trabalhadores locais, famílias em crescimento e público que valoriza acesso à praia.',
    'infra': 'Praia, mercado local, padarias, transporte público e caminhabilidade razoável até a orla.',
    'diferenciais': 'Bom para fluxo contínuo e não só temporada curta. Destaque custo-benefício e liquidez gradual para corretores.',
    'footer': 'Guarujá / Guarujá Mirim | Praia Digital | 2026'
  },
  'guaruja-vila-lucy': {
    'title': 'Guarujá — Vila Lucy | Praia Digital',
    'header': '🏘️ Guarujá — Vila Lucy',
    'breadcrumb': 'Guarujá / Vila Lucy',
    'preco': 'R$ 5.800',
    'entrada': 'Valor de entrada médio: R$ 348.000',
    'valorizacao': '+6,0% ao ano',
    'airbnb_level': 'Baixo-Médio',
    'airbnb_detail': 'Ocupação estimada: 50%-55%',
    'diaria': 'R$ 250',
    'perfil': 'População local, jovens casais e aposentados que buscam custo menor e rotina mais sossegada.',
    'infra': 'Comércio popular, praia, escolas, posto de saúde e ruas residenciais com pouco ruído.',
    'diferenciais': 'Ponto de entrada acessível pode funcionar como porta para aumento de patrimônio com tempo.',
    'footer': 'Guarujá / Vila Lucy | Praia Digital | 2026'
  },
  'guaruja-vila-maheta': {
    'title': 'Guarujá — Vila Maheta | Praia Digital',
    'header': '🏘️ Guarujá — Vila Maheta',
    'breadcrumb': 'Guarujá / Vila Maheta',
    'preco': 'R$ 6.200',
    'entrada': 'Valor de entrada médio: R$ 372.000',
    'valorizacao': '+6,4% ao ano',
    'airbnb_level': 'Médio',
    'airbnb_detail': 'Ocupação estimada: 60%',
    'diaria': 'R$ 290',
    'perfil': 'Famílias de renda média e profissionais liberais que buscam equilíbrio entre custo e qualidade.',
    'infra': 'Praia acessível, comércio local, farmácias, mercados, transporte público e escolas.',
    'diferenciais': 'Combinação de perfil estável e custo menor que a orla principal. Posicionamento bom para captação recorrente.',
    'footer': 'Guarujá / Vila Maheta | Praia Digital | 2026'
  },
  'guaruja-penteado': {
    'title': 'Guarujá — Penteado | Praia Digital',
    'header': '🏘️ Guarujá — Penteado',
    'breadcrumb': 'Guarujá / Penteado',
    'preco': 'R$ 7.800',
    'entrada': 'Valor de entrada médio: R$ 468.000',
    'valorizacao': '+7,2% ao ano',
    'airbnb_level': 'Médio alto',
    'airbnb_detail': 'Ocupação estimada: 70%',
    'diaria': 'R$ 360',
    'perfil': 'Alta renda, segunda residência e veranistas que preferem menor aglomeração e experiência mais exclusiva.',
    'infra': 'Praia exclusiva, loteamentos com privacidade, padarias finas, comércio seletivo e boa acessibilidade.',
    'diferenciais': 'Perfil premium favorece imóveis com acabamento médio/alto e experiência. Corretor: destaque exclusividade e tranquilidade.',
    'footer': 'Guarujá / Penteado | Praia Digital | 2026'
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

print('bairros de guaruja criados')
