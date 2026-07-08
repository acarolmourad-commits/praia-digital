
# Roteiro de Execução — Próximos 7 Dias
Gerado em: 2026-07-08
Objetivo: avançar negociação com leads ativos usando assets existentes.

## Dia 1 — Hoje
- Enviar `envio-auto-655.html` para Lead 655 (follow-up comercial).
- Enviar `envio-auto-631.html` para Lead 631 (nova proposta personalizada).
- Registrar datacom confirmacão do envio no tracker.

## Dia 2
- Enviar `followup-call-lead-655.html` para agendar call com Lead 655.
- Enviar 5 novos `envio-auto-*` para leads prioritários sem contato recente.
- Atualizar status no tracker para `call agendada` quando houver resposta.

## Dia 3
- Disparar `followup-3dias-lead-*.html` para leads com envio inicial no Dia 1.
- Revisar respostas recebidas e aplicar `script-objecoes-comerciais.html` conforme objeção.
- Commitar atualizações do tracker.

## Dia 4
- Enviar `call-lead-*.html` para leads com respostas positivas.
- Reativar leads neutros com conteúdo de SEO: `blog/captacao-leads-digitais-litoral-2026.html`.
- Registrar calls agendadas.

## Dia 5
- Disparar `followup-7dias-lead-*.html` para leads do Dia 1.
- Aplicar `email-resposta-proposta-comercial.html` para respostas recebidas.
- Reforçar CTA de parceria com CTA direto.

## Dia 6
- Follow-up pós-call para leads que receberam `call-lead-*.html`.
- Onboarding inicial para leads com call confirmada usando `onboarding-parceria-automatizado.html`.
- Medir taxa de resposta e atualizar dashboard.

## Dia 7
- Fechamento para leads prontos usando `fechamento-lead-*.html`.
- Revisar tracker e identificar leads para reativação.
- Planejar próxima semana e renovar lote de 20 novos leads se taxa permitir.

## Métricas a acompanhar
- Envios realizados vs. planejado.
- Respostas recebidas por tipo (positivo, neutro, negativo).
- Calls agendadas e realizadas.
- Parcerias fechadas.

## Observações
- Quando SMTP for configurado, substituir envio manual por `scripts/email_batch_sender.py`.
- Manter site e API monitorados; erros em fetch devem ser tratados com fallback local.
