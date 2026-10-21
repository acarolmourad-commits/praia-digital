# Sentinela Airbnb + Booking — Praia Digital

Agente autônomo de novidades das plataformas de temporada. Autonomia concedida pelo proprietário em 2026-10-21: o agente faz a própria revisão e publica como post, sem depender de aprovação manual, respeitando as travas abaixo.

## Como funciona
- Workflow `.github/workflows/sentinela-airbnb-booking.yml` roda a cada 6 horas (03:17, 09:17, 15:17, 21:17 UTC) e por disparo manual (Actions > Sentinela Airbnb + Booking > Run workflow).
- `scripts/sentinela_airbnb_booking.py` monitora o sitemap oficial do Airbnb Newsroom (posts novos), Airbnb Product Releases, Airbnb Resource Center e Booking Partner Hub / Join Booking.
- Post novo relevante gera artigo em `blog/novidades-AAAA-MM-DD-<slug>.html` e atualiza o hub `blog/novidades-airbnb-booking.html`.
- Cada publicação abre uma issue de acompanhamento com o relatório `automation/marketplaces/sentinela-ultimo-relatorio.md`.
- Estado (URLs já vistas, artigos publicados, status das fontes) em `automation/marketplaces/sentinela-estado.json`.

## Auto-revisão (travas antes de publicar)
1. Fonte obrigatoriamente oficial (`news.airbnb.com` para artigos).
2. Artigo precisa ter as seções: O que mudou, O que isso significa, O que fazer agora e Fonte oficial.
3. Um único H1, HTML íntegro e nenhum preço (`R$`) ou dado confidencial.
4. Conteúdo irrelevante para anfitriões/hóspedes (ex.: ações humanitárias sem relação com hospedagem) é registrado e ignorado, não publicado.
5. Máximo de 3 artigos por execução, para evitar enxurrada.

## Booking.com
O Partner Hub retorna HTTP 202 (proteção anti-robô) para acessos automatizados; o agente registra o status e NÃO inventa novidades da Booking. Artigos de Booking só são gerados quando houver manchete estruturada acessível em fonte oficial; mudanças sem manchete aparecem no relatório/issue para conferência no Partner Hub.

## Modelo de artigo (assertivo)
O que mudou → resumo oficial → o que significa para anfitriões do litoral → o que fazer agora (checklist) → fonte oficial com data.
