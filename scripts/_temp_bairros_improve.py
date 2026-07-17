from pathlib import Path

repo = Path('.')
bairros_dir = repo/'bairros'

pages = {
  'bertioga-riviera-de-sao-lourenco.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bertioga — Riviera de São Lourenço | Praia Digital</title>
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
  <h1>🏘️ Bertioga — Riviera de São Lourenço</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Bertioga / Riviera de São Lourenço</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 8.200</div>
      <div class="label">Valor de entrada médio: R$ 492.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+7,2% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Alto</div>
      <div class="label">Ocupação estimada: 75%-80% na temporada</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 420</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Predominam famílias de alta renda em busca de segunda residência e turistas de fim de semana. Também há movimento de investidores que compram unidades para temporada com expectativa de valorização acelerada.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Praia privada, loteamento fechado, mercados, farmácia, centro comercial e acesso fácil à rodovia. Resultado: menor percepção de risco e conveniência para famílias.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Perfil do bairro favorece imóveis com vaga, área de lazer, acabamento médio/alto e boa insolação. Para imobiliárias, o argumento de venda é mais segurança e exclusividade do que apenas localização.</p>
  </div>
</div>
<footer>
  <p>Bertioga / Riviera de São Lourenço | Praia Digital | 2026</p>
</footer>
</body>
</html>""",

  'bertioga-indaiá.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bertioga — Indaiá | Praia Digital</title>
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
  <h1>🏘️ Bertioga — Indaiá</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Bertioga / Indaiá</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 6.500</div>
      <div class="label">Valor de entrada médio: R$ 390.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+6,8% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Médio-Alto</div>
      <div class="label">Ocupação estimada: 65%-70%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 320</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Famílias de renda média-alta e locais, além de aposentados que preferem ambiente tranquilo próximo à praia. Há demanda por imóveis funcionais e com boa relação custo-benefício.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Praia tranquila, comércio local, escola, posto de saúde e transporte público regular. Equilíbrio entre sossego e conveniência para permanência prolongada.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Unidades com área externa, boa ventilação e proximidade de serviços públicos costumam ter maior liquidez. Para parceiros, o foco é praticidade e permanência fora do pico de verão.</p>
  </div>
</div>
<footer>
  <p>Bertioga / Indaiá | Praia Digital | 2026</p>
</footer>
</body>
</html>""",

  'bertioga-centro.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bertioga — Centro | Praia Digital</title>
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
  <h1>🏘️ Bertioga — Centro</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Bertioga / Centro</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 5.800</div>
      <div class="label">Valor de entrada médio: R$ 348.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+6,5% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Médio</div>
      <div class="label">Ocupação estimada: 55%-60%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 280</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Investidores e comerciantes que buscam presença urbana, além de população local interessada em moradia funcional perto de serviços essenciais.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Comércio completo, bancos, hospital, delegacia e acesso ferroviário. Acessibilidade e serviços concentrados aumentam a liquidez por conveniência.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Imóveis compactos, com garagem e boa insolação tendem a ser mais procurados. Posicionamento ideal para perfis voltados a yield/renda e não só veraneio.</p>
  </div>
</div>
<footer>
  <p>Bertioga / Centro | Praia Digital | 2026</p>
</footer>
</body>
</html>""",

  'bertioga-boraceia.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bertioga — Boraceia | Praia Digital</title>
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
  <h1>🏘️ Bertioga — Boraceia</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Bertioga / Boraceia</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 7.200</div>
      <div class="label">Valor de entrada médio: R$ 432.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+7,5% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Alto</div>
      <div class="label">Ocupação estimada: 70%-75%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 380</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Famílias de alta renda, veranistas e surfistas. Procura Selante: imóveis próximos ao mar e com menor densidade de ruas movimentadas.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Praia selvagem, pousadas, mercadinho, ponto de ônibus e trilhas. A infraestrutura combina atendimento turístico com acesso natural para quem busca experiências fora do padrão.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Boa combinação para vendas casuais e temporada curta. Anúncios que destacam experiência, natureza e privacidade costumam converter melhor.</p>
  </div>
</div>
<footer>
  <p>Bertioga / Boraceia | Praia Digital | 2026</p>
</footer>
</body>
</html>""",

  'bertioga-guaratuba.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bertioga — Guaratuba | Praia Digital</title>
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
  <h1>🏘️ Bertioga — Guaratuba</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Bertioga / Guaratuba</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 5.400</div>
      <div class="label">Valor de entrada médio: R$ 324.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+6,2% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Baixo-Médio</div>
      <div class="label">Ocupação estimada: 50%-55%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 250</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Trabalhadores locais e famílias de renda média que valorizam custo reduzido e acesso direto à praia pública. Perfil menos interessado em temporada curta e mais em uso contínuo.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Praia pública, mercado local, escola municipal e postinho de saúde. Serviços suficientes para uso cotidiano, mas não concentrados para público de alta renda.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Para corretores, o foco é entrada acessível e liquidez gradual. Para imobiliárias, pode ser um fluxo complementar se alinhado com atendimento local e documentação simplificada.</p>
  </div>
</div>
<footer>
  <p>Bertioga / Guaratuba | Praia Digital | 2026</p>
</footer>
</body>
</html>""",
}

for filename, content in pages.items():
    (bairros_dir / filename).write_text(content, encoding='utf-8')

print('bairros melhorados')
