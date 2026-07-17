from pathlib import Path

repo = Path('.')
bairros_dir = repo/'bairros'
bairros_dir.mkdir(exist_ok=True)

pages = {
  'peruibe-centro.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Peruibe — Centro | Praia Digital</title>
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
  <h1>🏘️ Peruíbe — Centro</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Peruíbe / Centro</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 6.800</div>
      <div class="label">Valor de entrada médio: R$ 408.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+7,9% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Médio</div>
      <div class="label">Ocupação estimada: 62%-66%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 240</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Famílias e investidores que buscam custo-benefício com potencial de valorização.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Comércio local, acesso às praias e serviços urbanos consolidados.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Bom ponto de entrada para investidores em fase inicial.</p>
  </div>
</div>
<footer>
  <p>Peruíbe / Centro | Praia Digital | 2026</p>
</footer>
</body>
</html>""",
  'peruibe-jardim-peruibe.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Peruibe — Jardim Peruibe | Praia Digital</title>
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
  <h1>🏘️ Peruíbe — Jardim Peruíbe</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Peruíbe / Jardim Peruíbe</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 7.200</div>
      <div class="label">Valor de entrada médio: R$ 432.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+8,1% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Alto</div>
      <div class="label">Ocupação estimada: 70%-74%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 260</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Investidores e veranistas com foco em rentabilidade de temporada.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Área turística consolidada, serviços de apoio à temporada.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Alta procura no verão e retorno locação acima da média da região.</p>
  </div>
</div>
<footer>
  <p>Peruíbe / Jardim Peruíbe | Praia Digital | 2026</p>
</footer>
</body>
</html>""",
  'peruibe-balneario.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Peruibe — Balneario | Praia Digital</title>
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
  <h1>🏘️ Peruíbe — Balneário</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Peruíbe / Balneário</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 8.100</div>
      <div class="label">Valor de entrada médio: R$ 486.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+8,4% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Alto</div>
      <div class="label">Ocupação estimada: 72%-76%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 280</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Investidores focados em temporada e retorno de aluguel.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Orla movimentada, serviços turísticos, comércio e lazer.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Alta demanda sazonal e potencial de rentabilidade comprovada.</p>
  </div>
</div>
<footer>
  <p>Peruíbe / Balneário | Praia Digital | 2026</p>
</footer>
</body>
</html>""",
  'peruibe-indaia.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Peruibe — Indaia | Praia Digital</title>
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
  <h1>🏘️ Peruíbe — Indaiá</h1>
  <p>Análise por bairro | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="breadcrumb"><a href="/praia-digital/">Home</a> / Peruíbe / Indaiá</div>
  <div class="grid">
    <div class="card">
      <h3>Preço médio do m²</h3>
      <div class="value">R$ 7.500</div>
      <div class="label">Valor de entrada médio: R$ 450.000</div>
    </div>
    <div class="card">
      <h3>Valorização</h3>
      <div class="value">+7,6% ao ano</div>
      <div class="label">Comparado ao ano anterior</div>
    </div>
    <div class="card">
      <h3>Potencial Airbnb</h3>
      <div class="value">Médio-Alto</div>
      <div class="label">Ocupação estimada: 66%-70%</div>
    </div>
    <div class="card">
      <h3>Diária média</h3>
      <div class="value">R$ 250</div>
      <div class="label">Referência temporada alta</div>
    </div>
  </div>
  <div class="section">
    <h2>Perfil dos compradores</h2>
    <p>Famílias e casais que buscam tranquilidade e proximidade com a praia.</p>
  </div>
  <div class="section">
    <h2>Infraestrutura</h2>
    <p>Bairro tranquilo, comércio próximo e boa acessibilidade.</p>
  </div>
  <div class="section">
    <h2>Diferenciais de negócio</h2>
    <p>Perfil estável com crescimento constante em temporadas.</p>
  </div>
</div>
<footer>
  <p>Peruíbe / Indaiá | Praia Digital | 2026</p>
</footer>
</body>
</html>""",
}

for name, html in pages.items():
  (bairros_dir / name).write_text(html, encoding='utf-8')

print('bairros de peruibe criados')
