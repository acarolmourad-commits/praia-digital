import {crm} from './crm.mjs';
import {sendPending} from './notifications.mjs';
const ORIGINS = new Set(['https://praia.digital', 'https://www.praia.digital']);
const SOURCES = ['Ainda não faço lives', 'Celular / câmera', 'OBS ou outro estúdio', 'TikTok Shop', 'Shopee', 'Outra plataforma'];
const CHANNELS = ['Instagram', 'Facebook', 'TikTok'];
const MARKETPLACES = ['TikTok Shop', 'Shopee', 'Mercado Livre', 'Outros', 'Ainda não vendo'];
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const SERVICES = ["LiveBridge AI","Estoque Vivo","Atendimento e relacionamento","Automação de processos","Conteúdo e comunicação","Conhecimento e apoio à equipe","Diagnóstico e capacitação","Projeto personalizado"];
const PAGE = 'https://praia.digital/ia/marketplaces/';
const CONSENT_VERSION = 'livebridge-contact-2026-11-12';

class InputError extends Error {
  constructor(message, status = 422) { super(message); this.status = status; }
}
function text(value, max, required = false) {
  if (typeof value !== 'string') throw new InputError('Confira os campos do formulário.');
  const result = value.trim();
  if (result.length > max || (required && !result) || /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(result)) throw new InputError('Confira os campos do formulário.');
  return result;
}
function choices(value, allowed) {
  if (!Array.isArray(value) || value.length > allowed.length || value.some(item => !allowed.includes(item))) throw new InputError('Confira os canais selecionados.');
  return [...new Set(value)].sort();
}
export function validate(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) throw new InputError('Formulário inválido.');
  if (!UUID.test(body.submission_id || '')) throw new InputError('Atualize a página e tente novamente.');
  if (body.website !== '') throw new InputError('Não foi possível validar o envio.');
  if (body.consent !== true || body.consent_version !== CONSENT_VERSION) throw new InputError('Autorize o contato para enviar sua solicitação.');
  const email = text(body.email, 254, true).toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new InputError('Informe um e-mail válido.');
  const phone = text(body.phone, 30).replace(/[\s()+.-]/g, '');
  if (phone && !/^\d{10,15}$/.test(phone)) throw new InputError('Informe o WhatsApp com DDD ou deixe esse campo em branco.');
  if (!SOURCES.includes(body.source)) throw new InputError('Selecione a origem das lives.');
  const utm = {};
  for (const key of ['source', 'medium', 'campaign', 'content', 'term']) utm[key] = text(body.utm?.[key] ?? '', 160);
  return {
    name: text(body.name, 100, true), email, phone,
    business: text(body.business, 100, true), source: body.source,
    destinations: choices(body.destinations, CHANNELS),
    marketplaces: choices(body.marketplaces, MARKETPLACES),
    goal: text(body.goal, 1500), utm
  };
}
async function readBody(request) {
  if (Number(request.headers.get('Content-Length')) > 12000) throw new InputError('Formulário muito longo.', 413);
  if (!request.body) throw new InputError('Formulário vazio.', 400);
  const reader = request.body.getReader();
  let length = 0;
  const parts = [];
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    length += value.byteLength;
    if (length > 12000) { await reader.cancel(); throw new InputError('Formulário muito longo.', 413); }
    parts.push(value);
  }
  const bytes = new Uint8Array(length);
  let offset = 0;
  for (const part of parts) { bytes.set(part, offset); offset += part.length; }
  try { return JSON.parse(new TextDecoder().decode(bytes)); } catch { throw new InputError('Formulário inválido.', 400); }
}
function response(status, body, origin, extra = {}) {
  const headers = { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Vary': 'Origin', ...extra };
  if (ORIGINS.has(origin)) headers['Access-Control-Allow-Origin'] = origin;
  return new Response(status === 204 ? null : JSON.stringify(body), { status, headers });
}
export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get('Origin');
    const path = new URL(request.url).pathname;
    if (path === '/' && new URL(request.url).hostname === 'crm.praia.digital') return Response.redirect(new URL('/crm/',request.url),302);
    if (path === '/crm' || path.startsWith('/crm/')) return crm(request,env);
    if (path === '/health' && request.method === 'GET') return response(200, { ok: true, service: 'livebridge-leads' }, origin);
    if (path !== '/leads') return response(404, { ok: false }, origin);
    if (!ORIGINS.has(origin)) return response(403, { ok: false, error: 'Origem não autorizada.' }, origin);
    if (request.method === 'OPTIONS') return response(204, null, origin, { 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Max-Age': '600' });
    if (request.method !== 'POST') return response(405, { ok: false }, origin, { Allow: 'POST, OPTIONS' });
    if (request.headers.get('Content-Type')?.split(';')[0].trim().toLowerCase() !== 'application/json') return response(415, { ok: false, error: 'Formato inválido.' }, origin);
    try {
      const limit = await env.LEAD_LIMITER.limit({ key: request.headers.get('CF-Connecting-IP') || 'unknown' });
      if (!limit.success) return response(429, { ok: false, error: 'Muitas tentativas. Aguarde um minuto e tente novamente.' }, origin, { 'Retry-After': '60' });
      const body = await readBody(request);
      const lead = validate(body);
      const service = body.service || 'LiveBridge AI';
      if (!SERVICES.includes(service)) throw new InputError('Selecione um serviço válido.');
      if (body.service) lead.service = service;
      const hash = [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(JSON.stringify(lead))))].map(b => b.toString(16).padStart(2, '0')).join('');
      const id = body.submission_id.toLowerCase();
      const saved = await env.LEADS_DB.prepare(`INSERT INTO leads
        (id, created_at, name, email, phone, business, live_source, marketplaces, destinations, goal, page_url, utm, consent_version, consent_at, payload_hash, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'novo')
        ON CONFLICT(id) DO NOTHING`).bind(id, new Date().toISOString(), lead.name, lead.email, lead.phone, lead.business, lead.source, JSON.stringify(lead.marketplaces), JSON.stringify(lead.destinations), lead.goal, PAGE, JSON.stringify(lead.utm), CONSENT_VERSION, new Date().toISOString(), hash).run();
      if (saved.success !== true) throw new Error('storage_failed');
      const receipt = await env.LEADS_DB.prepare('SELECT payload_hash FROM leads WHERE id = ?').bind(id).first();
      if (!receipt) throw new Error('receipt_missing');
      if (receipt.payload_hash !== hash) return response(409, { ok: false, error: 'O formulário mudou. Revise as informações e envie novamente.' }, origin);
      await env.LEADS_DB.prepare('INSERT INTO service_requests (lead_id, service) VALUES (?, ?) ON CONFLICT(lead_id) DO NOTHING').bind(id, service).run();
      const notify = sendPending(env, id).catch(() => console.error(JSON.stringify({event:'team_notification_queue_failed'})));
      if (ctx?.waitUntil) ctx.waitUntil(notify); else await notify;
      // No personal data in logs, URLs, responses or a public read endpoint.
      return response(saved.meta?.changes ? 201 : 200, { ok: true, id, email_status: 'pending_setup', team_notification: env.EMAIL_NOTIFICATIONS_ENABLED === 'true' ? 'queued' : 'pending_setup' }, origin);
    } catch (error) {
      if (error instanceof InputError) return response(error.status, { ok: false, error: error.message }, origin);
      console.error(JSON.stringify({ event: 'lead_capture_failed' }));
      return response(503, { ok: false, error: 'Não foi possível confirmar o cadastro. Tente novamente em instantes.' }, origin);
    }
  },
  async scheduled(event, env, ctx) {
    ctx.waitUntil(sendPending(env).catch(() => console.error(JSON.stringify({event:'team_notification_queue_failed'}))));
  }
};
