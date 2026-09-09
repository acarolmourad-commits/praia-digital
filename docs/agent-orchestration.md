# Orquestração — Bots Praia Digital

Objetivo: evitar retrabalho e garantir que cada bot atue na sua especialidade, recebendo contexto pronto e devolvendo artefatos acionáveis.

## Responsabilidades por bot

- **Hermes**: núcleo operacional do projeto.
  - Delega por tema, consolida entregues e decide próximo passo.
- **Hermes SEO**: indexação, conteúdo, canonical, sitemap, robots, cache-bust, HTTP 200, links quebrados.
- **Hermes Leads**: captura, qualificação, CTAs, funil, integração WhatsApp.
- **Hermes Analytics**: métricas, AdSense readiness, ads.txt, snippets, conversão, health-check pós-deploy.
- **Hermes Deploy**: validação de build/deploy, HTTP 200, cache-bust, 404/?nocache=1, rollback rápido.
- **Hermes Outreach**: prospecção e follow-up multicanal, templates, réguas D2/D5/D10, listas de outreach, `noindex`.

## Regra geral de handoff

- Entrada sempre no formato: objetivo + arquivos/pastas afetados + restrições.
- Saída sempre no formato: o que mudou + onde conferir + próximo passo sugerido.
- Nenhum bot altera áreas fora do seu domínio sem instrução explícita do núcleo.

## Fluxo operacional sugerido

1. SEO estrutura/corrige conteúdo e sinaliza URLs/landings candidatas.
2. Leads recebe essas URLs e verifica CTAs, formulários e rastreamento.
3. Outreach recebe leads qualificados e prepara templates/listas; páginas de outreach saem do sitemap e recebem `noindex`.
4. Deploy valida build/push e confirma HTTP 200 + cache-bust.
5. Analytics confere métricas/snippets/AdSense após deploy.
6. SEO trata ajustes finos de desempenho/indexação quando Analytics aponta problema de conteúdo/SEO.

## Restrições globais

- Sem alteração de AdSense/ads.txt/snippets sem autorização.
- Sem PII sensível em arquivos de outreach.
- Sem envio externo sem aprovação.
- Debug/contraste sempre que possível com evidência verificável.
