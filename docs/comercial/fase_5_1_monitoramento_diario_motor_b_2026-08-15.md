# Fase 5.1 — Monitoramento diário do Motor B
Data: 2026-08-15
Estado: coleta real iniciada com base limpa

## Regras

- Coleta orgânica sem mídia paga
- Não classificar funil como VALIDADO/OTIMIZAR/REESTRUTURAR com base em menos de 20-30 conclusões
- 20-30 conclusões servem como primeiro marco operacional: dados suficientes para escolher o primeiro experimento baseado em comportamento observado, não como validação estatística definitiva
- Não alterar perguntas, pontuação, CTA, oferta ou tracking antes de evidência suficiente, exceto erro técnico
- Não otimizar aquilo que ainda não apresentou evidência de problema
- O primeiro 1/1/1/1/1 é sinal de funcionamento técnico, não taxa de conversão estrutural

## Operação autônoma

O Hermes deve operar sem pedir autorização a cada ciclo:
coletar → registrar → detectar anomalias → gerar relatório → continuar.

## Gatilho automático quando houver novos dados

1. Atualizar o acumulado
2. Comparar com o dia anterior
3. Verificar anomalias
4. Identificar o maior gargalo
5. Manter o sistema intacto até a amostra chegar ao marco de 20–30 conclusões
6. Quando atingir 20-30 conclusões, propor um único primeiro experimento, com hipótese e critério de sucesso

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

Importante: a classificação é um ponto de partida para o primeiro experimento, não um veredito final de validação estrutural.

## Motor A

- Leads em ENVIADO_D0: 6
- D2: 17/08 às 09:00
- Sem alterações
