# Estoque Vivo — Praia Digital

Versão piloto 1.2.0 em https://estoque.praia.digital/. Fonte do painel e API, com um Durable Object SQLite por espaço de marca. Não depende de dados em localStorage.

## Escopo entregue

- Produtos por SKU/variação, saldo inicial e mínimo de reposição.
- Entrada, venda direta, reserva, confirmação de venda reservada, liberação, devolução, perda e contagem física.
- Saldo físico, reservado e disponível; bloqueio de saldo negativo, contagem desatualizada e referência duplicada.
- Histórico com identificação informada pelo operador e exportação CSV de produtos e histórico completo, paginado no servidor.
- Atualização via WebSocket entre telas conectadas; reconexão e consulta de segurança a cada 30 segundos.
- Chave de gestão por marca e acessos individuais revogáveis para influenciadores; sessão de 12 horas.
- Reservas atribuídas ao vendedor, com controle de confirmação/liberação por responsável.
- Radar de disponibilidade: alerta padrão em 150 unidades livres por SKU, sem repetição por venda, novo ciclo após reposição e aviso adicional ao zerar.
- Pedidos com até 30 SKUs, reserva integral, confirmação da saída física e cancelamento antes da saída.
- API autenticada de pedidos normalizados, com revisão por pedido e proteção contra repetição de eventos.
- Apresentação pública em https://estoque.praia.digital/apresentacao.html e instruções em /integracao.html.
- PWA com manifesto, ícones e Web Push opcional; fila persistente, criptografia e tentativas limitadas.

Selecionar TikTok Shop, Instagram, Facebook, Shopee ou Mercado Livre identifica o canal do registro. A API recebe pedidos normalizados de um servidor autorizado; os adaptadores nativos, autorização de lojas e atualização dos anúncios ainda precisam ser implementados e validados por marca. Não há importação de planilhas, ERP conectado, múltiplos depósitos, importação histórica nem mensagens de WhatsApp/e-mail. A gestão identifica o influenciador ao criar sua chave; o nome informado no login não substitui essa identificação. O nome da gestão é autodeclarado. Não há verificação civil da identidade.

Limites do piloto: 2.000 SKUs (incluindo arquivados), 100.000 operações, 30 telas WebSocket, 50 sessões, 100 influenciadores ativos e 30 dispositivos de push, 20 conexões ativas e 20.000 pedidos por espaço. Quantidades inteiras. Sem SLA. Exportar periodicamente. Não há recuperação de chave por e-mail. A chave de gestão dá acesso completo; a chave de influenciador permite ler o estoque, vender e administrar suas próprias reservas. Chaves não devem ser compartilhadas entre pessoas. A gestão pode confirmar/liberar reservas de outro responsável. Reservas não vencem automaticamente.

## Desenvolvimento e testes

Node 24 e npm. Execute `npm ci`, `npm test` e `npm run dev`. O servidor de desenvolvimento usa 127.0.0.1:4173 com persistência local isolada. `npm run build` gera assets.mjs e o bundle dist/worker.mjs. Ícones PNG, manifesto e service worker são servidos pelo mesmo Worker. O app requer conexão para consultar e gravar; não há cache de estoques nem fila de vendas offline.

Os testes usam o runtime real workerd pelo plugin oficial Cloudflare/Vitest. Cobrem acesso, origem, isolamento entre marcas, idempotência, concorrência, reservas, contagem obsoleta, duplicidade, SKU, validação, arquivamento, WebSocket, revogação, CSV e persistência após reinício do Durable Object.

## Publicação

Worker `praia-estoque-vivo`, domínio `estoque.praia.digital`. Configuração declarada em wrangler.jsonc. A publicação é feita pelo conector Cloudflare com o bundle dist/worker.mjs como módulo worker.mjs; a migração v1 cria InventoryRoom com SQLite. Para publicação pela CLI autenticada: `npm run build` e `npx wrangler deploy`. Não excluir/recriar o namespace ou trocar o nome da classe: isso pode separar o app dos dados existentes. Mudanças de esquema exigem migração compatível e preservação dos dados.

O repositório contém a fonte; alterações no GitHub não publicam automaticamente este Worker. Os hubs estáticos da Praia Digital são publicados pelo fluxo existente do site. Nenhuma mudança de plano ou contratação paga foi feita nesta entrega. Uso sujeito aos limites da conta Cloudflare.

## Segurança e operação

Chaves e sessões aleatórias de 256 bits; apenas hashes persistidos. Cookie HttpOnly, Secure, SameSite=Strict; chave fora de URL e armazenamento web. POST da interface e WebSocket exigem mesma origem. A rota de integração usa uma chave específica por conexão, rejeita cabeçalho Origin e é destinada somente a servidor. Rate limits por IP: 10 autenticações/minuto e 120 requisições/minuto; a chave de gestão permanece com a marca; cada influenciador recebe sua própria chave e permissões restritas. Não colocar dados de clientes ou segredos nas observações.

Transações SQLite síncronas mantêm saldo e histórico juntos. IDs de operação impedem repetição da mesma tentativa; pedidos usam referência única por canal dentro da marca. Movimentações avulsas antigas não são convertidas em pedidos: definir corte para evitar baixa duplicada. Contagens físicas exigem versão atual. Não há fila offline: erro ou perda de conexão não confirma gravação; repetir o mesmo formulário preserva o ID da tentativa.

`/health` expõe somente saúde/versão. Logs não incluem corpo, chave ou cookie. API e páginas privadas usam no-store/noindex. Exportações escapam fórmulas de planilha. Monitorar erros/limites pelo painel Cloudflare; nunca incluir chaves nos logs ou issues.

Antes de conectar marketplaces: definir fonte oficial do estoque, credenciais por marca, correspondência de SKUs, reservas/cancelamentos, idempotência por evento, reconciliação e tratamento de falhas. Não anunciar baixa automática antes de validar cada integração.


## Notificações nas últimas 150 unidades

O evento usa `físico − reservado`, por SKU/variação, não a soma de produtos diferentes. O limite padrão 150 pode ser ajustado no cadastro. Cada entrada na faixa gera um evento persistido. Permanecer abaixo do limite não dispara a cada venda; repor acima rearma o alerta. Zero disponível gera um novo aviso. Produto já cadastrado abaixo do limite entra no radar imediatamente.

`VAPID_KEYS` é um secret do Worker, com JSON `{subject, publicKey, privateKey}`. As chaves foram geradas no ambiente Cloudflare e a privada não foi gravada no código, nos arquivos ou no GitHub. A API push-config retorna somente a chave pública. Ao atualizar o Worker via API, preservar bindings `secret_text`. Não regenerar VAPID sem um plano para reinscrever os dispositivos.

O usuário precisa ativar notificações em cada dispositivo. No iPhone/iPad compatível, adicionar à Tela de Início e abrir pelo ícone antes de ativar. O botão Enviar teste enfileira uma mensagem para o próprio dispositivo. Notificações continuam após expiração da sessão, até desativação/logout/revogação; ao sair, as inscrições daquele acesso são removidas. Trocar a chave de gestão remove todas as inscrições e sessões e pausa todas as conexões de API, mas as chaves individuais continuam válidas até revogação explícita.

Envio Web Push com @block65/webcrypto-web-push 2.0.0, aes128gcm/VAPID. Destinos HTTPS restritos aos serviços de Google, Mozilla, Apple e Windows; redirects não são seguidos. Fila SQLite com até três tentativas, descarte de eventos substituídos, validade máxima de 15 minutos na fila e TTL de cinco minutos no provedor. HTTP 404/410 remove inscrições expiradas. Aceite do provedor não comprova exibição ao destinatário; permissões, rede e sistema operacional podem atrasar ou impedir a entrega. O histórico do painel é a referência para conferência.

A reserva identifica o responsável; o registro guarda separadamente quem executou e a quem pertence a reserva/venda. Influenciadores veem o próprio histórico, inclusive intervenções da gestão em suas reservas. A gestão vê o conjunto. O limite de estoque protege operações registradas neste app; vendas externas precisam ser lançadas pela equipe ou recebidas pela API após configuração e validação da integração.

Referências: [Apple/WebKit — Web Push no iOS](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/), [MDN Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API), [biblioteca Web Push](https://github.com/block65/webcrypto-web-push).


## Pedidos e integração — versão 1.2

Pedidos reservam todos os itens numa transação. A confirmação de saída baixa físico e reservado juntos; cancelar antes da saída libera apenas a reserva daquele pedido. Reservas avulsas permanecem separadas. Não há expedição parcial, reabertura nem troca de itens. Devoluções são conferidas fisicamente e registradas separadamente. SKUs vinculados a pedidos não podem ser renomeados.

A API `POST /api/integration/order` exige Bearer EI1 e não usa a chave da gestão. O responsável e o canal ficam definidos na conexão; somente hashes são persistidos. Guardar a chave no secret do servidor que fará a integração. O adaptador deve normalizar eventos, manter uma revisão monotônica por pedido, repetir o mesmo event_id em falhas de rede e tratar pedidos rejeitados. Esta versão não inclui fila de rejeitados ou reconciliação externa automática.

Pausar uma conexão revoga sua chave e permite intervenção manual nos pedidos pendentes. Revogar um influenciador pausa suas conexões. Pedidos e reservas são preservados. Uma conexão nova é uma origem nova: pedidos antigos precisam de conferência e encerramento antes da retomada, pois não são transferidos automaticamente.

A migração 1.2 cria apenas tabelas e índices adicionais no mesmo Durable Object, sem apagar catálogo, reservas, acessos ou histórico. O namespace e o secret VAPID devem ser preservados na publicação.
