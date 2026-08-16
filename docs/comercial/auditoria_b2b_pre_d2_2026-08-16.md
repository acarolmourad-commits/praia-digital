# Auditoria B2B — Operação Paralela Pré-D2
Data: 2026-08-16
Fonte: docs/sales/csv-lotes-b2b/

## Resumo
- Total raw: 733 leads
- Phones únicos: 586
- Duplicatas por telefone: 20
- Lotes principais: b2b-rev (477 dedup), b2b-wl (95), automacao (8), captacao (8), descricao (16), consultoria (8), seo-local (8), avaliacao (8), proptech (16), planos (6)

## Status
- pendente_msg1: 717
- enviado_msg1: 16

## Problemas encontrados
1. 597 leads sem Valor_Estimado
2. 24 leads sem Email
3. 20 duplicatas por telefone exato
4. Lotes `b2b-rev` e `b2b-wl` concentram 572 leads (78% do total)

## Ranking preliminar (top 20)
- Topo dominado por `b2b-rev` com score 98-99
- Maioria sem valor estimado preenchido
- Sem valores diferentes de zero para a maioria

## Classificação por potencial de receita
- Alta prioridade: leads com score >= 95 e valor estimado preenchido
- Média: score 80-94 com valor estimado
- Baixa: score < 80 ou sem valor

## Pendências
- Preencher Valor_Estimado para 597 leads
- Preencher Email para 24 leads
- Remover/consolidar 20 duplicatas
- Definir ação por lote

## Próximos passos
1. Gerar CSV limpo dedup
2. Cruzar com tracker de envios para evitar reenvio
3. Preparar ranking por potencial econômico
4. Definir ação por segmento

## Restrições
- NÃO disparar mensagens automaticamente sem autorização
- NÃO misturar com Motor A/D2 atual
- Preservar rastreabilidade
