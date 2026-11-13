# CRM Praia Digital — versão inicial

URL: https://crm.praia.digital/crm/

Área comercial privada no Worker existente, com D1. Não cria assinatura de plataforma. O uso segue os limites da conta Cloudflare existente.

## Operação

- Solicitar código pelo painel; enviado somente à caixa comercial configurada no Worker. Código de uso único, expira em 15 minutos; sessão de até 8 horas. Não compartilhar códigos.
- Formulários atendidos pelo endpoint `/leads` entram automaticamente pelo trigger de `service_requests`. Cadastros históricos são incorporados pela migração. Testes marcados `teste_tecnico` são excluídos no momento da captura/migração.
- Um cliente por e-mail normalizado. Cada solicitação é uma negociação independente. E-mails externos, WhatsApp e reuniões podem ser cadastrados manualmente.
- Etapas: novo, contato, proposta, negociação, ganho, perdido. Execução/entrega e recebimentos exigem negócio ganho.
- Valores em centavos. Valor proposto/contratado, recebido acumulado e saldo separados. Lançamentos manuais: sem cobrança, conciliação bancária ou integração Stripe.
- Histórico de alterações de negociações e notas, responsável, prazo e próximo contato; busca, arquivamento e exportação CSV dos registros filtrados.
- Arquivar remove dos indicadores, mas preserva o histórico. CSV contém dados pessoais e deve ser guardado privadamente.
- Aviso de e-mail “aceito” significa aceitação pelo provedor, não comprovação individual de chegada à caixa.

## Limites explícitos

Não importa automaticamente toda a caixa Gmail, não envia respostas comerciais, não sincroniza pedidos dos marketplaces e não confirma pagamento por conta própria. Não é sistema fiscal ou contábil. Acesso inicial único pela caixa comercial; sem permissões por funcionário. Listagem carregada integralmente nesta primeira versão, a paginar antes de grande volume. Atualizar painel para buscar novas entradas. Não há exclusão definitiva pela interface.

## Implementação e manutenção

1. Aplicar `schema.sql` e depois `crm-migration.sql` na base existente. A migração é aditiva e repetível; preservar dados existentes.
2. Editar `crm.html`, `crm.css`, `crm.js` e rodar `python build-crm.py` para gerar `crm-ui.mjs`.
3. Rodar `node --test worker.test.mjs crm.test.mjs` (Node com SQLite nativo).
4. Publicar módulos `worker.mjs`, `notifications.mjs`, `crm.mjs`, `crm-ui.mjs`, preservando bindings, cron e observabilidade de `deploy-metadata.json`.
5. Domínio personalizado `crm.praia.digital` aponta ao mesmo Worker. Apex e MX Google não são alterados.

Tokens e sessões guardados como hashes; cookie HttpOnly/Secure/SameSite Strict; APIs exigem sessão e mutações exigem Origin exata e JSON. Dados não são incluídos nos arquivos públicos. Consultas parametrizadas, tamanho de entrada limitado, controle de versão nos updates e CSP restritiva. Referência: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

## Validação da entrega

18 testes locais aprovados: regressão dos formulários/notificações, autenticação, código de uso único/expiração, CSRF, deduplicação, pagamentos, histórico, conflito de edição e migração. Tela de acesso publicada revisada em navegador desktop; envio de código recebido na caixa comercial. Contagens da migração verificadas sem exportar contatos. Navegação autenticada em produção e aparelho móvel físico ainda não verificados nesta entrega. Nenhum código de acesso, identificador de mensagem ou dado de cliente deve ser incluído no repositório.
