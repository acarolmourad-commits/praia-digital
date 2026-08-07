# GA4 — Checklist de implantação no Praia Digital

## Status atual
- Placeholder `GA4_MEASUREMENT_ID` injetado em **~6212 páginas públicas**.
- Pastas sem GA4: `outreach/` (**3504 páginas**), `docs/` (**948**), `dashboards/` (**600**), `litoral-prime-imoveis/` (**215**), `eventos-litoral-paulista-2026-2027/` (**72**).
- Injeção automática em massa **paralisada** para evitar sobrescrever o `_temp_inject_ga4.py` repetidamente.

## O que falta para ativar o GA4
1. **Criar propriedade GA4** no Google Analytics e obter o `Measurement ID` real (ex.: `G-XXXXXXXXXX`).
2. **Definir eventos principais de conversão**:
   - Visualização de página (`page_view`) — automático
   - Clique em WhatsApp (`whatsapp_click`)
   - Envio de formulário de lead (`form_submit`)
   - Clique em CTA de curso (`cta_course_click`)
3. **Substituir o placeholder** por scripts de eventos de conversão reais.
4. **Conectar ao Google Search Console** para cruzar dados de busca e conversão.

## Como substituir o ID real
- Procurar e substituir `GA4_MEASUREMENT_ID` pelo ID real em todas as páginas.
- Recomendado: usar `scripts/_temp_inject_ga4.py` como base, trocando a constante do snippet.

## Observações
- `outreach/` contém templates de e-mail em HTML e não deve ser rastreado como página pública.
- `docs/` e `dashboards/` são internos; considerar bloqueio via `robots.txt`.
- `litoral-prime-imoveis/` precisa de revisão manual antes de ativar GA4.

## Próximo passo operacional
Fornecer o ID GA4 real para que eu:
1. Aplique a substituição global com script versionado.
2. Valide com `frontend_health_check.py` e `check_links.py`.
3. Commit + push da ativação.
