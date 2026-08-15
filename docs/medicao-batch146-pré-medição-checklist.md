# Pré-medição Batch146 — Checklist rápido para 2026-09-12

Execute este checklist na manhã de 2026-09-12 antes de rodar `scripts/collect_batch146_metrics.py`.

## 1. Repositório
- [ ] Working directory limpo: `git status --short` sem arquivos não commitados
- [ ] Branch `main` atualizada: `git pull origin main`

## 2. Blog — existência local
- [ ] Confirmar 23 slugs em `blog/` via script ou glob
- [ ] Nenhum arquivo ausente ou com nome divergente

## 3. Blog — publicação remota
- [ ] `https://praia.digital/blog/<slug>.html` retorna HTTP 200 para os 23 slugs
- [ ] Sem redirects inesperados

## 4. Script de coleta
- [ ] `scripts/collect_batch146_metrics.py` existe e é executável
- [ ] Execução anterior não quebrou dependências

## 5. Execução
- [ ] Rodar `python scripts/collect_batch146_metrics.py`
- [ ] Confirmar `docs/medicao-batch146-resultado.json` atualizado
- [ ] Confirmar `summary.local.exists == 23/23`
- [ ] Confirmar `summary.remote.remote_ok == 23/23`

## 6. Pós-coleta
- [ ] Atualizar `docs/medicao-batch146.json` com `status: measurement_done`
- [ ] Atualizar `docs/medicao-batch146-resultado.json` com `measurement_date: 2026-09-12`
- [ ] `git add docs/medicao-batch146*.json`
- [ ] `git commit -m "docs: Batch146 — registro de medição 2026-09-12"`
- [ ] `git push origin main`

## Observações
- Métricas de GSC/ferramentas externas devem ser inseridas manualmente em `docs/medicao-batch146-resultado.json` após coleta automatizada
- Não executar antes de 2026-09-09 para respeitar janela de medição de 30 dias
