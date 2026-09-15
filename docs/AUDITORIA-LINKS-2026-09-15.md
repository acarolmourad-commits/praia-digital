# Auditoria de links internos — 2026-09-15

Auditoria executada sobre **~12.570 páginas HTML** com `check_links.py` + varredura interna completa.

## Evolução do dia

| Marco | Alvos quebrados | Ocorrências |
|---|---|---|
| Início | 1.361 | 1.712 |
| Após PR #3 (correções automáticas v1) | ~1.100 | 1.542 |
| Após PR #5 (fallback para raiz) + PR #4 (redirects) | ~970 | ~1.370 |
| Após redirects outreach/* + aliases CSS + artigos novos | **~800** | **~1.000** |

> ⚠️ Nota: um rebase externo (sync com upstream, commits `00e81b73`/`80d75225`) removeu parte dos arquivos de correção da `main` no fim do dia. Os arquivos foram restaurados em commit posterior de `restore`. Se números regredirem, rode `scripts/fix_broken_links.py` e reaplique os redirects.

## Como as correções foram feitas

1. **Correção automática** (`scripts/fix_broken_links.py`, 3 regras de alta confiança): segmentos duplicados, nome único no repo, fallback para arquivo na raiz — 1.453 correções em ~705 arquivos
2. **Redirects canônicos** para páginas consolidadas: `hub/automacao-imobiliaria.html`, `blog/artigo-completo.html`, `blog/segundo.html`, `inteligencia.html`, `outreach/desempenho|despacho|tracker|posts-redes-sociais.html`, `outreach/docs/sales/send-execution-tracker-2026.html`, `backup/cases/case-imobiliaria-porto-da-lua-35-leads-2026.html`, `litoral-prime-imoveis/outreach/servicos/captura-rapida.html`
3. **Aliases CSS**: `style.css`, `styles.css`, `assets/css/style.css` → `@import` da folha principal `css/style.css`
4. **Conteúdo novo**: 6 artigos `blog/<cidade>-aluguel-temporada-2026.html` (Santos, Guarujá, Bertioga, Itanhaém, Mongaguá, Peruíbe)

## Restantes (precisam de decisão de conteúdo)

| Alvo ausente | Refs | Ação sugerida |
|---|---|---|
| `docs/sales/backups/.../whatsapp-50-mensagens-prontas.html` | 12 | Conteúdo interno de vendas — criar ou remover |
| Falsos positivos (`blog/calculate`, `blog/reset` — atributos de form/JS) | ~12 | Ignorar |
| Cauda longa (~800 alvos, maioria 1-2 refs) | ~950 | Triage manual / re-rodar corretor |

## Manutenção contínua

- `python scripts/fix_broken_links.py --dry-run` — simula correções
- `python scripts/fix_broken_links.py` — aplica correções de alta confiança
- `python scripts/seo_h1_autofix.py` — injeta h1 acessível onde falta
- `python check_links.py` — auditoria completa (inclui links externos)
- Workflows: `link-check.yml` (semanal), `fix-links-apply.yml` e `seo-h1-apply.yml` (sob demanda)
