import test from 'node:test';
import assert from 'node:assert/strict';
import {createState, apply, reconcile, available, runScenario, CATALOG, ACTORS, CHANNELS} from '../ia/marketplaces/piloto/modelo.mjs';
const reserve = (overrides = {}) => ({id:'DEMO-E1',orderId:'DEMO-P1',type:'reserve',sku:CATALOG[0].sku,quantity:12,actor:ACTORS[0],channel:CHANNELS[0],...overrides});
test('roteiro completo produz 10 evidências e saldo reconciliado', () => {
  const {state, checks} = runScenario(); assert.equal(checks.length,10); assert.ok(checks.every(c=>c.pass));
  assert.equal(state.products[0].physical,150); assert.equal(state.products[0].reserved,0); assert.ok(reconcile(state));
});
test('reserva não altera a entrada e duplicidade é idempotente', () => {
  const initial=createState(), event=reserve(), result=apply(initial,event);
  assert.equal(initial.products[0].reserved,0); assert.equal(result.state.products[0].reserved,12);
  const replay=apply(result.state,event); assert.equal(replay.code,'duplicate'); assert.deepEqual(replay.state,result.state);
  const conflict=apply(result.state,reserve({quantity:13})); assert.equal(conflict.code,'event_conflict'); assert.deepEqual(conflict.state,result.state);
  assert.equal(apply(result.state,reserve({id:'DEMO-E2'})).code,'order_conflict');
});
test('quantidades e referências inválidas não alteram a base', () => {
  for(const quantity of [0,-1,1.5,NaN,Infinity,'12',Number.MAX_SAFE_INTEGER+1]) {
    const state=createState(),r=apply(state,reserve({quantity})); assert.equal(r.ok,false); assert.deepEqual(r.state,state);
  }
  for(const extra of [{sku:'inexistente'},{channel:'real'},{actor:'real'},{id:''},{orderId:'<script>'},{type:'refund'}]) assert.equal(apply(createState(),reserve(extra)).ok,false);
});
test('duas reservas sequenciais não compartilham a última unidade', () => {
  const r=apply(createState(),reserve({quantity:160}));assert.equal(available(r.state.products[0]),0);
  const next=apply(r.state,reserve({id:'DEMO-E2',orderId:'DEMO-P2',quantity:1,actor:ACTORS[1]}));
  assert.equal(next.code,'insufficient');assert.deepEqual(next.state,r.state);
});
test('saída e cancelamento preservam reservas de outros pedidos', () => {
  let s=apply(createState(),reserve()).state;
  s=apply(s,reserve({id:'DEMO-E2',orderId:'DEMO-P2',quantity:8})).state;
  s=apply(s,{id:'DEMO-E3',orderId:'DEMO-P1',type:'ship',actor:ACTORS[0]}).state;
  assert.equal(s.products[0].physical,148);assert.equal(s.products[0].reserved,8);
  s=apply(s,{id:'DEMO-E4',orderId:'DEMO-P2',type:'cancel',actor:ACTORS[0]}).state;
  assert.equal(s.products[0].physical,148);assert.equal(s.products[0].reserved,0);assert.ok(reconcile(s));
  assert.equal(apply(s,{id:'DEMO-E5',orderId:'DEMO-P2',type:'ship',actor:ACTORS[0]}).code,'state');
});
test('reinício cria uma base independente e detecta adulteração do saldo', () => {
  const a=createState(),b=createState();a.products[0].physical=3;assert.equal(b.products[0].physical,160);assert.equal(reconcile(a),false);
});
