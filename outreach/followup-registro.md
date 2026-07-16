# Follow-up Registro — Lote WhatsApp Proprietários Autogestores 149

**Template base:** `outreach/template-whatsapp-proprietarios.md`
**Lote CSV:** `docs/sales/csv-lotes-email/lote-whatsapp-proprietarios-149-2026-07-15.csv`
**Data base (Msg 1):** 2026-07-15 (quarta)
**Timing:** Msg 2 em +1 a 2 dias (16–17/07) · Msg 3 em +3 a 4 dias (18–19/07)
**Canal:** WhatsApp manual (sem API/SMTP) — copiar do CSV e colar por contato.

## Status por lead

| Nome | Cidade | Tel | Msg1 | Msg2 | Msg3 | Status final |
|------|--------|-----|------|------|------|--------------|
| Fernanda Lima | Santos | (13) 99999-7301 | ☐ 15/07 | ☐ 16-17/07 | ☐ 18-19/07 | pendente |
| Paulo Vieira | Guarujá | (11) 99999-7302 | ☐ 15/07 | ☐ 16-17/07 | ☐ 18-19/07 | pendente |
| Ricardo Mendes | Praia Grande | (13) 99999-7303 | ☐ 15/07 | ☐ 16-17/07 | ☐ 18-19/07 | pendente |
| Bruno Costa | Itanhaém | (13) 99999-7304 | ☐ 15/07 | ☐ 16-17/07 | ☐ 18-19/07 | pendente |
| Larissa Barros | São Vicente | (11) 99999-7305 | ☐ 15/07 | ☐ 16-17/07 | ☐ 18-19/07 | pendente |

## Regras
- Após enviar cada msg, marcar ☑ na data real e atualizar `Status final`.
- Sem resposta após Msg 3 → marcar `sem_interesse`, não insistir.
- Resposta positiva → mover para pipeline de proposta (Gestão Completa + Precificação Dinâmica).
- O cron `followup-whatsapp-149` avisa diariamente quem deve receber Msg 2 / Msg 3.
