/**
 * Composio Lead Alert — Praia Digital
 *
 * Recebe payloads de leads dos formulários de Afiliados e Corretores
 * e envia alerta estruturada para canal interno via Composio.
 *
 * Uso:
 *   node scripts/composio-lead-alert.js <payload.json>
 *
 * Variáveis de ambiente:
 *   COMPOSIO_WEBHOOK_URL  - endpoint do webhook/app interno
 *   COMPOSIO_API_KEY      - chave da integração
 */

const fs = require('fs');

const COMPOSIO_WEBHOOK_URL = process.env.COMPOSIO_WEBHOOK_URL || 'https://SEU_WEBHOOK_COMPOSIO/lead';
const COMPOSIO_API_KEY = process.env.COMPOSIO_API_KEY || '';

function parsePayload(path) {
  const raw = fs.readFileSync(path, 'utf-8');
  return JSON.parse(raw);
}

function formatAlert(payload) {
  const lead = payload.lead || {};
  const meta = payload.metadata || {};
  return {
    source: payload.source || 'unknown',
    title: 'Novo lead Praia Digital',
    message: [
      `Origem: ${meta.page || '-'}`,
      `Nome: ${lead.nome || '-'}`,
      `WhatsApp: ${lead.whatsapp || lead.telefone || '-'}`,
      `E-mail: ${lead.email || '-'}`,
      `CRECI: ${lead.creci || '-'}`,
      `Imobiliária: ${lead.imobiliaria || '-'}`,
      `Endereço: ${lead.endereco || '-'}`,
      `Cidade/Bairro: ${lead.cidade || '-'} / ${lead.bairro || '-'}`,
      `Tipo: ${lead.tipo_imovel || '-'}`,
      `Negócio: ${lead.negocio || '-'}`,
      `Valor: ${lead.valor || '-'}`,
      `Características: ${Array.isArray(lead.caracteristicas) ? lead.caracteristicas.join(', ') : '-'}`,
      `Recebido em: ${meta.received_at || '-'}`
    ].join('\n')
  };
}

async function sendAlert(alert) {
  const body = JSON.stringify(alert);
  try {
    const res = await fetch(COMPOSIO_WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(COMPOSIO_API_KEY ? { Authorization: `Bearer ${COMPOSIO_API_KEY}` } : {})
      },
      body
    });
    console.log('Enviado:', res.status, await res.text());
  } catch (err) {
    console.error('Falha no envio:', err);
    process.exitCode = 1;
  }
}

(function main(){
  const path = process.argv[2];
  if(!path){
    console.error('Uso: node scripts/composio-lead-alert.js <payload.json>');
    process.exit(1);
  }
  const payload = parsePayload(path);
  const alert = formatAlert(payload);
  sendAlert(alert);
})();
