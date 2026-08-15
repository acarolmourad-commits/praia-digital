# Batch 152 — Candidate Topics

Generated at: 2026-08-15T00:40:00+00:00

Fonte: `docs/banco-editorial.json` → Auditoria de cobertura (gaps estrategicamente relevantes)

## Metodologia
- Analisar combinações cidade+cluster com menos de 3 artigos
- Excluir gaps já atendidos pelas batches anteriores
- Priorizar clusters de maior impacto comercial
- Selecionar top 6 gaps

## Observação
- As cidades específicas (Santos, Guarujá, Praia Grande, São Vicente, São Sebastião, etc.) já estão com >=3 artigos por cluster.
- Os gaps restantes são majoritariamente **regionais**: `litoral_norte`, `litoral_sp`, `litoral_sul`.
- Existe 1 gap sem city definida: `(none) + financiamento`.

## Gaps Selecionados

1. Litoral Norte + bairros e cidades (`litoral-norte-bairros-imoveis-2026.html`)
2. Litoral Norte + editorial (`litoral-norte-editorial-imoveis-2026.html`)
3. Litoral Norte + investimento (`litoral-norte-investimento-imoveis-2026.html`)
4. Litoral SP + compra e venda (`litoral-sp-compra-venda-imoveis-2026.html`)
5. Litoral SP + editorial (`litoral-sp-editorial-imoveis-2026.html`)
6. Litoral SP + aluguel de temporada (`litoral-sp-aluguel-temporada-2026.html`)

## Observação
Esses são os últimos gaps de cobertura disponíveis em `banco-editorial.json` para <3 artigos por combinação.

Próximo passo: gerar conteúdo seguindo a ordem de clusters definida no projeto.
