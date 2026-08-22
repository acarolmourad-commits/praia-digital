# Pipeline de retomada — execução externa

## Gatilho
Quando for confirmado um ambiente/execução fora do gateway atual, executar automaticamente na ordem abaixo.

## Passo 1 — Lote 1
```bash
cd C:\Users\Carolina\praia-digital
python scripts/link_automation/apply_lote_1.py
```

Critérios:
- batch_id deve ser registrado
- applied deve ser 21
- skipped/errors devem ser 0
- rollbacks/ deve conter 8 snapshots

## Passo 2 — Validação pós-Lote 1
```bash
git diff --name-only
```
Esperado: exatamente 8 arquivos alterados.

```bash
python scripts/link_automation/rollback.py <batch_id>
```
Usar apenas se houver regressão.

```bash
python scripts/bounded_link_check.py
```
Esperado: redução de 21 quebras nos destinos alvo.

```bash
cd academy && python -m pytest tests/test_delivery_flow.py tests/test_e2e_delivery.py tests/test_security.py tests/test_financeiro.py tests/test_financeiro_integration.py tests/test_64_cursos_compatibilidade.py -q
```
Esperado: todos verdes.

## Passo 3 — Arquitetura B
Somente após:
- Lote 1 aplicado
- Validação pós-lote OK
- Autorização humana confirmada

Executar:
- Ajuste de navegação/hierarquia
- Separação de CTAs por jornada
- Validação SEO + acessibilidade + conversão

## Regras
- Nada de edição manual dos 21 arquivos
- Rollback sempre disponível
- Um lote por vez
- Autorização humana obrigatória para Arquitetura B
- Manter DRY_RUN ativo por padrão até execução externa

## Bloqueio atual
- GATE_EXECUCAO_PYTHON = BLOQUEADO
- Dependência: ambiente externo confirmado
