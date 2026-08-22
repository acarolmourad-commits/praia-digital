# Lote 1 — Especificação de reparo de links determinísticos

## Estado
- PENDENTE_DE_EXECUÇÃO
- Bloqueio: gateway impede execução de scripts Python no ambiente atual
- Solução: executar em ambiente externo separado

## Escopo
- Apenas arquivos em `anfitrioes/` e `assets/`
- Apenas 21 ocorrências classificadas como `REPARAR` pelo scaffold
- Não ampliar regras para outros arquivos
- Não executar correções ambíguas

## Candidatos

### Grupo 1 — anfitrioes/
| Arquivo | Link original | Novo destino | Regra | Confiança |
|---------|---------------|--------------|-------|-----------|
| anfitrioes/central-airbnb.html | tutoriais-anfitrioes.html | anfitrioes/tutoriais-anfitrioes.html | R002 | ALTO |
| anfitrioes/central-airbnb.html | checklists-anfitrioes.html | anfitrioes/checklists-anfitrioes.html | R003 | ALTO |
| anfitrioes/central-airbnb.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-airbnb.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-booking.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-booking.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-booking.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-priceplabs.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-priceplabs.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-priceplabs.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-stays.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |
| anfitrioes/central-stays.html | tutoriais-anfitrioes.html | anfitrioes/tutoriais-anfitrioes.html | R002 | ALTO |
| anfitrioes/central-stays.html | diagnosticos-anfitrioes.html | anfitrioes/diagnosticos-anfitrioes.html | R001 | ALTO |

### Grupo 2 — assets/
| Arquivo | Link original | Novo destino | Regra | Confiança |
|---------|---------------|--------------|-------|-----------|
| assets/busca-inteligente.html | analise-completa-imovel.html | assets/analise-completa-imovel.html | R004 | ALTO |
| assets/painel-ferramentas.html | analise-completa-imovel.html | assets/analise-completa-imovel.html | R004 | ALTO |
| assets/retorno-gestao-completa.html | roi-ia-imobiliaria.html | assets/roi-ia-imobiliaria.html | R005 | ALTO |
| assets/retorno-gestao-completa.html | servico-avaliacao-preco-imoveis-litoral.html | assets/servico-avaliacao-preco-imoveis-litoral.html | R006 | ALTO |
| assets/simulador-roi-proprietario.html | roi-ia-imobiliaria.html | assets/roi-ia-imobiliaria.html | R005 | ALTO |
| assets/simulador-roi-proprietario.html | servico-avaliacao-preco-imoveis-litoral.html | assets/servico-avaliacao-preco-imoveis-litoral.html | R006 | ALTO |

Total: 21 ocorrências em 8 arquivos.

## Pré-requisitos
- Ambiente de execução separado do gateway atual
- `scripts/link_automation/apply_lote_1.py`
- `scripts/link_automation/scaffold.py`
- `scripts/link_automation/rollback.py`
- dry-run-report.json atualizado
- batch-log.json inicializado
- diretório rollbacks/ criado

## Procedimento
1. Confirmar que DRY_RUN=False no script
2. Executar apply_lote_1.py
3. Verificar batch-log.json
4. Verificar rollbacks/ com snapshots
5. Validar que apenas 8 arquivos foram alterados
6. Validar que nenhum arquivo fora do escopo foi alterado
7. Verificar links com bounded_link_check.py
8. Executar testes da Academy se houver alteração em academy/
9. Se houver regressão: rollback do lote
10. Se houver sucesso: reportar detalhes

## Validações pós-execução
- git diff --name-only deve listar exatamente: os 8 arquivos do escopo
- Nenhum arquivo em uploads/, academy/financeiro/, tests/ pode estar alterado
- batch-log.json deve conter o lote com dry_run=false
- rollbacks/ deve conter 8 arquivos de snapshot
- link-check deve mostrar redução de 21 quebras nos destinos alvo

## Rollback
- Comando: python scripts/link_automation/rollback.py <batch_id>
- Restaura apenas os arquivos do lote
- Não afeta outros lotes ou alterações existentes

## Critérios de sucesso
- 21 ocorrências processadas
- 21 aplicadas com sucesso
- 0 erros
- 0 arquivos fora do escopo alterados
- rollback funcional

## Registro do bloqueio
- GATE_EXECUCAO_PYTHON = BLOQUEADO
- Motivo: gateway impede execução de scripts Python
- Dependência: EXECUÇÃO EXTERNA / AMBIENTE SEPARADO
- Data: 2026-08-18
