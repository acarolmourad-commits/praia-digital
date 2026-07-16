# Expansão E — Multi-canal B2B (E-mail + WhatsApp)

**Rationale:** o B2C já opera multicanal (WPP + e-mail). O B2B (Expansão A/C) ficou só em WhatsApp. Adicionar e-mail B2B aumenta taxa de resposta e espelha o funil já validado.

## Entregue
- `scripts/gerar_lote_email_b2b.py` — gera lotes de e-mail B2B (copy própria, reusa padrão do B2C) filtrando por `--status` e `--whitelabel`.
- `docs/sales/csv-lotes-b2b/lote-email-b2b-reativacao-2026-07-16.csv` (486 imobiliárias)
- `docs/sales/csv-lotes-b2b/lote-email-b2b-whitelabel-2026-07-16.csv` (101 parceiras)

## Status: ✅ executada
- 587 leads B2B agora têm sequência multicanal (WPP Msg1-3 + E-mail E1-3).
- Reuso total: copy B2B, base B2B real, sem duplicar estrutura.

## Próximos passos
- [ ] Consolidar e-mail B2B no disparo (igual `preparar_disparo_b2b.py` mas p/ e-mail)
- [ ] Cron de follow-up e-mail B2B (paralelo ao `followup-b2b-imobiliarias`)
- [ ] Tracker e-mail B2B (isolado do B2C e do WPP B2B)
