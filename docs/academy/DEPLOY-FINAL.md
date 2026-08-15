# Academy — Finalização para deploy

## 1. Inventário final dos 64 cursos
- Arquivo: `docs/academy/inventory-64-cursos.json`
- Status: **64/64 PRONTO_PARA_VENDA**
- Nenhum curso com conteúdo obrigatório ausente que impeça deploy

## 2. Padronização da apresentação
- Template comercial por curso: `docs/academy/catalog-64-cursos-template.md`
- Estrutura normalizada:
  - proposta de valor
  - para quem é
  - o que o aluno aprende
  - módulos
  - benefícios
  - entrega
  - FAQ
  - CTA de compra

## 3. Pacote comercial
- Catálogo base: `docs/academy/catalog-64-cursos.json`
- Categorias/clusters: automacao_ia, compra_venda, locacao_temporada, investimento, financiamento, marketing_digital, bairros_cidades, juridico, cases, editorial
- Textos de venda: `education/cursos/<slug>/vendas.html`
- Mensagens pós-compra: `education/cursos/<slug>/vendas.html`
- Elementos de checkout: slug, título, preço, CTA

## 4. Pacote técnico de deploy
- Variáveis: listadas em `docs/academy/TECH-DEPLOY.md`
- URLs/domínios: `https://academy.praia.digital`
- Rotas críticas: `/health`, `/courses`, `/academy/payments/webhook`
- Checkout: `education/checkout.html?slug=<slug>&title=<nome>&price=<valor>`
- Webhook: público, idempotente
- Acesso do aluno: matrícula ativa pós-pagamento
- Tracking: GA4 snippet + eventos recomendados em `docs/academy/TRACKING.md`
- Smoke test: `scripts/validate_academy_prod.py`

## 5. Validação final
- 64/64 cursos → PRONTO_PARA_VENDA
- Conteúdo obrigatório presente em todos os 64 cursos
- Rotas críticas mapeadas
- CTAs apontando para destinos existentes
- Nenhum bloqueio comercial conhecido
- Scripts de validação prontos

## 6. Estado do deploy
- 🟡 Dependente de humano: preencher variáveis no provedor
- Após preenchimento: deploy → smoke tests → checkout → acesso/entrega → tracking → regressão → evidências
- Não inventar credenciais; não subir SQLite em produção
