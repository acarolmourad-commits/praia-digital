# Captação LiveBridge AI

Formulário público em `https://praia.digital/ia/marketplaces/#cadastro`.
Endpoint: `https://praia-livebridge-leads.kleber-f63.workers.dev/leads`.

## Atendimento e acesso aos cadastros

Na conta Cloudflare da Praia Digital, abra **Storage & databases → D1 → praia-livebridge-leads → Explore → leads**. O acesso exige login administrativo na Cloudflare. Cada linha contém contato, empresa, canais, objetivo, data, origem/campanha, autorização de contato e status inicial `novo`. Não há consulta pública nem chave administrativa no frontend.

Para acompanhar os mais recentes no console autenticado:

```sql
SELECT created_at, name, email, phone, business, live_source, marketplaces,
       destinations, goal, status, id
FROM leads ORDER BY created_at DESC LIMIT 100;
```

A equipe pode atualizar `status` para `em_contato` ou `concluido` no painel. Atender solicitações de consulta/correção/exclusão recebidas em comercial@praia.digital após verificar a identidade do solicitante. Não exportar dados reais para este repositório público. Caso exporte CSV, tratar células como texto para evitar execução de fórmulas em planilhas.

O formulário **salva o lead**, sem enviar e-mail, mensagem no WhatsApp ou newsletter automaticamente. O acompanhamento é feito pela equipe na base privada. O cadastro não representa contratação nem disponibilização do produto.

## Implementação

Worker `praia-livebridge-leads`, D1 `praia-livebridge-leads`, tabela `leads`. `schema.sql` é idempotente. O frontend só mostra sucesso após confirmação de gravação no servidor. O UUID da tentativa é reaproveitado em repetição sem alteração do conteúdo; a chave primária impede duplicação. Falhas de rede preservam campos e não mostram confirmação falsa.

Validação no servidor, consultas parametrizadas, corpo limitado a 12 KB, honeypot, origem restrita e rate limiter de 5 tentativas/minuto por IP por localização Cloudflare (limite aproximado, não um CAPTCHA). O IP não é salvo na tabela de leads. Logs da aplicação registram somente código genérico de erro. Não existe endpoint de listagem. A única resposta de sucesso contém `ok` e protocolo.

## Publicação e validação

Frontend publicado pelo fluxo GitHub Pages existente. Backend publicado pela API oficial Cloudflare, com `worker.mjs` e `deploy-metadata.json` em multipart; identificadores no metadata não são credenciais. Habilitar workers.dev apenas para este Worker. Não modificar os Workers de Academy. Nenhuma assinatura paga é necessária para o fluxo dentro das cotas disponíveis; não alterar plano automaticamente.

Execute `node --test workers/livebridge-leads/worker.test.mjs` com Node 24 para testar gravação SQLite, repetição, validação, restrições de acesso e falha de armazenamento. A CI executa os mesmos testes. Após alterações, confirme um envio com dados sintéticos `@example.invalid` na página publicada, confira a linha via D1 autenticado e remova somente os registros de teste identificados. Nunca registrar dados reais de clientes nos testes.

Limitação: os testes de Node usam SQLite local e adaptador D1; o envio publicado precisa ser conferido separadamente. Monitorar os limites do plano e os erros do Worker. Em caso de limite ou indisponibilidade, o site informa que o envio não foi confirmado e oferece nova tentativa ou contato por e-mail.
