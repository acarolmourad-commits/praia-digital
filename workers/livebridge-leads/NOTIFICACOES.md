# Avisos à equipe — preparação de 13/11/2026

Destino único comercial@praia.digital; remetente solicitacoes@avisos.praia.digital. Subdomínio Email Routing configurado. MX principal praia.digital continua smtp.google.com. E-mail de verificação solicitado ao destinatário; falta confirmação.

Worker contém consumidor imediato após gravação e scheduled para fila pendente. Ativação protegida por EMAIL_NOTIFICATIONS_ENABLED=true e binding EMAIL. Não ativar antes da verificação do destinatário e teste real controlado. O recebimento no Gmail ainda não foi validado. Dez testes offline aprovados.

Binding de ativação: type send_email, name EMAIL, destination_address comercial@praia.digital. Não adicionar destinos arbitrários, não alterar plano pago nem MX principal. Cron recomendado */5 * * * * apenas após validação de entrega. Preservar D1 e rate limiter atuais.

Outbox team: pending_setup/queued -> sending -> accepted (aceito pelo provedor, não prova caixa de entrada). Falha ambígua -> review_required para não duplicar automaticamente. Se processo interromper em sending, revisar antes de reencaminhar. Monitorar review_required e sending; não prometer entrega garantida. Confirmação para visitante (receipt) permanece pending_setup e fora desta ativação.

Antes de ativar, completar service_requests ausentes com LiveBridge AI apenas para inscrições históricas do formulário original, e testar com dados fictícios e destinatário comercial real controlado. Não exportar dados reais. Após teste, conferir Gmail pelo protocolo exato e registrar confirmação da entrega. Mensagens incluem contatos/demanda apenas para a própria Praia Digital.
