/**
 * Praia Digital — Captura de Leads (Google Apps Script Web App)
 *
 * COMO IMPLANTAR (manual, ~5 min):
 * 1. Em script.google.com, crie um projeto e cole este arquivo (Code.gs).
 * 2. Projeto > Configurações > Propriedades do script: adicione
 *      SHEET_ID = 1sv7zfFhbjoUgVhgZPBXVCK-vUwoP8tGNdwkjL0eo02w
 *      NOTIFY_EMAIL = comercial@praia.digital   (opcional)
 * 3. Implantar > Nova implantação > Tipo: App da Web
 *      Executar como: Eu  |  Acesso: Qualquer pessoa
 * 4. Copie a URL /exec e informe para preencher:
 *      - SHEETS_ENDPOINT em anunciar-temporada.html
 *      - LEADS_ENDPOINT em interesse.html (opcional, substitui o FormSubmit)
 *
 * ROTAS POR ORIGEM:
 *  a) origem='anunciar-temporada.html' -> aba 'Temporada' (ficha completa de cadastro)
 *     campos: nome, documento, telefone, email, vinculo, tipo, cidade, bairro,
 *     endereco, quartos, hospedes, diaria, temporada_ano, descricao,
 *     link_anuncio, comprovante
 *  b) demais origens -> aba 'Leads' (form-encoded ou JSON)
 *     campos: nome, telefone, cidade, produto, pagamento, origem | JSON: name, email, phone, city, source, magnet
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

  var sheetId = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  var email = PropertiesService.getScriptProperties().getProperty('NOTIFY_EMAIL');
  var origem = p.origem || d.source || '';

  if (origem === 'anunciar-temporada.html') {
    var t = {
      data: new Date(),
      nome: p.nome || '',
      documento: p.documento || '',
      telefone: p.telefone || '',
      emailLead: p.email || '',
      vinculo: p.vinculo || '',
      tipo: p.tipo || '',
      cidade: p.cidade || '',
      bairro: p.bairro || '',
      endereco: p.endereco || '',
      quartos: p.quartos || '',
      hospedes: p.hospedes || '',
      diaria: p.diaria || '',
      temporadaAno: p.temporada_ano || '',
      descricao: p.descricao || '',
      linkAnuncio: p.link_anuncio || '',
      comprovante: p.comprovante || ''
    };
    if (sheetId) {
      var ss = SpreadsheetApp.openById(sheetId);
      var sh = ss.getSheetByName('Temporada') || ss.insertSheet('Temporada');
      if (sh.getLastRow() === 0) {
        sh.appendRow(['Data','Nome','CPF/CNPJ','WhatsApp','E-mail','Vínculo','Tipo','Cidade','Bairro','Endereço','Quartos','Hóspedes','Diária','Ano todo?','Descrição','Link anúncio','Comprovante','Status validação']);
      }
      sh.appendRow([t.data, t.nome, t.documento, t.telefone, t.emailLead, t.vinculo, t.tipo, t.cidade, t.bairro, t.endereco, t.quartos, t.hospedes, t.diaria, t.temporadaAno, t.descricao, t.linkAnuncio, t.comprovante, 'Pendente']);
    }
    if (email && t.nome) {
      MailApp.sendEmail(email,
        'Novo cadastro de temporada — ' + t.nome + ' (' + t.cidade + ')',
        'Nome: ' + t.nome + '\nCPF/CNPJ: ' + t.documento + '\nWhatsApp: ' + t.telefone + '\nE-mail: ' + t.emailLead +
        '\nVínculo: ' + t.vinculo + '\n\nImóvel: ' + t.tipo + ' em ' + t.bairro + ', ' + t.cidade +
        '\nEndereço: ' + t.endereco + '\nQuartos: ' + t.quartos + ' · Hóspedes: ' + t.hospedes + ' · Diária: R$ ' + t.diaria +
        '\nAno todo: ' + t.temporadaAno + '\nDescrição: ' + t.descricao +
        '\n\nLink anúncio: ' + t.linkAnuncio + '\nComprovante: ' + t.comprovante +
        '\n\n-> Validar na aba Temporada da planilha.');
    }
  } else {
    var lead = {
      data:      new Date(),
      nome:      p.nome      || d.name    || '',
      emailLead: p.email     || d.email   || '',
      telefone:  p.telefone  || d.phone   || '',
      cidade:    p.cidade    || d.city    || '',
      produto:   p.produto   || '',
      pagamento: p.pagamento || '',
      origem:    origem,
      magnet:    p.magnet    || d.magnet  || ''
    };
    if (sheetId) {
      var ss2 = SpreadsheetApp.openById(sheetId);
      var sh2 = ss2.getSheetByName('Leads') || ss2.insertSheet('Leads');
      if (sh2.getLastRow() === 0) {
        sh2.appendRow(['Data','Nome','E-mail','Telefone','Cidade','Produto','Pagamento','Origem','Lead magnet']);
      }
      sh2.appendRow([lead.data, lead.nome, lead.emailLead, lead.telefone, lead.cidade,
                     lead.produto, lead.pagamento, lead.origem, lead.magnet]);
    }
    if (email && lead.nome) {
      MailApp.sendEmail(email,
        'Novo lead praia.digital — ' + lead.nome,
        'Nome: ' + lead.nome + '\nE-mail: ' + lead.emailLead + '\nTelefone: ' + lead.telefone +
        '\nCidade: ' + lead.cidade + '\nProduto: ' + lead.produto + '\nPagamento: ' + lead.pagamento +
        '\nOrigem: ' + lead.origem + '\nMagnet: ' + lead.magnet);
    }
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
