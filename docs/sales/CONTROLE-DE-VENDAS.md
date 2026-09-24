# Controle de Vendas — Praia Digital

## Princípio
**O produto só é entregue após a confirmação do pagamento.** Nenhuma venda é registrada sem produto identificado.

## Pipeline obrigatório por lead
1. **Produto_Consultado** — o que o lead perguntou/demonstrou interesse (ex.: avaliação de imóvel, plano profissional, captação, automação).
2. **Produto_Comprado** — o que foi efetivamente vendido (obrigatório para marcar Status=fechou).
3. **Proposta_ID** — referência da proposta enviada (ver `tracker-propostas-comerciais-praia-digital-2026.html`).
4. **Data_Fechamento** — quando o cliente aceitou.
5. **Forma_Pagamento** — Pix / boleto / cartão / transferência.
6. **Status_Pagamento** — `pendente` | `pago` | `atrasado` | `estornado`.
7. **Comprovante** — link/arquivo do comprovante (obrigatório para confirmar pagamento).
8. **Data_Pagamento** — quando o pagamento foi confirmado.
9. **Data_Entrega** — quando o produto foi entregue (somente após pagamento confirmado).

## Arquivos
- `csv-lotes-email/tracker-whatsapp-proprietarios.csv` — funil WhatsApp (colunas de venda ampliadas em 2026-09-23)
- `csv-lotes-email/tracker-email-proprietarios.csv` — funil e-mail (mesma estrutura)
- `pagamentos.csv` — livro-caixa: cada pagamento/comprovante/entrega por lead
- Dashboards consolidados leem os trackers a cada cronjob diário.

## Regras
- Status `fechou` **exige**: Produto_Comprado + Proposta_ID + Data_Fechamento.
- Receita nos dashboards só conta com Status_Pagamento = `pago` e Comprovante preenchido.
- Venda sem produto identificado → manter Status `respondeu` + Obs explicando (caso Fernanda Lima, lote 149 — não registrada em 2026-09-23 por falta de produto).
