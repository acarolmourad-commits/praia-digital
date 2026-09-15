# Auditoria de links internos — 2026-09-15

Auditoria executada sobre **12.562 páginas HTML** com `check_links.py` + varredura interna completa.

## Resultado

| Métrica | Valor |
|---|---|
| Alvos internos quebrados encontrados | 1.361 |
| Ocorrências corrigidas automaticamente (alta confiança) | **1.166** |
| Arquivos modificados | 500 |
| Ocorrências sem correção segura (página alvo não existe) | 1.712 |

## Como as correções foram feitas

1. **Segmentos duplicados**: `blog/blog/x.html` → `blog/x.html` (4 casos)
2. **Arquivo existe com nome único em outro caminho**: link reescrito para o caminho relativo correto (1.162 casos) — ex.: `eventos-litoral-paulista-2026-2027/santos.html` → `santos.html`

O patch completo (500 arquivos) está disponível para aplicação com `git apply`.

## Pendências (precisam de decisão de conteúdo)

Os 1.712 casos restantes apontam para páginas que **nunca existiram** no repositório. Principais padrões:

| Alvo ausente | Referências | Ação sugerida |
|---|---|---|
| `outreach/docs/sales/send-execution-tracker-2026.html` | 144 | Criar página ou remover links |
| `hub/automacao-imobiliaria.html` | 129 | Criar página hub ou apontar para `automacao-imobiliarias.html` |
| `outreach/desempenho.html`, `outreach/despacho.html`, `outreach/posts-redes-sociais.html`, `outreach/tracker.html` | ~200 | Criar seção outreach ou remover |
| `blog/artigo-completo.html` | 41 | Criar template de artigo ou remover links |
| `assets/css/style.css`, `style.css`, `styles.css` | ~44 | Padronizar folha de estilo |
| `blog/segundo.html` | 12 | Revisar |
| `inteligencia.html` | 10 | Criar página ou remover |

## Manutenção contínua

- `python scripts/fix_broken_links.py --dry-run` — simula correções
- `python scripts/fix_broken_links.py` — aplica correções de alta confiança
- `python check_links.py` — auditoria completa (inclui links externos)
- CI: workflow `Link Check` roda toda segunda-feira
