const fs = require('fs');
const path = require('path');

function sanitize(s){ return (s||'').toString().replace(/;/g,',').replace(/\n/g,' ').trim(); }
function ensureFile(filePath, header){
  if (!fs.existsSync(filePath)) fs.mkdirSync(path.dirname(filePath), {recursive:true});
  fs.writeFileSync(filePath, header + '\n', 'utf8');
}

// Endpoint: Avaliacao de imovel (secao #avaliacao da home)
// Recebe o e-mail do usuario + dados da avaliacao e registra a solicitacao
// para envio do relatorio de avaliacao da regiao selecionada.
module.exports = async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.status(204).end(); return; }
  if (req.method !== 'POST') { res.status(405).json({error:'Method not allowed'}); return; }

  try {
    const body = req.body || {};
    const email = sanitize(body.email || '');
    const cidade = sanitize(body.cidade || '');
    const regiao = sanitize(body.regiao || '');
    const tipo = sanitize(body.tipo || '');
    const area = sanitize(body.area || '');
    const dormitorios = sanitize(body.dormitorios || '');
    const valorMin = sanitize(body.valor_min || '');
    const valorMedio = sanitize(body.valor_medio || '');
    const valorMax = sanitize(body.valor_max || '');
    const origem = sanitize(body.origem || 'avaliacao-home');

    if (!email || email.indexOf('@') < 0) { res.status(400).json({error:'valid email required'}); return; }
    if (!cidade) { res.status(400).json({error:'cidade required'}); return; }

    const folder = path.join(__dirname, '../../../docs/sales/csv-lotes-b2b');
    const today = new Date().toISOString().slice(0,10);
    const fileName = `lote-avaliacao-${today}.csv`;
    const filePath = path.join(folder, fileName);
    const now = new Date().toLocaleString('sv');

    const header = 'Lote;Email;Cidade;Regiao;Tipo;Area_m2;Dormitorios;ValorMin;ValorMedio;ValorMax;Data;Status;Origem';
    const row = `avaliacao;${email};${cidade};${regiao};${tipo};${area};${dormitorios};${valorMin};${valorMedio};${valorMax};${now};relatorio-solicitado;${origem}`;

    ensureFile(filePath, header);
    fs.appendFileSync(filePath, row + '\n', 'utf8');

    res.status(200).json({ ok:true, file: fileName, savedAt: now, relatorio: { cidade, regiao, valorMedio } });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
