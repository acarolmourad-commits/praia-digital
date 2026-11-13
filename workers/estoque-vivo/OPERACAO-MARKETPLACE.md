# Operação de estoque entre marca e influenciadores

## Fluxo recomendado para o piloto

1. A marca cria seu espaço, guarda a chave de gestão e cadastra um SKU para cada variação vendável. O saldo inicial deve vir de uma contagem ou fonte conferida.
2. A gestão cria um acesso individual para cada influenciador e entrega a chave pelo canal privado habitual. O app não envia chaves por mensagem automaticamente.
3. Antes de comprometer unidades, o influenciador consulta o disponível e usa Pedidos → Novo pedido, com referência única do canal e todos os produtos. Todos passam a ver o disponível reduzido. A reserva fica atribuída ao acesso dele.
4. Após a saída física, usa Confirmar saída no pedido. Se a negociação for cancelada antes da saída, usa Cancelar e liberar. As movimentações avulsas continuam disponíveis, mas não devem repetir vendas já registradas em Pedidos.
5. A gestão acompanha reservas pendentes, repõe produtos, confere devoluções e corrige contagens com justificativa. A reserva não expira sozinha nesta versão.
6. Ao entrar em 150 unidades disponíveis ou menos, o produto aparece em alerta. Dispositivos que ativaram push entram na fila de notificação. O saldo zero gera novo aviso.

## Exemplo

| Situação | Físico | Reservado | Disponível |
|---|---:|---:|---:|
| Saldo inicial | 200 | 0 | 200 |
| Influenciador A reserva 30 | 200 | 30 | 170 |
| Influenciador B reserva 20 | 200 | 50 | 150 |
| Alerta de últimas unidades | 200 | 50 | 150 |
| A confirma a venda de 30 reservadas | 170 | 20 | 150 |
| B libera a reserva de 20 | 170 | 0 | 170 |

Cada quantidade pertence a um SKU/variação. Não somar tamanhos ou produtos diferentes para decidir o alerta.

## Regras de responsabilidade

A marca administra catálogo, estoque físico e acessos. O influenciador consulta o estoque central, registra vendas e controla as próprias reservas. A gestão pode intervir em qualquer reserva, mantendo executor e responsável no histórico. Revogar acesso não libera automaticamente as unidades: a gestão precisa conferir o que foi vendido antes de liberar.

O alerta ajuda a coordenar a divulgação, mas não pausa anúncios externos nem cancela campanhas. O número mostrado só acompanha entradas, reservas e saídas efetivamente registradas no app. Nenhum conector nativo de marketplace está ativo nesta versão. A API normalizada está preparada para um adaptador autorizado e validado por marca.

## Próxima etapa: integrar um canal piloto

Escolher uma marca, seu sistema atual e o primeiro marketplace. Confirmar a fonte oficial do estoque, mapear SKUs/variações e obter as permissões da conta. Depois validar eventos de pedido, pagamento, cancelamento, devolução e expedição, com idempotência, reconciliação e tratamento de falhas. Só então ampliar a sincronização para outros canais. Disponibilidade e aprovação de APIs dependem de cada plataforma.

O piloto atual é uma PWA para uso compartilhado com conexão, instalada pelo navegador quando suportado. Publicação em lojas de aplicativos, integração com ERP, importação de planilhas, comissões e faturamento são evoluções separadas, ainda não entregues.


## Cuidados ao ativar um canal

Definir horário de corte e quais pedidos já estão refletidos no saldo inicial. A referência é única por canal na marca; não registrar novamente pedidos importados. A integração deve consultar o estado atual da origem antes de avançar a revisão e manter a fila de erros no adaptador. Confirmar a saída apenas quando houver saída física, não apenas pagamento. Cancelar no painel não cancela a compra na plataforma.

Se o adaptador falhar, pausar a conexão e conferir os pedidos antes da intervenção manual. Reservas não são liberadas automaticamente. Trocar a chave da gestão pausa todas as conexões de API. Uma conexão nova não assume os pedidos da anterior. Devoluções e envios parciais precisam de procedimento próprio e não estão automatizados.

Apresentação: https://estoque.praia.digital/apresentacao.html. Guia técnico: https://estoque.praia.digital/integracao.html.
