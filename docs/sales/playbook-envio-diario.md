
# Playbook de Envio Diário — Outreach Praia Digital
Objetivo: transformar assets em prospecção enviada de verdade, sem inventar mais templates repetidos.

## 1) Preparar lote no Gmail (Mail Merge)
- Abra o arquivo `outreach/importacao-email.csv`
- Crie um rascunho no Gmail baseado em `outreach/kit-comercial-completo.html`
- Use colunas: {{email}} e {{subject}}
- Dispare até 50 envios/dia

## 2) Acompanhar respostas
- Marque no `docs/sales/followup-registro.md` leads que responderam
- Separe: positivos, neutros, objeções

## 3) Executar follow-ups
- Dispare `followup-3dias-*` no dia 3 e `followup-7dias-*` no dia 7
- Para neutros, use `outreach/reativacao-inicial-*.html`

## 4) Fechar calls
- Use `outreach/call-lead-*.html` e atualize status no tracker

## 5) Métricas diárias
- Envios do dia
- Respostas
- Calls agendadas
- Parcerias iniciadas
