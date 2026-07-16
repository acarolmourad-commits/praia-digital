# Expansão Praia Digital — Resumo Executivo (Sessão 16/07)

Plano de expansão produto/mercado executado e **publicado em produção** (`praia.digital`). Todas as frentes operam sobre o tráfego SEO já existente (1.300+ artigos de blog), sem mídia paga.

## Frentes (A→F)

| # | Frente | Público | Canal | Estado |
|---|--------|---------|-------|--------|
| A | B2B Imobiliárias (reativação) | 486 + 101 WL | WPP | ⏳ armada (aguarda disparo) |
| B | Norte B2B | imobiliárias norte | Site/SEO | ✅ ao vivo |
| C | White-label Calc | 101 parceiras | WPP | ✅ ao vivo |
| D | Norte B2C | donos norte | Site/SEO | ✅ ao vivo |
| E | B2B E-mail | 486 + 101 WL | WPP+E-mail | ⏳ armada |
| F | Quiz perfil de dono | donos (blog) | Site/SEO | ✅ ao vivo |

## Ativos ao vivo (URLs públicas validadas — HTTP 200)
- Quiz: `praia.digital/assets/quiz-perfil-dono.html`
- Landing dono norte: `praia.digital/dono-norte/dono-{ubatuba,ilhabela,caraguatatuba,sao-sebastiao}.html`
- Landing parceria norte: `praia.digital/parcerias-norte/parceria-{cidade}.html`
- Calculadora: `praia.digital/assets/calculadora-widget-standalone.html?tenant=pd-norte|santos-ancora`
- Dashboard: `praia.digital/docs/product/dashboard-expansao.html`

## Próximos passos (requerem autorização/dados)
1. **Disparar B2B A/E** — 587 imobiliárias (WPP + e-mail). Risco: escala 3× o outbound.
   - `python scripts/preparar_disparo_b2b.py` + `marcar_primeiro_envio_b2b.py`
   - `python scripts/consolidar_tracker_email_b2b.py` + `marcar_primeiro_envio_email_b2b.py`
2. **Calibrar calculadora** — exportar contratos reais → `docs/data/reservas-internas.csv` → `python scripts/ingest_historico_interno.py`. Hoje roda em "estimativa base".
3. **Nova frente** — Floripa/RJ, seguro de temporada, inside-sales norte.

## Métricas de entrega
- 8 landings geradas (4 dono + 4 parceria norte)
- 357 artigos B2C com quiz + 26 com landing dono norte + 70 com CTA B2B norte
- 587 leads B2B armados (WPP + e-mail), trackers isolados
- 101 propostas white-label + widget funcional
- Dashboard 360° + relatório executivo + skill reutilizável
