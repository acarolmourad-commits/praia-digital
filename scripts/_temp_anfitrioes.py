from pathlib import Path
from datetime import datetime

repo = Path('.')
anfitrioes = repo/'anfitrioes'
anfitrioes.mkdir(exist_ok=True)

# Central Airbnb
airbnb = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Central Airbnb — Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
  .card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .card h2 { margin: 0 0 0.75rem; color: #0a1628; font-size: 1.1rem; }
  .card a { color: #2563eb; text-decoration: none; }
  .card a:hover { text-decoration: underline; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>🏠 Central Airbnb</h1>
  <p>Ferramentas, tutoriais e diagnósticos exclusivos para anfitriões</p>
</header>
<div class="container">
  <div class="card-grid">
    <div class="card">
      <h2>📹 Tutoriais</h2>
      <p>Vídeos passo a passo sobre cadastro, fotos, avaliações e otimização de anúncios.</p>
      <a href="tutoriais-airbnb.html">Acessar tutoriais →</a>
    </div>
    <div class="card">
      <h2>✅ Checklists</h2>
      <p>Checklists prontas para uso: check-in, limpeza, segurança e experiência do hóspede.</p>
      <a href="checklists-airbnb.html">Baixar checklists →</a>
    </div>
    <div class="card">
      <h2>🔎 Diagnóstico</h2>
      <p>Diagnóstico gratuito do seu anúncio: preço sugerido, avaliação de fotos e descrição.</p>
      <a href="diagnostico-airbnb.html">Fazer diagnóstico →</a>
    </div>
    <div class="card">
      <h2>📈 Dados do Mercado</h2>
      <p>Diária média, ocupação e roi por cidade para competir com preços justos.</p>
      <a href="dados-mercado-airbnb.html">Ver dados →</a>
    </div>
  </div>
</div>
<footer>
  <p>Central Airbnb | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'central-airbnb.html').write_text(airbnb, encoding='utf-8')

# Central PriceLabs
priceplabs = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Central PriceLabs — Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
  .card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .card h2 { margin: 0 0 0.75rem; color: #0a1628; font-size: 1.1rem; }
  .card a { color: #2563eb; text-decoration: none; }
  .card a:hover { text-decoration: underline; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>💡 Central PriceLabs</h1>
  <p>Estratégia, integração e automação de preços para anfitriões</p>
</header>
<div class="container">
  <div class="card-grid">
    <div class="card">
      <h2>🎓 Treinamentos</h2>
      <p>Aprenda a configurar regras de preço, sazonalidade e eventos na plataforma.</p>
      <a href="treinamentos-pricelabs.html">Ver treinamentos →</a>
    </div>
    <div class="card">
      <h2>🧪 Testes A/B</h2>
      <p>Roteiro para testar faixas de preço e comparar ocupação e faturamento.</p>
      <a href="testes-pricelabs.html">Acessar roteiro →</a>
    </div>
    <div class="card">
      <h2>📋 Checklist</h2>
      <p>Checklist de lançamento e ajustes semanais recomendados para anfitriões.</p>
      <a href="checklist-pricelabs.html">Baixar checklist →</a>
    </div>
    <div class="card">
      <h2>🔌 Integração</h2>
      <p>Guias de integração com Airbnb, Booking e Stays em um só lugar.</p>
      <a href="integracao-pricelabs.html">Ver guias →</a>
    </div>
  </div>
</div>
<footer>
  <p>Central PriceLabs | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'central-priceplabs.html').write_text(priceplabs, encoding='utf-8')

# Central Stays
stays = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Central Stays — Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
  .card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .card h2 { margin: 0 0 0.75rem; color: #0a1628; font-size: 1.1rem; }
  .card a { color: #2563eb; text-decoration: none; }
  .card a:hover { text-decoration: underline; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>🏨 Central Stays</h1>
  <p>Gestão de estadia, automação e experiência do hóspede</p>
</header>
<div class="container">
  <div class="card-grid">
    <div class="card">
      <h2>📋 Templates</h2>
      <p>Templates de mensagens, regras de check-in e check-out.</p>
      <a href="templates-stays.html">Ver templates →</a>
    </div>
    <div class="card">
      <h2>📚 Tutoriais</h2>
      <p>Vídeos curtos sobre auto-reserva, limpeza e manutenção preventiva.</p>
      <a href="tutoriais-stays.html">Acessar tutoriais →</a>
    </div>
    <div class="card">
      <h2>🧪 Diagnóstico</h2>
      <p>Diagnóstico de reputação, tempo de resposta e taxa de aprovação.</p>
      <a href="diagnostico-stays.html">Fazer diagnóstico →</a>
    </div>
    <div class="card">
      <h2>📊 Indicadores</h2>
      <p>Métricas-chave para acompanhar performance e qualidade da estadia.</p>
      <a href="indicadores-stays.html">Ver indicadores →</a>
    </div>
  </div>
</div>
<footer>
  <p>Central Stays | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'central-stays.html').write_text(stays, encoding='utf-8')

# Central Booking
booking = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Central Booking — Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
  .card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .card h2 { margin: 0 0 0.75rem; color: #0a1628; font-size: 1.1rem; }
  .card a { color: #2563eb; text-decoration: none; }
  .card a:hover { text-decoration: underline; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>🌐 Central Booking</h1>
  <p>Integração multicanal, conteúdo visual e conversão</p>
</header>
<div class="container">
  <div class="card-grid">
    <div class="card">
      <h2>📸 Fotos e Vídeos</h2>
      <p>Guias de fotografia profissional para anúncios de alta conversão.</p>
      <a href="fotos-videos-booking.html">Ver guias →</a>
    </div>
    <div class="card">
      <h2>🧾 Descrição AOB</h2>
      <p>Templates de descrição AOB para destacar diferenciais da propriedade.</p>
      <a href="descricao-booking.html">Acessar templates →</a>
    </div>
    <div class="card">
      <h2>📊 Diagnóstico</h2>
      <p>Diagnóstico de competitividade: preço, avaliações e posicionamento.</p>
      <a href="diagnostico-booking.html">Fazer diagnóstico →</a>
    </div>
    <div class="card">
      <h2>🔗 Integrações</h2>
      <p>Conecte Airbnb, Booking, Stays e PriceLabs em painel unificado.</p>
      <a href="integracoes-booking.html">Ver integrações →</a>
    </div>
  </div>
</div>
<footer>
  <p>Central Booking | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'central-booking.html').write_text(booking, encoding='utf-8')

# Central Index
central_index = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Área do Anfitrião — Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .hub-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
  .hub-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .hub-card h2 { margin: 0 0 0.75rem; color: #0a1628; font-size: 1.15rem; }
  .hub-card p { color: #64748b; line-height: 1.6; }
  .hub-card a { color: #2563eb; text-decoration: none; font-weight: 600; }
  .hub-card a:hover { text-decoration: underline; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>🌟 Área Exclusiva do Anfitrião</h1>
  <p>Tools, conteúdo e suporte para Airbnb, PriceLabs, Stays e Booking</p>
</header>
<div class="container">
  <div class="hub-grid">
    <div class="hub-card">
      <h2>🏠 Central Airbnb</h2>
      <p>Tutoriais, checklists, diagnóstico e dados de mercado.</p>
      <a href="central-airbnb.html">Acessar Central Airbnb →</a>
    </div>
    <div class="hub-card">
      <h2>💡 Central PriceLabs</h2>
      <p>Treinamentos, testes A/B, checklist e integração.</p>
      <a href="central-priceplabs.html">Acessar Central PriceLabs →</a>
    </div>
    <div class="hub-card">
      <h2>🏨 Central Stays</h2>
      <p>Templates, tutoriais, diagnóstico e indicadores.</p>
      <a href="central-stays.html">Acessar Central Stays →</a>
    </div>
    <div class="hub-card">
      <h2>🌐 Central Booking</h2>
      <p>Fotos, descrição AOB, diagnóstico e integrações.</p>
      <a href="central-booking.html">Acessar Central Booking →</a>
    </div>
  </div>
</div>
<footer>
  <p>Área do Anfitrião | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'index.html').write_text(central_index, encoding='utf-8')

# Tutoriais com vídeos
tutoriais = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tutoriais — Área do Anfitrião | Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1000px; margin: 0 auto; padding: 2rem 1rem; }
  .video-item { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .video-item h2 { margin: 0 0 0.5rem; color: #0a1628; }
  .video-item p { color: #64748b; line-height: 1.6; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>🎓 Tutoriais para Anfitriões</h1>
  <p>Vídeos curtos e práticos para Airbnb, PriceLabs, Stays e Booking</p>
</header>
<div class="container">
  <div class="video-item">
    <h2>Airbnb: como criar um anúncio campeão</h2>
    <p>Passo a passo para montar título, descrição e política de cancelamento.</p>
  </div>
  <div class="video-item">
    <h2>PriceLabs: definindo preço por temporada</h2>
    <p>Aprenda a configurar regras de alta e baixa temporada.</p>
  </div>
  <div class="video-item">
    <h2>Stays: automação de check-in</h2>
    <p>Reduza stress operacional com automação passo a passo.</p>
  </div>
  <div class="video-item">
    <h2>Booking: fotos que vendem</h2>
    <p>Guia rápido de fotografia profissional para aumentar conversão.</p>
  </div>
</div>
<footer>
  <p>Tutoriais | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'tutoriais-anfitrioes.html').write_text(tutoriais, encoding='utf-8')

# Checklists
checklists = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Checklists — Área do Anfitrião | Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1000px; margin: 0 auto; padding: 2rem 1rem; }
  .checklist { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .checklist h2 { margin: 0 0 0.75rem; color: #0a1628; }
  .checklist ul { color: #475569; line-height: 1.8; padding-left: 1.25rem; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>✅ Checklists do Anfitrião</h1>
  <p>Listas prontas para usar na operação diária</p>
</header>
<div class="container">
  <div class="checklist">
    <h2>Check-in</h2>
    <ul>
      <li>Confirmar horário de entrada</li>
      <li>Preparar chaves e acesso</li>
      <li>Check de limpeza rápida</li>
      <li>Mensagem de boas-vindas</li>
    </ul>
  </div>
  <div class="checklist">
    <h2>Limpeza</h2>
    <ul>
      <li>Troca de roupas de cama</li>
      <li>Limpeza de banheiros</li>
      <li>Reposição de amenities</li>
      <li>Vistoria de danos</li>
    </ul>
  </div>
  <div class="checklist">
    <h2>Segurança</h2>
    <ul>
      <li>Verificar extintor e iluminação</li>
      <li>Validar travas e fechaduras</li>
      <li>Confirmar funcionamento de WI-FI</li>
      <li>Checar rota de emergência</li>
    </ul>
  </div>
</div>
<footer>
  <p>Checklists | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'checklists-anfitrioes.html').write_text(checklists, encoding='utf-8')

# Diagnósticos
diagnosticos = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diagnósticos — Área do Anfitrião | Praia Digital</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
  header { background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%); color: white; padding: 2rem 1rem; text-align: center; }
  header h1 { margin: 0; font-size: 2rem; }
  .container { max-width: 1000px; margin: 0 auto; padding: 2rem 1rem; }
  .diagnostic-card { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .diagnostic-card h2 { margin: 0 0 0.75rem; color: #0a1628; }
  .diagnostic-card p { color: #475569; line-height: 1.6; }
  .diagnostic-card a { color: #2563eb; text-decoration: none; font-weight: 600; }
  footer { text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>🧎 Diagnósticos do Anfitrião</h1>
  <p>Avaliações gratuitas para melhorar resultado</p>
</header>
<div class="container">
  <div class="diagnostic-card">
    <h2>Diagnóstico de Anúncio</h2>
    <p>Verificamos título, descrição, preço e fotos e sugerimos ajustes para maior conversão.</p>
    <a href="diagnostico-anuncio.html">Iniciar diagnóstico →</a>
  </div>
  <div class="diagnostic-card">
    <h2>Diagnóstico de Reputação</h2>
    <p>Analisamos avaliações, taxa de resposta e tempo de resposta.</p>
    <a href="diagnostico-reputacao.html">Iniciar diagnóstico →</a>
  </div>
  <div class="diagnostic-card">
    <h2>Diagnóstico de Precificação</h2>
    <p>Comparamos sua diária média versus o mercado e sugerimos faixas.</p>
    <a href="diagnostico-preco.html">Iniciar diagnóstico →</a>
  </div>
</div>
<footer>
  <p>Diagnósticos | Praia Digital | {datetime.now().strftime('%d/%m/%Y')}</p>
</footer>
</body>
</html>"""

(anfitrioes/'diagnosticos-anfitrioes.html').write_text(diagnosticos, encoding='utf-8')

print('area do anfitriao criada')
