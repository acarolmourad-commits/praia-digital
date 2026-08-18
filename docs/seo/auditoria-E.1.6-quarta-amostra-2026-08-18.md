# E.1.6 — Relatório de quarta amostra independente
Data: 2026-08-18
Tipo: medição / teste de replicação, sem edição nas páginas

## 1. Inventário

Amostra independente de 11 páginas do estoque `blog/`, excluídas todas as URLs participantes de E.1, E.1.2, E.1.3 e E.1.4. Seleção randômica com seed fixa.

- `blog/imovel-litoral-investimento-imovel-usado-2026.html`
- `blog/acelerar-fechamento-vendas-litoral-paulista-2026.html`
- `blog/mongagua-curso-locacao-temporada-imoveis-2026.html`
- `blog/guaruja-case-sucesso-financiamento-imoveis-2026.html`
- `blog/itanhaem-curso-juridico-imoveis-2026.html`
- `blog/case-sucesso-automacao-imoveis-sao-sebastiao-2026.html`
- `blog/imovel-litoral-averbacao-imovel-prazo-2026.html`
- `blog/sao-sebastiao-oeste-bairros-imoveis-2026.html`
- `blog/case-de-sucesso-proprietario-guaruja-temporada-2026.html`
- `blog/geracao-descricoes-anuncios-ia.html`
- `blog/imovel-litoral-custo-obra-reforma-2026.html`

## 2. Independência

Confirmação: todas as 11 URLs são novas em relação a E.1, E.1.2, E.1.3 e E.1.4. Nenhuma apareceu em amostras ou listas de recuperação anteriores.

Resultado: **INDEPENDENTE_CONFIRMADA**

## 3. Resultado

| Classificação | Quantidade | Percentual |
|---|---:|---:|
| ALTO_VALOR | 0 | 0% |
| VALOR_MEDIO | 0 | 0% |
| ESTÁVEL | 4 | 36% |
| PRECISA_MELHORIA | 0 | 0% |
| RECUPERAR_AGORA | 7 | 64% |
| ATUALIZAR_DEPOIS | 0 | 0% |
| BLOQUEAR_POR_RISCO_FACTUAL | 0 | 0% |

## 4. Métrica principal

RECUPERAR_AGORA = 7/11 = 64%

## 5. Matriz de padrões

| URL | Placeholder | Repetição | Seções incompletas | Guia rápido | Gestão | Leads | Temporada |
|---|---|---|---|---|---|---|---|
| `imovel-litoral-investimento-imovel-usado-2026.html` | NÃO | NÃO | SIM | NÃO | NÃO | NÃO | NÃO |
| `acelerar-fechamento-vendas-litoral-paulista-2026.html` | NÃO | NÃO | NÃO | NÃO | NÃO | NÃO | NÃO |
| `mongagua-curso-locacao-temporada-imoveis-2026.html` | SIM | SIM | SIM | NÃO | NÃO | NÃO | SIM |
| `guaruja-case-sucesso-financiamento-imoveis-2026.html` | SIM | SIM | SIM | NÃO | NÃO | NÃO | NÃO |
| `itanhaem-curso-juridico-imoveis-2026.html` | SIM | SIM | SIM | NÃO | NÃO | NÃO | NÃO |
| `case-sucesso-automacao-imoveis-sao-sebastiao-2026.html` | SIM | SIM | SIM | NÃO | NÃO | NÃO | NÃO |
| `imovel-litoral-averbacao-imovel-prazo-2026.html` | NÃO | NÃO | SIM | NÃO | NÃO | NÃO | NÃO |
| `sao-sebastiao-oeste-bairros-imoveis-2026.html` | NÃO | NÃO | SIM | NÃO | NÃO | NÃO | NÃO |
| `case-de-sucesso-proprietario-guaruja-temporada-2026.html` | NÃO | NÃO | NÃO | NÃO | NÃO | NÃO | SIM |
| `geracao-descricoes-anuncios-ia.html` | NÃO | NÃO | NÃO | NÃO | NÃO | NÃO | NÃO |
| `imovel-litoral-custo-obra-reforma-2026.html` | NÃO | NÃO | SIM | NÃO | NÃO | NÃO | NÃO |

## 6. Grupos

- **Curso/city-curso**: presença confirmada
  - `mongagua-curso-locacao-temporada-imoveis-2026.html`
  - `itanhaem-curso-juridico-imoveis-2026.html`
- **Case de sucesso genérico**: presença confirmada
  - `guaruja-case-sucesso-financiamento-imoveis-2026.html`
  - `case-sucesso-automacao-imoveis-sao-sebastiao-2026.html`
- **Artigo operacional thin**: presença confirmada
  - `imovel-litoral-investimento-imovel-usado-2026.html`
  - `imovel-litoral-averbacao-imovel-prazo-2026.html`
  - `imovel-litoral-custo-obra-reforma-2026.html`
- **Bairro/guia regional**: presença confirmada
  - `sao-sebastiao-oeste-bairros-imoveis-2026.html`
- **Operação de temporada**: presença confirmada
  - `case-de-sucesso-proprietario-guaruja-temporada-2026.html`

Grupos sem recorrência relevante nesta amostra:
- guia rápido
- gestão
- leads

Novo grupo observado: artigo operacional thin com estrutura mínima e link “Próximo passo: veja ...”.

## 7. Padrões textuais

| Padrão | Ocorrências | URLs | Grupo | Confiança |
|---|---:|---|---|---|
| placeholder + parágrafo duplicado + “conteúdo completo em breve” | 4 | `mongagua...`, `guaruja-financiamento...`, `itanhaem...`, `case-sucesso-sao-sebastiao...` | curso / case | ALTA |
| artigo mínimo com 2–3 H2 e parágrafo único + “Próximo passo: veja ...” | 3 | `imovel-usado...`, `averbacao...`, `custo-obra...` | artigo operacional thin | ALTA |
| seção curta + placeholder final + CTA ferramentas | 1 | `sao-sebastiao-oeste...` | bairro/guia regional | MÉDIA |
| sem placeholder, conteúdo desenvolvido | 4 | `acelerar-fechamento...`, `case-de-sucesso-proprietario-guaruja...`, `geracao-descricoes...` | — | — |

## 8. Evidência estrutural

Classificação: **EVIDÊNCIA_FORTE**

Evidência:
- páginas degradadas compartilham bloco final idêntico com CTA para painel de ferramentas;
- repetição idêntica de parágrafos introdutórios em múltiplos H2;
- heading + 1 parágrafo + CTA em estrutura mínima;
- schema/SEO técnico preservado enquanto o corpo editorial é insuficiente.

## 9. Teste de replicação

Resultado: **PADRÃO_REPLICADO**

Justificativa:
- na amostra independente E.1.6, os mesmos tipos de degradação voltaram a aparecer de forma relevante;
- grupos previamente suspeitos estão presentes novamente;
- a proporção de RECUPERAR_AGORA se manteve em patamar elevado e comparável às amostras anteriores.

## 10. Comparação histórica

| Fase | Amostra | RECUPERAR_AGORA | Percentual |
|---|---:|---:|---:|
| E.1.2 | 11 | 4 | 36% |
| E.1.4 | 11 | 6 | 55% |
| E.1.6 | 11 | 7 | 64% |

Observação:
- amostras pequenas; não usar para afirmar tendência populacional absoluta;
- utilizar apenas como indicador de recorrência em amostras independentes.

## 11. Diagnóstico

O problema parece predominantemente **potencialmente estrutural**.

Há combinação de:
- padrões textuais repetidos;
- estrutura semelhante entre páginas independentes;
- componentes repetidos;
- recorrência em múltiplas páginas de grupos diferentes.

## 12. Recomendação

**B — DIAGNÓSTICO ESTRUTURAL**

Justificativa: a recorrência não se explica por coincidência editorial pontual.

## 13. Próximo passo

Investigar o template/processo gerador das páginas em `curso`, `case de sucesso` e `artigo operacional thin`, sem alterar páginas nem executar recuperações nesta fase.
