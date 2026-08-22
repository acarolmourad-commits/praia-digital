# Auditoria cluster documentação imobiliária
Data: 2026-08-17

## Escopo
- Documentação imobiliária + financiamento + escritura + registro + avaliação/PTAM + estrangeiros + inventário/herança.
- `education/cursos`/`academy/cursos`/`backup`: fora do cluster editorial; apenas como oportunidade de link interno.
- Não publicado/alterado/removido; somente diagnóstico.

## Arquivo CSV
- docs\editorial\auditoria-cluster-documentacao-2026-08-17.csv

## Totais por categoria
- AVALIACAO: 238
- COMPRA_VENDA: 1107
- DOC_COMPRA_VENDA: 447
- DOC_TEMPORADA: 20
- ESTRANGEIRO: 15
- HERANCA_INVENTARIO: 4
- LOCACAO_TEMPORADA: 1079
- RELACIONADO: 10486

## Critérios de classificação
- MANTER: página alinhada à intenção, sem canibalização aparente.
- ATUALIZAR: conteúdo existente, mas título/meta desatualizados ou desalinhados; sem mudança estrutural.
- EXPANDIR: página rasa que responde à intenção, mas sem profundidade suficiente para competir.
- FUNDIR: duas ou mais páginas com intenção e título quase idênticos; uma deve canônica e as outras devem apontar para ela.
- NOVO GAP: intenção expressiva sem página dedicada suficiente.

## Regra de canibalização
- Se duas páginas competem pela mesma query principal e têm títulos/meta quase iguais, priorizar FUNDIR.
- Não manter páginas com canonical divergente para mesma intenção.

## Mapa inicial de oportunidades (PENDENTE CRUZAMENTO GSC)
- Conferir impressões/CTR por URL em `docs/seo/gsc-improvement-plan-2026-08-17.md` e `docs/seo/gsc-improvement-checklist-pos-d2-2026-08-17.md`.
- Priorizar por: evidência real no GSC > intenção comercial > potencial conversão > ausência de conteúdo.

## Recomendações provisórias
- Manter separado: documentação de compra/venda, financiamento, escritura/registro, avaliação/PTAM, estrangeiro, herança/inventário.
- Locação/temporada: manter cluster separado; ligar com links internos para documentação quando houver relevância.
- Não criar hub genérico “documentação” se já houver múltiplas páginas especializadas; evitar canibalização.

## Próximos passos
- Cruzar CSV com GSC real para priorizar URLs com impressão.
- Selecionar amostra para leitura profunda e validar classificação.
- Propor arquitetura definitiva e ordem de produção.
