# Fase 1 — Plano de Execução da Consolidação
Data: 2026-08-17
Status: PLANO DE FASE 1 PRONTO — AGUARDANDO APROVAÇÃO
Restrição: Nenhuma alteração executada; somente planejamento.

---

## 1. Resumo executivo

Esta fase cobre exclusivamente as canibalizações ALTAS do cluster de documentação imobiliária:

- Escritura/registro
- Financiamento
- Avaliação
- Documentação compra

Objetivo: definir, para cada grupo, a URL canônica, o conteúdo a preservar e o plano de redirect futuro, sem executar mudanças.

---

## 2. Matriz operacional

| Grupo | URL atual | URL candidata à consolidação | Decisão | Conteúdo preservado | Conteúdo absorvido | Redirect futuro | Risco | Validação necessária |
|---|---|---|---|---|---|---|---|---|
| Escritura/registro | blog/escritura-registro-imovel-litoral-passo-passo-2026.html | blog/escritura-registro-imovel-litoral-passo-passo-2026.html | MANTER | Passo a passo, documentos, cartório, prazos | Custos/itbi da página passos-custos | blog/escritura-imovel-litoral-passos-custos-2026.html → blog/escritura-registro-imovel-litoral-passo-passo-2026.html | MÉDIO | Ler conteúdo integral de `passos-custos` e confirmar se há seção de custos única |
| Escritura/registro | blog/escritura-imovel-litoral-passos-custos-2026.html | blog/escritura-registro-imovel-litoral-passo-passo-2026.html | REDIRECIONAR — FUTURO | Seção de custos/itbi | — | blog/escritura-imovel-litoral-passos-custos-2026.html → blog/escritura-registro-imovel-litoral-passo-passo-2026.html | MÉDIO | Confirmar canonical e tracking antes de qualquer redirect |
| Financiamento | blog/financiamento-imoveis-litoral-guia.html | blog/financiamento-imoveis-litoral-guia.html | MANTER | Visão geral, tipos, dicas, aprovação | Exemplos regionais das páginas 2026 | blog/financiamento-imobiliario-litoral-guia-2026.html → blog/financiamento-imoveis-litoral-guia.html; blog/financiamento-imoveis-litoral-paulista-guia-2026.html → blog/financiamento-imoveis-litoral-guia.html | MÉDIO | Ler conteúdo das páginas 2026 e confirmar se há exemplos/subsídios únicos |
| Financiamento | blog/financiamento-imobiliario-litoral-guia-2026.html | blog/financiamento-imoveis-litoral-guia.html | REDIRECIONAR — FUTURO | Exemplos litoral se únicos | — | blog/financiamento-imobiliario-litoral-guia-2026.html → blog/financiamento-imoveis-litoral-guia.html | MÉDIO | Confirmar se há seção de subsídios/taxa realmente única |
| Financiamento | blog/financiamento-imoveis-litoral-paulista-guia-2026.html | blog/financiamento-imoveis-litoral-guia.html | REDIRECIONAR — FUTURO | Abrangência estadual se relevante | — | blog/financiamento-imoveis-litoral-paulista-guia-2026.html → blog/financiamento-imoveis-litoral-guia.html | MÉDIO | Confirmar se há conteúdo não coberto pela canônica |
| Avaliação | blog/avaliacao-preco-imoveis-litoral.html | blog/avaliacao-preco-imoveis-litoral.html | MANTER | Métodos, mercado, precificação, checklist | Comparativos/métodos da página avaliacao-preco-mercado | blog/avaliacao-preco-mercado-litoral.html → blog/avaliacao-preco-imoveis-litoral.html | MÉDIO | Ler conteúdo de `avaliacao-preco-mercado` e confirmar método comparativo único |
| Avaliação | blog/avaliacao-preco-mercado-litoral.html | blog/avaliacao-preco-imoveis-litoral.html | REDIRECIONAR — FUTURO | Método comparativo se único | — | blog/avaliacao-preco-mercado-litoral.html → blog/avaliacao-preco-imoveis-litoral.html | MÉDIO | Confirmar se há conteúdo de comparação realmente distinto |
| Documentação compra | blog/documentacao-compra-imovel-litoral-guia-2026.html | blog/documentacao-compra-imovel-litoral-guia-2026.html | MANTER | Listagem por etapa, prazos, documentos | Checklist resumido da página documentos-essenciais | blog/documentos-essenciais-compra-imovel-litoral-2026.html → blog/documentacao-compra-imovel-litoral-guia-2026.html | BAIXO | Confirmar checklist não duplicado |
| Documentação compra | blog/documentos-essenciais-compra-imovel-litoral-2026.html | blog/documentacao-compra-imovel-litoral-guia-2026.html | CONSOLIDAR | Checklist direto, exemplos práticos | — | blog/documentos-essenciais-compra-imovel-litoral-2026.html → blog/documentacao-compra-imovel-litoral-guia-2026.html | BAIXO | Confirmar exemplos práticos únicos antes de absorção |

Classificações usadas:
- MANTER = página canônica
- CONSOLIDAR = conteúdo a ser absorvido na canônica
- REDIRECIONAR — FUTURO = proposta de redirect futuro; não executar agora
- REVISÃO NECESSÁRIA = não aplicável nesta fase; todas as canônicas têm evidência suficiente
- OBSERVAR = não aplicável para canibalizações altas nesta fase

---

## 3. Conteúdo a preservar por grupo

### Escritura/registro
- Passo a passo de escritura e registro
- Lista de documentos por etapa
- Referências a cartório e prazos
- Seção de custos/itbi/registro da página `passos-custos`

### Financiamento
- Tipos de financiamento
- Dicas de aprovação
- Exemplos de entrada vs financiamento
- Possível conteúdo regional das páginas 2026:
  - `financiamento-imobiliario-litoral-guia-2026.html`: exemplos litoral, subsídios, dicas de aprovação rápida, erros comuns
  - `financiamento-imoveis-litoral-paulista-guia-2026.html`: cobertura estadual, tipos SBPE/Verde e Amarelo/Minha Casa Minha Vida

### Avaliação
- Métodos de avaliação
- Critérios locais do litoral
- Checklist de avaliação
- Método comparativo da página `avaliacao-preco-mercado`

### Documentação compra
- Checklist de documentos pessoa física
- Checklist de documentos do imóvel
- Exemplos de prazos por etapa
- Erros comuns em documentação de compra

---

## 4. URL canônica candidata

| Grupo | Canônica candidata | Justificativa |
|---|---|---|
| Escritura/registro | blog/escritura-registro-imovel-litoral-passo-passo-2026.html | Título mais completo, intenção mais forte, potencial de guia definitivo |
| Financiamento | blog/financiamento-imoveis-litoral-guia.html | URL mais genérica e duradoura; sem ano no slug; maior capacidade de absorção |
| Avaliação | blog/avaliacao-preco-imoveis-litoral.html | Alinhada a serviço; intenção comercial mais clara |
| Documentação compra | blog/documentacao-compra-imovel-litoral-guia-2026.html | Guia completo; maior profundidade aparente |

---

## 5. Redirects futuros

### Formato

URL ANTIGA → URL DESTINO PROPOSTA → MOTIVO → RISCO → VALIDAÇÕES NECESSÁRIAS

### Lista

- `blog/escritura-imovel-litoral-passos-custos-2026.html` → `blog/escritura-registro-imovel-litoral-passo-passo-2026.html`
  - Motivo: canibalização direta; conteúdo de custos/itbi a ser absorvido
  - Risco: MÉDIO
  - Validações: checar intenção, title/meta, canonical, links internos, schema

- `blog/financiamento-imobiliario-litoral-guia-2026.html` → `blog/financiamento-imoveis-litoral-guia.html`
  - Motivo: duplicidade de intenção; exemplos regionais a serem absorvidos
  - Risco: MÉDIO
  - Validações: checar exemplos únicos, links internos, schema

- `blog/financiamento-imoveis-litoral-paulista-guia-2026.html` → `blog/financiamento-imoveis-litoral-guia.html`
  - Motivo: duplicidade de intenção; abrangência estadual pode ser incorporada
  - Risco: MÉDIO
  - Validações: checar conteúdo estadual relevante, links internos, schema

- `blog/avaliacao-preco-mercado-litoral.html` → `blog/avaliacao-preco-imoveis-litoral.html`
  - Motivo: canibalização direta; método comparativo a ser absorvido
  - Risco: MÉDIO
  - Validações: checar método comparativo, links internos, schema

- `blog/documentos-essenciais-compra-imovel-litoral-2026.html` → `blog/documentacao-compra-imovel-litoral-guia-2026.html`
  - Motivo: checklist complementar; evitar duplicidade
  - Risco: BAIXO
  - Validações: checar checklist e exemplos práticos, links internos, schema

---

## 6. Impacto SEO

### Baixo
- Documentação compra: perda limitada de intenção; conteúdo pode ser absorvido sem desalinhamento.

### Médio
- Escritura/registro: possível perda de intenção específica; preservar conteúdo absorvendo seções distintas.
- Financiamento: possível perda de intenção específica; preservar exemplos regionais.
- Avaliação: possível perda de intenção específica; preservar método comparativo.

### Alto
- Nenhum nesta fase.

---

## 7. Links internos que precisarão ser revisados futuramente

### Escritura/registro
- Verificar links de entrada para `blog/escritura-imovel-litoral-passos-custos-2026.html`
- Atualizar para `blog/escritura-registro-imovel-litoral-passo-passo-2026.html` após redirect

### Financiamento
- Verificar links de entrada para:
  - `blog/financiamento-imobiliario-litoral-guia-2026.html`
  - `blog/financiamento-imoveis-litoral-paulista-guia-2026.html`
- Atualizar para `blog/financiamento-imoveis-litoral-guia.html` após redirect

### Avaliação
- Verificar links de entrada para `blog/avaliacao-preco-mercado-litoral.html`
- Atualizar para `blog/avaliacao-preco-imoveis-litoral.html` após redirect

### Documentação compra
- Verificar links de entrada para `blog/documentos-essenciais-compra-imovel-litoral-2026.html`
- Atualizar para `blog/documentacao-compra-imovel-litoral-guia-2026.html` após redirect

---

## 8. Ordem exata de execução futura

### Passo 1
Absorver conteúdo de `blog/escritura-imovel-litoral-passos-custos-2026.html` em `blog/escritura-registro-imovel-litoral-passo-passo-2026.html`.

### Passo 2
Propor redirect de `blog/escritura-imovel-litoral-passos-custos-2026.html` → `blog/escritura-registro-imovel-litoral-passo-passo-2026.html`.

### Passo 3
Absorver conteúdo de `blog/financiamento-imobiliario-litoral-guia-2026.html` e `blog/financiamento-imoveis-litoral-paulista-guia-2026.html` em `blog/financiamento-imoveis-litoral-guia.html`.

### Passo 4
Propor redirects das duas páginas de financiamento → `blog/financiamento-imoveis-litoral-guia.html`.

### Passo 5
Absorver conteúdo de `blog/avaliacao-preco-mercado-litoral.html` em `blog/avaliacao-preco-imoveis-litoral.html`.

### Passo 6
Propor redirect de `blog/avaliacao-preco-mercado-litoral.html` → `blog/avaliacao-preco-imoveis-litoral.html`.

### Passo 7
Absorver conteúdo de `blog/documentos-essenciais-compra-imovel-litoral-2026.html` em `blog/documentacao-compra-imovel-litoral-guia-2026.html`.

### Passo 8
Propor redirect de `blog/documentos-essenciais-compra-imovel-litoral-2026.html` → `blog/documentacao-compra-imovel-litoral-guia-2026.html`.

### Passo 9
Após cada absorção/redirect:
- validar HTTP 200;
- validar title/meta/H1;
- validar canonical;
- validar schema;
- validar links internos;
- validar tracking;
- confirmar ausência de conteúdo duplicado relevante.

---

## 9. Validações pós-execução

Para cada grupo consolidado:

- [ ] HTTP 200 na canônica
- [ ] Title e meta preservados ou atualizados com coerência
- [ ] H1 preservado ou atualizado
- [ ] Canonical próprio mantido
- [ ] Schema preservado
- [ ] BreadcrumbList preservado
- [ ] Tracking preservado
- [ ] Links internos atualizados
- [ ] CTA preservado
- [ ] Conteúdo absorvido documentado
- [ ] Redirect futuro documentado
- [ ] Nenhum conteúdo duplicado relevante

---

## 10. Itens que continuam bloqueados

- Criação do Hub de Documentação Imobiliária
- Consolidação de canibalizações médias
- Expansão de páginas canônicas
- Novos artigos
- Alterações em `blog/ptam-avaliacao-mercadologica-pratica-litoral-paulista-2026.html`
- Alterações em `blog/documentacao-estrangeiro-compra-imovel-brasil-litoral-2026.html`
- Alterações em `blog/heranca-inventario-transferencia-imovel-brasil-pratica-2026.html`
- Alterações em páginas de canibalização alta sem execução da Fase 1
- Alterações em Front A
- Alterações em canonical/redirects/sitemap/tracking

---

## 11. Revisão factual do Lote 3

URL: `blog/heranca-inventario-transferencia-imovel-brasil-pratica-2026.html`

Ponto: seção "Inventário judicial e extrajudicial"

Status: REVISÃO FACTUAL PENDENTE

Motivo: a regra atual pode deixar a impressão de que o inventário extrajudicial depende apenas de capacidade e consenso. Essa orientação é simplificada; existem condicionantes adicionais, como existência de testamento, unanimidade entre herdeiros e exigências documentais específicas do cartório.

Fonte recomendada: CNJ, legislação de registros públicos, cartórios oficiais.

Correção sugerida: adicionar menção a testamento/unanimidade e indicar que exigências específicas variam por cartório.

Ação: NÃO editar agora; registrar para revisão futura.

---

## 12. Integridade

Executar antes de qualquer ação futura:

```bash
git status
git diff
```

Confirmar nesta etapa:

- nenhuma página editorial alterada: SIM
- nenhum redirect criado: SIM
- nenhum canonical alterado: SIM
- nenhum sitemap alterado: SIM
- nenhum tracking alterado: SIM
- Front A intacta: SIM
- três novos conteúdos intactos: SIM

---

STATUS = PLANO DE FASE 1 PRONTO — AGUARDANDO APROVAÇÃO
