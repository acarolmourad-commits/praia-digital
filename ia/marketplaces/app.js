'use strict';
const channelButtons = [...document.querySelectorAll('[data-channel]')];
const simulate = document.getElementById('simulate');
const demoVisual = document.querySelector('.demo-visual');
const state = document.getElementById('demo-state');
const status = document.getElementById('demo-status');
const count = document.getElementById('demo-count');
let timerIds = [];
let running = false;
function selectedChannels() { return channelButtons.filter(button => button.getAttribute('aria-pressed') === 'true').map(button => button.dataset.channel); }
function clearSimulation() { timerIds.forEach(clearTimeout); timerIds = []; running = false; demoVisual.classList.remove('running'); simulate.textContent = 'Simular distribuição'; }
function syncChannels() {
  clearSimulation();
  const selected = selectedChannels();
  count.textContent = `${selected.length} ${selected.length === 1 ? 'destino selecionado' : 'destinos selecionados'}`;
  state.textContent = 'PRÉVIA DA OPERAÇÃO';
  document.querySelectorAll('[data-target]').forEach(target => { const active = selected.includes(target.dataset.target); target.classList.toggle('off', !active); target.classList.remove('reached'); target.querySelector('small').textContent = active ? 'Selecionado' : 'Não selecionado'; });
  simulate.disabled = selected.length === 0;
  status.replaceChildren();
  const icon = document.createElement('span'); icon.className = 'status-icon'; icon.textContent = '+';
  const p = document.createElement('p'); p.textContent = selected.length ? `Uma fonte. ${selected.length} ${selected.length === 1 ? 'destino na simulação.' : 'destinos na simulação.'}` : 'Selecione pelo menos um destino para explorar o fluxo.';
  const small = document.createElement('small'); small.textContent = 'A compatibilidade real será verificada nas contas do piloto.'; p.append(small); status.append(icon, p);
}
channelButtons.forEach(button => button.addEventListener('click', () => { const selected = button.getAttribute('aria-pressed') !== 'true'; button.setAttribute('aria-pressed', String(selected)); button.classList.toggle('selected', selected); syncChannels(); }));
simulate.addEventListener('click', () => {
  if (running) { syncChannels(); return; }
  const selected = selectedChannels(); if (!selected.length) return;
  clearSimulation(); running = true; demoVisual.classList.add('running'); simulate.textContent = 'Reiniciar simulação'; state.textContent = 'SIMULANDO O FLUXO';
  document.querySelectorAll('[data-target]').forEach(target => { target.classList.remove('reached'); if (selected.includes(target.dataset.target)) target.querySelector('small').textContent = 'Preparando…'; });
  status.querySelector('p').textContent = 'Simulando a preparação do sinal e dos destinos selecionados…';
  selected.forEach((name, index) => timerIds.push(setTimeout(() => { const target = document.querySelector(`[data-target="${name}"]`); target.classList.add('reached'); target.querySelector('small').textContent = 'Fluxo ilustrado'; }, 550 + index * 500)));
  timerIds.push(setTimeout(() => { state.textContent = 'SIMULAÇÃO CONCLUÍDA'; running = false; demoVisual.classList.remove('running'); simulate.textContent = 'Simular novamente'; const p = status.querySelector('p'); p.textContent = `Fluxo ilustrado para ${selected.join(', ')}.`; const small = document.createElement('small'); small.textContent = 'Nenhuma live foi captada ou transmitida. Esta é uma demonstração conceitual.'; p.append(small); }, 800 + selected.length * 500));
});
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
