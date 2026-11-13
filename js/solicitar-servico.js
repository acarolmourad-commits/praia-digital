const form = document.getElementById('brief-form');
const result = document.getElementById('brief-result');
const submitButton = document.getElementById('lead-submit');
const errorMessage = document.getElementById('lead-error');
const leadStatus = document.getElementById('lead-status');
const ENDPOINT = 'https://praia-livebridge-leads.kleber-f63.workers.dev/leads';
let pending = false;
let submissionId = null;
let previousPayload = '';
for (const id of ['lead-name', 'business', 'lead-phone']) {
  document.getElementById(id).addEventListener('input', event => event.target.setCustomValidity(''));
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (pending) return;
  for (const id of ['lead-name', 'business']) {
    const field = document.getElementById(id);
    field.setCustomValidity(field.value.trim() ? '' : 'Preencha este campo.');
  }
  const phoneField = document.getElementById('lead-phone');
  const phone = phoneField.value.trim().replace(/[\s()+.-]/g, '');
  phoneField.setCustomValidity(!phone || /^\d{10,15}$/.test(phone) ? '' : 'Informe o WhatsApp com DDD ou deixe em branco.');
  if (!form.reportValidity()) return;
  const query = new URLSearchParams(location.search);
  const utm = {};
  for (const key of ['source', 'medium', 'campaign', 'content', 'term']) utm[key] = (query.get('utm_' + key) || '').slice(0, 160);
  const payload = {
    service: document.getElementById('lead-service')?.value || 'LiveBridge AI',
    name: document.getElementById('lead-name').value.trim(),
    email: document.getElementById('lead-email').value.trim(),
    phone, business: document.getElementById('business').value.trim(),
    source: document.getElementById('source').value,
    marketplaces: [...form.querySelectorAll('[name="marketplace"]:checked')].map(el => el.value),
    destinations: [...form.querySelectorAll('[name="destination"]:checked')].map(el => el.value),
    goal: document.getElementById('goal').value.trim(),
    website: document.getElementById('website').value,
    consent: document.getElementById('lead-consent').checked,
    consent_version: 'livebridge-contact-2026-11-12', utm
  };
  const serialized = JSON.stringify(payload);
  if (serialized !== previousPayload || !submissionId) { submissionId = crypto.randomUUID(); previousPayload = serialized; }
  payload.submission_id = submissionId;
  pending = true;
  const fields = [...form.elements];
  fields.forEach(field => field.disabled = true);
  form.setAttribute('aria-busy', 'true');
  errorMessage.hidden = true;
  leadStatus.textContent = 'Enviando sua solicitação…';
  submitButton.textContent = 'Enviando…';
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload), signal: controller.signal, credentials: 'omit' });
    const receipt = await response.json();
    if (!response.ok || receipt.ok !== true || receipt.id !== submissionId) {
      if (response.status === 409) submissionId = null;
      throw new Error(receipt.error || 'Não foi possível confirmar seu cadastro. Tente novamente.');
    }
    document.getElementById('lead-receipt').textContent = receipt.id;
    form.hidden = true;
    result.hidden = false;
    form.reset();
    document.getElementById('lead-success-title').focus();
  } catch (error) {
    errorMessage.textContent = error.name === 'AbortError' || error instanceof TypeError
      ? 'Não foi possível confirmar o envio. Seus dados continuam preenchidos. Confira sua conexão e tente novamente. Se preferir, fale com comercial@praia.digital.'
      : error.message;
    errorMessage.hidden = false;
    leadStatus.textContent = '';
  } finally {
    clearTimeout(timeout);
    pending = false;
    fields.forEach(field => field.disabled = false);
    form.removeAttribute('aria-busy');
    submitButton.textContent = 'Quero conversar sobre meu piloto';
  }
});

// Enable only after the submit handler is ready; no native GET with contact data.
submitButton.disabled = false;

const requested = new URLSearchParams(location.search).get('servico');
const serviceSelect = document.getElementById('lead-service');
if (serviceSelect && [...serviceSelect.options].some(o=>o.value===requested)) serviceSelect.value=requested;
