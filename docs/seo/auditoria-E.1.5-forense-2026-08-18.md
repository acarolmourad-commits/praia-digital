# E.1.5 — Auditoria forense da E.1.4
Data: 2026-08-18
Tipo: reconciliação de amostra, sem edição nas páginas

## 1. Inventário das 11 URLs da E.1.4
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

## 2. Histórico de cada URL

| URL | Amostra 1 | Amostra 2 | E.1.2 | Recuperada E.1 | Recuperada E.1.3 | Status E.1.4 |
|---|---|---|---|---|---|---|
| `bertioga-case-sucesso-automacao-imoveis-2026.html` | Não | Não | Não | Não | Não | Auditada |
| `precificacao-dinamica-temporada-litoral-2026.html` | Não | Não | Não | Não | Não | Auditada |
| `imovel-litoral-financiamento-aprovacao-2026.html` | Não | Não | Não | Não | Não | Auditada |
| `guaruja-ilha-panqueca-fim-semana-2026-sp-2026-07-14.html` | Não | Não | Não | Não | Não | Auditada |
| `guia-rapido-ia-corretores-litoral-2026-v2.html` | Não | Não | Não | Não | Não | Auditada |
| `gestao-temporada-imobiliarias-litoral-2026.html` | Não | Não | Não | Não | Não | Auditada |
| `passo-a-passo-abrir-imobiliaria-litoral-2026.html` | Não | Não | Não | Não | Não | Auditada |
| `operacao-cadastro-imoveis-massa-litoral.html` | Não | Não | Não | Não | Não | Auditada |
| `bertioga-guia-compra-imoveis-2026.html` | Não | Não | Não | Não | Não | Auditada |
| `praia-da-enseada-editorial-imoveis-2026.html` | Não | Não | Não | Não | Não | Auditada |
| `guia-rapido-captar-leads-temporada-litoral-sem-anuncios-2026.html` | Não | Não | Não | Não | Não | Auditada |

## 3. Independência
Resultado: **INDEPENDENTE_CONFIRMADA**

Nenhuma das 11 páginas da amostra E.1.4 havia sido:
- auditada em Amostra 1, Amostra 2 ou E.1.2;
- recuperada em E.1 ou E.1.3.

## 4. Caso das duas páginas "apartamento"
Inconsistência: o relatório E.1.4 listou `apartamento-barra-norte-2026.html` e `apartamento-centro-historico-investimento-2026.html` como exemplos do grupo "páginas antigas genéricas".

Evidência histórica:
- E.1.2: ambas classificadas como ESTÁVEL.
- E.1.3: ambas recuperadas.
- E.1.4: NÃO foram auditadas; apenas citadas como histórico.

Conclusão: **inconsistência de redação no relatório E.1.4, não contaminação da amostra.** As duas URLs não fazem parte do inventário das 11 páginas auditadas em E.1.4.

## 5. Validade da métrica 55%
Resultado: **VALIDADA**

A amostra E.1.4 é independente e não contém URLs recuperadas anteriormente. Portanto, 6/11 = 55% é uma métrica válida para esta amostra específica.

## 6. Padrões estruturais
Foram observados padrões recorrentes nas páginas classificadas como RECUPERAR_AGORA:
- template de “guia rápido” com seções curtas sem aprofundamento;
- template operacional com parágrafo introdutório + lista + CTA + “veja .”;
- páginas com schema e SEO técnico saudáveis, mas conteúdo editorial thin.

## 7. Padrões textuais
- repetição de parágrafos introdutórios idênticos em `bertioga-case-sucesso-automacao-imoveis-2026.html`;
- “conteúdo completo em breve” em `praia-da-enseada-editorial-imoveis-2026.html` e `bertioga-guia-compra-imoveis-2026.html`;
- links “Próximo passo: veja .” presentes em várias páginas operacionais.

## 8. Causa provável
Tipo: **CAUSA_TEMPLATE / CAUSA_MISTA**

Evidência:
- páginas degradadas compartilham estrutura semelhante;
- repetição de frases e blocos entre diferentes slugs;
- SEO técnico preservado enquanto o conteúdo editorial é insuficiente.

Confiança: **MÉDIA/ALTA**

Há indício de templates geradores de conteúdo, mas ainda não há confirmação de origem automatizada.

## 9. Diagnóstico
Pergunta: Existe evidência suficiente para afirmar que novas páginas estão sendo geradas com o mesmo problema por um template ou processo?

Resposta: **NÃO DETERMINADO**

Há evidência de padrão estrutural e textual, mas não há confirmação de template/processo gerador. Amostra ainda insuficiente para afirmação categórica.

## 10. Recomendação
**NOVA AMOSTRA**

- Avançar com uma quarta amostra independente para confirmar se os padrões observados se repetem.
- Não ampliar recuperações antes de nova validação.

## 11. Próximo passo sugerido
Executar E.1.6 — quarta amostra independente para validar recorrência.
