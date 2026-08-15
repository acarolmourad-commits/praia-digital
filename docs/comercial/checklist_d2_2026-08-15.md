# Checklist — Execução D2 (16/08)
Data alvo: 2026-08-16
Horário: 09:00 (cron diário)

## Pré-requisitos
- [x] Script `follow_up_automacao.py` testado
- [x] Cron diário ativo às 09:00
- [x] Mensagens D2 preparadas
- [x] CRM com status ENVIADO_D0 e datas

## Execução em 16/08
1. Cron executa script às 09:00
2. Script verifica respostas nos 6 leads
3. Se sem resposta: marca ENVIADO_D2 no CRM
4. Se com resposta: aplica regra correspondente
5. Atualiza métricas no painel

## Ação humana após D2
- Revisar status dos leads
- Enviar mensagens D2 para leads sem resposta
- Responder leads que perguntaram preço
- Handoff para leads com resposta positiva/agendamento

## Métricas esperadas
- Taxa de resposta: 0-16% (0-1/6)
- Taxa de resposta positiva: 0-16% (0-1/6)
- Pedidos de preço: 0-1
- Pedidos de agendamento: 0-1

## Próxima atualização
Após D2 ou quando houver primeira resposta.
