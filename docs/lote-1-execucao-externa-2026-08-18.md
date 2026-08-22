# Lote 1 — Execução EXCLUSIVA em ambiente externo

## Estado
- PRONTO_PARA_EXECUCAO_EXTERNA
- NÃO EDITAR MANUALMENTE
- NÃO aplicar correções por sed/awk/edit manual
- NÃO alterar arquivos fora do scaffold

## Motivo
- O ambiente atual bloqueia execução de scripts Python por restrição de gateway
- Qualquer edição manual dos 21 arquivos quebra o pipeline automatizado
- O objetivo é manter automação, não substituí-la por trabalho manual

## Arquivos necessários
- scripts/link_automation/apply_lote_1.py
- scripts/link_automation/rollback.py
- scripts/link_automation/scaffold.py
- scripts/link_automation/dry-run-report.json
- scripts/link_automation/batch-log.json
- docs/link-automation-lote-1-especificacao-2026-08-18.md

## Procedimento externo
1. Abrir terminal FORA do gateway atual
2. cd C:\Users\Carolina\praia-digital
3. Verificar DRY_RUN=False em apply_lote_1.py
4. Executar: python scripts/link_automation/apply_lote_1.py
5. Verificar saída: 21 aplicadas, 0 erros
6. Verificar git diff --name-only (8 arquivos esperados)
7. Verificar batch-log.json
8. Verificar rollbacks/ com 8 snapshots
9. Se regressão: python scripts/link_automation/rollback.py <batch_id>
10. Se sucesso: reportar detalhes

## Proteções
- Escopo limitado a 8 arquivos
- Uploads/, academy/financeiro/, tests/ não serão alterados
- Rollback exclusivo do lote
- Nenhum commit automático

## Critério de sucesso
- 21/21 aplicadas
- 0 arquivos fora do escopo alterados
- rollback funcional
