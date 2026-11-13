# Estoque Vivo — Praia Digital

Versão piloto em https://estoque.praia.digital/. Fonte do painel e API, com um Durable Object SQLite por espaço de marca. Não depende de dados em localStorage.

## Escopo entregue

- Produtos por SKU/variação, saldo inicial e mínimo de reposição.
- Entrada, venda direta, reserva, confirmação de venda reservada, liberação, devolução, perda e contagem física.
- Saldo físico, reservado e disponível; bloqueio de saldo negativo, contagem desatualizada e referência duplicada.
- Histórico com identificação informada pelo operador e exportação CSV de produtos e histórico completo, paginado no servidor.
- Atualização via WebSocket entre telas conectadas; reconexão e consulta de segurança a cada 30 segundos.
- Chave por espaço, sessão de 12 horas, troca de chave e revogação das sessões anteriores.

Registro manual: selecionar TikTok Shop, Instagram, Facebook, Shopee ou Mercado Livre apenas identifica a origem. Não há integração automática, importação de planilhas, ERP, múltiplos depósitos, contas individuais com perfis, nem mensagens externas. O nome do operador é autodeclarado.

Limites do piloto: 2.000 SKUs (incluindo arquivados), 100.000 operações, 30 telas WebSocket e 50 sessões por espaço. Quantidades inteiras. Sem SLA. Exportar periodicamente. Não há recuperação de chave por e-mail. Quem possui a chave tem acesso completo ao espaço.

## Desenvolvimento e testes

Node 24 e npm. Execute `npm ci`, `npm test` e `npm run dev`. O servidor de desenvolvimento usa 127.0.0.1:4173 com persistência local isolada. `npm run build` gera assets.mjs a partir de index.html, app.js, style.css e domain.mjs.

Os testes usam o runtime real workerd pelo plugin oficial Cloudflare/Vitest. Cobrem acesso, origem, isolamento entre marcas, idempotência, concorrência, reservas, contagem obsoleta, duplicidade, SKU, validação, arquivamento, WebSocket, revogação, CSV e persistência após reinício do Durable Object.

## Publicação

Worker `praia-estoque-vivo`, domínio `estoque.praia.digital`. Configuração declarada em wrangler.jsonc. A publicação inicial foi feita pelo conector Cloudflare com os módulos worker.mjs, room.mjs, domain.mjs e assets.mjs gerado; a migração v1 cria InventoryRoom com SQLite. Para publicação pela CLI autenticada: `npm run build` e `npx wrangler deploy`. Não excluir/recriar o namespace ou trocar o nome da classe: isso pode separar o app dos dados existentes. Mudanças de esquema exigem migração compatível e preservação dos dados.

O repositório contém a fonte; alterações no GitHub não publicam automaticamente este Worker. Os hubs estáticos da Praia Digital são publicados pelo fluxo existente do site. Nenhuma mudança de plano ou contratação paga foi feita nesta entrega. Uso sujeito aos limites da conta Cloudflare.

## Segurança e operação

Chaves e sessões aleatórias de 256 bits; apenas hashes persistidos. Cookie HttpOnly, Secure, SameSite=Strict; chave fora de URL e armazenamento web. POST e WebSocket exigem mesma origem. Rate limits por IP: 10 autenticações/minuto e 120 requisições/minuto; chaves por marca são compartilhadas apenas com operadores autorizados. Não colocar dados de clientes ou segredos nas observações.

Transações SQLite síncronas mantêm saldo e histórico juntos. IDs de operação impedem repetição da mesma tentativa; para pedidos externos, usar referência única por produto/tipo/canal. Contagens físicas exigem versão atual. Não há fila offline: erro ou perda de conexão não confirma gravação; repetir o mesmo formulário preserva o ID da tentativa.

`/health` expõe somente saúde/versão. Logs não incluem corpo, chave ou cookie. API e páginas privadas usam no-store/noindex. Exportações escapam fórmulas de planilha. Monitorar erros/limites pelo painel Cloudflare; nunca incluir chaves nos logs ou issues.

Antes de conectar marketplaces: definir fonte oficial do estoque, credenciais por marca, correspondência de SKUs, reservas/cancelamentos, idempotência por evento, reconciliação e tratamento de falhas. Não anunciar baixa automática antes de validar cada integração.
