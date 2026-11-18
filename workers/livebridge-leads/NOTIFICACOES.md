# Avisos à equipe — ativos em 13/11/2026

Destino único verificado: comercial@praia.digital. Remetente: solicitacoes@avisos.praia.digital. MX principal preservado no Google.

Binding EMAIL restrito ao comercial, EMAIL_NOTIFICATIONS_ENABLED=true. Publicação inclui worker.mjs e notifications.mjs. Cron separado: */5 * * * *. O formulário processa seu aviso após gravação, e o Cron alcança pendências. Dez testes offline aprovados e teste real de formulário recebido na INBOX comercial. Identificadores de entrega ficam nos sistemas privados.

Os avisos incluem serviço, contato, descrição e protocolo. Reply-To aponta ao solicitante. Não há envio de cotação automática nem confirmação por e-mail ao visitante: receipt permanece pending_setup.

Outbox team: pending_setup/queued → sending → accepted. Accepted não comprova caixa de entrada. Falha ambígua → review_required. Inspecionar review_required e sending antes de reenviar para evitar duplicação. Não prometer entrega garantida. Teste técnico identificado no banco, sem remoção do histórico. Registros anteriores sem serviço são do formulário original LiveBridge AI e foram preparados para processamento periódico.
