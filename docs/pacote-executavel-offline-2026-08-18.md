# Pacote executável offline — Link Automation + Evolução Praia Digital

## Bloqueio registrado
- GATE_EXECUCAO_PYTHON = BLOQUEADO
- Motivo: gateway impede execução de scripts Python que poderiam reiniciar/parar o próprio gateway
- Dependência: EXECUÇÃO EXTERNA / AMBIENTE SEPARADO
- Data: 2026-08-18

## Arquivos preparados
- scripts/link_automation/scaffold.py
- scripts/link_automation/apply_lote_1.py
- scripts/link_automation/rollback.py
- scripts/link_automation/dry-run-report.json
- scripts/link_automation/batch-log.json
- docs/link-automation-lote-1-especificacao-2026-08-18.md
- docs/roteiro-marca-jornada-2026-08-17.md
- docs/plano-priorizacao-2026-08-17.md

## Checklist pré-execução
- [ ] Confirmar que o ambiente NÃO é o gateway bloqueado
- [ ] Confirmar que DRY_RUN=False em apply_lote_1.py
- [ ] Confirmar que rollbacks/ existe
- [ ] Confirmar que batch-log.json existe
- [ ] Confirmar que dry-run-report.json está atualizado
- [ ] Confirmar que os 8 arquivos do escopo existem
- [ ] Confirmar que uploads/, academy/financeiro/, tests/ não serão alterados
- [ ] Fazer backup do repositório antes da execução

## Checklist pós-execução
- [ ] Verificar git diff --name-only
- [ ] Confirmar exatamente 8 arquivos alterados
- [ ] Verificar batch-log.json
- [ ] Verificar rollbacks/ com 8 snapshots
- [ ] Executar bounded_link_check.py
- [ ] Executar testes da Academy
- [ ] Se regressão: executar rollback
- [ ] Se sucesso: reportar detalhes

## Instruções de execução
1. Abrir terminal fora do gateway atual
2. cd C:\Users\Carolina\praia-digital
3. python scripts/link_automation/apply_lote_1.py
4. Verificar saída
5. Executar validações pós-execução

## Dependências
- Python 3.11+
- pathlib
- json
- csv
- hashlib
- datetime
- re
- dataclasses

## Registro de bloqueio
Este pacote NÃO pode ser executado no ambiente atual.
Executar somente em ambiente externo separado.
