# Piloto de marketplaces — especificação para avaliação

Versão 1.0, 18/11/2026. Material compartilhável, somente dados fictícios.

## Objetivo prioritário

Avaliar primeiro o controle de estoque compartilhado: registrar uma reserva,
liberá-la ou confirmar sua saída e conferir que **disponível = físico − reservado**.
Esse recorte tem um resultado observável antes de introduzir autenticação de
lojas, adaptadores de marketplaces ou transmissão de vídeo.

O foco recomendado é **Estoque Vivo**. LiveBridge AI permanece uma frente
complementar. A escolha é uma proposta técnica para avaliação, não um aceite
do cliente, contratação, prazo de entrega ou autorização de despesas.

## Materiais

- [Laboratório interativo](./): modelo didático local, sem login ou API.
- [Apresentação Estoque Vivo](https://estoque.praia.digital/apresentacao.html).
- [Contrato de integração](https://estoque.praia.digital/integracao.html).
- [Conceito LiveBridge AI](https://praia.digital/ia/marketplaces/#demonstracao).
- [Fonte do Worker](https://github.com/acarolmourad-commits/praia-digital/tree/main/workers/estoque-vivo): implementação distinta do laboratório.

O laboratório só fica publicado após integração e deploy do site. Um link para
uma branch ou PR demonstra código disponível para revisão, não publicação.

## Escopo da demonstração

Uma marca fictícia, dois operadores fictícios, dois canais simulados e três
SKUs. O canal é uma etiqueta do registro, não uma conexão. Nenhum campo livre
solicita nome, contato ou dados reais. O estado existe apenas na memória da aba;
recarregar, reiniciar ou executar o roteiro cria uma base nova. Não há envio de
dados, armazenamento remoto, cookies da aplicação ou sincronização entre abas.

| SKU fictício | Saldo físico inicial | Reservado inicial |
| --- | ---: | ---: |
| DEMO-CAM-AZ-M | 160 | 0 |
| DEMO-BOL-CR | 12 | 0 |
| DEMO-BON-VD | 5 | 0 |

O radar visual sinaliza até 150 unidades disponíveis **por SKU**, inclusive 150.
Ele não comprova Web Push, entrega de mensagem ou alerta no celular.

## Modelo e comportamento

`Product`: sku, nome, saldo inicial, físico e reservado. `Order`: referência,
SKU, quantidade, operador, canal e estado (reserved, shipped, cancelled).
`Event`: ID, tipo, pedido e conteúdo; registra os saldos depois da aplicação.

- `reserve`: quantidade inteira positiva, limitada ao disponível; aumenta
  reservado sem reduzir físico.
- `ship`: somente pedido reservado; reduz físico e reservado juntos.
- `cancel`: somente pedido reservado; libera reservado e preserva físico.
- Mesmo ID com mesmo conteúdo retorna duplicate, sem segunda operação.
- Mesmo ID com outro conteúdo ou pedido já existente é recusado.
- Falhas de validação preservam saldos, pedidos e histórico de aplicações.
- A conciliação recalcula reservas e saídas pelos pedidos. SKUs são isolados.

O laboratório usa um modelo independente, sem importar o código de produção.
Não prova concorrência no servidor, segurança dos acessos, permissões dos
operadores ou persistência. Os dois operadores são etiquetas fictícias, não
usuários autenticados. Quantidades fracionadas e devoluções ficam fora do recorte.

## Roteiro e critérios de sucesso da demonstração

1. Reservar 12 camisetas: físico 160, reservado 12, disponível 148.
2. Exibir radar visual em 148 unidades livres.
3. Recusar reserva de 149, mantendo disponível 148.
4. Repetir o primeiro evento, mantendo uma reserva e um registro aplicado.
5. Repetir o ID com quantidade diferente: recusar sem alterar saldo.
6. Cancelar primeira reserva: físico 160, reservado 0, disponível 160.
7. Reservar 10 e confirmar saída: físico 150, reservado 0, disponível 150.
8. Recusar cancelamento do pedido já expedido.
9. Preservar bolsa em 12 e boné em 5, sem reservas.
10. Reconciliar todos os saldos com o histórico e os pedidos.

Aceite demonstrativo: **10/10 verificações aprovadas, zero divergência e zero
baixa duplicada**. O JSON exportado informa versão, data/hora, cenário, resultados,
histórico e tentativas manuais. Registra expressamente que produção e aceite do
cliente não foram validados. As verificações automáticas referem-se ao último
roteiro executado; operações manuais posteriores aparecem separadamente no
relatório e precisam de conferência própria.

## Passagem para um piloto operacional

| Etapa | Evidência necessária | Responsável proposto |
| --- | --- | --- |
| Escolher o recorte | Estoque Vivo ou LiveBridge; objetivo e aprovador nominados | Coordenação do projeto + responsável da operação |
| Preparar dados | Marca autorizada, SKUs mapeados, saldo inicial assinado, fonte oficial definida | Responsável pelo estoque |
| Homologar backend | Ambiente separado, usuários distintos, permissões, eventos repetidos e fora de ordem, falha de rede, reconciliação e disputa pela última unidade | Equipe técnica |
| Validar notificações | Registro do evento e recebimento observado no aparelho; aceite do provedor sozinho é insuficiente | Equipe técnica + operador |
| Avaliar operação | Mesmo conjunto de tarefas antes/depois; tempo medido, divergências, pedidos aceitos e recusados | Operação + aprovador |
| Decidir produção | Escopo, aceite, janela, plano de retorno e condições comerciais formalizados | Aprovador do cliente e coordenação |

Os papéis acima são propostos. Nenhuma pessoa ou marca está confirmada por este
material. Não se define calendário comercial antes dessas confirmações.

Em homologação, a soma reservada não pode superar o físico. Duas solicitações
concorrentes para a última unidade devem resultar em somente uma reserva aceita.
O mesmo evento reenviado não pode criar nova baixa. Pedidos externos não
registrados no app ficam fora dessa garantia e precisam ser conciliados.

Interromper o piloto se houver saldo divergente, duplicidade ou falha de
autorização. Pausar somente a integração de teste, preservar logs sem segredos,
reconciliar pela fonte oficial e retomar apenas após revisão. Não testar sobre
estoque comercial nem recriar namespaces ou chaves de produção.

A redução de trabalho manual precisa ser medida, não presumida. Medir
tempo por tarefa em uma amostra fixa antes/depois e registrar o tamanho da
amostra. O piloto não promete vendas, receita, ausência de penalidades ou escala.

## LiveBridge: o que falta para escolher essa frente

Definir fonte de vídeo autorizada, um destino inicial e operador. Conferir acesso
efetivo da conta ao método de transmissão e as permissões aplicáveis antes de
agendar teste. Lives, stories, posts, catálogo, carrinho e pedidos têm escopos
distintos. Não há integração nativa comprovada por selecionar um destino na tela.

Critério futuro proposto: início e encerramento observados no destino autorizado,
áudio/vídeo verificados, latência medida contra limite acordado, interrupção
controlada e registro do resultado. A duração e os limites serão acordados após
conferir as contas. O presente laboratório não executa nenhum desses testes.

## Estado verificado e limites

Em 18/11/2026, a consulta somente de leitura a
`https://estoque.praia.digital/health` retornou HTTP 200 e versão 1.2.0.
O repositório possui fonte 1.3; isso não comprova deploy. Os PRs #162 (publicação
manual do Worker) e #163 (apresentação LiveBridge) permaneciam abertos como
rascunho na consulta desta data. O PR #163 informava conflito de integração.

Este pacote não publica o Worker, não muda autenticação, DNS, planos, chaves ou
integrações. Documentação pode ser consultada sem abrir uma sala comercial.
