const fs = require('fs');
const path = require('path');

function sanitize(s){ return (s||'').replace(/;/g,',').replace(/\n/g,' ').trim(); }
function ensureFile(filePath, header){
  if (!fs.existsSync(filePath)) fs.mkdirSync(path.dirname(filePath), {recursive:true});
  fs.writeFileSync(filePath, header + '\n', 'utf8');
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
    const email = sanitize(body.email || '');
    const cidade = sanitize(body.cidade || '');
    const telefone = sanitize(body.telefone || '');
    const origem = sanitize(body.origem || 'relatorio-valorizacao');

    if (!nome || !email) { res.status(400).json({error:'nome and email required'}); return; }

    const folder = path.join(__dirname, '../../../docs/sales/csv-lotes-b2b');
    const today = new Date().toISOString().slice(0,10);
    const fileName = `lote-report-${today}.csv`;
    const filePath = path.join(folder, fileName);
    const now = new Date().toLocaleString('sv');

    const header = 'Lote;Nome;Email;Telefone;Cidade;Data;Status;Origem';
    const row = `report;${nome};${email};${telefone};${cidade};${now};novo;${origem}`;

    ensureFile(filePath, header);
    fs.appendFileSync(filePath, row + '\n', 'utf8');

    res.status(200).json({ ok:true, file: fileName, savedAt: now });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
