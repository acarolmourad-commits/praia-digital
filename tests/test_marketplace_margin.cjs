// Run: node tests/test_marketplace_margin.cjs
// Extract the actual calculator functions; do not duplicate production formulas.
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const html=fs.readFileSync(path.resolve(__dirname,'../apps/calculadora-precificacao-shopee/index.html'),'utf8');
const match=html.match(/function taxaShopee[\s\S]*?(?=function calc\()/);
if(!match) throw new Error('Calculator functions not found');
vm.runInThisContext(match[0]);
const assert=require('node:assert/strict');
assert.equal(precoParaMargem(43.2,'shopee',0,0,15),73.39);
assert.equal(precoParaMargem(10,'shopee',0,0,0),18.13);
assert.equal(precoParaMargem(10,'tiktok',0,0,15),18.67);
assert.equal(precoParaMargem(38,'tiktok',0,0,15),55.70);
assert.equal(precoParaMargem(38,'tiktok',10,0,15),63.77);
assert.equal(precoParaMargem(10,'tiktok',85,0,6),533.34);
assert.equal(taxaTikTok(45,0),8.50);
assert.equal(taxaTikTok(75,0),10.50);
assert.equal(taxaTikTok(45,10),13);
assert.equal(lucro(45,38,'tiktok',0,0).lucro,-1.50);
assert.deepEqual([4999n,5000n,5001n].map(c=>[tiktokTier(c).rate,tiktokTier(c).fixed]),
                 [[1000n,400n],[600n,600n],[600n,600n]]);
assert.deepEqual([49.99,50,50.01].map(p=>taxaTikTok(p,0)),[8.999,9,9.0006]);
for(const [cost,target,minPrice] of [
  [10,15,18.67], [38,15,55.70],
  [33.49,15,49.99], [33.50,15,50], [33.51,15,50.02],
  [35.99,10,49.99], [36,10,50], [36.01,10,50.02],
]){
  const result=precoParaMargem(cost,'tiktok',0,0,target);
  assert.equal(result,minPrice);
  const prev=(Math.round(result*100)-1)/100;
  assert(lucro(prev,cost,'tiktok',0,0).lucro/prev*100<target,'previous cent must fail');
  assert(lucro(result,cost,'tiktok',0,0).lucro/result*100>=target-1e-10);
}
assert.equal(precoParaMargem(0,'tiktok',0,0,0),4.45);
assert.equal(precoParaMargem(10.001,'tiktok',0,0,15),null);
assert.equal(precoParaMargem(10,'tiktok',100,0,15),null);
assert.equal(precoParaMargem(-1,'shopee',0,0,15),null);
assert.equal(precoParaMargem(10,'shopee',0,0,100),null);
let cases=0;
for(const pl of ['shopee','tiktok']) for(const c of [0,10,43.2,47.5,50,60,100,150,200]) for(const target of [0,10,15,30,70,90]){
 const price=precoParaMargem(c,pl,0,3,target);
 if(price===null) continue;
 assert(lucro(price,c,pl,0,3).lucro/price*100>=target-1e-8);
 for(let cent=1;cent<Math.round(price*100);cent++) assert(lucro(cent/100,c,pl,0,3).lucro/(cent/100)*100<target+1e-8);
 cases++;
}
console.log('PASS: both TikTok ranges, official examples, exact cents, affiliate and '+cases+' brute-force minimum-price cases.');
assert.equal(precoParaMargem(10,'invalid',0,0,15),null);
for (const value of [NaN,Infinity,-Infinity]) assert.equal(precoParaMargem(value,'shopee',0,0,15),null);
console.log('PASS: invalid platform and non-finite costs rejected');

// Exercise the actual UI script, not a duplicate of its calculations.
const ids=['plat','afWrap','custo','preco','afiliado','frete','margemAlvo','res','alerta','kLucro','kMargem','kTaxa','sugestao','detalheBody','calc-status','preco-label','tt-lower-range','tt-lower-fee','tt-upper-range','tt-upper-fee'];
const nodes=Object.fromEntries(ids.map(id=>[id,{value:'',style:{},textContent:'',innerHTML:'',className:'',listeners:{},classList:{values:new Set(),add(x){this.values.add(x)},remove(x){this.values.delete(x)},contains(x){return this.values.has(x)}},addEventListener(type,fn){(this.listeners[type]??=[]).push(fn)},scrollIntoView(){}}]));
const alerts=[];const context={document:{getElementById:id=>nodes[id]},alert:m=>alerts.push(m)};
vm.createContext(context);const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].find(m=>m[1].includes('function calc()'))[1];vm.runInContext(script,context);
function valid(){for(const [k,v]of Object.entries({plat:'shopee',custo:'40',preco:'70',afiliado:'10',frete:'0',margemAlvo:'15'}))nodes[k].value=v;context.calc();assert(nodes.res.classList.contains('show'));}
valid();
for(const id of ['plat','custo','preco','afiliado','frete','margemAlvo'])for(const event of ['input','change']){
 for(const fn of nodes[id].listeners[event]||[])fn();assert(!nodes.res.classList.contains('show'),id+' '+event+' must invalidate old result');valid();
}
nodes.preco.value='';context.calc();assert(!nodes.res.classList.contains('show'));assert(alerts.length);
valid();nodes.plat.value='invalid';context.calc();assert(!nodes.res.classList.contains('show'));
valid();nodes.custo.value='1e308';nodes.frete.value='1e308';context.calc();assert(!nodes.res.classList.contains('show'));
assert.equal(nodes['tt-lower-range'].textContent,'Abaixo de R$ 50,00');
assert.equal(nodes['tt-upper-range'].textContent,'A partir de R$ 50,00');
assert.equal(nodes['tt-lower-fee'].textContent,'10% + R$ 4,00 por item vendido');
assert.equal(nodes['tt-upper-fee'].textContent,'6% + R$ 6,00 por item vendido');
assert.match(html,/knowledge_id=24428156307201/);
assert.match(html,/<time datetime="2026-07-15">/);
assert.match(html,/sem arredondar as taxas intermediárias/);
assert.match(html,/valor extra é fixo e não representa uma taxa variável/);
assert.match(html,/id="afiliado"[^>]+value="0"/);
assert(!html.includes('6% + R$ 2,00 por pedido'));
for(const [k,v]of Object.entries({plat:'tiktok',custo:'38',preco:'45',afiliado:'0',frete:'0',margemAlvo:'15'}))nodes[k].value=v;
for(const fn of nodes.plat.listeners.change)fn();
assert.match(nodes['preco-label'].textContent,/desconto do vendedor/);
context.calc();
assert.equal(nodes.kLucro.textContent,'R$ -1,50');
assert.equal(nodes.kTaxa.textContent,'R$ 8,50');
assert.match(nodes.sugestao.textContent,/R\$ 55,70/);
assert.doesNotMatch(nodes.detalheBody.innerHTML,/Comissão de afiliado/);
nodes.afiliado.value='10';
for(const fn of nodes.afiliado.listeners.input)fn();
assert(!nodes.res.classList.contains('show'));
context.calc();
assert.equal(nodes.kLucro.textContent,'R$ -6,00');
assert.equal(nodes.kTaxa.textContent,'R$ 8,50');
assert.match(nodes.detalheBody.innerHTML,/Comissão de afiliado \(10%\).*R\$ 4,50/);
assert.match(nodes.sugestao.textContent,/R\$ 63,77/);
nodes.preco.value='45.001';
context.calc();
assert(!nodes.res.classList.contains('show'));
assert.match(alerts.at(-1),/duas casas decimais/);
console.log('PASS: all pricing inputs invalidate, invalid platform/overflow do not leave stale results.');
