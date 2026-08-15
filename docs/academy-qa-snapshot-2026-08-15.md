# Academy — QA snapshot 2026-08-15

## Estado atual
- Repositório: `main` limpo
- Cursos: 64/64 mapeados
- Testes: maior parte verde
- Deploy: **aguardando humano**

## Resultado de smoke
- `tests/test_smoke.py`: 12 passed
- `tests/test_e2e_delivery.py`: 10 passed
- `tests/test_phase1.py` a `test_phase5.py`: green
- `tests/test_delivery_flow.py`: green
- `tests/test_leads.py`: green

## Pendências conhecidas
- `tests/test_checkout_public.py`: 2 failures — comportamento atual parece rejeitar checkout sem usuário autenticado; revisar regra de negócio antes de considerar bug.
- Outras falhas residuais podem ser de escopo de DB em módulos específicos; verificar individualmente.

## Evidência
- Arquivo de teste: `academy/tests/`
- Schema local usada pelos testes: `sqlite:///:memory:`
- Nenhuma alteração destrutiva feita fora de `academy/tests/` e `academy/pyproject.toml`.
