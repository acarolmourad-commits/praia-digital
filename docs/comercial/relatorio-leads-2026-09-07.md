# Relatório de leads — 2026-09-07 (modo autônomo)

## Status das réguas comerciais
- D2: 0
- D5: 0
- D10: 0
- Follow-up geral: OK
- Dia classificado como silencioso: sim

## Leads capturados
- Fonte principal: `docs/comercial/leads_sao_sebastiao_bertioga.csv`
- Total: 8

## Ações executadas
- Geração de CSVs de envio:
  - `docs/sales/csv-lotes-b2b/para-brevo-captacao-2026-09-07.csv`
  - `docs/sales/csv-lotes-b2b/para-whatsapp-captacao-2026-09-07.csv`
- Checklist de envio:
  - `docs/sales/checklist-envio-captacao-2026-09-07.txt`
- Registro comercial:
  - `docs/comercial/lote_envio_dia_2026-09-07.md`
  - `docs/comercial/relatorio_followup_2026-09-07.json`

## Instagram/Composio
- Status: indisponível para publicação automática.
- Verificação executada: `composio connections list --toolkit instagram`
- Resultado: existem conexões listadas, mas validação real retornou HTTP 401 (`OAuthException code=190`).
- Decisão: manter bloqueio automático e aguardar reautorização válida para seguir.

## Próximo passo operacional
1. Atualizar token/conta do Instagram no Composio manualmente.
2. Após validação OK, eu publico automaticamente o lote `docs/redes-sociais/lote-atual/manifesto-batch13.md`.
