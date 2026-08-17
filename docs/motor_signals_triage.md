# Motor A/B — Triagem Pós-D2
Data-alvo: 17/08 09:00+
Data da triagem: 17/08/2026

## Objetivo
Cruzar eventos do Motor A com o Motor B para identificar clusters/conteúdos de maior potencial comercial.

## Métricas pré-D2
- Motor A: 10 leads
- Motor B: 0 respostas
- Academy: 64/64
- B2B: 586 leads

## Regras aplicadas
- 0 respostas pré-D2 é normal; não simular métricas antes da liberação.
- Textos ficam em doc separado até envio real.
- D2 não executado; aguardando aprovação de preço.
- Batch mantido como stream separado de D2.
- Nenhuma alteração editorial executada antes da classificação.

## Classificação individual dos 10 leads — Motor A

| lead_id | origem | cidade | cluster | evento_MotorA | evento_MotorB | potencial | proxima_acao |
|---------|--------|--------|---------|---------------|---------------|-----------|--------------|
| 26 | Instagram | Bertioga | Fotografia + Edição de anúncio | D0 enviado A | Nenhum (pré-D2) | Alto | Aguardar D2 (09:00) e monitorar resposta |
| 30 | OLX | Bertioga | Gestão Airbnb + Fotografia/Edição | D0 enviado B | Nenhum (pré-D2) | Alto | Aguardar D2 (09:00) e monitorar resposta |
| 35 | TemporadaLivre | Bertioga | Fotografia + Edição de anúncio | NOVO_ESTOQUE | Nenhum (pré-D2) | Alto | Preparar inclusão no fluxo D0/D2 pós-aprovação de preço |
| 34-alt | Zap Imóveis | São Sebastião | SEO local + Edição de anúncio | NOVO_ESTOQUE | Nenhum (pré-D2) | Alto | Preparar inclusão no fluxo D0/D2 pós-aprovação de preço |
| 31-alt | OLX | Bertioga | Fotografia + Edição de anúncio | NOVO_ESTOQUE | Nenhum (pré-D2) | Médio | Preparar inclusão no fluxo D0/D2 pós-aprovação de preço |
| 18 | Facebook | São Sebastião | Fotografia + Edição de anúncio | D0 enviado B | Nenhum (pré-D2) | Médio | Aguardar D2 (09:00) e monitorar resposta |
| 33 | Instagram | Bertioga | Gestão Airbnb | NOVO_ESTOQUE | Nenhum (pré-D2) | Médio | Preparar inclusão no fluxo D0/D2 pós-aprovação de preço |
| 16 | Facebook | Bertioga | Gestão Airbnb + Edição de anúncio | D0 enviado B | Nenhum (pré-D2) | Médio | Aguardar D2 (09:00) e monitorar resposta |
| 12 | OLX | Bertioga | Fotografia + Edição de anúncio | D0 enviado B | Nenhum (pré-D2) | Médio | Aguardar D2 (09:00) e monitorar resposta |
| 32 | OLX | São Sebastião | Fotografia + Edição de anúncio | NOVO_ESTOQUE | Nenhum (pré-D2) | Baixo | Avaliar viabilidade; score 72 e anúncio básico |

## Cruzamento Motor A × Motor B

Motor B status pré-D2: 0 respostas reais. Sem eventos vinculados aos 10 leads do Motor A.

Sinais instrumentados disponíveis (batch controlado em 16/08):
- 3 leads gerados (scores 80, 43, 82), todos perfil proprietário.
- Caminho 3 (Anúncio competitivo) com scores altos (80-82).
- Caminho 2 (Anúncio com oportunidades) com score 43.

Alinhamento observado:
- Scores altos do Motor B corroboram o potencial dos clusters Fotografia + Edição e Gestão Airbnb no Motor A.
- Perfil proprietário no Motor B coincide com o perfil majoritário dos 10 leads.
- Sem dados reais de resposta/conversão para cruzamento direto por lead.

## Clusters por potencial (sinal forte / médio / fraco)

### Sinal FORTE
| cluster | leads | score_médio | cidades | justificativa |
|---------|-------|-------------|---------|---------------|
| Fotografia + Edição de anúncio | 5 (26, 35, 31-alt, 18, 12) | 77.2 | Bertioga, São Sebastião | Volume alto + scores majoritariamente altos + alinhamento com Motor B (Caminho 3) |
| Gestão Airbnb + Fotografia/Edição | 3 (30, 33, 16) | 75.3 | Bertioga | Alta recorrência (ticket recorrente) + score consistente + alinhamento com Motor B |

### Sinal MÉDIO
| cluster | leads | score_médio | cidades | justificativa |
|---------|-------|-------------|---------|---------------|
| SEO local + Edição de anúncio | 1 (34-alt) | 78.0 | São Sebastião | Score alto, mas volume insuficiente para sinal forte; nicho específico com potencial de crescimento |

### Sinal FRACO
| cluster | leads | score_médio | cidades | justificativa |
|---------|-------|-------------|---------|---------------|
| Fotografia + Edição (lead 32) | 1 | 72.0 | São Sebastião | Score abaixo da média do cluster; anúncio básico com evidência frágil |

## Seleção de artigos para enriquecimento/copy (pré-envio)

Baseado nos clusters fortes e médios identificados. Nenhuma alteração editorial será executada antes da aprovação e do envio real.

### Cluster Fotografia + Edição de anúncio (Sinal FORTE)
- `fotografia-imoveis-praia-dicas-2026.html`
- `foto-profissional-imoveis-litoral-2026.html`
- `edicao-fotografia-anuncio-temporada-litoral-2026.html`
- `ab-testing-anuncios-imobiliarios-locais-litoral-2026.html`
- `anuncios-imoveis-litoral-paulista-2026.html`
- `redacao-anuncios-imoveis-convertem-litoral-2026.html`
- `checklist-venda-imovel-litoral-anuncio-photos-2026.html`

### Cluster Gestão Airbnb + Fotografia/Edição (Sinal FORTE)
- `airbnb-boa-paginao-primeiro-mes-litoral-2026.html`
- `gestao-profissional-airbnb-litoral-paulista-2026.html`
- `gestao-aluguel-temporada-iniciantes-passo-a-passo-litoral-2026.html`
- `imovel-litoral-aluguel-airbnb-2026.html`
- `aluguel-temporada-litoral-checkout-atrasado-gestao-2026.html`

### Cluster SEO local + Edição de anúncio (Sinal MÉDIO)
- `bertioga-seo-local-imoveis-2026.html`
- `seo-local-imobiliaria-litoral-2026.html`
- `seo-local-bairros-litoral-paulista-2026.html`
- `checklist-seo-local-imobiliarias-litoral-2026.html`

## Próximos passos operacionais
1. Aguardar aprovação de preço para D2.
2. Executar disparo D2 em 17/08 às 09:00 para leads elegíveis.
3. Monitorar Motor B pós-D2 para respostas reais.
4. Cruzar respostas com esta classificação para atualizar clusters.
5. Selecionar artigos da lista acima para enriquecimento/copy APÓS evidência de resposta.
