/**
 * Praia Digital — Captura de Leads do Formulário de Interesse
 * Planilha: https://docs.google.com/spreadsheets/d/1sv7zfFhbjoUgVhgZPBXVCK-vUwoP8tGNdwkjL0eo02w
 *
 * COMO ATIVAR (2 minutos, uma vez só):
 * 1. Abra a planilha acima → menu Extensões → Apps Script
 * 2. Cole este código e salve
 * 3. Implantar → Nova implantação → tipo: App da Web
 *    - Executar como: Eu (comercial@praia.digital)
 *    - Quem tem acesso: Qualquer pessoa
 * 4. Copie a URL do web app (termina em /exec)
 * 5. No arquivo interesse.html, substitua LEADS_ENDPOINT pela URL copiada e faça commit
 */
const SHEET_ID = '1sv7zfFhbjoUgVhgZPBXVCK-vUwoP8tGNdwkjL0eo02w';

function doPost(e) {
  const p = e.parameter || {};
  const ss = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
  ss.appendRow([
    new Date().toLocaleString('pt-BR', {timeZone: 'America/Sao_Paulo'}),
    p.nome || '', p.telefone || '', p.cidade || '',
    p.produto || '', p.pagamento || '', p.origem || 'interesse.html',
    'pendente', '', 'não'
  ]);
  return ContentService.createTextOutput(JSON.stringify({ok: true}))
    .setMimeType(ContentService.MimeType.JSON);
}
