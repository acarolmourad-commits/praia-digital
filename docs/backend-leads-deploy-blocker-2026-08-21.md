# Backend Leads Deploy Blocker — 2026-08-21
## Diagnóstico
Os endpoints de captura de leads retornam HTTP 405 em produção:
- `/backend/api/leads/b2b.js`
- `/backend/api/leads/report.js`
- `/backend/api/leads/index.js`

## Causa raiz
O caminho `/backend/**` está sendo servido como arquivos estáticos pelo host atual, sem execução serverless/runtime. Os arquivos existem no repositório, mas não há provedor ativo processando funções serverless no momento.

## Status do deploy
- Nenhuma autenticação de deploy ativa disponível no ambiente atual:
  - Render CLI: não autenticado
  - Vercel/Netlify/AWS CLI: ausentes
  - GitHub Actions: deploy atual serve apenas site estático

## Mitigação atual
- Frontend com fallback via `mailto:comercial@praia.digital` para B2B e relatório.
- CSV local preparado para gravação quando o backend for ativado.
- Código das rotas valida payload e responde HTTP 200/201 em runtime serverless.

## Próximos passos
1. Autenticar provedor serverless e reimplantar funções em `/backend/api/leads/*`.
2. Validar POST real com payload de teste.
3. Remover fallback mailto quando API estiver 200/201 confirmado.
