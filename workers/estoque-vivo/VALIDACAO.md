# Validação da versão piloto 1.2.0

## Testes da versão 1.2

44 testes aprovados em 3 arquivos no runtime workerd com Durable Objects SQLite. Execução de 13/11/2026, 23:08 UTC, por `npm test`; duração 2,83 segundos. Mantém os 27 casos anteriores e acrescenta 17 casos de pedidos/API.

Cobertura nova: reserva de vários SKUs em uma transação, reversão integral quando falta saldo, separação de reservas avulsas e de pedidos, confirmação sem baixa duplicada, cancelamento, versão obsoleta, concorrência, referência repetida, autenticação da integração, escopo de influenciador, revisões repetidas/fora de ordem, cancelamento recebido antes da reserva, SKU ausente/duplicado, itens alterados, pausa/revogação, isolamento, persistência e preservação do SKU vinculado a pedidos.

A API foi validada com eventos sintéticos. Nenhuma loja real foi autenticada; nenhum pedido real foi importado. O aceite de Web Push continua simulado nos testes e não comprova recebimento em dispositivo físico.

A apresentação nativa tem oito slides; todos foram renderizados e inspecionados visualmente. A página pública equivalente é `/apresentacao.html`. A conferência final da versão publicada será registrada abaixo após a publicação.

---

## Histórico de validação da versão 1.1.0


## Testes automatizados

27 testes aprovados em workerd com SQLite Durable Objects, incluindo concorrência, reservas, idempotência, isolamento de espaços, sessão, origem, revogação e persistência após reinício. Comando: `npm test`.

## Navegador público

URL conferida: https://estoque.praia.digital/. Chrome no ambiente cloud, desktop. Espaço sintético “Marca de teste — validação Praia Digital”; nenhum produto ou pedido real de cliente.

- Criação de espaço e apresentação da chave; chave não copiada, registrada ou publicada.
- Cadastro da camiseta TESTE-AZ-M, variação Azul/M, saldo inicial 20, mínimo 5.
- Duas abas conectadas ao mesmo espaço/sessão. Reserva de 3 via primeira aba: segunda aba mostrou físico 20, reservado 3, disponível 17 sem recarregar.
- Venda direta de 2: segunda aba mostrou físico 18, reservado 3, disponível 15.
- Tentativa de venda de 99 recusada com “Saldo insuficiente. Confira o disponível e as reservas.”; saldo preservado.
- Histórico exibiu saldo inicial, reserva (Instagram) e venda (TikTok Shop). Esses canais foram apenas rótulos de registros manuais.
- Exportações de produtos e histórico concluíram o download no navegador. O conteúdo CSV também tem verificação automatizada de escape de fórmulas.
- Logout confirmado e retorno à tela de acesso.

A imagem docs/painel.jpg mostra o teste com dados fictícios. Não contém chave de acesso.

## Limites da conferência

Não foram testados dispositivos móveis físicos, Safari/Firefox, acesso simultâneo com pessoas reais, volume de 2.000 SKUs, carga prolongada ou integrações com plataformas externas. As duas abas compartilham uma sessão do navegador; entrada por chave em nova sessão é coberta pelos testes automatizados. Não foi simulado corte de rede no navegador; reconexão está implementada, sem declaração de validação manual desse cenário.

A prévia local ficou bloqueada pela revisão automática de segurança do navegador. A conferência visual acima ocorreu no endereço público autorizado. O layout possui regras responsivas, mas esta entrega não representa validação visual em celular.


## Ampliação para influenciadores e alertas

27 testes atuais incluem permissões por acesso, identidade do influenciador, reserva individual, intervenção da gestão, revogação sem perda de saldo, alertas ao cruzar 150 disponíveis, deduplicação, rearme após reposição, alerta de zero, limite personalizável, idempotência por acesso, validação de endpoints push, payload cifrado, fila persistente, aceite simulado, reenvio em erro temporário, remoção de inscrição expirada, migração de dados da versão anterior e arquivos da PWA.

No endereço público, outro espaço com dados fictícios validou criação de influenciador, cadastro de produto com 200 unidades e limite padrão 150, reserva de 50 atribuída ao influenciador e alerta com físico 200/reservado 50/disponível 150. O histórico distinguiu Gestão de teste (executor) de Influenciador de teste A (responsável). Screenshot: docs/alerta-150.jpg.

Notificações foram configuradas no servidor. Ao clicar Ativar alertas, o navegador cloud retornou NotAllowedError, exibido como “Notificações não autorizadas”. Não se alterou nem contornou essa permissão. A inscrição e entrega real em Chrome/Safari/iPhone permanecem não validadas; os testes automatizados do envio usam um provedor simulado. Manifesto, ícones e service worker foram verificados nos testes. Não declarar instalação em celular ou entrega push real como concluídas.
