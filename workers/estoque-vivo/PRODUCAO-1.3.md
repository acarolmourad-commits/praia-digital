# Versão 1.3 preparada — estoque e produção sob demanda

Estado: fonte e bundle preparados; publicação no Worker pendente de reconexão Cloudflare (oauth_token_invalid_grant). Não anunciar o fluxo novo como ativo antes da publicação e conferência. GitHub não publica este Worker automaticamente.

## Regras confirmadas para o piloto

Ferri Shapes disponibiliza 20 unidades exclusivas. Produção sob demanda em até 20 dias corridos a partir do pagamento confirmado, separado do frete. O saldo 20 é uma referência fornecida pela gestão, não uma leitura em tempo real do TikTok. Confirmar o saldo no início da operação. O alerta 150 foi preservado; a sugestão de reduzi-lo a 5 não foi confirmada.

## Fonte preparada

- Aba Sob demanda (somente gestão): encomenda sem pagamento → produção após conferência manual → produção pronta com entrada e reserva atômicas → saída na aba Pedidos.
- Prazo = data do pagamento + 20 dias corridos, informado pela gestão no calendário de Brasília. Datas futuras e impossíveis recusadas.
- Histórico de marcos, prazos vencidos, cancelamento justificado, referência única por canal e versões contra edição concorrente.
- Produção não consome estoque pronto nem cria disponível antes da conclusão. Não há pagamento bancário automático, estorno, expedição parcial ou integração nativa com marketplaces.
- Gestão pode concluir encomenda de responsável revogado mantendo autoria e reserva; revogação não dá novo acesso nem perde estoque.
- Botão de preenchimento Ferri Shapes no novo produto. Sugere SKU interno, saldo 20 e alerta 150; exige revisão e salvamento pela gestão. Não cria marca ou produto automaticamente.
- Guia `/piloto.html`: responsabilidades, contas, conexões existentes versus pendentes, teste com duas pessoas, cancelamento, alerta 150/zero, produção e checklist comercial. Cópia autossuficiente em `docs/guia-influenciadores.html` informa a pendência de publicação.

## Validação

55 testes passaram em 4 arquivos com workerd/Durable Objects SQLite. Incluem os 44 anteriores e 11 novos casos de produção, datas, isolamento, permissões, idempotência, concorrência, referência duplicada, preservação de SKU, revogação, persistência e assets do guia.

Build gerado por `npm test` e `npm run build`. Browser cloud não conseguiu abrir a prévia local (ERR_CONNECTION_REFUSED); a retomada do tab foi bloqueada pela política de URL. Não houve contorno do bloqueio. Revisão visual e testes em aparelho físico não concluídos. Nenhuma compra, pagamento, estoque comercial ou anúncio externo foi alterado. Nenhum acesso de influencer real foi criado ou enviado nesta rodada.

## Publicação após reconectar

Ler settings atuais do Worker `praia-estoque-vivo`, preservar ROOMS/namespace InventoryRoom, limitadores e secret VAPID_KEYS. Publicar bundle `dist/worker.mjs`; migração aditiva cria production e production_events no mesmo espaço. Não apagar/recriar namespace. Conferir versão 1.3.0 em /health, guia, aba Sob demanda, acesso por gestão versus influencer, e ciclo em espaço de treinamento separado. Só então liberar a nova funcionalidade para testes comerciais acompanhados.
