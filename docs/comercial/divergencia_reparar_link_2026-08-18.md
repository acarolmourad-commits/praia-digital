# Divergência encontrada — REPARAR_LINK vs realidade técnica
Data: 2026-08-18
Fonte: docs/comercial/plano_reparo_404_2026-08-18.csv + bounded_link_check.py

## Achado
Há 13 registros classificados como `REPARAR_LINK` (prioridade 1).
Após verificação:
- Para todos os 13, o campo `substituta_local` é idêntico à URL quebrada.
- Destino confirmado existente localmente para todos.
- Não há substituta diferente; portanto NÃO se trata de link quebrado.

## Interpretação correta
É um caso de `DEPLOY_NAO_ENTREGA_200`:
arquivo existe localmente, conteúdo aparentemente válido, URL conhecida,
mas ambiente publicado não retorna HTTP 200.

## Categorias sugeridas
REPARAR_LINK: 0 neste lote
DEPLOY_NAO_ENTREGA_200: 13 (blog + outreach)
Nenhuma ação de substituição deve ser executada agora.
