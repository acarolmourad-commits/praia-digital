const https = require('https');
const http = require('http');

function isHttps(url){ return url.startsWith('https'); }

function postJSON(url, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const lib = isHttps(url) ? https : http;
    const u = new URL(url);
    const payload = JSON.stringify(body);
    const opts = {
      hostname: u.hostname, port: u.port || (isHttps(url) ? 443 : 80),
      path: u.pathname + u.search, method: 'POST',
      headers: { 'Content-Type':'application/json', 'Content-Length': Buffer.byteLength(payload), ...headers }
    };
    const req = lib.request(opts, res => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        try { resolve({ status: res.status, data: JSON.parse(Buffer.concat(chunks).toString()) }); }
        catch (e) { resolve({ status: res.status, data: Buffer.concat(chunks).toString() }); }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

const systemPrompt = (agent) => `Você é o agente de IA da Praia Digital para o setor "${agent}". Responda em português, de forma objetiva, prática e完成。`;

const handlers = {
  comercial: require('./agents/comercial'),
  marketing: require('./agents/marketing'),
  captacao: require('./agents/captacao'),
  avaliacao: require('./agents/avaliacao'),
  juridica: require('./agents/juridica'),
  temporada: require('./agents/temporada'),
  investidores: require('./agents/investidores'),
  portais: require('./agents/portais'),
  gestao: require('./agents/gestao'),
  atendimento: require('./agents/atendimento'),
  conteudo: require('./agents/conteudo'),
  mercado: require('./agents/mercado'),
  imagens: require('./agents/imagens'),
  videos: require('./agents/videos'),
};

module.exports = async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.status(204).end(); return; }
  if (req.method !== 'POST') { res.status(405).json({error:'Method not allowed'}); return; }

  const body = req.body || {};
  const { agent, input, context } = body;
  if (!agent || !handlers[agent]) { res.status(400).json({error:'Invalid or missing agent'}); return; }

  const useAI = process.env.AI_PROVIDER_URL && process.env.AI_API_KEY;
  if (!useAI) {
    const fallback = await handlers[agent](input, context);
    return res.status(200).json({ agent, provider: 'fallback', output: fallback });
  }

  try {
    const url = process.env.AI_PROVIDER_URL;
    const key = process.env.AI_API_KEY;
    const model = process.env.AI_MODEL || 'gpt-4o-mini';
    const payload = {
      model,
      messages: [
        { role:'system', content: systemPrompt(agent) },
        { role:'user', content: input || '' }
      ],
      temperature: 0.4,
      max_tokens: 600
    };
    const result = await postJSON(url, payload, { Authorization: `Bearer ${key}` });
    if (result.status !== 200) throw new Error('Provider error: ' + (result.data?.error || result.data));
    const text = result.data?.choices?.[0]?.message?.content || result.data?.message || '';
    res.status(200).json({ agent, provider: process.env.AI_PROVIDER_LABEL || 'ai', output: text });
  } catch (err) {
    const fallback = await handlers[agent](input, context);
    res.status(200).json({ agent, provider:'fallback', output: fallback + ' | IA indisponível: ' + err.message });
  }
};
