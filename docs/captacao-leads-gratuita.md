# Captação de contato sem nova assinatura

## Escopo

`contato.html` e `imoveis.html` passam a enviar solicitações ao endpoint AJAX do FormSubmit já utilizado no site, para comercial@praia.digital. Nome, e-mail, interesse, telefone opcional, mensagem opcional, caminho da página e registro da autorização de contato são enviados. Não há cadastro em newsletter, automação de campanhas ou gravação de dados pessoais no repositório, analytics, query string ou armazenamento local.

`interesse.html` continua oferecendo WhatsApp com revisão da mensagem pelo visitante. Retirado o POST silencioso paralelo; há link para o formulário por e-mail. O coletor Python por imagem de `js/main.js` foi removido: GitHub Pages não executa Python e aquele mecanismo expunha dados na URL.

## Custo e dependências

Reutiliza FormSubmit (documentação oficial https://formsubmit.co/, consultada em 12/11/2026: serviço gratuito, sem registro). Não cria conta, não usa plano pago, banco de dados ou API de marketing. Depende da disponibilidade, filtros antispam e ativação do destinatário no provedor. Não promete gratuidade futura nem entrega garantida. Há evidência histórica de recebimento no Gmail comercial, mas isso não substitui um teste atual destas páginas.

O rascunho Apps Script existente em `docs/sales/apps-script-leads/Code.gs` não foi implantado; não há alegação de que os novos contatos estejam sendo gravados em planilha. Brevo e Resend não foram configurados.

## Proteções e comportamento

- Autorização de contato desmarcada e obrigatória; política e processamento FormSubmit explicados junto ao envio.
- Não solicitar documentos, informações bancárias ou sensíveis.
- Validação nativa, limites de tamanho, campo-isca antispam básico.
- Bloqueio de clique repetido enquanto envia e após resposta positiva.
- Timeout de 15 s, preservação dos dados em erro e nenhum retry automático.
- Só resposta HTTP bem-sucedida com `success: true` ou `"true"` gera confirmação de aceitação pelo serviço, nunca promessa de chegada ao Gmail.
- Links manuais de WhatsApp/e-mail se houver erro ou JavaScript indisponível. Botão de envio inicialmente desabilitado para não vazar dados por GET sem JavaScript.
- Campo-isca não substitui controles de abuso do provedor; não é um backend próprio com deduplicação garantida.

## Validação

- `node --check js/lead-capture.js`
- `node tests/lead-capture-unit.cjs`: 11 cenários simulados (sucesso boolean/string; false/string; resposta ausente; HTTP; JSON inválido; rede; timeout; inválido; campo-isca; nome vazio), inclui clique concorrente e ausência de query privada.
- `python -m unittest discover -s tests -p test_services_hub.py`: 5 testes.
- `node tests/lead-capture-browser.cjs`: teste preparado, 390/1280 px, contato/imóveis; todas as requisições externas interceptadas. **Não executado com sucesso neste ambiente**: Chromium aborta por `socket() failed: Operation not permitted`, inclusive na tentativa autorizada fora do sandbox.

Antes de liberar: executar o teste de navegador em CI e validar um envio fictício autorizado por página, conferindo a chegada à caixa comercial (inclusive Spam) e eventual pedido de ativação. Nenhum envio real foi feito nesta implementação. Confirmar deploy e disponibilização no site após merge. Não coletar leads em arquivos públicos do GitHub.

## Revisão de transparência (12/11/2026)

Aviso específico adicionado à política, com dados, finalidade, FormSubmit, caixa Google, canal comercial para solicitações e distinção do WhatsApp. Fontes oficiais: https://formsubmit.co/ e https://formsubmit.co/privacy.pdf (effective date 17/01/2019, consultadas 12/11/2026). Não inferimos prazo de retenção, localização de processamento ou SLA de exclusão a partir dessas fontes. A ausência de expurgo automático corresponde à implementação; não é uma política de conservação aprovada.

**Gate organizacional antes da publicação:** responsável pelo site deve definir identidade do controlador e política operacional de retenção/atendimento a direitos, incluindo tratamento de cópias e fornecedores. A página não inventa CNPJ, encarregado, prazo ou garantia LGPD. Esta revisão documental não equivale a auditoria jurídica e não resolve sozinha esse gate.
