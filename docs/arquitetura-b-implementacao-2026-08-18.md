# Implementação — Arquitetura B

## Ação
Aguardando autorização humana para executar.

## Pré-requisitos
- Autorização explícita
- Lote 1 validado
- Backup do repositório

## Arquivos-alvo
- index.html
- servicos.html
- contato.html
- education/index.html
- cidades/*.html
- servicos/cidade-servico/*.html

## Alterações planejadas
1. Navegação principal separada por cluster:
   - Imobiliário
   - Tecnologia/IA
   - Academy
2. Breadcrumbs ajustados por cluster
3. Schema.org atualizado por seção
4. CTAs separados por jornada
5. Página dedicada para IA para imobiliárias
6. Preservar URLs sempre que possível
7. Redirects somente quando necessário

## Validações
- Links internos
- Canonical
- Sitemap
- Headings
- Schema
- Acessibilidade
- Mobile

## Proteções
- uploads/proprietarios/: NÃO TOCAR
- Academy/Financeiro: preservar gateway
- Dados de produção: preservar
- Rollback por lote

## Critério de sucesso
- Navegação separada por intenção
- CTAs claros por jornada
- SEO preservado
- Acessibilidade mantida
- Conversão melhorada
