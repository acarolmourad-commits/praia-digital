import {VERSION, CATALOG, CHANNELS, ACTORS, createState, available, reconcile, apply, runScenario} from './modelo.mjs';
const $ = id => document.getElementById(id);
let state = createState(), checks = [], sequence = 0, lastReservation;
const labels = {reserved: 'Reservado', shipped: 'Expedido na simulação', cancelled: 'Cancelado'};
function cell(row, text) { const td = document.createElement('td'); td.textContent = text; row.append(td); return td; }
function message(text) { $('feedback').textContent = text; }
function render() {
  $('inventory').replaceChildren();
  for (const p of state.products) {
    const tr = document.createElement('tr');
    cell(tr, p.name); cell(tr, p.sku); cell(tr, p.physical); cell(tr, p.reserved); cell(tr, available(p));
    cell(tr, available(p) <= 150 ? (available(p) === 0 ? 'Sem saldo livre' : 'Até 150 livres') : 'Acima de 150 livres');
    $('inventory').append(tr);
  }
  $('orders').replaceChildren();
  for (const o of state.orders) {
    const item = document.createElement('li');
    const text = document.createElement('p');
    text.textContent = `${o.id} · ${o.sku} · ${o.quantity} un. · ${o.channel} · ${o.actor} · ${labels[o.status]}`;
    item.append(text);
    if (o.status === 'reserved') for (const [type, label] of [['ship', 'Confirmar saída'], ['cancel', 'Cancelar reserva']]) {
      const button = document.createElement('button'); button.type = 'button'; button.textContent = `${label} ${o.id}`;
      button.addEventListener('click', () => perform({type, id: `DEMO-M${++sequence}`, orderId: o.id, actor: o.actor}));
      item.append(button);
    }
    $('orders').append(item);
  }
  $('empty').hidden = state.orders.length > 0;
  $('event-count').textContent = `${state.events.length} operações aplicadas`;
  $('reconciliation').textContent = reconcile(state) ? 'Saldo e histórico conciliados' : 'Divergência encontrada';
  $('replay').disabled = !lastReservation;
  $('check-count').textContent = checks.length ? `Último roteiro automático: ${checks.filter(c => c.pass).length}/${checks.length} verificações aprovadas` : 'Roteiro ainda não executado';
  $('checks').replaceChildren();
  for (const check of checks) {
    const li = document.createElement('li'); li.textContent = `${check.pass ? 'Aprovado' : 'Falhou'} — ${check.name}. Esperado: ${check.expected}. Observado: ${check.observed}.`;
    $('checks').append(li);
  }
  $('history').replaceChildren();
  for (const e of state.events) {
    const li = document.createElement('li'); li.textContent = `${e.id}: ${e.type} / ${e.orderId}. Físico ${e.physical}, reservado ${e.reserved}, disponível ${e.available}.`;
    $('history').append(li);
  }
}
function perform(event) {
  const result = apply(state, event); state = result.state;
  state.attempts.push({event: {...event}, result: result.code});
  message(result.message); render();
}
for (const p of CATALOG) { const option = document.createElement('option'); option.value = p.sku; option.textContent = p.name; $('sku').append(option); }
for (const [id, values] of [['channel', CHANNELS], ['actor', ACTORS]]) for (const v of values) { const option = document.createElement('option'); option.textContent = v; $(id).append(option); }
$('reserve-form').addEventListener('submit', e => {
  e.preventDefault();
  lastReservation = {id: `DEMO-M${++sequence}`, orderId: `DEMO-PM${sequence}`, type: 'reserve', sku: $('sku').value, quantity: Number($('quantity').value), channel: $('channel').value, actor: $('actor').value};
  perform(lastReservation);
});
$('replay').addEventListener('click', () => { if (lastReservation) perform(lastReservation); });
$('run').addEventListener('click', () => {
  ({state, checks} = runScenario()); sequence = 0; lastReservation = undefined;
  message('Roteiro executado em uma base fictícia nova. Os resultados abaixo pertencem somente ao simulador.'); render();
});
$('reset').addEventListener('click', () => {
  state = createState(); checks = []; sequence = 0; lastReservation = undefined;
  message('Demonstração reiniciada com os três produtos fictícios.'); render();
});
$('download').addEventListener('click', () => {
  const report = {kind: 'SIMULACAO_LOCAL_SEM_INTEGRACAO', version: VERSION, generatedAt: new Date().toISOString(), productionValidated: false, customerAcceptance: 'não registrado', checks, reconciled: reconcile(state), products: state.products, orders: state.orders, events: state.events, manualAttempts: state.attempts};
  const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], {type: 'application/json'}));
  const a = document.createElement('a'); a.href = url; a.download = 'evidencias-piloto-ficticio.json'; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000); message('Relatório da simulação preparado para download. Não é aceite de cliente nem validação de produção.');
});
for (const el of document.querySelectorAll('[data-ready]')) el.disabled = false;
render();
