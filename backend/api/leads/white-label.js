const fs = require('fs');
const path = require('path');
const FILE = path.join(__dirname, '../../../docs/sales/csv-lotes-b2b/lote-b2b-planos-geral-2026-07-21.csv');
const headers = 'Lote;Nome;Telefone;Cidade;Data_Msg1;Status;Resposta;Valor_Estimado;Obs;Acao_Conversao;Msg1;Msg2;Msg3;Email;Imobiliaria';
function now(){ return new Date().toISOString().replace('T',' ').slice(0,19); }
function sanitize(s){ return (s||'').replace(/;/g,',').replace(/\n/g,' ').trim(); }
function ensureFile(){
  if (!fs.existsSync(FILE)) fs.mkdirSync(path.dirname(FILE), {recursive:true}); fs.writeFileSync(FILE, headers + '\n', 'utf8');
}
module.exports = async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.status(204).end(); return; }
  if (req.method !== 'POST') { res.status(405).json({error:'Method not allowed'}); return; }
  try {
    const body = req.body || {};
    const nome = sanitize(body.nome || '');
    const telefone = sanitize(body.telefone || '');
    const cidade = sanitize(body.cidade || '');
    const perfil = sanitize(body.perfil || '');
    const plano = sanitize(body.plano || '');
    if (!nome || !telefone) { res.status(400).json({error:'nome and telefone required'}); return; }
    const row = `leads;${nome};${telefone};${cidade};${now()};novo;;;;autofill-page;;;comercial@praia.digital;`;
    ensureFile();
    fs.appendFileSync(FILE, row + '\n', 'utf8');
    res.status(200).json({ok:true, savedAt:now()});
  } catch (err) { res.status(500).json({error: err.message}); }
};
