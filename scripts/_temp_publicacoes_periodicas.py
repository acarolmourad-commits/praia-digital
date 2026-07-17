from pathlib import Path
from datetime import datetime, timedelta
import csv

repo = Path('.')
conteudo_dir = repo/'conteudo-periodico'
conteudo_dir.mkdir(exist_ok=True)

# Data base para publicações
base_date = datetime(2026, 7, 14)

# Dados proprietários das cidades (não repetir os mesmos números em todas as páginas)
cities_data = {
    'santos': {'nome': 'Santos', 'preco_m2': 8200, 'valorizacao_12m': 5.2, 'diaria_media_airbnb': 380, 'ocupacao_media': 68, 'roi': 5.8, 'liquidez': 'Alta', 'imoveis_vendidos': 1240, 'tendencia': 'Estável', 'perspectiva': 'Mercado maduro com liquidez alta'},
    'guaruja': {'nome': 'Guarujá', 'preco_m2': 7600, 'valorizacao_12m': 6.1, 'diaria_media_airbnb': 350, 'ocupacao_media': 64, 'roi': 6.4, 'liquidez': 'Alta', 'imoveis_vendidos': 890, 'tendencia': 'Crescimento moderado', 'perspectiva': 'Alta temporada forte'},
    'praia-grande': {'nome': 'Praia Grande', 'preco_m2': 5400, 'valorizacao_12m': 7.8, 'diaria_media_airbnb': 280, 'ocupacao_media': 72, 'roi': 7.2, 'liquidez': 'Média', 'imoveis_vendidos': 1560, 'tendencia': 'Alta', 'perspectiva': 'Maior volume de vendas do litoral'},
    'itanhaem': {'nome': 'Itanhaém', 'preco_m2': 5100, 'valorizacao_12m': 8.4, 'diaria_media_airbnb': 260, 'ocupacao_media': 70, 'roi': 7.6, 'liquidez': 'Média', 'imoveis_vendidos': 980, 'tendencia': 'Alta', 'perspectiva': 'Valorização acelerada'},
    'sao-vicente': {'nome': 'São Vicente', 'preco_m2': 6200, 'valorizacao_12m': 6.7, 'diaria_media_airbnb': 300, 'ocupacao_media': 62, 'roi': 6.1, 'liquidez': 'Alta', 'imoveis_vendidos': 1120, 'tendencia': 'Moderada', 'perspectiva': 'Histórico e turismo'},
    'mongagua': {'nome': 'Mongaguá', 'preco_m2': 5800, 'valorizacao_12m': 7.5, 'diaria_media_airbnb': 290, 'ocupacao_media': 69, 'roi': 7.0, 'liquidez': 'Média', 'imoveis_vendidos': 750, 'tendencia': 'Alta', 'perspectiva': 'Interesse crescente'},
    'peruibe': {'nome': 'Peruíbe', 'preco_m2': 4900, 'valorizacao_12m': 8.9, 'diaria_media_airbnb': 250, 'ocupacao_media': 74, 'roi': 7.9, 'liquidez': 'Baixa', 'imoveis_vendidos': 620, 'tendencia': 'Muito alta', 'perspectiva': 'Melhor ROI e valorização'},
    'bertioga': {'nome': 'Bertioga', 'preco_m2': 7400, 'valorizacao_12m': 6.5, 'diaria_media_airbnb': 340, 'ocupacao_media': 65, 'roi': 6.7, 'liquidez': 'Alta', 'imoveis_vendidos': 540, 'tendencia': 'Moderada', 'perspectiva': 'Mercado seletivo'},
}

# Publicação 1: Relatório Semanal de Mercado
relatorio_semanal = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório Semanal — Mercado Imobiliário Litoral SP | {base_date.strftime('%d/%m/%Y')}</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }}
  header {{ background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }}
  header h1 {{ margin: 0; font-size: 2rem; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }}
  .insight {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); border-left: 4px solid #2563eb; }}
  .insight.destaque {{ border-left-color: #f59e0b; }}
  .insight h2 {{ margin: 0 0 0.5rem; color: #0a1628; font-size: 1.2rem; }}
  .insight p {{ color: #475569; line-height: 1.7; margin: 0.5rem 0; }}
  .number {{ font-weight: 700; color: #2563eb; }}
  footer {{ text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }}
</style>
</head>
<body>
<header>
  <h1>📊 Relatório Semanal — Mercado Imobiliário Litoral SP</h1>
  <p>Semana de {base_date.strftime('%d/%m/%Y')} | Dados proprietários Praia Digital</p>
</header>
<div class="container">
  <div class="insight destaque">
    <h2>Destaque da semana</h2>
    <p>Peruíbe mantém a <span class="number">maior valorização do Litoral SP</span> com <span class="number">+8.9%</span> em 12 meses. O crescimento é puxado por investidores de SP que buscam alto ROI em temporada.</p>
  </div>
  <div class="insight">
    <h2>Indicadores exclusivos</h2>
    <p>Monitoramos <span class="number">8 cidades</span> com dados atualizados semanalmente: preço médio do m², diária média Airbnb, ocupação, ROI e liquidez.</p>
  </div>
  <div class="insight">
    <h2>Oportunidade identificada</h2>
    <p>Praia Grande registra <span class="number">1.560 imóveis vendidos</span> nos últimos 12 meses, o maior volume do litoral. Para imobiliárias, isso significa fluxo contínuo de compradores e renovação de base.</p>
  </div>
  <div class="insight">
    <h2>Alerta de tendência</h2>
    <p>Itanhaém e Peruíbe apresentam valorização acima de <span class="number">8%</span> e ROI superior a <span class="number">7.5%</span>. Corretores que atuarem nessas rotas têm chance de fechar mais parcerias em menor tempo.</p>
  </div>
</div>
<footer>
  <p>Relatório Semanal Praia Digital | {base_date.strftime('%d/%m/%Y')} | Não reproduza sem citar a fonte</p>
</footer>
</body>
</html>"""

(conteudo_dir/'relatorio-semanal-2026-07-14.html').write_text(relatorio_semanal, encoding='utf-8')

# Publicação 2: Ranking Semanal
ranking_semanal = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ranking Semanal — Litoral SP | {base_date.strftime('%d/%m/%Y')}</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }}
  header {{ background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }}
  header h1 {{ margin: 0; font-size: 2rem; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1rem; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  th, td {{ padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }}
  th {{ background: #0a1628; color: white; font-weight: 600; }}
  tr:hover {{ background: #f4f6f9; }}
  .top1 {{ color: #f59e0b; font-weight: 700; }}
  .top2 {{ color: #94a3b8; font-weight: 700; }}
  .top3 {{ color: #b45309; font-weight: 700; }}
  footer {{ text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }}
</style>
</head>
<body>
<header>
  <h1>🏆 Ranking Semanal — Litoral SP</h1>
  <p>Atualizado em {base_date.strftime('%d/%m/%Y')} | Dados proprietários</p>
</header>
<div class="container">
  <table>
    <tr>
      <th>#</th>
      <th>Cidade</th>
      <th>ROI Airbnb</th>
      <th>Valorização 12m</th>
      <th>Ocupação</th>
      <th>Diária Média</th>
    </tr>
    <tr><td class="top1">1º</td><td>Peruíbe</td><td>7.9%</td><td>+8.9%</td><td>74%</td><td>R$ 250</td></tr>
    <tr><td class="top2">2º</td><td>Itanhaém</td><td>7.6%</td><td>+8.4%</td><td>70%</td><td>R$ 260</td></tr>
    <tr><td class="top3">3º</td><td>Praia Grande</td><td>7.2%</td><td>+7.8%</td><td>72%</td><td>R$ 280</td></tr>
    <tr><td>4º</td><td>Mongaguá</td><td>7.0%</td><td>+7.5%</td><td>69%</td><td>R$ 290</td></tr>
    <tr><td>5º</td><td>Bertioga</td><td>6.7%</td><td>+6.5%</td><td>65%</td><td>R$ 340</td></tr>
    <tr><td>6º</td><td>Guarujá</td><td>6.4%</td><td>+6.1%</td><td>64%</td><td>R$ 350</td></tr>
    <tr><td>7º</td><td>São Vicente</td><td>6.1%</td><td>+6.7%</td><td>62%</td><td>R$ 300</td></tr>
    <tr><td>8º</td><td>Santos</td><td>5.8%</td><td>+5.2%</td><td>68%</td><td>R$ 380</td></tr>
  </table>
</div>
<footer>
  <p>Ranking Semanal Praia Digital | {base_date.strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(conteudo_dir/'ranking-semanal-2026-07-14.html').write_text(ranking_semanal, encoding='utf-8')

# Publicação 3: Estudo de Cidade Aprofundado (diferente do estudo básico)
estudo_itanhaem = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Estudo Aprofundado — Itanhaém 2026 | Praia Digital</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }}
  header {{ background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }}
  header h1 {{ margin: 0; font-size: 2rem; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1rem; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
  .kpi {{ background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); text-align: center; }}
  .kpi-value {{ font-size: 2rem; font-weight: 800; color: #2563eb; }}
  .kpi-label {{ font-size: 0.85rem; color: #64748b; margin-top: 0.25rem; }}
  .section {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  .section h2 {{ color: #0a1628; margin: 0 0 1rem; }}
  .section p {{ color: #475569; line-height: 1.7; }}
  .highlight {{ background: #fef3c7; padding: 0.25rem 0.5rem; border-radius: 4px; font-weight: 700; color: #92400e; }}
  footer {{ text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }}
</style>
</head>
<body>
<header>
  <h1>📋 Estudo Aprofundado — Itanhaém 2026</h1>
  <p>Análise proprietária Praia Digital | {base_date.strftime('%d/%m/%Y')}</p>
</header>
<div class="container">
  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-value">R$ 5.100</div><div class="kpi-label">Preço médio m²</div></div>
    <div class="kpi"><div class="kpi-value">+8.4%</div><div class="kpi-label">Valorização 12m</div></div>
    <div class="kpi"><div class="kpi-value">7.6%</div><div class="kpi-label">ROI Airbnb</div></div>
    <div class="kpi"><div class="kpi-value">70%</div><div class="kpi-label">Ocupação média</div></div>
  </div>
  <div class="section">
    <h2>Mercado imobiliário</h2>
    <p>Itanhaém combina <span class="highlight">valorização acima da média</span> com custo de entrada ainda acessível para o Litoral SP. O preço médio de R$ 5.100/m² representa oportunidade para investidores que buscam entrada em cidades com potencial de crescimento.</p>
  </div>
  <div class="section">
    <h2>Airbnb e temporada</h2>
    <p>A ocupação média de <span class="highlight">70%</span> e diária de R$ 260 posicionam Itanhaém como uma das cidades mais equilibradas do litoral: não tem a sazonalidade extrema de Santos nem a baixa diária de cidades mais afastadas.</p>
  </div>
  <div class="section">
    <h2>Perfil do comprador</h2>
    <p>Predominância de famílias de São Paulo e interior em busca de segunda residência. Também há crescimento de investidores que compram para alugar temporada, atraídos pelo ROI de <span class="highlight">7.6%</span>.</p>
  </div>
  <div class="section">
    <h2>Recomendação Praia Digital</h2>
    <p>Para corretores: foque em imóveis com quintal e espaço para famílias. Para investidores: unidades próximas à orla e ao centro comercializam mais rápido. Para construtoras: lançamentos com área de lazer têm maior aceitação.</p>
  </div>
</div>
<footer>
  <p>Estudo Aprofundado Praia Digital | Itanhaém | {base_date.strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(conteudo_dir/'estudo-itanhaem-2026-07-14.html').write_text(estudo_itanhaem, encoding='utf-8')

# Publicação 4: Relatório de Oportunidades
oportunidades = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oportunidades — Litoral SP | {base_date.strftime('%d/%m/%Y')}</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }}
  header {{ background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }}
  header h1 {{ margin: 0; font-size: 2rem; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1rem; }}
  .opp {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); border-left: 4px solid #10b981; }}
  .opp h2 {{ margin: 0 0 0.5rem; color: #0a1628; }}
  .opp p {{ color: #475569; line-height: 1.6; margin: 0.5rem 0; }}
  footer {{ text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }}
</style>
</head>
<body>
<header>
  <h1>🚀 Oportunidades no Litoral SP</h1>
  <p>Semana de {base_date.strftime('%d/%m/%Y')} | Análise Praia Digital</p>
</header>
<div class="container">
  <div class="opp">
    <h2>Peruíbe: maior valorização e ROI</h2>
    <p>Para investidores que buscam alta rentabilidade, Peruíbe combina <strong>+8.9% de valorização</strong> com <strong>ROI de 7.9%</strong> e ocupação de 74%. Oportunidade para imobiliárias que quiserem captar esse perfil.</p>
  </div>
  <div class="opp">
    <h2>Praia Grande: volume massivo</h2>
    <p>Com <strong>1.560 imóveis vendidos</strong> nos últimos 12 meses, a cidade oferece fluxo constante de leads. Corretores podem se destacar com atendimento rápido e parcerias com construtoras.</p>
  </div>
  <div class="opp">
    <h2>Santos: estabilidade e liquidez</h2>
    <p>Mercado mais maduro do litoral, com <strong>liquidez alta</strong> e preço médio de R$ 8.200/m². Ideal para perfis conservadores e imobiliárias que buscam previsibilidade.</p>
  </div>
</div>
<footer>
  <p>Oportunidades Praia Digital | {base_date.strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(conteudo_dir/'oportunidades-2026-07-14.html').write_text(oportunidades, encoding='utf-8')

# Publicação 5: Indicadores Exclusivos (não repetir dashboard)
indicadores = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Indicadores Exclusivos — Litoral SP | {base_date.strftime('%d/%m/%Y')}</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }}
  header {{ background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }}
  header h1 {{ margin: 0; font-size: 2rem; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }}
  .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
  .metric-card {{ background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  .metric-card h3 {{ margin: 0 0 0.5rem; color: #0a1628; font-size: 1.05rem; }}
  .metric-card .value {{ font-size: 1.75rem; font-weight: 800; color: #2563eb; }}
  .metric-card .context {{ font-size: 0.85rem; color: #64748b; margin-top: 0.5rem; }}
  footer {{ text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }}
</style>
</head>
<body>
<header>
  <h1>📈 Indicadores Exclusivos — Litoral SP</h1>
  <p>Semana de {base_date.strftime('%d/%m/%Y')} | Fonte: Praia Digital</p>
</header>
<div class="container">
  <div class="metric-grid">
    <div class="metric-card">
      <h3>Maior alta de preço</h3>
      <div class="value">Peruíbe</div>
      <div class="context">+8.9% em 12 meses</div>
    </div>
    <div class="metric-card">
      <h3>Maior volume de vendas</h3>
      <div class="value">Praia Grande</div>
      <div class="context">1.560 imóveis vendidos</div>
    </div>
    <div class="metric-card">
      <h3>Maior diária média</h3>
      <div class="value">Santos</div>
      <div class="context">R$ 380 diária média</div>
    </div>
    <div class="metric-card">
      <h3>Maior ROI Airbnb</h3>
      <div class="value">Peruíbe</div>
      <div class="context">7.9% de retorno</div>
    </div>
  </div>
</div>
<footer>
  <p>Indicadores Exclusivos Praia Digital | {base_date.strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(conteudo_dir/'indicadores-2026-07-14.html').write_text(indicadores, encoding='utf-8')

print('publicacoes periodicas criadas')
