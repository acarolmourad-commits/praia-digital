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
const dialog = document.getElementById('brief-dialog');
const form = document.getElementById('brief-form');
const result = document.getElementById('brief-result');
const briefText = document.getElementById('brief-text');
let opener;
document.querySelectorAll('[data-open-brief]').forEach(button => button.addEventListener('click', event => { event.preventDefault(); opener = button; dialog.showModal(); }));
function closeDialog() { dialog.close(); if (opener) opener.focus(); }
document.querySelector('.close-dialog').addEventListener('click', closeDialog);
dialog.addEventListener('click', event => { if (event.target !== dialog) return; const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDialog(); });
form.addEventListener('submit', event => {
  event.preventDefault();
  const business = document.getElementById('business');
  if (!business.value.trim()) { business.setCustomValidity('Informe o nome da sua marca ou negócio.'); business.reportValidity(); return; }
  business.setCustomValidity('');
  const destinations = [...form.querySelectorAll('input[name="destination"]:checked')].map(input => input.value);
  const body = `Olá, equipe Praia Digital!\n\nTenho interesse em desenhar um piloto do LiveBridge AI.\n\nMarca / negócio: ${business.value.trim()}\nOrigem atual das lives: ${document.getElementById('source').value}\nCanais de interesse: ${destinations.length ? destinations.join(', ') : 'A definir'}\nObjetivo: ${document.getElementById('goal').value.trim() || 'A definir na conversa'}\n\nGostaria de avaliar a viabilidade, o escopo, o investimento e o prazo.\n\nEntendo que o projeto está em concepção e que as integrações dependem de validação.\n\nObrigado(a)!`;
  briefText.textContent = body;
  document.getElementById('send-email').href = `mailto:comercial@praia.digital?subject=${encodeURIComponent('Piloto LiveBridge AI — ' + business.value.trim())}&body=${encodeURIComponent(body)}`;
  form.hidden = true; result.hidden = false; dialog.scrollTop = 0; document.getElementById('send-email').focus();
});
document.getElementById('business').addEventListener('input', event => event.target.setCustomValidity(''));
document.getElementById('edit-brief').addEventListener('click', () => { result.hidden = true; form.hidden = false; document.getElementById('business').focus(); });
document.getElementById('copy-brief').addEventListener('click', async () => { const copyStatus = document.getElementById('copy-status'); try { await navigator.clipboard.writeText(briefText.textContent); copyStatus.textContent = 'Briefing copiado. Cole no seu e-mail e revise antes de enviar.'; } catch { const selection = window.getSelection(); const range = document.createRange(); range.selectNodeContents(briefText); selection.removeAllRanges(); selection.addRange(range); copyStatus.textContent = 'Selecione e copie o briefing acima. Nenhuma mensagem foi enviada.'; } });
