# Plano executivo — Auditoria 404 + SEO + interlinking
Data: 2026-08-18
Estado: FASE 1 concluída — sem reparos de link aplicáveis no momento

## 1. Descoberta principal
O plano `docs/comercial/plano_reparo_404_2026-08-18.csv` contém:
- `REPARAR_LINK`: 13 itens
- `MANTER_404`: 1.255 itens
- `REMOVER_REFERENCIA`: 531 itens
Total: 1.799 linhas (inclui header duplicado)

## 2. Divergência: REPARAR_LINK
Após verificação técnica:
- Todos os 13 registros `REPARAR_LINK` têm `substituta_local` idêntica à URL quebrada.
- Destino existe localmente.
- Isso não configura link quebrado: é **DEPLOY_NAO_ENTREGA_200**.

Exemplos:
- `/blog/maresias-checklist-juridico-imoveis-2026.html` → destino existe, status HTTP 503 no deploy
- `/outreach/convites-demo-15min/...` → destino existe, status HTTP 503 no deploy
- `/blog/...` → destino existe, status HTTP 404 no deploy

Referências internas encontradas: 10 ocorrências em 6 arquivos do próprio site.

## 3. Decisão operacional
**NÃO executar substituição de links** neste lote porque:
1. A substituição seria idêntica (origem = destino).
2. O problema é de deploy/configuração, não de conteúdo.
3. Alterar HTML sem resolver deploy não resolve o 404.

## 4. Ação recomendada
DEPLOY_NAO_ENTREGA_200 (13 URLs):
- blog/maresias-checklist-juridico-imoveis-2026.html (503)
- blog/* (9 URLs) (404)
- outreach/convites-demo-15min/* (2 URLs) (503)
- outreach/emails-followup-d3-20prontos-2026-07-11.html (503)

Verificar:
- Configuração do servidor/Render para essas rotas
- Cache/CDN
- Sitemap.xml não deve ser alterado apenas por esse problema

MANTER_404 (1.255 URLs):
- academy.praia.digital/* (55 URLs) — DNS pendente
- outreach/lote-prospeccao-* (531 URLs) — rotas removidas sem substituta
- Outros (669 URLs) — manter

## 5. Próximos passos
- SEO/interlinking em páginas comerciais
- Auditoria de 20 URLs não indexadas
- Valorização editorial do estoque existente
- Não recomeçar auditoria 404 do zero
