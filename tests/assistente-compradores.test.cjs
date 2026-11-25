'use strict';
// NODE_PATH=/tmp/assistente-qa-deps/node_modules node --test tests/assistente-compradores.test.cjs
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs'), path = require('node:path');
const root = path.join(__dirname,'..');
const api = require('../js/assistente-compradores.js');
const html = fs.readFileSync(path.join(root,'ferramentas/assistente-virtual.html'),'utf8');
const js = fs.readFileSync(path.join(root,'js/assistente-compradores.js'),'utf8');
const { JSDOM } = require('jsdom');
function load(q='') { const dom = new JSDOM(html,{runScripts:'outside-only',url:'https://praia.digital/ferramentas/assistente-virtual.html'+q}); const w=dom.window;w.eval(js);const get=id=>w.document.getElementById(id);return {w,get,dom}; }
test('Different budgets produce different summaries',()=>{assert.notEqual(api.summary({city:'Santos',budget:800000}),api.summary({city:'Santos',budget:200000}));assert.match(api.summary({budget:800000}),/800\.000/);});
test('Missing or invalid budgets do not invent values',()=>{for(const budget of ['',-1,Infinity,1e10,'abc'])assert.match(api.summary({budget}),/Orçamento máximo: a definir/);});
test('Bertioga and investment topics coexist',()=>{const answers=api.guidance('Procuro casa em condomínio em Bertioga para temporada');assert.equal(answers.length,2);assert.match(answers[0].text,/Bertioga/);assert.match(answers[1].text,/retorno garantido/);});
test('Negation does not produce a credit recommendation',()=>{for(const q of ['Quero investir sem financiamento','Não quero financiar','Compra à vista']) {const a=api.guidance(q);assert.ok(a.some(x=>x.text.includes('sem financiamento')));assert.ok(!a.some(x=>x.text.includes('Custo Efetivo Total')));}});
test('FGTS still receives eligibility caveat with cash purchase',()=>assert.ok(api.guidance('Compra à vista usando FGTS').some(x=>x.text.includes('FGTS'))));
test('Sources link rather than invented rates',()=>{assert.ok(api.guidance('Financiamento e FGTS').some(x=>x.url==='#fontes'));for(const word of ['15%','8-12%','595 mil','GA4_MEASUREMENT_ID'])assert.ok(!html.includes(word)&&!js.includes(word));});
test('Profile submission prepares local preview, no outbound call',()=>{const {w,get}=load();let calls=0;w.open=()=>calls++;get('buyer-city').value='Santos';get('buyer-budget').value='800000';get('buyer-profile').dispatchEvent(new w.Event('submit',{cancelable:true}));assert.equal(get('buyer-preview').hidden,false);assert.match(get('buyer-summary').value,/Santos/);assert.equal(calls,0);assert.equal(w.localStorage.length,0);w.close();});
test('Changed profile invalidates old summary',()=>{const {w,get}=load();get('buyer-profile').dispatchEvent(new w.Event('submit',{cancelable:true}));get('buyer-city').dispatchEvent(new w.Event('input',{bubbles:true}));assert.equal(get('buyer-preview').hidden,true);assert.equal(get('buyer-summary').value,'');w.close();});
test('Email includes only reviewed summary, safely encoded',()=>{const {w,get}=load();let opened;w.open=(...a)=>opened=a;get('buyer-summary').value='Olá! A&B #1';get('buyer-whatsapp').click();assert.equal(new URL(opened[0]).searchParams.get('body'),'Olá! A&B #1');assert.equal(new URL(opened[0]).pathname,'comercial@praia.digital');assert.match(opened[2],/noopener/);assert.match(get('buyer-status').textContent,/não confirma entrega/);w.close();});
test('Empty summary cannot open an email',()=>{const {w,get}=load();w.open=()=>assert.fail('unexpected open');get('buyer-whatsapp').click();assert.match(get('buyer-status').textContent,/Preencha/);w.close();});
test('Untrusted query only prefills and is length bounded',()=>{const {w,get}=load('?q='+encodeURIComponent('<img src=x onerror=alert(1)>'.repeat(100)));assert.equal(get('msg').value.length,2000);assert.equal(get('chat').children.length,0);assert.equal(w.document.querySelectorAll('#chat img').length,0);w.close();});
test('Chat renders user text without HTML execution',()=>{const {w,get}=load();get('msg').value='<img src=x onerror=alert(1)> & "';get('buyer-ask').click();assert.equal(get('chat').querySelectorAll('img').length,0);assert.match(get('chat').textContent,/<img/);assert.ok(get('chat').querySelector('a'));w.close();});
test('Chip prefills only; Enter sends and Shift Enter does not',()=>{const {w,get}=load();w.document.querySelector('[data-q]').click();assert.match(get('msg').value,/Bertioga/);assert.equal(get('chat').children.length,0);get('msg').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Enter',shiftKey:true,cancelable:true}));assert.equal(get('chat').children.length,0);get('msg').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Enter',cancelable:true}));assert.ok(get('chat').children.length>=2);w.close();});
test('Composition Enter does not submit',()=>{const {w,get}=load();get('msg').value='teste';get('msg').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Enter',isComposing:true,cancelable:true}));assert.equal(get('chat').children.length,0);w.close();});
test('Clear deletes local profile, question, summary and chat',()=>{const {w,get}=load();get('msg').value='teste';get('buyer-ask').click();get('buyer-city').value='Santos';get('buyer-clear').click();for(const id of ['buyer-city','msg','buyer-summary'])assert.equal(get(id).value,'');assert.equal(get('chat').children.length,0);assert.equal(get('buyer-preview').hidden,true);w.close();});
test('Copy failure provides manual fallback',async()=>{const {w,get}=load();get('buyer-summary').value='Meu resumo';get('buyer-copy').click();await new Promise(r=>setTimeout(r,0));assert.match(get('buyer-status').textContent,/manualmente/);w.close();});
test('All in-page references exist; single footer marker',()=>{const {w}=load();for(const a of w.document.querySelectorAll('a[href^="#"]'))assert.ok(w.document.querySelector(a.getAttribute('href')),a.href);assert.equal(w.document.querySelectorAll('meta[name="pd-shared-footer"]').length,1);assert.equal(w.document.querySelectorAll('h1').length,1);w.close();});
test('Local transcript stays bounded',()=>{const {w,get}=load();for(let i=0;i<30;i++){get('msg').value='Bertioga temporada';get('buyer-ask').click();}assert.ok(get('chat').children.length<=36);w.close();});

test('a reviewed visit question reaches the addressed email once', () => {
  const {w, get} = load();
  let destination;
  w.open = href => { destination = new URL(href); };
  get('buyer-visit').value = 'A vaga A&B está disponível?';
  get('buyer-profile').dispatchEvent(new w.Event('submit', {cancelable: true}));
  const summary = get('buyer-summary');
  assert.equal(summary.value.split('Pergunta para a visita:').length, 2);
  assert.ok(summary.value.includes(get('buyer-visit').value));
  summary.value = summary.value.replace('disponível', 'coberta');
  get('buyer-whatsapp').click();
  assert.equal(destination.pathname, 'comercial@praia.digital');
  assert.equal(destination.searchParams.get('body'), summary.value);
  get('buyer-clear').click();
  assert.equal(get('buyer-visit').value, '');
  w.close();
});
