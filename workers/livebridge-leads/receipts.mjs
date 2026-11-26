// Disabled by default. No access to Gmail, no briefings sent to the provider.
const ADMIN = 'comercial@praia.digital';
const FROM = 'Praia Digital <solicitacoes@confirmacoes.praia.digital>';
const CONSENT = 'livebridge-contact-2026-11-12';
const UUID = /^[0-9a-f-]{36}$/;
export function receiptsEnabled(env) {
  return ['test', 'live'].includes(env.RECEIPTS_MODE) && !!env.RESEND_API_KEY &&
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(env.RECEIPTS_START_AT || '') &&
    Number.isFinite(Date.parse(env.RECEIPTS_START_AT));
}
export function receiptMessage(lead, mode) {
  const text = `Sua solicitação foi registrada pela Praia Digital.\n\nProtocolo: ${lead.id}\n\nA equipe analisará seu pedido e retornará pelo contato informado. Este registro não confirma contratação, preço, prazo ou disponibilidade de integrações.\n\nSe você não fez esta solicitação, ignore esta mensagem ou avise comercial@praia.digital. Não há inscrição em publicidade.\n\nPara corrigir ou excluir seus dados: comercial@praia.digital.`;
  return {from: FROM, to: [lead.email], reply_to: ADMIN,
    subject: `${mode === 'test' ? '[TESTE INTERNO] ' : ''}Recebemos sua solicitação — Praia Digital`, text};
}
const query = (env, sql, ...params) => env.LEADS_DB.prepare(sql).bind(...params);

export async function enqueueReceipts(env, onlyId = '', now = new Date()) {
  if (!receiptsEnabled(env)) return 'pending_setup';
  const time = now.toISOString();
  const dayAgo = new Date(+now - 86400000).toISOString();
  const monthAgo = new Date(+now - 31 * 86400000).toISOString();
  const rows = await query(env, `SELECT l.id,l.email FROM leads l
    JOIN service_requests s ON s.lead_id=l.id
    JOIN notification_outbox o ON o.lead_id=l.id AND o.kind='receipt'
    WHERE o.status IN ('pending_setup','quota_hold') AND l.created_at>=?
    AND l.consent_version=? AND l.consent_at<>'' AND l.status<>'teste_tecnico'
    AND (?='' OR l.id=?) AND (?='live' OR lower(l.email)=?)
    ORDER BY l.created_at LIMIT 200`, env.RECEIPTS_START_AT, CONSENT,
    onlyId, onlyId, env.RECEIPTS_MODE, ADMIN).all();
  for (const lead of rows.results || []) {
    if (!UUID.test(lead.id)) continue;
    // One SQLite statement: simultaneous consumers cannot exceed these reservations.
    // Reserved capacity is never refunded following an ambiguous provider response.
    await query(env, `INSERT INTO receipt_delivery(lead_id,recipient,message_json,admitted_at)
      SELECT ?,?,?,? WHERE
      (SELECT count(*) FROM receipt_delivery WHERE admitted_at>?)<90 AND
      (SELECT count(*) FROM receipt_delivery WHERE admitted_at>?)<2700 AND
      (SELECT count(*) FROM receipt_delivery WHERE recipient=? AND admitted_at>?)<3
      ON CONFLICT(lead_id) DO NOTHING`, lead.id, lead.email,
      JSON.stringify(receiptMessage(lead, env.RECEIPTS_MODE)), time,
      dayAgo, monthAgo, lead.email, dayAgo).run();
    await query(env, `UPDATE notification_outbox SET status=coalesce(
      (SELECT status FROM receipt_delivery WHERE lead_id=?),'quota_hold')
      WHERE lead_id=? AND kind='receipt' AND status IN ('pending_setup','quota_hold')`, lead.id, lead.id).run();
  }
  if (!onlyId) return 'queued';
  const row = await query(env, "SELECT status FROM notification_outbox WHERE lead_id=? AND kind='receipt'", onlyId).first();
  return row?.status || 'pending_setup';
}

export async function sendReceipts(env, onlyId = '', transport = fetch, now = new Date()) {
  if (!receiptsEnabled(env)) return {sent: 0};
  const time = now.toISOString();
  // A crash might follow provider acceptance. Never automatically reclaim this send.
  await query(env, `UPDATE receipt_delivery SET status='review_required',error_code='interrupted'
    WHERE status='sending' AND started_at<?`, new Date(+now - 120000).toISOString()).run();
  await query(env, `UPDATE notification_outbox SET status='review_required' WHERE kind='receipt'
    AND lead_id IN (SELECT lead_id FROM receipt_delivery WHERE status='review_required')`).run();
  const rows = await query(env, `SELECT r.* FROM receipt_delivery r JOIN leads l ON l.id=r.lead_id
    WHERE r.status='queued' AND l.created_at>=? AND l.consent_version=? AND l.consent_at<>''
    AND l.status<>'teste_tecnico' AND r.recipient=l.email AND (?='' OR r.lead_id=?) AND (?='live' OR r.recipient=?)
    ORDER BY r.admitted_at LIMIT 20`, env.RECEIPTS_START_AT, CONSENT, onlyId, onlyId,
    env.RECEIPTS_MODE, ADMIN).all();
  let sent = 0;
  for (const job of rows.results || []) {
    // Old queued notices need review, never surprise recipients after a long outage.
    if (+now - Date.parse(job.admitted_at) >= 23 * 3600000) {
      await query(env, "UPDATE receipt_delivery SET status='review_required',error_code='expired' WHERE lead_id=? AND status='queued'", job.lead_id).run();
      await query(env, "UPDATE notification_outbox SET status='review_required' WHERE lead_id=? AND kind='receipt'", job.lead_id).run();
      continue;
    }
    const claim = await query(env, `UPDATE receipt_delivery SET status='sending',started_at=?
      WHERE lead_id=? AND status='queued'`, time, job.lead_id).run();
    if (!claim.meta?.changes) continue;
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 8000);
      let response, result;
      try {
        response = await transport('https://api.resend.com/emails', {
          method: 'POST', redirect: 'error', signal: controller.signal,
          headers: {'Authorization': `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json',
            'Idempotency-Key': `service-receipt-v1/${job.lead_id}`}, body: job.message_json
        });
        result = await response.json();
      } finally { clearTimeout(timer); }
      if (!response.ok || typeof result?.id !== 'string' || !result.id) throw new Error('provider_not_confirmed');
      const update = await query(env, `UPDATE receipt_delivery SET status='accepted',accepted_at=?,provider_id=?
        WHERE lead_id=? AND status='sending'`, time, result.id, job.lead_id).run();
      if (!update.success || !update.meta?.changes) throw new Error('record_not_confirmed');
      await query(env, `UPDATE notification_outbox SET status='accepted',sent_at=?,provider_id=?
        WHERE lead_id=? AND kind='receipt'`, time, result.id, job.lead_id).run();
      sent++;
    } catch {
      // Errors, 429/5xx, timeouts and interrupted persistence are deliberately held.
      // Inspect the provider before any manually approved retry; its key lasts 24 h.
      await query(env, `UPDATE receipt_delivery SET status='review_required',error_code='provider_or_storage'
        WHERE lead_id=? AND status='sending'`, job.lead_id).run();
      await query(env, `UPDATE notification_outbox SET status=(SELECT status FROM receipt_delivery WHERE lead_id=?)
        WHERE lead_id=? AND kind='receipt'`, job.lead_id, job.lead_id).run();
      console.error(JSON.stringify({event: 'receipt_review_required'}));
    }
  }
  return {sent};
}
