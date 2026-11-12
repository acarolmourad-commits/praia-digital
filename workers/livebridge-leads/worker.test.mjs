import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import worker from './worker.mjs';

function setup() {
  const db = new DatabaseSync(':memory:');
  db.exec(readFileSync(new URL('./schema.sql', import.meta.url), 'utf8'));
  const env = {
    LEAD_LIMITER: { limit: async () => ({ success: true }) },
    LEADS_DB: { prepare(sql) { return { bind(...params) { return {
      async run() { const result = db.prepare(sql).run(...params); return { success: true, meta: { changes: Number(result.changes) } }; },
      async first() { return db.prepare(sql).get(...params); }
    }; } }; } }
  };
  return { env, db };
}
function payload(overrides = {}) {
  return { submission_id: crypto.randomUUID(), name: "Teste d'Água", email: 'TESTE@example.invalid', phone: '(11) 99999-0000', business: 'Empresa de teste', source: 'TikTok Shop', marketplaces: ['Shopee'], destinations: ['Instagram'], goal: '<script>teste</script>', website: '', consent: true, consent_version: 'livebridge-contact-2026-11-12', ...overrides };
}
function request(body, options = {}) {
  return new Request('https://worker.test/leads', { method: 'POST', headers: { Origin: 'https://praia.digital', 'Content-Type': 'application/json', ...options.headers }, body: JSON.stringify(body), ...options });
}
test('saves private contact, consent, context; retries do not duplicate', async () => {
  const { env, db } = setup(); const body = payload();
  const response = await worker.fetch(request(body), env);
  assert.equal(response.status, 201);
  assert.deepEqual(await response.json(), { ok: true, id: body.submission_id });
  const row = db.prepare('SELECT * FROM leads').get();
  assert.equal(row.email, 'teste@example.invalid');
  assert.equal(row.phone, '11999990000');
  assert.equal(row.name, body.name); assert.equal(row.goal, body.goal);
  assert.equal(row.consent_version, body.consent_version); assert.equal(row.status, 'novo');
  assert.equal((await worker.fetch(request(body), env)).status, 200);
  assert.equal(db.prepare('SELECT COUNT(*) AS n FROM leads').get().n, 1);
  assert.equal((await worker.fetch(request({ ...body, business: 'Outra empresa' }), env)).status, 409);
  assert.equal(db.prepare('SELECT business FROM leads').get().business, body.business);
});
test('rejects missing consent, bad contact, unexpected enum, honeypot and overlong fields without saving', async () => {
  const { env, db } = setup();
  for (const change of [{ consent: false }, { name: '  ' }, { email: 'invalid' }, { phone: 'abc' }, { website: 'spam' }, { destinations: ['fake'] }, { source: 'fake' }, { goal: 'x'.repeat(1501) }, { name: null }, { submission_id: 'guess' }]) {
    assert.equal((await worker.fetch(request(payload(change)), env)).status, 422, JSON.stringify(change));
  }
  assert.equal(db.prepare('SELECT COUNT(*) AS n FROM leads').get().n, 0);
});
test('allows optional fields empty', async () => {
  const { env } = setup();
  assert.equal((await worker.fetch(request(payload({ phone: '', goal: '', destinations: [], marketplaces: [] })), env)).status, 201);
});
test('restricts origin, method, content type and never exposes listing', async () => {
  const { env } = setup();
  const denied = await worker.fetch(request(payload(), { headers: { Origin: 'https://foreign.test', 'Content-Type': 'application/json' } }), env);
  assert.equal(denied.status, 403); assert.equal(denied.headers.get('Access-Control-Allow-Origin'), null);
  assert.equal((await worker.fetch(new Request('https://worker.test/leads', { headers: { Origin: 'https://praia.digital' } }), env)).status, 405);
  assert.equal((await worker.fetch(request(payload(), { headers: { Origin: 'https://praia.digital', 'Content-Type': 'text/plain' } }), env)).status, 415);
  const preflight = await worker.fetch(new Request('https://worker.test/leads', { method: 'OPTIONS', headers: { Origin: 'https://praia.digital' } }), env);
  assert.equal(preflight.status, 204); assert.equal(preflight.headers.get('Access-Control-Allow-Origin'), 'https://praia.digital');
});
test('rejects oversized and malformed requests', async () => {
  const { env } = setup();
  assert.equal((await worker.fetch(request(payload({ goal: 'x'.repeat(13000) })), env)).status, 413);
  assert.equal((await worker.fetch(new Request('https://worker.test/leads', { method: 'POST', headers: { Origin: 'https://praia.digital', 'Content-Type': 'application/json' }, body: '{bad' }), env)).status, 400);
});
test('database failures never return success; rate limit blocks writes', async () => {
  const { env, db } = setup();
  env.LEAD_LIMITER.limit = async () => ({ success: false });
  const limited = await worker.fetch(request(payload()), env);
  assert.equal(limited.status, 429); assert.equal(limited.headers.get('Retry-After'), '60');
  assert.equal(db.prepare('SELECT COUNT(*) AS n FROM leads').get().n, 0);
  env.LEAD_LIMITER.limit = async () => ({ success: true });
  env.LEADS_DB.prepare = () => { throw new Error('private database details'); };
  const failed = await worker.fetch(request(payload()), env);
  assert.equal(failed.status, 503); assert.equal((await failed.json()).ok, false);
});
