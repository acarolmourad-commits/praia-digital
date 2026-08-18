# Classificação de 404 — Praia Digital
Data: 2026-08-18
Auditoria: docs/comercial/auditoria_404_2026-08-18.csv

## Totais
- Total de falhas: 1.799
- HTTP 404: 1.730
- DNS/resolution error: 57
- HTTP 503: 12

## Padrões identificados
- `/outreach/` e `/proprietarios/`: 1.677 URLs — forte indício de rotas antigas removidas
- `academy.praia.digital` + `www.praia.digital`: 57 URLs — erro de DNS/resolução
- `/blog/`: 14 URLs — páginas que existem no repositório, mas podem não estar deployadas
- `/servicos/`: 2 URLs
- `/rss.xml`: 1 URL

## Classificação proposta
A. 404 legítimo/intencional
   - Rotas `/outreach/`, `/proprietarios/`, `/servicos/` removidas sem substituta clara
   - `/rss.xml` removido

B. link quebrado
   - `/blog/` URLs que existem localmente mas retornam 404 no deploy
   - Pode indicar problema de deploy/cache/config

C. página removida que precisa de redirect
   - Somente se houver substituta inequívoca documentada
   - Caso contrário, manter como A

D. URL digitada incorretamente
   - Nenhum caso claro identificado ainda

E. referência antiga
   - Maioria dos `/outreach/` e `/proprietarios/`
   - Precisa de varredura manual para confirmar se há substituta

F. recurso inexistente que deve ser removido
   - Não aplicável no momento

## Pendente
- Varredura manual dos arquivos que referenciam `/outreach/`, `/proprietarios/`, `/servicos/`
- Verificar deploy/config do blog
- Verificar configuração DNS de `academy.praia.digital`
- Confirmar se `/rss.xml` foi removido intencionalmente
