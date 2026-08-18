# Análise pós-D5 — Motor A
Data de referência: 2026-08-18
Gatilho: 20/08

## Pré-requisitos
- [ ] Confirmar 0 respostas nos 6 leads antes de disparar D5
- [ ] Confirmar que D2 foi enviado em 17/08
- [ ] Disparar D5 conforme `roteiro_envio_d5_execucao_2026-08-20.md`

## Classificação obrigatória após D5
- **Positiva** → `HANDOFF_HUMANO` + registrar: `SERVIÇO → VALOR POTENCIAL → ESTÁGIO → PRÓXIMA AÇÃO → RESPONSÁVEL`
- **Preço** → `RESPONDENDO_PRECO` + responder com preço aprovado
- **Agendamento** → `AGENDAMENTO_HUMANO`
- **Negativa** → `ENCERRADO`
- **Bloqueio** → `BLOQUEADO`
- **Sem resposta** → aguardar D10 em 25/08

## Critérios de parada
- Resposta negativa → encerrar follow-up
- Pedido para parar → bloquear
- Interessado/preço/agendamento → handoff humano e parar follow-up

## Métricas a registrar individualmente
- Taxa de resposta: respostas / 6
- Taxa de resposta positiva: positivas / 6
- Pedidos de preço: count
- Pedidos de agendamento: count
- Objeções recorrentes: lista
- Tempo até primeira resposta: média em horas

## Próximo passo pós-D5
- Se respostas: classificar → handoff ou continuar
- Se 0 respostas: D10 em 25/08
- Bloqueio de prospecção mantido até 25/08
