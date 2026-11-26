# Confirmações ao solicitante — proposta, não ativada

Preparada em 17/11/2026 sobre main 7f659405449f30d9a5d91c1549efa54d021f845d.
Nenhuma publicação, integração, mensagem ou migração foi executada nesta revisão.

## Arquitetura e limites

O cadastro, o serviço e as duas entradas da outbox passam a ser gravados na mesma
transação D1.batch. O protocolo e o hash existentes são preservados. Depois do
commit, os consumidores de aviso comercial e confirmação funcionam separadamente.
Falhas na confirmação não desfazem o cadastro nem impedem o aviso comercial.

O binding EMAIL continua restrito a comercial@praia.digital. A confirmação usa
Resend Free, por HTTP, com chave restrita a envio e ao subdomínio confirmado.
O remetente proposto é solicitacoes@confirmacoes.praia.digital, com Reply-To
comercial@praia.digital. Não reutilizar credenciais do Gmail ou da Academy.

A chave de idempotência é service-receipt-v1/PROTOCOLO. O corpo é congelado no D1
antes da chamada: somente e-mail, protocolo e instruções genéricas, sem briefing,
nome, telefone ou empresa. O modo test aceita exclusivamente comercial@praia.digital.
O modo off é o padrão. Nunca incluir secrets nos metadados ou no repositório.

RECEIPTS_START_AT é obrigatório: data UTC ISO com milissegundos, definida no momento
da ativação aprovada. Não retroagir a 13/11 nem reenviar filas antigas. Consentimento,
limite por IP, honeypot e validações existentes continuam exigidos. A chave de
protocolo impede duplicação da mesma submissão; novos UUIDs representam novas
solicitações, mesmo que o conteúdo seja igual.

Reservas locais: 90 confirmações em 24 horas, 2.700 em 31 dias e três por destinatário
em 24 horas. Esses limites deixam margem em relação ao plano gratuito divulgado
(100/dia, 3.000/mês); exigem conta/projeto sem outros envios consumindo a mesma cota.
Reservas contam mesmo quando uma tentativa fica incerta. O custo zero depende de
manter o plano Free e não autorizar upgrades. Limite atingido mantém quota_hold e
preserva o cadastro. O cron existente tenta admitir pendências novamente.

## Estados e recuperação

- pending_setup: confirmação desativada ou fora do corte aprovado.
- queued: envio reservado; não significa entrega.
- sending: tentativa assumida atomicamente por um consumidor.
- accepted: provedor aceitou e retornou identificador; não prova recebimento.
- quota_hold: aguarda capacidade, sem perder o protocolo.
- review_required: timeout, falha, resposta incompleta, interrupção ou fila antiga.

Não há reenvio automático após erro do provedor, inclusive 429/5xx: a aceitação pode
ter ocorrido antes da falha. Consultar o provedor e os registros antes de autorizar
qualquer reenvio. A chave do Resend vale por 24 horas; não prometer exatamente uma
entrega após essa janela. Trabalhos em sending há mais de dois minutos ou queued
há 23 horas exigem revisão. Não trocar o corpo/chave para tentar contornar erros.

Consultas administrativas de acompanhamento (somente contagens, sem contatos):

```sql
SELECT kind,status,count(*) AS total FROM notification_outbox GROUP BY kind,status;
SELECT status,error_code,count(*) AS total FROM receipt_delivery GROUP BY status,error_code;
```

Os registros privados da nova tabela contêm o destinatário; a exclusão de um lead
deve continuar seguindo o procedimento administrativo, removendo referências da
outbox/CRM. receipt_delivery tem exclusão em cascata. Não fazer exclusão automática
de histórico nesta implantação. Não publicar respostas ou logs com contatos.

## Piloto a aprovar

1. Publicar branch e PR em rascunho; sem merge ou produção. Executar o CI novo,
   incluindo navegador. O CI antigo não valida estas mudanças.
2. Preparar Resend Free sem cobrança e validar o subdomínio confirmacoes.praia.digital
   com os registros DKIM/SPF/retorno gerados pelo provedor. Não alterar MX do domínio
   principal nem o envio comercial atual. Se exigir plano pago, interromper.
3. Criar D1 e Worker de homologação separados: schema.sql, notification-migration.sql,
   crm-migration.sql e receipt-migration.sql. Não copiar dados reais nem sessões.
   Publicar worker.mjs, notifications.mjs, receipts.mjs, crm.mjs e crm-ui.mjs juntos.
   Preservar no template o rate limiter e o binding EMAIL restrito ao comercial;
   criar recursos de teste isolados e não apontar homologação ao banco de produção.
4. Guardar RESEND_API_KEY como secret. Definir RECEIPTS_MODE=test e
   RECEIPTS_START_AT no início do piloto. Não criar ou alterar cron em produção.
5. Submeter um cadastro fictício identificado TESTE INTERNO, com consentimento e
   e-mail comercial@praia.digital; repetir o mesmo submission_id para verificar
   deduplicação. Destino único: comercial@praia.digital. Esperado: exatamente dois
   e-mails, um aviso à equipe e uma confirmação. Sem CC/BCC ou destinatários externos.
   Testes de falha continuam simulados; nenhum cliente real será utilizado.
6. Conferir os dois recebimentos no Gmail e autenticação do domínio. Aceitação na
   API, sozinha, não aprova entrega. Revisar layout desktop/mobile; iPhone real
   permanece uma validação distinta. Retornar com evidências antes da produção.

## Produção: aprovação posterior

Somente depois do piloto e de nova autorização: revisar diferenças entre main e
patch; aplicar migração aditiva no D1 correto; publicar todos os módulos inicialmente
com modo off; preservar cron */5 * * * *, CRM e binding comercial; publicar aviso de
privacidade e interfaces; ativar modo live com corte futuro. Confirmar Free e saldo
de cota antes disso. Nunca usar o Worker de homologação no formulário público.
Desativação rápida: RECEIPTS_MODE=off; preservar filas e protocolos para revisão.

## Testes

node --test workers/livebridge-leads/*.test.mjs
python3 -m unittest discover -s tests -p test_ia_services.py
NODE_PATH=<dependências> node tests/ia-services-browser.cjs

Os testes Node usam SQLite local e provedores simulados. Os testes de navegador
interceptam requisições. Não usar endereços example.invalid em testes reais.
Não confundir mensagens históricas de 13/11 com entregas desta proposta.

## Documentação oficial consultada

- https://resend.com/pricing
- https://resend.com/docs/dashboard/emails/idempotency-keys
- https://resend.com/docs/api-reference/emails/send-email
- https://developers.cloudflare.com/email-service/
- https://developers.cloudflare.com/d1/worker-api/d1-database/
