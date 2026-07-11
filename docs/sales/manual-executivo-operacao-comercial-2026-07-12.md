# Manual Executivo de Operação Comercial — Praia Digital
**Versão:** 2026-07-12  
**Canal principal:** E-mail + WhatsApp  
**Automação:** scripts em `scripts/automation/`  
**Lead base:** `docs/sales/leads-litoral-enriquecido-emails-validos.csv`

---

## 1. Fluxo resumido
1. Importe o lote top20 no Brevo: `docs/sales/csv-lotes-email/lote-brevo-top20-2026-07-12.csv`
2. Confira os e-mails prontos em: `outreach/whatsapp-top20-mensagens-prontas.html`
3. Dispare primeiro contato por e-mail e WhatsApp
4. Em 3 dias: rode `python scripts/automation/agendar_followup_tracker_auto.py`
5. Em 7 dias: envie follow-up com case baseado em `docs/sales/email-follow-up-b2b-litoral.md`
6. Quando houver resposta: use `docs/sales/classificador-respostas-leads-praia-digital-2026.html`
7. Pós-demo: gere e-mails com `python scripts/automation/gerar_emails_pos_demo.py` e importe `docs/sales/csv-lotes-email/emails-pos-demo-importaveis-2026-07-12.csv`
8. Follow-up final: use `docs/sales/follow-up-3-fechamento.md`

---

## 2. Arquivos por função
| Função | Arquivo |
|---|---|
| Lote e-mail Brevo | `docs/sales/csv-lotes-email/lote-brevo-top20-2026-07-12.csv` |
| Lote WhatsApp | `outreach/whatsapp-top20-mensagens-prontas.html` |
| Follow-up 3d | `docs/sales/follow-up-1-3dias.md` |
| Follow-up 7d | `docs/sales/follow-up-2-7dias.md` |
| Fechamento | `docs/sales/follow-up-3-fechamento.md` |
| Classificador | `docs/sales/classificador-respostas-leads-praia-digital-2026.html` |
| Pós-demo | `outreach/emails-pos-demo/` |
| CSVs pós-demo | `docs/sales/csv-lotes-email/emails-pos-demo-importaveis-2026-07-12.csv` |
| Agenda de reuniões | `docs/sales/agendamento-call-top20-2026-07-12.html` |
| Roteiro de call | `docs/sales/roteiro-videocall-top20-2026-07-12.html` |
| Dashboard | `docs/sales/dashboard-prospeccao-top20-2026-07-12.html` |
| Relatório diário | `docs/sales/relatorio-diario-execucao-2026-07-12.html` |

---

## 3. Regra de ouro
**Não criar novo conteúdo** enquanto houver ação pendente não executada desta lista.

Ação prioritária agora: importar o top20 no Brevo e enviar.

Site: https://acarolmourad-commits.github.io/praia-digital/  
Ferramentas gratuitas: https://praia.digital
