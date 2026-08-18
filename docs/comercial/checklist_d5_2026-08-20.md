# Checklist de execução D5 — 20/08
Uso: executar em 20/08 se 0 respostas após D2.

## Pré-requisitos
- [ ] Confirmar 0 respostas nos 6 leads em `docs/comercial/leads_sao_sebastiao_bertioga.csv`
- [ ] Confirmar `d2_enviado_em = 2026-08-17` nos 6 leads
- [ ] Ter acesso aos canais: OLX, Instagram, Facebook/WhatsApp

## Sequência de envio
1. Lead 9 — Juquehy (OLX)
2. Lead 11 — Indaiá (OLX)
3. Lead 14 — Indaiá (Instagram)
4. Lead 15 — Bertioga Centro (Facebook)
5. Lead 27 — Temporada Bertioga (Instagram)
6. Lead 29 — Bertioga Aluga (Facebook)

## Após cada envio
- [ ] Registrar data/hora no CRM
- [ ] Confirmar mensagem entregue

## Após todos os envios
- [ ] Rodar `python scripts/follow_up_automacao.py`
- [ ] Verificar métricas do dia
- [ ] Commit no CRM se houver alterações
- [ ] Atualizar `docs/comercial/monitoramento_resultados_2026-08-15.md`

## Regras de parada
- Resposta negativa → encerrar follow-up do lead
- Pedido para parar → bloquear lead
- Interessado/preço/agendamento → handoff humano
