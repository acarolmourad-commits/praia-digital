const {test}=require('node:test'),assert=require('node:assert/strict');
const {calculate:c}=require('../apps/planejador-entrada/calculadora.js');
const base={valor:450000,pct:20,guardado:15000,mensal:2500,rend:0};
test('default: 30 end-of-month contributions, no return',()=>{const r=c(base);assert.equal(r.months,30);assert.equal(r.balance,90000);assert.equal(r.interest,0);});
test('interest precedes contribution; compare closed form',()=>{const r=c({valor:1000,pct:100,guardado:100,mensal:100,rend:1});const expected=100*1.01**r.months+100*Math.expm1(r.months*Math.log1p(.01))/.01;assert(Math.abs(r.balance-expected)<1e-8);assert(r.balance>=1000);assert((r.balance-100)/1.01<1000);});
test('zero contributions, reached and growing initial balance',()=>{assert.equal(c({...base,guardado:90000,mensal:0}).months,0);assert.equal(c({...base,guardado:95000,mensal:0}).interest,0);assert.equal(c({...base,pct:0,mensal:0}).months,0);assert.equal(c({valor:121,pct:100,guardado:100,mensal:0,rend:10}).months,2);});
test('unreached horizon is not a completion date',()=>{for(const changes of [{mensal:1,guardado:0},{mensal:0,guardado:0,rend:100},{mensal:0}]){const r=c({...base,...changes});assert.equal(r.months,null);assert.equal(r.reached,false);assert.equal(r.elapsed,1200);}assert.equal(c({...base,mensal:1,guardado:0}).balance,1200);});
test('exact horizon success, beyond horizon failure',()=>{assert.equal(c({valor:1200,pct:100,guardado:0,mensal:1,rend:0}).months,1200);assert.equal(c({valor:1201,pct:100,guardado:0,mensal:1,rend:0}).months,null);});
test('fractions avoid spurious extra month',()=>assert.equal(c({valor:1,pct:100,guardado:0,mensal:.1,rend:0}).months,10));
test('reject invalid and out-of-range values',()=>{for(const key of Object.keys(base)){for(const v of ['', ' ',null,undefined,NaN,Infinity,-1,'abc'])assert(c({...base,[key]:v}).error,key+' '+v);}for(const [key,v] of [['valor',0],['valor',1e9+1],['pct',100.01],['guardado',1e9+1],['mensal',1e9+1],['rend',100.01]])assert(c({...base,[key]:v}).error);});
test('all boundary results finite and repeated calls deterministic',()=>{for(const rend of [0,1e-12,100])for(const mensal of [0,.01,1e9]){const v={valor:1e9,pct:100,guardado:0,mensal,rend};const r=c(v);for(const n of Object.values(r).filter(x=>typeof x==='number'))assert(Number.isFinite(n));assert.deepEqual(c(v),r);}});
test('DOM hides stale result on every edit and recovers from invalid input',()=>{
  const fs=require('node:fs'),vm=require('node:vm');const elements={};
  for(const id of [...Object.keys(base),'res','erro','calcular','meta','falta','guard','juros','saldo','tempo','periodo','dica'])elements[id]={value:String(base[id]??''),hidden:true,textContent:'',events:{},attrs:{},addEventListener(n,fn){this.events[n]=fn;},setAttribute(k,v){this.attrs[k]=v;},removeAttribute(k){delete this.attrs[k];},focus(){this.focused=true;}};
  vm.runInNewContext(fs.readFileSync(require.resolve('../apps/planejador-entrada/calculadora.js'),'utf8'),{document:{getElementById:id=>elements[id]}});
  const click=elements.calcular.events.click;click();assert.equal(elements.res.hidden,false);assert.equal(elements.tempo.textContent,'30 mês(es)');
  for(const id of Object.keys(base)){elements[id].events.input();assert.equal(elements.res.hidden,true);click();elements[id].events.change();assert.equal(elements.res.hidden,true);click();}
  elements.mensal.value='';click();assert.equal(elements.erro.hidden,false);assert.equal(elements.res.hidden,true);assert.equal(elements.mensal.attrs['aria-invalid'],'true');assert(elements.mensal.focused);
  elements.mensal.value='0';elements.guardado.value='90000';elements.mensal.events.input();click();assert.equal(elements.res.hidden,false);assert.equal(elements.erro.hidden,true);assert.match(elements.tempo.textContent,/0 meses/);click();assert.equal(elements.res.hidden,false);
});
