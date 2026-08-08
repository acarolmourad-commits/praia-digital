# Automação de Atendimento — Praia Digital Academy

Visão: reduzir o tempo de resposta e manter atendimento 24h usando automação sem perder tom humano.

## Regras principais
- Sem automação cega; mensagens devem ser contextualizadas.
- Sempre oferecer saída humana rápida.
- Nunca simular leitura de arquivos/pastas.
- Não prometer prazos impossíveis.

## Fluxo WhatsApp
1. Cliente envia mensagem para (11) 95434-6288
2. Bot responde saudação + menu inicial:
   - 1) Suporte ao curso
   - 2) Financeiro/pagamento
   - 3) Dúvida antes de comprar
   - 4) Falar com humano
3. Respostas usam FAQ_ACADEMY.md como base.

## Templates de mensagem
- Saudação: "Olá! Bem-vindo à Praia Digital Academy. Como posso ajudar?"
- Suporte: "Posso ajudar com acesso, login ou conteúdo. Qual o erro?"
- Financeiro: "Para pagamentos e notas fiscais, informe o pedido."
- Indefinido: "Não entendi. Quer falar com um atendente?"

## Follow-up automático
- 10min: "Ainda está aí? Posso ajudar com mais alguma coisa?"
- 1h: "Se a dúvida persistir, chame no WhatsApp (11) 95434-6288."
- 24h: encerrar se sem resposta.

## Entregáveis
- Integração com WhatsApp Business API ou Zenvia/Wati.
- Script Python para enviar mensagens automáticas.
- Relatório de atendimento automático.
