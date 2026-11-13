# Validação da versão piloto 1.0.0

## Testes automatizados

13 testes aprovados em workerd com SQLite Durable Objects, incluindo concorrência, reservas, idempotência, isolamento de espaços, sessão, origem, revogação e persistência após reinício. Comando: `npm test`.

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
