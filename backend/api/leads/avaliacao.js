const fs = require('fs');
const path = require('path');

function sanitize(s){ return (s||'').toString().replace(/;/g,',').replace(/\n/g,' ').trim(); }
function ensureFile(filePath, header){
  if (!fs.existsSync(filePath)) fs.mkdirSync(path.dirname(filePath), {recursive:true});
  fs.writeFileSync(filePath, header + '\n', 'utf8');
}
function escapeHtml(s){ return (s||'').toString().replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function fmtBRL(v){
  const n = Number(v);
  if (!isFinite(n) || n <= 0) return '—';
  return 'R$ ' + Math.round(n).toLocaleString('pt-BR');
}

// Monta o relatório de avaliação (texto + HTML) para envio por e-mail
function buildReport(d){
  const text = [
    'RELATÓRIO DE AVALIAÇÃO DE IMÓVEL — PRAIA DIGITAL',
    '',
    'REGIÃO: ' + d.cidade + (d.regiao ? ' (' + d.regiao + ')' : ''),
    'Tipo: ' + d.tipo + ' | Área: ' + d.area + ' m² | Dormitórios: ' + d.dormitorios,
    '',
    'ESTIMATIVA DE MERCADO',
    '  Mínimo:      ' + fmtBRL(d.valor_min),
    '  Valor médio: ' + fmtBRL(d.valor_medio),
    '  Máximo:      ' + fmtBRL(d.valor_max),
    '',
    'Estimativa automatizada baseada em dados públicos de mercado do litoral paulista.',
    'Para laudo formal, consulte um avaliador credenciado (CRECI/CNAI).',
    'https://praia.digital'
  ].join('\n');

  const html = '<div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;color:#1e293b">' +
    '<h2 style="color:#023047">📊 Relatório de Avaliação de Imóvel</h2>' +
    '<p><strong>Região:</strong> ' + escapeHtml(d.cidade) + (d.regiao ? ' (' + escapeHtml(d.regiao) + ')' : '') + '<br>' +
    '<strong>Tipo:</strong> ' + escapeHtml(d.tipo) + ' &nbsp;|&nbsp; <strong>Área:</strong> ' + escapeHtml(d.area) + ' m² &nbsp;|&nbsp; <strong>Dormitórios:</strong> ' + escapeHtml(d.dormitorios) + '</p>' +
    '<table style="width:100%;border-collapse:collapse;margin:1rem 0">' +
    '<tr style="background:#f1f5f9"><td style="padding:.6rem">Mínimo</td><td style="padding:.6rem;text-align:right;font-weight:700">' + fmtBRL(d.valor_min) + '</td></tr>' +
    '<tr><td style="padding:.6rem">Valor médio</td><td style="padding:.6rem;text-align:right;font-weight:800;color:#0077B6">' + fmtBRL(d.valor_medio) + '</td></tr>' +
    '<tr style="background:#f1f5f9"><td style="padding:.6rem">Máximo</td><td style="padding:.6rem;text-align:right;font-weight:700">' + fmtBRL(d.valor_max) + '</td></tr>' +
    '</table>' +
    '<p style="font-size:.85rem;color:#64748b">Estimativa automatizada baseada em dados públicos de mercado do litoral paulista. Para laudo formal, consulte um avaliador credenciado (CRECI/CNAI).</p>' +
    '<p style="font-size:.85rem"><a href="https://praia.digital">praia.digital</a></p>' +
    '</div>';

  return { text, html };
}

// Envio via Resend API (sem dependências extras). Requer RESEND_API_KEY no ambiente.
// Se a variável não estiver configurada, retorna {sent:false, reason:'not_configured'}.
async function sendReportEmail(to, report){
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) return { sent:false, reason:'not_configured' };
  const from = process.env.EMAIL_FROM || 'Praia Digital <no-reply@praia.digital>';
  try {
    const resp = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + apiKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: from,
        to: [to],
        subject: '📊 Sua avaliação de imóvel — Praia Digital',
        text: report.text,
        html: report.html
      })
    });
    if (!resp.ok) {
      const detail = await resp.text();
      return { sent:false, reason:'provider_error', status: resp.status, detail: detail.slice(0, 300) };
    }
    const data = await resp.json();
    return { sent:true, id: data.id || null };
  } catch (err) {
    return { sent:false, reason:'network_error', detail: err.message };
  }
}

// Endpoint: Avaliacao de imovel (secao #avaliacao da home)
// Recebe o e-mail do usuário + dados da avaliação, registra o lead e envia
// o relatório de avaliação da região selecionada.
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

    // Envia o relatório solicitado para o e-mail do usuário
    const report = buildReport({ cidade, regiao, tipo, area, dormitorios, valor_min: valorMin, valor_medio: valorMedio, valor_max: valorMax });
    const mail = await sendReportEmail(email, report);

    res.status(200).json({ ok:true, file: fileName, savedAt: now, emailSent: mail.sent, emailDetail: mail.sent ? undefined : mail.reason });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
