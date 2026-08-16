# Execução D2 — 2026-08-17
Regra: executar apenas se não houver resposta até 17/08. Se houver resposta positiva/negativa/preço/agendamento, aplicar regra correspondente.

## Ação do script follow_up_automacao.py em 17/08
- Para cada lead com status ENVIADO_D0 e sem resposta:
  - Atualizar status para ENVIADO_D2
  - Registrar d2_enviado_em = 2026-08-17
  - Não enviar mensagem automaticamente — apenas marcar no CRM
- Para leads com resposta positiva: parar follow-up + HANDOFF
- Para leads com resposta negativa: encerrar
- Para leads com pedido de preço: responder com preço aprovado
- Para leads com pedido de agendamento: HANDOFF HUMANO

## Mensagens D2 prontas para envio humano
| lead_id | canal | D2 |
|---------|-------|-----|
| 9 | OLX | "Olá, passando para lembrar que podemos melhorar as fotos e a descrição da casa em Juquehy e ajudar a aumentar as reservas. Se quiser, envio um exemplo rápido." |
| 11 | OLX | "Olá, passando para lembrar que podemos melhorar as fotos e a descrição da casa em Indaiá e ajudar a aumentar as reservas. Se quiser, envio um exemplo rápido." |
| 14 | Instagram | "Olá, passando para lembrar que podemos melhorar as fotos e a apresentação da casa em Indaiá e ajudar a aumentar as reservas. Se quiser, envio um exemplo rápido." |
| 15 | Facebook/WhatsApp | "Olá, passando para lembrar que podemos melhorar o anúncio e a gestão da temporada em Bertioga Centro e ajudar a aumentar a ocupação. Se quiser, envio um diagnóstico rápido." |
| 27 | Instagram/WhatsApp | "Olá, passando para lembrar que podemos melhorar a gestão da temporada e ajudar a aumentar a ocupação e avaliações. Se quiser, envio um diagnóstico rápido." |
| 29 | Facebook/WhatsApp | "Olá, passando para lembrar que podemos melhorar a gestão e os anúncios de Bertioga e ajudar a aumentar a ocupação. Se quiser, envio um diagnóstico rápido." |

## Regras de parada
- Resposta negativa → encerrar
- Pedido para não receber mensagens → bloquear
- Interessado → HANDOFF HUMANO
- Perguntou preço → responder com preço aprovado
- Pediu agendamento → HANDOFF HUMANO
