// Laboratório didático em memória. Não importa nem chama o Worker de produção.
export const VERSION = '1.0.0';
export const CATALOG = Object.freeze([
  {sku: 'DEMO-CAM-AZ-M', name: 'Camiseta demonstração · azul / M', initial: 160},
  {sku: 'DEMO-BOL-CR', name: 'Bolsa demonstração · cru', initial: 12},
  {sku: 'DEMO-BON-VD', name: 'Boné demonstração · verde', initial: 5},
]);
export const CHANNELS = ['Canal A (simulado)', 'Canal B (simulado)'];
export const ACTORS = ['Operador A (fictício)', 'Operador B (fictício)'];
export function createState() {
  return {products: CATALOG.map(p => ({...p, physical: p.initial, reserved: 0})), orders: [], events: [], attempts: []};
}
export function available(product) { return product.physical - product.reserved; }
export function reconcile(state) {
  return state.products.every(p => {
    const reserved = state.orders.filter(o => o.sku === p.sku && o.status === 'reserved').reduce((n, o) => n + o.quantity, 0);
    const shipped = state.orders.filter(o => o.sku === p.sku && o.status === 'shipped').reduce((n, o) => n + o.quantity, 0);
    return Number.isSafeInteger(p.physical) && Number.isSafeInteger(p.reserved) &&
      p.physical >= 0 && p.reserved >= 0 && available(p) >= 0 &&
      p.reserved === reserved && p.physical === p.initial - shipped;
  });
}
export function apply(state, event) {
  const fail = (code, message) => ({ok: false, code, message, state});
  if (!event || !/^DEMO-[A-Z0-9-]{1,60}$/.test(event.id || '') || !/^DEMO-[A-Z0-9-]{1,60}$/.test(event.orderId || ''))
    return fail('invalid', 'Referência de demonstração inválida.');
  if (!['reserve', 'ship', 'cancel'].includes(event.type) || !ACTORS.includes(event.actor))
    return fail('invalid', 'Operação ou operador inválido.');
  const signature = JSON.stringify([event.type, event.orderId, event.sku ?? null, event.quantity ?? null, event.actor, event.channel ?? null]);
  const prior = state.events.find(e => e.id === event.id);
  if (prior) return prior.signature === signature
    ? {ok: true, code: 'duplicate', message: 'Evento já aplicado. Saldo e histórico preservados.', state}
    : fail('event_conflict', 'A referência já foi usada com outro conteúdo. Nada foi alterado.');
  const next = structuredClone(state);
  let order = next.orders.find(o => o.id === event.orderId);
  let product;
  if (event.type === 'reserve') {
    if (order) return fail('order_conflict', 'Pedido já existe. Nada foi reservado novamente.');
    product = next.products.find(p => p.sku === event.sku);
    if (!product || !CHANNELS.includes(event.channel) || !Number.isSafeInteger(event.quantity) || event.quantity < 1)
      return fail('invalid', 'Escolha um SKU e uma quantidade inteira positiva.');
    if (event.quantity > available(product)) return fail('insufficient', 'Reserva recusada: saldo disponível insuficiente.');
    product.reserved += event.quantity;
    order = {id: event.orderId, sku: event.sku, quantity: event.quantity, actor: event.actor, channel: event.channel, status: 'reserved'};
    next.orders.push(order);
  } else {
    if (!order || order.status !== 'reserved') return fail('state', 'Somente pedidos reservados podem ser confirmados ou cancelados.');
    product = next.products.find(p => p.sku === order.sku);
    product.reserved -= order.quantity;
    if (event.type === 'ship') product.physical -= order.quantity;
    order.status = event.type === 'ship' ? 'shipped' : 'cancelled';
  }
  next.events.push({...event, signature, physical: product.physical, reserved: product.reserved, available: available(product)});
  if (!reconcile(next)) return fail('invariant', 'Conferência inconsistente. Operação descartada.');
  return {ok: true, code: 'applied', message: 'Operação simulada registrada. Conferência de saldo aprovada.', state: next};
}
export function runScenario() {
  let state = createState();
  const checks = [];
  const record = (name, pass, expected, observed) => checks.push({name, pass, expected, observed});
  const event = (id, type, orderId, extra = {}) => ({id, type, orderId, actor: ACTORS[0], ...extra});
  const send = e => {const r = apply(state, e); state = r.state; return r;};
  const p = () => state.products[0];
  const first = event('DEMO-E1', 'reserve', 'DEMO-P1', {sku: CATALOG[0].sku, quantity: 12, channel: CHANNELS[0]});
  let result = send(first);
  record('Reserva mantém o saldo físico', result.ok && p().physical === 160 && p().reserved === 12 && available(p()) === 148, '160 físico / 12 reservado / 148 disponível', `${p().physical} / ${p().reserved} / ${available(p())}`);
  record('Radar sinaliza 150 unidades ou menos', available(p()) <= 150, 'Alerta visual em 148', String(available(p())));
  result = send(event('DEMO-E2', 'reserve', 'DEMO-P2', {sku: CATALOG[0].sku, quantity: 149, channel: CHANNELS[1], actor: ACTORS[1]}));
  record('Excesso de reserva é recusado', result.code === 'insufficient' && available(p()) === 148, 'Recusado; disponível 148', result.code);
  const before = state.events.length;
  result = send(first);
  record('Repetição não duplica reserva', result.code === 'duplicate' && state.events.length === before && p().reserved === 12, 'Uma reserva / um evento', `${p().reserved} reservado / ${state.events.length} evento`);
  result = send({...first, quantity: 13});
  record('Mesmo ID com outro conteúdo é recusado', result.code === 'event_conflict' && p().reserved === 12, 'Conflito; saldo preservado', result.code);
  result = send(event('DEMO-E3', 'cancel', 'DEMO-P1'));
  record('Cancelamento libera somente a reserva', result.ok && p().physical === 160 && p().reserved === 0, '160 físico / 0 reservado', `${p().physical} / ${p().reserved}`);
  send(event('DEMO-E4', 'reserve', 'DEMO-P3', {sku: CATALOG[0].sku, quantity: 10, channel: CHANNELS[1], actor: ACTORS[1]}));
  result = send(event('DEMO-E5', 'ship', 'DEMO-P3', {actor: ACTORS[1]}));
  record('Saída baixa físico e reservado juntos', result.ok && p().physical === 150 && p().reserved === 0 && available(p()) === 150, '150 físico / 0 reservado / 150 disponível', `${p().physical} / ${p().reserved} / ${available(p())}`);
  result = send(event('DEMO-E6', 'cancel', 'DEMO-P3'));
  record('Pedido expedido não pode ser cancelado', result.code === 'state' && p().physical === 150, 'Recusado; físico 150', result.code);
  record('Outros SKUs permanecem isolados', state.products.slice(1).every(x => x.physical === x.initial && x.reserved === 0), 'Bolsa 12 / boné 5', state.products.slice(1).map(available).join(' / '));
  record('Histórico e saldo são conciliáveis', reconcile(state), 'Nenhuma divergência', reconcile(state) ? 'Conciliado' : 'Divergente');
  return {state, checks};
}
