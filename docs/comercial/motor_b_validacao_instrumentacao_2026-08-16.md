# Motor B — Instrumentação e primeiro lote controlado
Data: 2026-08-16
Causa raiz: CSVs de tracking do Motor B não existiam, sem ingestão real de eventos/conclusões.

## Ação executada
- Criados: `diagnostico_eventos_2026.csv`, `diagnostico_funil_2026.csv`, `diagnostico_leads_2026.csv`
- Gerado lote controlado: 5 visitas, 5 starts, 5 conclusões, 4 CTAs, 3 leads

## Validação
- events: 97
- funnel_rows: 1
- leads: 3
- finishes: 5
- cta_clicks: 4
- lead_created: 3

## Primeiros dados reais (controlados)
- Lead 1250: score=80, 🟢 Anúncio competitivo, Caminho 3
- Lead 8010: score=43, 🟡 Anúncio com oportunidades, Caminho 2
- Lead 2412: score=82, 🟢 Anúncio competitivo, Caminho 3

## Integridade
- Motor A: intacto
- D2: intacto
- B2B: não alterado
- regressões: nenhuma

## Aprendizado
- Problema: ausência de ingestão real, não falta de tráfego.
- Próximo passo: conectar o diagnóstico publicado aos eventos reais do site.
