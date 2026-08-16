# Fase 5.1 — Monitoramento diário do Motor B
Data: 2026-08-15
Estado: coleta real iniciada com base limpa

## Regras

- Coleta orgânica sem mídia paga
- Não classificar funil como VALIDADO/OTIMIZAR/REESTRUTURAR com base em menos de 20-30 conclusões
- Não alterar perguntas, pontuação, CTA, oferta ou tracking antes de evidência suficiente, exceto erro técnico

## Report diário

Script: `scripts/relatorio_diario_motor_b.py`
Arquivo: `docs/comercial/acompanhamento_diario_motor_b_YYYY-MM-DD.md`

Registrar:
- visitantes
- inícios
- conclusões
- CTAs
- leads
- taxas entre etapas
- pontuação média
- distribuição 🔴 🟡 🟢
- origem do tráfego
- abandonos por etapa
- leads duplicados bloqueados
- novos leads qualificados
- observações qualitativas

Comparação:
- resultado do dia
- acumulado
- variação contra dia anterior
- gargalo atual

## Alertas

Sinalizar imediatamente:
- quebra de tracking
- duplicidade
- queda anormal de conversão
- erro no CRM
- lead sem origem
- evento registrado fora de ordem

## Regra comercial

Todo novo lead do Motor B entra no fluxo próprio:
LEAD → QUALIFICAÇÃO → D0 → D2 → D5 → D10
sem interferir nos 6 leads existentes do Motor A.

## Regra de decisão

Quando atingir 20-30 conclusões, apresentar:
- classificação: 🟢 VALIDADO / 🟡 OTIMIZAR / 🔴 REESTRUTURAR
- evidências
- principal gargalo
- hipótese
- experimento recomendado
- impacto esperado
- critério de sucesso

## Motor A

- Leads em ENVIADO_D0: 6
- D2: 17/08 às 09:00
- Sem alterações
