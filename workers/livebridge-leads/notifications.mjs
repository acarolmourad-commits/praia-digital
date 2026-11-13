const TO = 'comercial@praia.digital';
const FROM = 'solicitacoes@avisos.praia.digital';
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function messageFor(lead) {
  const text = [
    'Nova solicitação de serviço — Praia Digital',
    `Serviço: ${lead.service}`, `Protocolo: ${lead.id}`, `Registro (UTC): ${lead.created_at}`,
    `Nome: ${lead.name}`, `Empresa: ${lead.business}`, `E-mail: ${lead.email}`,
    `WhatsApp: ${lead.phone || 'Não informado'}`,
    `Marketplaces: ${lead.marketplaces}`, `Redes: ${lead.destinations}`,
    `Origem das lives: ${lead.live_source}`, `Solicitação: ${lead.goal || 'Não informada'}`,
    '', 'Próximo passo: responder ao solicitante, entender a necessidade e preparar atendimento ou cotação.',
    'Este cadastro não representa contratação nem aprovação de valores ou prazos.'
  ].join('\n');
  return {from:FROM,to:TO,replyTo:lead.email,subject:`[Solicitação] ${lead.service} — ${lead.id}`,text,
    html:`<h2>Nova solicitação — Praia Digital</h2><pre style="white-space:pre-wrap;font:15px/1.6 Arial,sans-serif">${escape(text)}</pre>`};
}
export async function sendPending(env, onlyId = '') {
  if (env.EMAIL_NOTIFICATIONS_ENABLED !== 'true' || !env.EMAIL?.send) return {enabled:false,sent:0};
  const rows = await env.LEADS_DB.prepare(`SELECT l.*, s.service FROM notification_outbox o
    JOIN leads l ON l.id=o.lead_id JOIN service_requests s ON s.lead_id=l.id
    WHERE o.kind='team' AND o.status IN ('pending_setup','queued') AND (?='' OR l.id=?)
    ORDER BY o.created_at LIMIT 20`).bind(onlyId,onlyId).all();
  let sent=0;
  for (const lead of rows.results || []) {
    const claim=await env.LEADS_DB.prepare(`UPDATE notification_outbox SET status='sending'
      WHERE lead_id=? AND kind='team' AND status IN ('pending_setup','queued')`).bind(lead.id).run();
    if (!claim.meta?.changes) continue;
    try {
      const result=await env.EMAIL.send(messageFor(lead));
      await env.LEADS_DB.prepare(`UPDATE notification_outbox SET status='accepted',sent_at=?,provider_id=?
        WHERE lead_id=? AND kind='team' AND status='sending'`).bind(new Date().toISOString(),result?.messageId || '',lead.id).run();
      sent++;
    } catch {
      // A timeout can occur after the provider accepted a message. Do not blindly resend.
      await env.LEADS_DB.prepare(`UPDATE notification_outbox SET status='review_required'
        WHERE lead_id=? AND kind='team' AND status='sending'`).bind(lead.id).run();
      console.error(JSON.stringify({event:'team_notification_review_required'}));
    }
  }
  return {enabled:true,sent};
}
