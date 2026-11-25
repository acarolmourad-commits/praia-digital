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

// Shopee CNPJ: the low-price variable component replaces, rather than adds to, the fixed fee.
const shopeeCases=[[8,5.60],[8.99,6.293],[9,6.30],[9.01,6.302],
  [79.99,20.498],[80,27.20],[99.99,29.9986],[100,34],[199.99,47.9986],[200,54]];
for(const [price,fee] of shopeeCases) assert(Math.abs(taxaShopee(price)-fee)<1e-9,`Shopee fee at ${price}`);
const lowPrice=lucro(8,2,'shopee',0,0);
assert.equal(fmt(lowPrice.taxa),'R$ 5,60');
assert.equal(fmt(lowPrice.lucro),'R$ 0,40');
assert.equal(precoParaMargem(2,'shopee',0,0,5),8);
assert.equal(precoParaMargem(0,'shopee',0,0,30),0.01);
assert.equal(precoParaMargem(0,'shopee',0,0,86),null);
assert.equal(precoParaMargem(2,'shopee',0,0,90),null);

// Independent integer reference: fee rates and target are basis points, prices are cents.
function shopeeCnpjMeets(price,cost,extra,target){
  const [rate,fixed]=price<900?[7000,0]:price<8000?[2000,450]:
    price<10000?[1400,1600]:price<20000?[1400,2000]:[1400,2600];
  return price*(10000-rate-target)>=(cost+extra+fixed)*10000;
}
let shopeeMinimalityCases=0;
for(const cost of [0,1,155,200,269,270,271,500,4000,7900,12000]){
 for(const extra of [0,1,100]) for(const target of [0,500,1500,2500,2999,3000]){
  const estimate=precoParaMargem(cost/100,'shopee',0,extra/100,target/100);
  let cent=1;
  // These bounded fixtures can all meet their target by R$ 300 under the unchanged high-price tier.
  while(cent<=30000&&!shopeeCnpjMeets(cent,cost,extra,target))cent++;
  assert(cent<=30000,'fixture must be feasible within bound');
  assert.equal(estimate,cent/100,`minimum cents for Shopee CNPJ ${cost}/${extra}/${target}`);
  shopeeMinimalityCases++;
 }
}
assert.match(html,/<option value="shopee">Shopee \(CNPJ\)<\/option>/);
assert.match(html,/seller\.shopee\.com\.br\/edu\/article\/26839/);
console.log('PASS: Shopee CNPJ threshold, display precision, infeasibility and '+shopeeMinimalityCases+' exact cent minima.');
assert.equal(precoParaMargem(43.2,'shopee',0,0,15),73.39);
assert.equal(precoParaMargem(10,'shopee',0,0,0),18.13);
assert.equal(precoParaMargem(10,'tiktok',0,0,15),15.19);
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
console.log('PASS: 6 assertions + '+cases+' minimum-price cases verified in cents.');
assert.equal(precoParaMargem(10,'invalid',0,0,15),null);
for (const value of [NaN,Infinity,-Infinity]) assert.equal(precoParaMargem(value,'shopee',0,0,15),null);
console.log('PASS: invalid platform and non-finite costs rejected');

// Exercise the actual UI script, not a duplicate of its calculations.
const ids=['plat','afWrap','custo','preco','afiliado','frete','margemAlvo','res','alerta','kLucro','kMargem','kTaxa','sugestao','detalheBody','calc-status'];
const nodes=Object.fromEntries(ids.map(id=>[id,{value:'',style:{},textContent:'',innerHTML:'',className:'',listeners:{},classList:{values:new Set(),add(x){this.values.add(x)},remove(x){this.values.delete(x)},contains(x){return this.values.has(x)}},addEventListener(type,fn){(this.listeners[type]??=[]).push(fn)},scrollIntoView(){}}]));
const alerts=[];const context={document:{getElementById:id=>nodes[id]},alert:m=>alerts.push(m)};
vm.createContext(context);const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].find(m=>m[1].includes('function calc()'))[1];vm.runInContext(script,context);
function valid(){for(const [k,v]of Object.entries({plat:'shopee',custo:'40',preco:'70',afiliado:'10',frete:'0',margemAlvo:'15'}))nodes[k].value=v;context.calc();assert(nodes.res.classList.contains('show'));}
valid();
for(const id of ['plat','custo','preco','afiliado','frete','margemAlvo'])for(const event of ['input','change']){
 for(const fn of nodes[id].listeners[event]||[])fn();assert(!nodes.res.classList.contains('show'),id+' '+event+' must invalidate old result');valid();
}
for(const [k,v]of Object.entries({plat:'shopee',custo:'2',preco:'8',afiliado:'0',frete:'0',margemAlvo:'5'}))nodes[k].value=v;
context.calc();
assert(nodes.res.classList.contains('show'));
assert.equal(nodes.kTaxa.textContent,'R$ 5,60');
assert.equal(nodes.kLucro.textContent,'R$ 0,40');
assert.equal(nodes.kMargem.textContent,'5,0%');
assert.match(nodes.sugestao.textContent,/R\$ 8,00/);
nodes.preco.value='';context.calc();assert(!nodes.res.classList.contains('show'));assert(alerts.length);
valid();nodes.plat.value='invalid';context.calc();assert(!nodes.res.classList.contains('show'));
valid();nodes.custo.value='1e308';nodes.frete.value='1e308';context.calc();assert(!nodes.res.classList.contains('show'));
assert(html.includes('6% + R$ 2,00 por pedido + comissão de afiliado informada'));
console.log('PASS: all pricing inputs invalidate, invalid platform/overflow do not leave stale results.');
