# Pacote de Medição D2 — 17/08
Horário: 09:00

## 1. Verificação pré-D2
Arquivo: `docs/comercial/verificacao_pre_d2_2026-08-17.md`
Comando: `python scripts/verificacao_pre_d2_2026-08-17.py`
Saída: confirma 0 respostas e prontidão

## 2. Execução D2
Script: `scripts/executar_d2_2026-08-17.py`
Comando: `python scripts/executar_d2_2026-08-17.py`
Ação: atualiza CRM, gera resultado, roda automações, commita
Ordem: 9 → 11 → 14 → 15 → 27 → 29

## 3. Medição pós-D2
Comandos:
- `python scripts/follow_up_automacao.py`
- `python scripts/relatorio_diario_motor_b.py`
- `python scripts/painel_unificado_motor_a_b.py`

## 4. Validação
- `git status --short`
- `git log -1 --oneline`
- Verificar `docs/comercial/resultado_d2_2026-08-17.md`

## 5. Handoff humano
Se resposta positiva/preço/agendamento → comercial@praia.digital / (11) 95434-6288
