from pathlib import Path
import html

repo = Path('.')
ft = repo / 'ferramentas'
ft.mkdir(exist_ok=True)

hub = f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>Área Administrador Airbnb — Praia Digital</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;background:#f4f6f9;color:#1f2937;margin:0}}
main{{max-width:980px;margin:0 auto;padding:2rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem}}
a.card{{background:#fff;border-radius:12px;padding:1.2rem;box-shadow:0 2px 8px rgba(0,0,0,.08);text-decoration:none;color:#0f172a;display:block}}
h1{{color:#0a1628}}
</style>
</head>
<body>
<main>
  <h1>Área Administrador Airbnb</h1>
  <p>Ferramentas operacionais para yield, SEO, rotina, faturamento e parcerias.</p>
  <div class=\"grid\">
    <a class=\"card\" href=\"simulador-rendimento-airbnb-2026.html\"><strong>Simulador de rendimento Airbnb</strong><br/>Estimativa de receita por mês.</a>
    <a class=\"card\" href=\"calculadora-ocupacao-airbnb-2026.html\"><strong>Calculadora de ocupação</strong><br/>Diárias necessárias para bater metas.</a>
    <a class=\"card\" href=\"calculadora-diaria-ideal-airbnb-2026.html\"><strong>Calculadora de diária ideal</strong><br/>Preço sugerido por noite.</a>
    <a class=\"card\" href=\"pricelabs-airbnb-2026.html\"><strong>Integração PriceLabs</strong><br/>Ajuste dinâmico de preço.</a>
    <a class=\"card\" href=\"stays-airbnb-2026.html\"><strong>Integração Stays</strong><br/>Otimização de fluxo de entrada/saída.</a>
    <a class=\"card\" href=\"calendario-eventos-airbnb-2026.html\"><strong>Calendário de eventos</strong><br/>Datas de alta e baixa temporada.</a>
    <a class=\"card\" href=\"calculadora-limpeza-airbnb-2026.html\"><strong>Calculadora de limpeza</strong><br/>Custo operacional por estadia.</a>
    <a class=\"card\" href=\"comparador-airbnb-aluguel-tradicional-2026.html\"><strong>Comparador Airbnb x Aluguel tradicional</strong><br/>Análise de rentabilidade e liquidez.</a>
    <a class=\"card\" href=\"estimativa-faturamento-anual-airbnb-2026.html\"><strong>Estimativa anual de faturamento</strong><br/>Projeção anual com sazonalidade.</a>
  </div>
</main>
</body>
</html>"""
(ft / 'airbnb-admin.html').write_text(hub, encoding='utf-8')

pages = {
  'simulador-rendimento-airbnb-2026.html': (
    'Simulador de rendimento Airbnb',
    'Preço médio estimado R$ <input id="p" type="number" value="350"> | Ocupação % <input id="o" type="number" value="65"> | Dias/mês <input id="d" type="number" value="30"><br/><button onclick="const p=+document.getElementById(\'p\').value,o=+document.getElementById(\'o\').value/100,d=+document.getElementById(\'d\').value;document.getElementById(\'r\').textContent=(p*o*d).toLocaleString(\'pt-BR\',{style:\'currency\',currency:\'BRL\'});">Calcular</button><p id="r">R$ 0,00</p>'
  ),
  'calculadora-ocupacao-airbnb-2026.html': (
    'Calculadora de ocupação',
    'Receita desejada R$ <input id="meta" type="number" value="10000"> | Preço diária R$ <input id="p" type="number" value="350"> <button onclick="const meta=+document.getElementById(\'meta\').value,p=+document.getElementById(\'p\').value;document.getElementById(\'r\').textContent=\'Ocupação mínima: \'+Math.min(100,(meta/(30*p))*100).toFixed(1)+\' %\';">Calcular</button><p id="r"></p>'
  ),
  'calculadora-diaria-ideal-airbnb-2026.html': (
    'Calculadora de diária ideal',
    'Custo mensal R$ <input id="custo" type="number" value="4200"> | Despesas operacionais R$ <input id="op" type="number" value="1200"> | Ocupação % <input id="o" type="number" value="65"> <br/><button onclick="const custo=+document.getElementById(\'custo\').value,op=+document.getElementById(\'op\').value,o=+document.getElementById(\'o\').value/100;document.getElementById(\'r\').textContent=\'Diária ideal sugerida: R$ \'+Math.ceil((custo+op)/(30*o)).toLocaleString(\'pt-BR\');">Calcular</button><p id="r"></p>'
  ),
  'pricelabs-airbnb-2026.html': (
    'Integração PriceLabs',
    'Ajuste automático por temporada. (Placeholder) Use o painel do PriceLabs conectado à sua conta. Aqui é onde vamos ativar a sincronização futura.'
  ),
  'stays-airbnb-2026.html': (
    'Integração Stays',
    'Rotinas e fluxos de hospedagem. (Placeholder) Aqui entraremos com um checklist inteligente de operação.'
  ),
  'calendario-eventos-airbnb-2026.html': (
    'Calendário de eventos',
    'Meses de alta temporada: Dez-Jan-Fev. (Placeholder) Adicione datas e bloqueios locais para acessar sazonalidade automática.'
  ),
  'calculadora-limpeza-airbnb-2026.html': (
    'Calculadora de limpeza',
    'Custo por limpeza R$ <input id="c" type="number" value="180"> | Taxa de ocupação % <input id="o" type="number" value="65"> <br/><button onclick="const c=+document.getElementById(\'c\').value,o=+document.getElementById(\'o\').value/100;document.getElementById(\'r\').textContent=\'Custo mensal estimado: R$ \'+((c/0.65*30*o)).toFixed(2);">Calcular</button><p id="r"></p>'
  ),
  'comparador-airbnb-aluguel-tradicional-2026.html': (
    'Comparador Airbnb x Aluguel tradicional',
    'Aluguel tradicional mensal R$ <input id="a" type="number" value="2800"> | Diária média Airbnb R$ <input id="d" type="number" value="320"> | Ocupação % <input id="o" type="number" value="60"> <br/><button onclick="const a=+document.getElementById(\'a\').value,d=+document.getElementById(\'d\').value,o=+document.getElementById(\'o\').value/100;const anual_airbnb=d*o*365;const anual_trad=a*12;document.getElementById(\'r\').textContent=\'Anual Airbnb: R$ \'+anual_airbnb.toLocaleString(\'pt-BR\')+\' | Tradicional: R$ \'+anual_trad.toLocaleString(\'pt-BR\')+\' | Diferença: R$ \'+(anual_airbnb-anual_trad).toLocaleString(\'pt-BR\');">Comparar</button><p id="r"></p>'
  ),
  'estimativa-faturamento-anual-airbnb-2026.html': (
    'Estimativa anual de faturamento',
    'Diária média R$ <input id="d" type="number" value="320"> | Ocupação % <input id="o" type="number" value="60"> <br/><button onclick="const d=+document.getElementById(\'d\').value,o=+document.getElementById(\'o\').value/100;document.getElementById(\'r\').textContent=\'Estimativa anual: R$ \'+(d*o*365).toLocaleString(\'pt-BR\');">Calcular</button><p id="r"></p>'
  ),
}

for name, (title, body) in pages.items():
    safe_title = html.escape(title)
    safe_body = html.escape(body)
    content = f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>{safe_title}</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;background:#f4f6f9;color:#1f2937;margin:0}}
main{{max-width:900px;margin:0 auto;padding:2rem}}
input{{padding:.45rem;margin:.25rem}}
button{{padding:.5rem .9rem;border:0;background:#0a1628;color:#fff;border-radius:8px}}
</style>
</head>
<body>
<main>
  <h1>{safe_title}</h1>
  <p>{safe_body}</p>
  <p><a href=\"airbnb-admin.html\">← Voltar para Área Administrador Airbnb</a></p>
</main>
</body>
</html>"""
    (ft / name).write_text(content, encoding='utf-8')

print('airbnb admin created')
