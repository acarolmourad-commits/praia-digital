const form = document.getElementById('brief-form');
const result = document.getElementById('brief-result');
const submitButton = document.getElementById('lead-submit');
const errorMessage = document.getElementById('lead-error');
const leadStatus = document.getElementById('lead-status');
const ENDPOINT = 'https://praia-livebridge-leads.kleber-f63.workers.dev/leads';
const serviceSelect = document.getElementById('lead-service');
const goalField = document.getElementById('goal');
const requested = new URLSearchParams(location.search).get('servico');
const submitLabel = submitButton.textContent;
if ([...serviceSelect.options].some(option => option.value === requested)) serviceSelect.value = requested;

function updateServiceFields() {
  const live = serviceSelect.value === 'LiveBridge AI';
  const commerce = live || serviceSelect.value === 'Estoque Vivo';
  for (const [id, visible] of [['project-fields', !commerce], ['marketplace-fields', commerce], ['live-fields', live]]) {
    const group = document.getElementById(id);
    group.hidden = !visible;
    group.disabled = !visible;
  }
  goalField.maxLength = commerce ? 1500 : 600;
  goalField.setCustomValidity('');
  document.getElementById('goal-hint').textContent = `Até ${goalField.maxLength} caracteres. Não envie senhas ou dados pessoais de clientes.`;
  for (const link of document.querySelectorAll('[data-service-return]')) {
    link.href = commerce ? '/ia/marketplaces/' : '/servicos-ia.html';
    link.textContent = commerce ? 'Voltar à apresentação de marketplaces' : 'Voltar aos serviços de IA';
  }
}
serviceSelect.addEventListener('change', updateServiceFields);
updateServiceFields();
let pending = false;
let submissionId = null;
let previousPayload = '';
for (const id of ['lead-name', 'business', 'lead-phone', 'goal']) {
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
  goalField.setCustomValidity(goalField.value.length <= goalField.maxLength ? '' : `Use até ${goalField.maxLength} caracteres para o resultado esperado.`);
  if (!form.reportValidity()) return;
  const live = serviceSelect.value === 'LiveBridge AI';
  const commerce = live || serviceSelect.value === 'Estoque Vivo';
  // Keep the existing Worker contract: general briefing is stored in the private goal field.
  const goal = commerce ? goalField.value.trim() : [
    ['Processo', document.getElementById('process').value.trim()],
    ['Ferramentas', document.getElementById('tools').value.trim()],
    ['Volume ou frequência', document.getElementById('volume').value.trim()],
    ['Objetivo', goalField.value.trim()]
  ].filter(([, value]) => value).map(([label, value]) => `${label}: ${value}`).join('\n');
  if (goal.length > 1500) {
    goalField.setCustomValidity('Resuma a descrição do processo e do objetivo para enviar sua solicitação.');
    form.reportValidity();
    return;
  }
  const query = new URLSearchParams(location.search);
  const utm = {};
  for (const key of ['source', 'medium', 'campaign', 'content', 'term']) utm[key] = (query.get('utm_' + key) || '').slice(0, 160);
  const payload = {
    service: serviceSelect.value,
    name: document.getElementById('lead-name').value.trim(),
    email: document.getElementById('lead-email').value.trim(),
    phone, business: document.getElementById('business').value.trim(),
    source: live ? document.getElementById('source').value : 'Ainda não faço lives',
    marketplaces: commerce ? [...form.querySelectorAll('[name="marketplace"]:checked')].map(el => el.value) : [],
    destinations: live ? [...form.querySelectorAll('[name="destination"]:checked')].map(el => el.value) : [],
    goal,
    website: document.getElementById('website').value,
    consent: document.getElementById('lead-consent').checked,
    consent_version: 'livebridge-contact-2026-11-12', utm
  };
  const serialized = JSON.stringify(payload);
  if (serialized !== previousPayload || !submissionId) { submissionId = crypto.randomUUID(); previousPayload = serialized; }
  payload.submission_id = submissionId;
  pending = true;
  const fields = [...form.elements].map(field => [field, field.disabled]);
  fields.forEach(([field]) => field.disabled = true);
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
    fields.forEach(([field, wasDisabled]) => field.disabled = wasDisabled);
    form.removeAttribute('aria-busy');
    submitButton.textContent = submitLabel;
  }
});

// Enable only after the submit handler is ready; no native GET with contact data.
submitButton.disabled = false;

document.getElementById('copy-receipt').addEventListener('click', async () => {
  const status = document.getElementById('copy-status');
  try {
    await navigator.clipboard.writeText(document.getElementById('lead-receipt').textContent);
    status.textContent = 'Protocolo copiado. Guarde-o para acompanhar sua solicitação.';
  } catch {
    status.textContent = 'Não foi possível copiar. Selecione o protocolo acima e copie manualmente.';
  }
});
