/**
 * Praia Digital — Captura de Leads (Google Apps Script Web App)
 *
 * COMO IMPLANTAR (manual, ~5 min):
 * 1. Crie uma planilha Google chamada "Praia Digital — Leads" e copie o ID da URL.
 * 2. Em script.google.com, crie um projeto e cole este arquivo (Code.gs).
 * 3. Projeto > Configurações > Propriedades do script: adicione
 *      SHEET_ID = <id da planilha>
 *      NOTIFY_EMAIL = comercial@praia.digital   (opcional)
 * 4. Implantar > Nova implantação > Tipo: App da Web
 *      Executar como: Eu  |  Acesso: Qualquer pessoa
 * 5. Copie a URL /exec e informe para preencher:
 *      - LEADS_ENDPOINT em interesse.html
 *      - endpoint dos formulários das páginas de bairros (hoje apontam para
 *        https://academy.praia.digital/leads — domínio fora do ar)
 *
 * Aceita DOIS formatos:
 *  a) form-encoded (URLSearchParams, mode no-cors) — usado por interesse.html
 *     campos: nome, telefone, cidade, produto, pagamento, origem
 *  b) JSON (Content-Type text/plain ou application/json) — páginas de bairros
 *     campos: name, email, phone, city, source, magnet
 */

function doPost(e) {
  var d = {};
  try {
    if (e && e.postData && e.postData.contents) {
      var body = e.postData.contents;
      if (body && body.trim().charAt(0) === '{') {
        d = JSON.parse(body);
      }
    }
  } catch (err) {}
  var p = (e && e.parameter) || {};

  var lead = {
    data:      new Date(),
    nome:      p.nome      || d.name    || '',
    email:     p.email     || d.email   || '',
    telefone:  p.telefone  || d.phone   || '',
    cidade:    p.cidade    || d.city    || '',
    produto:   p.produto   || '',
    pagamento: p.pagamento || '',
    origem:    p.origem    || d.source  || '',
    magnet:    p.magnet    || d.magnet  || ''
  };

  var sheetId = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  if (sheetId) {
    var ss = SpreadsheetApp.openById(sheetId);
    var sh = ss.getSheetByName('Leads') || ss.insertSheet('Leads');
    if (sh.getLastRow() === 0) {
      sh.appendRow(['Data','Nome','E-mail','Telefone','Cidade','Produto','Pagamento','Origem','Lead magnet']);
    }
    sh.appendRow([lead.data, lead.nome, lead.email, lead.telefone, lead.cidade,
                  lead.produto, lead.pagamento, lead.origem, lead.magnet]);
  }

  var email = PropertiesService.getScriptProperties().getProperty('NOTIFY_EMAIL');
  if (email && lead.nome) {
    MailApp.sendEmail(email,
      'Novo lead praia.digital — ' + lead.nome,
      'Nome: ' + lead.nome + '\nE-mail: ' + lead.email + '\nTelefone: ' + lead.telefone +
      '\nCidade: ' + lead.cidade + '\nProduto: ' + lead.produto + '\nPagamento: ' + lead.pagamento +
      '\nOrigem: ' + lead.origem + '\nMagnet: ' + lead.magnet);
  }

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', service: 'praia-digital-leads' }))
    .setMimeType(ContentService.MimeType.JSON);
}
