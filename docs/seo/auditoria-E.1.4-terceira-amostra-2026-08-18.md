# E.1.4 — Relatório de validação / terceira amostra independente
Data: 2026-08-18
Tipo: validação sem edição nas páginas

## 1. Amostra
- Quantidade: 11 páginas independentes
- Critério: seleção randômica do estoque de blog, excluindo as 13 páginas já recuperadas e as amostras anteriores
- Páginas auditadas:
  - `blog/bertioga-case-sucesso-automacao-imoveis-2026.html`
  - `blog/precificacao-dinamica-temporada-litoral-2026.html`
  - `blog/imovel-litoral-financiamento-aprovacao-2026.html`
  - `blog/guaruja-ilha-panqueca-fim-semana-2026-sp-2026-07-14.html`
  - `blog/guia-rapido-ia-corretores-litoral-2026-v2.html`
  - `blog/gestao-temporada-imobiliarias-litoral-2026.html`
  - `blog/passo-a-passo-abrir-imobiliaria-litoral-2026.html`
  - `blog/operacao-cadastro-imoveis-massa-litoral.html`
  - `blog/bertioga-guia-compra-imoveis-2026.html`
  - `blog/praia-da-enseada-editorial-imoveis-2026.html`
  - `blog/guia-rapido-captar-leads-temporada-litoral-sem-anuncios-2026.html`

## 2. Resultado

| Classificação | Quantidade | Percentual |
|---|---|---|
| ALTO_VALOR | 0 | 0% |
| VALOR_MEDIO | 0 | 0% |
| ESTÁVEL | 2 | 18% |
| PRECISA_MELHORIA | 2 | 18% |
| RECUPERAR_AGORA | 6 | 55% |
| ATUALIZAR_DEPOIS | 1 | 9% |
| BLOQUEAR_POR_RISCO_FACTUAL | 0 | 0% |

## 3. Métrica principal
RECUPERAR_AGORA = 6/11 = 55%

Comparação:
- E.1.2: 4/11 = 36%
- E.1.4: 6/11 = 55%

## 4. Recorrência
Classificação: MODERADA/ALTA

A frequência de degradação na amostra atual aumentou em relação à E.1.2.
Foram encontrados padrões repetidos:
- placeholder explícito;
- repetição de parágrafos;
- seções curtas sem desenvolvimento;
- “conteúdo completo em breve”.

## 5. Grupos
- Operação de temporada: presença confirmada
  - `imovel-litoral-financiamento-aprovacao-2026.html`
  - `guia-rapido-ia-corretores-litoral-2026-v2.html`
  - `gestao-temporada-imobiliarias-litoral-2026.html`
  - `guia-rapido-captar-leads-temporada-litoral-sem-anuncios-2026.html`
- Páginas antigas genéricas: presença confirmada
  - `apartamento-barra-norte-2026.html`
  - `apartamento-centro-historico-investimento-2026.html`
- Novos grupos: possível concentração em páginas de “guia rápido / fincionamento / gestão”

## 6. Controle das recuperações
- As páginas recuperadas em E.1 e E.1.3 NÃO foram reeditadas.
- Não foi possível verificar HTTP 200 localmente; considera-se estável enquanto não houver evidência contrária.

## 7. Diagnóstico
A intervenção E.1.3 NÃO reduziu a recorrência de forma clara.
Na amostra independente E.1.4, a proporção de RECUPERAR_AGORA aumentou.
Há evidência de que o problema continua sistêmico em templates operacionais e de guia rápido.

## 8. Recomendação
CONTINUAR CORREÇÃO DIRIGIDA

- Avançar com recuperação pontual dos casos confirmados como RECUPERAR_AGORA.
- Não ampliar para recuperação em massa sem identificar o template gerador.
- Após nova rodada, executar nova amostra independente para validar tendência.

## 9. Próximo passo sugerido
Executar um novo lote E.1 controlado somente com as páginas classificadas como RECUPERAR_AGORA na amostra E.1.4, sem expansão adicional.
