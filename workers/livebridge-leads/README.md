# Solicitações de serviços de IA

Formulário central: https://praia.digital/solicitar-servico.html
Formulário de Marketplaces: https://praia.digital/ia/marketplaces/#cadastro
Destino comercial previsto: comercial@praia.digital.

## Estado real — 13/11/2026
Captura ativa em D1. Serviço escolhido em service_requests. Dois avisos por lead em notification_outbox (team, receipt), chave composta evita duplicação. Status pending_setup. NÃO há envio automático nem consumidor da fila implantado. Nenhum aviso é apresentado como enviado. Cloudflare Email Sending indisponível para a conta consultada; nenhum destinatário Routing verificado. Não alterar MX do Google Workspace para ativar Routing. Não contratar plano pago automaticamente.

## Fluxo comercial
Cadastro confirmado por protocolo → equipe consulta base privada → contato para entender necessidade → escopo e proposta → aprovação antes da execução. Não há contratação automática.

## Ativação pendente
Conectar transporte transacional autorizado (por exemplo Gmail OAuth para servidor, com credenciais em secrets), testar aviso à equipe e confirmação ao solicitante com endereços controlados, implementar consumidor com estados de envio, erro, retomada e deduplicação. O conector Gmail do chat não fornece credenciais ao Worker. Só ativar rotina após teste de entrega real. Tratar timeout após envio como resultado incerto; não repetir cegamente. Preservar registros antigos. Nunca exportar contatos para este repositório.

Aplicar notification-migration.sql antes do Worker. Os avisos antigos ficam pendentes, sem leitura ou exportação de dados pessoais. A fila não garante entrega enquanto não houver consumidor e transporte configurados.

Validação: node --test workers/livebridge-leads/worker.test.mjs (7 testes). Não confundir testes offline com envio real.
