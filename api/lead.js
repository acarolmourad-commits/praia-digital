const handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { Allow: 'POST', 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Method Not Allowed' }),
    };
  }

  let payload = {};
  try {
    payload = JSON.parse(event.body || '{}');
  } catch (err) {
    return {
      statusCode: 400,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Invalid JSON' }),
    };
  }

  const entry = {
    ts: new Date().toISOString(),
    source: payload.source || 'unknown',
    name: payload.name || null,
    email: payload.email || null,
    phone: payload.phone || null,
    city: payload.city || null,
    faixa_orcamento: payload.faixa_orcamento || null,
    prazo_interesse: payload.prazo_interesse || null,
    message: payload.message || null,
  };

  try {
    const fs = require('fs');
    const path = require('path');
    const logsDir = path.join(__dirname, '..', '..', '..', 'leads');
    fs.mkdirSync(logsDir, { recursive: true });
    const logFile = path.join(logsDir, 'leads.jsonl');
    fs.appendFileSync(logFile, JSON.stringify(entry) + '\n');
  } catch (e) {
    // logging is best-effort
  }

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ok: true, id: entry.ts }),
  };
};

module.exports = { handler };
