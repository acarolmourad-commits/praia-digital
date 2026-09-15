# Auditoria de links internos — 2026-09-15

Auditoria executada sobre **~12.570 páginas HTML** com `check_links.py` + varredura interna completa.

## Evolução do dia

| Marco | Alvos quebrados | Ocorrências |
|---|---|---|
| Início | 1.361 | 1.712 |
| Após PR #3 (correções automáticas v1) | ~1.100 | 1.542 |
| Após PR #5 (fallback para raiz) + PR #4 (redirects) | ~970 | ~1.370 |
| Após redirects outreach/* + aliases CSS + inteligencia.html | **894** | **1.111** |

**Total corrigido no dia: ~2.400 ocorrências de links quebrados** (via PRs #3, #4, #5, #6 e commits diretos).

## Como as correções foram feitas

1. **Correção automática** (`scripts/fix_broken_links.py`, 3 regras de alta confiança): segmentos duplicados, nome único no repo, fallback para arquivo na raiz — 1.453 correções em ~705 arquivos
2. **Redirects canônicos** para páginas consolidadas: `hub/automacao-imobiliaria.html`, `blog/artigo-completo.html`, `blog/segundo.html`, `inteligencia.html`, `outreach/desempenho|despacho|tracker|posts-redes-sociais.html`, `outreach/docs/sales/send-execution-tracker-2026.html`
3. **Aliases CSS**: `style.css`, `styles.css`, `assets/css/style.css` → `@import` da folha principal `css/style.css`

## Restantes (precisam de decisão de conteúdo)

| Alvo ausente | Refs | Ação sugerida |
|---|---|---|
| `blog/*-aluguel-temporada-2026.html` (6 cidades) | ~83 | **Pauta de conteúdo**: criar os artigos (alto potencial SEO) |
| `backup/cases/case-imobiliaria-porto-da-lua-*.html` | 22 | Apontar para `cases/` (arquivo existe lá) |
| `docs/sales/backups/.../whatsapp-50-mensagens-prontas.html` | 12 | Conteúdo interno de vendas — criar ou remover |
| `litoral-prime-imoveis/outreach/servicos/captura-rapida.html` | 7 | Apontar para `servicos/captura-rapida.html` |
| Falsos positivos (`blog/calculate`, `blog/reset` — atributos de form/JS) | ~12 | Ignorar |
| Cauda longa (~840 alvos, maioria 1-2 refs) | ~975 | Triage manual |

## Manutenção contínua

- `python scripts/fix_broken_links.py --dry-run` — simula correções
- `python scripts/fix_broken_links.py` — aplica correções de alta confiança
- `python scripts/seo_h1_autofix.py` — injeta h1 acessível onde falta
- `python check_links.py` — auditoria completa (inclui links externos)
- Workflows: `link-check.yml` (semanal), `fix-links-apply.yml` e `seo-h1-apply.yml` (sob demanda)
