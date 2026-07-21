const path = require('path');
const fs = require('fs');
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
  try {
    const result = await handlers[agent](input, context);
    res.status(200).json({ agent, output: result });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
