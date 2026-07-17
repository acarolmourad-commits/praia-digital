from pathlib import Path
from datetime import datetime

repo = Path('.')
exclusivos = repo/'exclusivos'
exclusivos.mkdir(exist_ok=True)

# Estudo de cidade exemplo: Santos
estudo_santos = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Estudo de Cidade — Santos 2026 | Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .study-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
  .study-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .study-card h3 { margin: 0 0 0.5rem; color: #0a1628; }
  .study-card .value { font-size: 1.75rem; font-weight: 700; color: #2563eb; }
  .study-card .label { font-size: 0.85rem; color: #64748b; }
  .analysis { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .analysis h2 { color: #0a1628; margin: 0 0 1rem; }
  .analysis p { color: #475569; line-height: 1.7; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>📋 Estudo de Cidade — Santos 2026</h1>
  <p>Análise exclusiva Praia Digital</p>
</header>
<div class="container">
  <div class="study-grid">
    <div class="study-card">
      <h3>Valorização 12m</h3>
      <div class="value">+5.2%</div>
      <div class="label">Mercado em estabilidade</div>
    </div>
    <div class="study-card">
      <h3>ROI Airbnb</h3>
      <div class="value">5.8%</div>
      <div class="label">Ocupação: 68%</div>
    </div>
    <div class="study-card">
      <h3>Diária Média</h3>
      <div class="value">R$ 380</div>
      <div class="label">Alta temporada: R$ 520</div>
    </div>
    <div class="study-card">
      <h3>Imóveis Vendidos</h3>
      <div class="value">1.240</div>
      <div class="label">Últimos 12 meses</div>
    </div>
  </div>
  <div class="analysis">
    <h2>Análise de Mercado</h2>
    <p>Santos mantém-se como referência imobiliária no Litoral SP, com mercado mais maduro e liquidez alta. O preço médio de R$ 8.200/m² reflete infraestrutura consolidada e forte procura por imóveis na orla.</p>
    <p>A rentabilidade Airbnb é mais baixa que em cidades vizinhas, mas compensa com volume elevado de turistas e menor sazonalidade. Indicado para perfis conservadores e imobiliárias que buscam previsibilidade.</p>
  </div>
  <div class="analysis">
    <h2>Recomendações</h2>
    <p>Para investidores: atenção a imóveis reformados na orla; para corretores: captação de parcerias com construtoras de médio porte; para proprietários: profissionalização da gestão aumenta ocupação em até 12%.</p>
  </div>
</div>
<footer>
  <p>Estudo Exclusivo Praia Digital | Santos | """ + datetime.now().strftime('%d/%m/%Y') + """</p>
</footer>
</body>
</html>"""

(exclusivos/'estudo-santos-2026.html').write_text(estudo_santos, encoding='utf-8')

# Conteúdo recorrente: feed semanal
conteudo_recorrente = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Conteúdo Recorrente — Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1000px; margin: 0 auto; padding: 2rem 1rem; }
  .feed-item { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .feed-item h2 { margin: 0 0 0.5rem; color: #0a1628; }
  .feed-item p { color: #64748b; line-height: 1.6; }
  .feed-item .meta { font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>📰 Conteúdo Recorrente</h1>
  <p>Atualizações semanais do mercado imobiliário do Litoral</p>
</header>
<div class="container">
  <div class="feed-item">
    <h2>📊 Dados da Semana: valorização em destaque</h2>
    <p>Peruíbe mantém a maior valorização do Litoral SP nos últimos 12 meses, com +8.9%. Acompanhe o relatório completo para entender por que a cidade está atraindo investidores de todo o estado.</p>
    <div class="meta">Publicado em """ + datetime.now().strftime('%d/%m/%Y') + """ | Categoria: Mercado</div>
  </div>
  <div class="feed-item">
    <h2>🏆 Rankings atualizados</h2>
    <p>Os rankings exclusivos Praia Digital foram atualizados com novos dados de ocupação e diária média. Veja quais cidades estão no topo em ROI Airbnb e valorização.</p>
    <div class="meta">Publicado em """ + datetime.now().strftime('%d/%m/%Y') + """ | Categoria: Rankings</div>
  </div>
  <div class="feed-item">
    <h2>🗺️ Mapa Inteligente: novas camadas</h2>
    <p>Adicionamos informações de gastronomia, transporte, parques e parceiros no Mapa Inteligente. Use as camadas para planejar investimentos com dados reais da região.</p>
    <div class="meta">Publicado em """ + datetime.now().strftime('%d/%m/%Y') + """ | Categoria: Ferramentas</div>
  </div>
</div>
<footer>
  <p>Conteúdo Recorrente Praia Digital | """ + datetime.now().strftime('%d/%m/%Y') + """</p>
</footer>
</body>
</html>"""

(exclusivos/'conteudo-rec-2026.html').write_text(conteudo_recorrente, encoding='utf-8')

# Comunidade
comunidade = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Comunidade Praia Digital — Corretores e Investidores</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .community-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
  .community-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .community-card h3 { margin: 0 0 0.75rem; color: #0a1628; }
  .community-card p { color: #64748b; line-height: 1.6; }
  .benefits { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .benefits h2 { color: #0a1628; margin: 0 0 1rem; }
  .benefits ul { color: #475569; line-height: 1.8; padding-left: 1.25rem; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>🤝 Comunidade Praia Digital</h1>
  <p>Espaço exclusivo para corretores, investidores e parceiros do mercado imobiliário do Litoral</p>
</header>
<div class="container">
  <div class="community-grid">
    <div class="community-card">
      <h3>👥 Corretores Parceiros</h3>
      <p>Acesso a ferramentas de prospecção, CRM integrado e indicações exclusivas. Cresça sua carteira com leads qualificados.</p>
    </div>
    <div class="community-card">
      <h3>💰 Investidores</h3>
      <p>Relatórios exclusivos, simuladores de rendimento e análises de ROI. Dados proprietários do Litoral SP.</p>
    </div>
    <div class="community-card">
      <h3>🏗️ Construtoras</h3>
      <p>Visibilidade para novos empreendimentos, integração com unidades em lançamento e acesso a compradores qualificados.</p>
    </div>
    <div class="community-card">
      <h3>🏠 Proprietários</h3>
      <p>Ferramentas para gestão de temporada, dicas de Airbnb e conexão com hóspedes qualificados.</p>
    </div>
  </div>
  <div class="benefits">
    <h2>Benefícios Exclusivos</h2>
    <ul>
      <li>Relatórios semanais de mercado com dados proprietários</li>
      <li>Rankings atualizados de ROI, valorização e volume de vendas</li>
      <li>Acesso antecipado a novas ferramentas e funcionalidades</li>
      <li>Networking com players do mercado imobiliário do Litoral</li>
      <li>Participação em estudos de caso e projetos-piloto</li>
      <li>Integração com hub Airbnb, PriceLabs e Stays</li>
    </ul>
  </div>
</div>
<footer>
  <p>Comunidade Praia Digital | """ + datetime.now().strftime('%d/%m/%Y') + """</p>
</footer>
</body>
</html>"""

(exclusivos/'comunidade-corretores-investidores.html').write_text(comunidade, encoding='utf-8')

print('estudos e comunidade criados')
