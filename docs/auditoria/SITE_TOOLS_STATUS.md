# SITE_TOOLS_STATUS.md
## Inventário Operacional — Ferramentas do Praia Digital

| Ferramenta | Status | Pública? | Backend | Produção | Risco | Próxima ação |
|---|---|---|---|---|---|---|
| Simulador de financiamento | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| AI Valuation | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| ROI Calculator | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| Rent vs Buy | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| QR Code | ISOLATED | Não | Nenhum | Não verificado | Médio | Reconstruir ou remover |
| Embed | ISOLATED | Não | Nenhum | Não verificado | Médio | Reconstruir ou remover |
| AI Description Generator | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| Transaction Costs | ISOLATED | Não | Nenhum | Não verificado | Médio | Reconstruir com backend real |
| Credit Analyzer | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| Rental Revenue | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| Equity Growth | ISOLATED | Não | Nenhum | Não verificado | Alto | Reconstruir com backend real |
| Report Generator | ISOLATED | Não | Nenhum | Não verificado | Médio | Reconstruir com backend real |
| Commission Calculator | ISOLATED | Não | Nenhum | Não verificado | Baixo | Reconstruir ou remover |
| Print/PDF tools | ISOLATED | Não | Nenhum | Não verificado | Baixo | Remover ou reconstruir com template engine |
| Header/navegação | HEALTHY | Sim | N/A | Verificado | Nenhum | Manter |
| Listagens de imóveis | HEALTHY | Sim | N/A | Verificado | Nenhum | Manter |
| Conteúdo editorial/blog | HEALTHY | Sim | N/A | Verificado | Nenhum | Manter |
| CTAs/WhatsApp | HEALTHY | Sim | N/A | Verificado | Nenhum | Manter |
| SEO/schema | HEALTHY | Sim | N/A | Verificado | Nenhum | Manter |

### Status permitidos
- HEALTHY
- FIXED
- ISOLATED
- BLOCKED
- REBUILD_REQUIRED
- NOT_VERIFIED

### Próxima ação padrão
Todas as ferramentas ISOLATED só podem ser reativadas após:
- código válido;
- backend funcional em produção;
- endpoint real confirmado;
- testes de sintaxe;
- browser/console/network;
- UX e segurança validadas;
- deploy confirmado.
