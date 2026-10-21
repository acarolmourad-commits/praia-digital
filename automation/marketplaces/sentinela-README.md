# Sentinela Airbnb + Booking — Praia Digital

Agente autonomo de monitoramento de novidades oficiais do Airbnb e da Booking.com.

## Como funciona
- Workflow `.github/workflows/sentinela-airbnb-booking.yml` roda a cada 6 horas (`0 3,9,15,21 * * *` UTC) e tambem pode ser disparado manualmente.
- Script `scripts/sentinela_airbnb_booking.py` (somente biblioteca padrao do Python) consulta apenas fontes oficiais:
  - Airbnb Product Releases: https://news.airbnb.com/product-releases/
  - Airbnb Newsroom: https://news.airbnb.com/
  - Airbnb Resource Center (anfitrioes): https://www.airbnb.com/resources/hosting-homes
  - Booking Partner Hub: https://partner.booking.com/en-us (pode retornar 202/protecao anti-robo; nesse caso registra indisponivel e NAO publica nada)
  - Booking (parceiros): https://join.booking.com/
- Estado (itens ja vistos, hashes e posts) fica em `automation/marketplaces/sentinela-estado.json`.
- Cada execucao gera `sentinela-report.md` no ambiente do workflow; quando ha novidade, ele vira o corpo da Issue de acompanhamento.

## Publicacao automatica (com revisao editorial fixa)
Quando surge item novo em fonte oficial, o agente:
1. Gera um post em `novidades-airbnb-booking/novidade-*.html` usando SOMENTE a manchete e o link oficiais.
2. Atualiza `novidades-airbnb-booking/index.html`.
3. Commita no `main`, dispara o deploy do GitHub Pages e abre uma Issue de acompanhamento.

O modelo do post e fixo e assertivo: **O que mudou -> O que isso significa para anfitrioes -> O que fazer agora -> Fonte oficial**.
O agente nunca inventa funcionalidade que nao esteja na manchete/fonte oficial. Para a Booking, alteracao detectada em pagina publica gera post de alerta pedindo confirmacao dentro do Partner Hub.

## Operacao
- Para pausar: desative o workflow em Actions > Sentinela Airbnb + Booking.
- Para forcar uma verificacao: Actions > Sentinela Airbnb + Booking > Run workflow.
- Posts publicados: https://praia.digital/novidades-airbnb-booking/
