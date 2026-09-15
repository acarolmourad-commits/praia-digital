# Auditoria SEO técnica — 2026-09-15

Varredura automatizada das **12.566 páginas HTML** do repositório.

## Resumo

| Verificação | Páginas com problema | % do total |
|---|---|---|
| Sem `<title>` | 53 | 0,4% |
| Sem meta description | 194 | 1,5% |
| Sem `<h1>` | 855 | 6,8% |
| Sem canonical | 229 | 1,8% |
| Sem meta viewport | 176 | 1,4% |
| Sem atributo `lang` | 50 | 0,4% |
| Com `noindex` (intencional: redirects, backups, propostas print) | 3.377 | 26,9% |

## Onde estão os problemas de meta description

| Diretório | Páginas | Natureza |
|---|---|---|
| `docs/` | 55 | Documentos internos de vendas — baixo impacto SEO |
| `backup/` | 39 | Backups — sem impacto |
| `partials/` | 27 | Fragmentos HTML incluídos em outras páginas — não precisam de meta |
| `education/` | 21 | Área de cursos — revisar |
| `blog/` | 13 | **Prioridade alta** — conteúdo público indexável |
| `hub/`, `academy/`, `assets/` | 19 | Revisar caso a caso |

## Recomendações por prioridade

1. **Blog (13 páginas sem meta description)** — impacto direto em CTR no Google; adicionar descriptions de 140-160 caracteres.
2. **Canonicals ausentes (229)** — padronizar `https://praia.digital/<path>` para evitar conteúdo duplicado (o site já consolida variações com redirects).
3. **`<h1>` ausente (855)** — grande parte são páginas de proposta/print e redirects (`noindex`); filtrar apenas páginas indexáveis antes de corrigir.
4. **Viewport/lang** — correções triviais nas ~180 páginas afetadas.
5. Manter o workflow semanal de links + `fix_broken_links.py` como guarda contínua.

## Estado dos links internos (pós-correções de 15/09)

- Início do dia: **1.361 alvos quebrados**
- Após PRs #3, #4, #5 e redirect `inteligencia.html`: **~1.450 ocorrências corrigidas**
- Restantes: páginas que nunca existiram (seção `outreach/`, artigos de blog planejados) — decisão de conteúdo

## Ferramentas

- `scripts/fix_broken_links.py` — correção automática de links (3 regras de alta confiança)
- `check_links.py` — auditoria completa incluindo links externos
- Workflows: `link-check.yml` (semanal), `fix-links-apply.yml` (sob demanda)
