# Expansão E — Multi-canal B2B (E-mail + WhatsApp)

**Rationale:** o B2C já opera multicanal (WPP + e-mail). O B2B (Expansão A/C) ficou só em WhatsApp. Adicionar e-mail B2B aumenta taxa de resposta e espelha o funil já validado.

## Entregue
- `scripts/gerar_lote_email_b2b.py` — gera lotes de e-mail B2B (copy própria, reusa padrão do B2C) filtrando por `--status` e `--whitelabel`.
- `docs/sales/csv-lotes-b2b/lote-email-b2b-reativacao-2026-07-16.csv` (486 imobiliárias)
- `docs/sales/csv-lotes-b2b/lote-email-b2b-whitelabel-2026-07-16.csv` (101 parceiras)

## Status: ✅ executada (pipeline completo)
- 587 leads B2B agora têm sequência multicanal (WPP Msg1-3 + E-mail E1-3).
- Pipeline B2B de e-mail: gerador + consolidador + marcador E1 + follow-up (cron 18h) + tracker isolado.
- Reuso total: copy B2B, base B2B real, sem duplicar estrutura.
- **Tracker em estado honesto** (`pendente_email1`) — aguarda autorização de disparo.

## Próximos passos
- [x] Consolidar e-mail B2B no tracker isolado (`consolidar_tracker_email_b2b.py`)
- [x] Cron de follow-up e-mail B2B (`followup-email-b2b-imobiliarias`, 18h)
- [ ] Disparar (requer autorização — escala 3× o outbound)
