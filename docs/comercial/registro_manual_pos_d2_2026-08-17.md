# Registro manual pós-D2 — 17/08
Uso: após executar `verificacao_pre_d2_2026-08-17.md`

## Leads e canais

| lead_id | canal | status pós-disparo |
|---------|-------|--------------------|
| 9 | OLX/WhatsApp | ENVIADO_D2 |
| 11 | OLX/WhatsApp | ENVIADO_D2 |
| 14 | Instagram/WhatsApp | ENVIADO_D2 |
| 15 | Facebook/WhatsApp | ENVIADO_D2 |
| 27 | Instagram/WhatsApp | ENVIADO_D2 |
| 29 | Facebook/WhatsApp | ENVIADO_D2 |

## Atualizações no CRM
- Arquivo: `docs/comercial/leads_sao_sebastiao_bertioga.csv`
- Coluna `d2_enviado_em` = 2026-08-17 para os 6 leads
- Coluna `status` = ENVIADO_D2 para os 6 leads

## Após atualização
- [ ] Rodar `python scripts/follow_up_automacao.py`
- [ ] Rodar `python scripts/relatorio_diario_motor_b.py`
- [ ] Atualizar `docs/comercial/painel_unificado_motor_a_b_2026-08-17.md`
- [ ] Commit com mensagem padrão

## Classificação de resposta
- Positiva/preço/agendamento → handoff humano
- Negativa/bloqueio → encerrar/bloquear
- Sem resposta → D5 em 20/08
