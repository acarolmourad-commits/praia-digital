# Follow-up execution plan — D0/D2/D5/D10
Data: 2026-08-15
Regra: parar imediatamente se houver resposta negativa, pedido de não contato, bloqueio ou desinteresse.

## Status atual dos 4 handoffs
| lead_id | serviço | score | status | preço |
|---------|---------|-------|--------|-------|
| 9 | Fotografia + Edição de anúncio | 82 | APROVADO_PARA_ABORDAGEM_HUMANA | R$ 700+ / R$ 497 |
| 11 | Fotografia + Edição de anúncio | 80 | APROVADO_PARA_ABORDAGEM_HUMANA | R$ 700+ / R$ 497 |
| 14 | Fotografia + Edição de anúncio | 83 | APROVADO_PARA_ABORDAGEM_HUMANA | R$ 700+ / R$ 497 |
| 15 | Edição de anúncio + Administração Airbnb | 79 | APROVADO_PARA_ABORDAGEM_HUMANA | R$ 497 / 10-15% |

## Execução automática permitida
- Documentação e templates prontos
- Nenhuma mensagem externa será enviada sem aprovação humana
- Follow-up D0/D2/D5/D10 documentado em follow_up_handoffs_2026-08-15.md

## Próxima ação humana necessária
1. Enviar mensagens D0 para leads 9, 11, 14, 15
2. Após envio, executar follow-up sequencial D0 → D2 → D5 → D10
3. Quando houver resposta positiva: mover para AÇÃO_HUMANA_PENDENTE com resumo
