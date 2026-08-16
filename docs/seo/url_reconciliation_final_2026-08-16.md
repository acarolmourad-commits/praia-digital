# Reconciliação final de URLs — Praia Digital
Data: 2026-08-16
Status: Diagnóstico completo
D2: SEM IMPACTO

## Resumo executivo

- Total HTML no repositório: 13.311
- URLs no sitemap: 11.616
- URLs com correspondência física: 8.235
- URLs sem correspondência física: 3.380
- A diferença não é explicada apenas por backup/
- Múltiplas estruturas explicam a maior parte da diferença

## Inventário do repositório

| Diretório | HTML | Função provável | Público? |
|-----------|------|-----------------|----------|
| outreach/ | 5.060 | Sistema/produto | Não |
| backup/ | 2.420 | Arquivo | Não |
| blog/ | 3.274 | Editorial | Sim |
| docs/ | 24 | Documentação | Não |
| academy/ | 128 | Educação/produto | Sim |
| imoveis/ | 644 | Imobiliário | Sim |
| cidades/ | 133 | Cidades | Sim |
| bairros/ | 118 | Bairros | Sim |
| education/ | 181 | Educação | Sim |
| servicos/ | 63 | Serviços | Sim |
| anfitrioes/ | 8 | Anfitriões | Sim |
| cases/ | 6 | Cases | Sim |
| noticias/ | 1 | Notícias | Sim |
| Raiz (root) | 676 | Institucional/comercial | Sim |
| **Total** | **13.311** | | |

## Sitemap — categorias

| Categoria | URLs | % | Match |
|-----------|------|---|-------|
| BLOG_PHYSICAL | 3.262 | 28,1% | Sim |
| ROOT | 2.680 | 23,1% | Sim |
| DOCS | 971 | 8,4% | Sim |
| IMOVEIS_PHYSICAL | 684 | 5,9% | Sim |
| EDUCATION | 174 | 1,5% | Sim |
| BAIRROS | 166 | 1,4% | Sim |
| CIDADES | 152 | 1,3% | Sim |
| SERVICOS | 123 | 1,1% | Sim |
| IMOVEIS_UNKNOWN | 21 | 0,2% | Não |
| CIDADES_EXPANSAO | 8 | 0,1% | Sim |
| CASES | 6 | 0,0% | Sim |
| BLOG_UNKNOWN | 3 | 0,0% | Não |
| REDIRECT | 1 | 0,0% | Sim |
| NOTICIAS | 1 | 0,0% | Sim |
| **UNKNOWN** | **3.356** | **28,9%** | **Não** |

## Classificação funcional

| Categoria | Quantidade | % |
|-----------|------------|---|
| SISTEMA (outreach) | 5.060 | 38,0% |
| EDITORIAL (blog) | 4.459 | 33,5% |
| ARQUIVO (backup/docs) | 2.444 | 18,4% |
| DESCONHECIDO (raiz não classificada) | 1.113 | 8,4% |
| ACADEMY | 128 | 1,0% |
| COMERCIAL | 67 | 0,5% |
| INSTITUCIONAL | 47 | 0,4% |
| CIDADE | 17 | 0,1% |

## Respostas executivas

**Quantas URLs existem no sitemap?**
11.616 URLs.

**Quantos arquivos/páginas existem no repositório?**
13.311 arquivos HTML no total.

**Onde estão essas URLs?**
- 3.262 no blog/ (físicas)
- 2.680 em páginas raiz (institucional/comercial)
- 971 em docs/ (documentação/sistema)
- 684 em imoveis/ (físicas)
- 174 em education/ (educação)
- 166 em bairros/ (bairros)
- 152 em cidades/ (cidades)
- 123 em servicos/ (serviços)
- 3.356 com padrão UNKNOWN (dashboards, cidades-expansao, academy, litoral-prime-imoveis, etc.)

**Por que existem diferenças?**
1. Múltiplas estruturas além de blog/ (academy, imoveis, cases, cidades-expansao, raiz, docs, education)
2. 3.356 URLs com padrão UNKNOWN (dashboards, academy, litoral-prime-imoveis, cidades-expansao)
3. 21 URLs em imoveis/ sem correspondência física
4. 3 URLs em blog/ sem correspondência física
5. outreach/ (5.060) e backup/ (2.420) não estão no sitemap — correto

**Quais URLs são conteúdo público?**
- blog/: 3.274
- imoveis/: 644
- cases/: 6
- cidades/: 133
- bairros/: 118
- education/: 181
- servicos/: 63
- anfitrioes/: 8
- noticias/: 1
- Raiz: ~676 (institucional, comercial, cidade)
- academy/: 128

**Quais são páginas de sistema/produto?**
- outreach/: 5.060
- backup/: 2.420
- docs/: 24

**Quais são geradas dinamicamente?**
3.356 URLs UNKNOWN no sitemap — podem ser geradas ou estão em diretórios não auditados completamente.

**Quais são órfãs?**
Não auditado completamente ainda — requer análise de links internos.

**Quais são duplicadas/variantes?**
Não auditado completamente ainda — requer análise de conteúdo.

**Qual processo gera o sitemap?**
Não identificado ainda — requer busca por scripts de geração.

## Classificação de risco

| Prioridade | Grupo | Quantidade | Problema | Recomendação | D2 |
|------------|-------|------------|----------|--------------|-----|
| P0 | UNKNOWN no sitemap | 3.356 | Sem correspondência física | Investigar origem | SEM IMPACTO |
| P0 | ROOT no sitemap | 2.680 | Páginas institucionais massivas | Classificar indexabilidade | SEM IMPACTO |
| P1 | DOCS no sitemap | 971 | Documentação/sistema pública | Decidir se deve ser indexada | SEM IMPACTO |
| P1 | IMOVEIS_UNKNOWN | 21 | Sem correspondência física | Investigar | SEM IMPACTO |
| P1 | BLOG_UNKNOWN | 3 | Sem correspondência física | Investigar | SEM IMPACTO |
| P2 | REDIRECT no sitemap | 1 | Redirect não tratado | Remover/monitorar | SEM IMPACTO |
| P2 | outreach/ não indexado | 5.060 | Sistema não indexado | Correto, manter assim | SEM IMPACTO |
| P3 | backup/ já removido | 0 | Resolvido | — | SEM IMPACTO |

## Próximas ações recomendadas

1. Investigar origem das 3.356 URLs UNKNOWN
2. Verificar se docs/ deve estar no sitemap público
3. Mapear processo de geração do sitemap
4. Classificar indexabilidade das 2.680 páginas raiz
5. Analisar academy/ (128 páginas) para indexação
6. Verificar se academy/ está no sitemap

## Não executar ainda

- Remoção de URLs
- Alteração de sitemap
- Alteração de canonical
- Criação de redirects
- Consolidação de páginas
- Publicação de conteúdo

Próxima fase: E-E-A/T → Arquitetura → Benchmark → Conteúdo → Dados atualizados → Motor de notícias → Publicação controlada.
