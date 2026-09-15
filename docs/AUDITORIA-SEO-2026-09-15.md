# Auditoria SEO técnica — 2026-09-15

Varredura automatizada das **~12.570 páginas HTML** do repositório.

## Estado das páginas públicas (7.647 páginas indexáveis)

| Verificação | Estado |
|---|---|
| `<title>` | ✅ 100% |
| Meta description | ✅ 100% |
| Canonical | ✅ 100% |
| Meta viewport | ✅ 100% |
| Atributo `lang` | ✅ 100% |
| `<h1>` | ✅ 100% após PR #6 (266 páginas receberam h1 sr-only via `scripts/seo_h1_autofix.py`) |

## Observações

- 3.377 páginas com `noindex` são intencionais: redirects de consolidação, propostas print, backups.
- Os números brutos iniciais (194 sem description, 855 sem h1) incluíam docs internos/backups/fragmentos; o filtro por páginas públicas mostrou o site em excelente estado.
- A técnica sr-only (`position:absolute; clip:rect(0 0 0 0)`) adiciona h1 sem impacto visual — válida para SEO e WCAG.

## Manutenção

- Rodar `python scripts/seo_h1_autofix.py --dry-run` após adicionar páginas novas.
- Páginas novas precisam de title + description + canonical + h1 (ver CONTRIBUTING.md).
