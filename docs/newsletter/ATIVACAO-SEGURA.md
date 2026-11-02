# Newsletter: ativação segura do piloto

Estado em 2026-11-02: **não ativada**. O RSS é a alternativa pública; não captar endereços nem simular confirmação enquanto os critérios abaixo estiverem pendentes.

## Estado operacional

Não existe endpoint de inscrição verificado neste piloto. Arquivos estáticos no GitHub Pages não executam um serviço de inscrição. O formulário público permanece desativado até a validação da infraestrutura, das permissões e dos critérios abaixo. Integrações comerciais existentes não devem ser reutilizadas como lista de assinantes.

## Caminho de menor custo adicional, ainda condicionado

Apps Script dedicado + planilha privada dedicada + MailApp na conta já existente. Não criar outra conta, contratar fornecedor, usar Consumer nem modificar Academy. A disponibilidade do Apps Script nessa conta e a permissão do administrador para aplicações públicas precisam ser verificadas após autenticação. Não há endpoint implantado validado neste momento.

**Ações/autorização específicas necessárias:**

1. Autenticar a conta correta no Apps Script, sem compartilhar senha no chat.
2. Autorizar criação de um projeto exclusivo e de uma planilha privada de inscritos. Não dar acesso público à planilha, nem colocar inscritos em planilhas de leads antigas.
3. Revisar e autorizar os escopos efetivamente pedidos pelo novo script: envio `https://www.googleapis.com/auth/script.send_mail` e acesso à planilha necessário à implementação. Não conceder leitura da caixa Gmail. Não prometer que um escopo de planilhas seja limitado a um único arquivo: conferir a tela real e preferir o menor escopo tecnicamente compatível.
4. Autorizar implantação pública do web app executando como proprietário, após revisão de segurança. Isso permite invocar o programa, não ler diretamente a planilha; ainda assim é uma superfície pública que deve ser explicitamente aprovada.
5. Autorizar testes transacionais em caixas controladas e a publicação do link somente após resultados reais. Sem disparos em massa, importação de contatos ou gatilho recorrente nesta etapa.

Não ligar o formulário antes desses passos. Se exigir permissões mais amplas, novo serviço, chave ou faturamento, parar e pedir aprovação específica.

## Contrato funcional e privacidade

Preferir página hospedada no próprio web app para inscrição/confirmar/cancelar, com retorno visível do servidor. Não usar `fetch(mode: 'no-cors')` como evidência de sucesso.

- Captar somente email e consentimento explícito não pré-marcado, com finalidade e frequência. Guardar versão do texto de consentimento, origem e datas.
- Validar tipo, tamanho, conteúdo e consentimento no servidor; rejeitar CR/LF, fórmulas de planilha, HTML e cargas excessivas. Não inferir autorização de newsletter de um lead comercial.
- Estado `pending` primeiro; resposta de envio não significa inscrição ativa. Depois de gravar com sucesso e o serviço aceitar o email: “Confira sua caixa de entrada para confirmar; a inscrição ainda não está ativa.” Aceitação não garante entrega.
- Token imprevisível de pelo menos 256 bits obtido de fonte criptográfica revisada; guardar somente hash. Nunca usar `Math.random()` nem presumir que UUID seja segredo criptográfico. Tokens distintos para confirmação/cancelamento, sem email no URL.
- Expiração de confirmação em 24 horas; uso único. GET mostra a página, sem ativar inscrição automaticamente por scanners de links; POST explícito confirma. Cancelamento simples, sem login, disponível em todas as edições.
- Confirmação, cancelamento e qualquer envio usam bloqueio/transação; cancelamento vence corrida com envio. Reinscrição exige novo consentimento e nova confirmação; nunca reativar ao receber formulário repetido.
- Resposta genérica a duplicados evita enumeração de inscritos. Falha de armazenamento/envio/quota jamais retorna “inscrito”. Falha de envio mantém pendente sem elegibilidade para boletim.
- Não registrar emails/tokens em logs, analytics, parâmetros públicos, Actions, issues, commits ou arquivos gerados. Não exportar planilha. Remover rastreadores da página de tokens; usar política de referência restritiva quando suportada.
- Proposta de retenção a aprovar: apagar pendentes vencidos em até 7 dias; cancelar envio imediatamente e eliminar email operacional em até 30 dias. Evidência mínima de consentimento/supressão tem prazo e finalidade a definir antes de abrir coleta. Limpeza manual verificada no piloto; não prometer limpeza automática sem execução programada autorizada.

## Contenção de abuso e custo

Limites propostos do piloto, não quotas do Google: 25 inscritos ativos, 10 confirmações por 24 horas, uma confirmação por endereço a cada 24 horas, no máximo 40 destinatários totais por janela móvel de 24 horas. Reservar pelo menos 10 destinatários da quota restante para outras atividades. Os números devem ser aplicados atomicamente no servidor; não contar só no navegador.

Antes de cada envio, consultar `MailApp.getRemainingDailyQuota()`. Se não houver margem, recusar sem envio e mostrar indisponibilidade temporária. Não enfileirar tentativas indefinidamente nem reexecutar envios de resultado incerto. Um envio por destinatário; nunca expor a lista em CC/To.

O evento Apps Script documentado não fornece IP confiável: não fingir rate limit por IP nem confiar em IP enviado pelo formulário. Honeypot/cooldown não são proteção suficiente contra abuso distribuído. Começar com piloto fechado por convite/allowlist, consentimento real e tokens de convite; abrir coleta pública somente após proteção antiabuso validada e autorizada. O endpoint público de cancelamento permanece funcional. Um teto global limita danos, mas não impede esgotamento malicioso da quota.

Custo fixo **adicional proposto: R$ 0**, condicionado ao uso dos recursos já incluídos na conta existente, sem upgrade, Cloud Billing ou fornecedor novo. Não significa Workspace gratuito nem garantia de disponibilidade/entrega. Parar na quota; não habilitar cobrança ou escalar automaticamente.

## Critérios de aceite antes da publicação

1. Conta, remetente, propriedade e compartilhamento privado da planilha verificados; acesso anônimo à planilha negado.
2. Convite de teste válido + consentimento cria exatamente uma linha pendente e um email de confirmação, sem boletim.
3. Ausência de consentimento, email inválido, fórmula, CR/LF, payload grande, honeypot, convite inválido e duplicado não geram envios indevidos.
4. GET de confirmação não ativa; POST válido ativa uma vez. Token alterado, expirado, reutilizado ou de outra finalidade não ativa.
5. Cancelamento funciona sem login, é idempotente e exclui o destinatário de qualquer lote. Reinscrição exige confirmação nova.
6. Solicitações simultâneas respeitam limites por endereço e global; quota baixa, exceção de MailApp e falha de planilha não produzem falso sucesso.
7. Email recebido em caixa controlada tem remetente correto, links funcionais e cancelamento; nenhum endereço aparece em repositório, feed, logs ou analytics.
8. Testar expiração/limpeza com relógio controlado em teste, não esperar sete dias; verificar processo operacional de limpeza antes de captar dados reais.
9. Até aprovação de disparos, nenhum gatilho agendado, campanha ou envio a contatos comerciais existentes. Depois, envio por edição exige idempotência por destinatário/edição e checagem final de status.

## Referências oficiais consultadas em 2026-11-02

- [Quotas Apps Script](https://developers.google.com/apps-script/guides/services/quotas): 100 destinatários/dia em contas consumer e 1.500 em Workspace; quotas por usuário, reinício 24h após a primeira solicitação, sujeitas a alterações e restrições de avaliação. Limite de execução: 6 minutos; 30 execuções simultâneas por usuário. O plano efetivo desta conta não foi comprovado; usar quota runtime, não assumir 1.500.
- [MailApp](https://developers.google.com/apps-script/reference/mail/mail-app): serviço de envio sem leitura da caixa; `getRemainingDailyQuota()` informa destinatários restantes. A autorização de envio é distinta da conexão Gmail do assistente.
- [Web apps](https://developers.google.com/apps-script/guides/web): publicação pelo menu Deploy, execução como proprietário ou visitante e objeto de evento documentado. Implantação exige autorização; código local não é serviço publicado.
