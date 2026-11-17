const {test}=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const {calculate:c}=require('../apps/custo-de-compra/calculadora.js');
const base={valor:500000,itbi:10000,escritura:2500,registro:2000,banco:1500,outros:500};
test('sum only provided costs, reference price not added',()=>{assert.deepEqual(c(base),{total:16500,ratio:3.3000000000000003});const r=c({...base,valor:250000});assert.equal(r.total,16500);assert(Math.abs(r.ratio-6.6)<1e-12);});
test('all costs explicit zero accepted',()=>assert.deepEqual(c({valor:1,itbi:0,escritura:0,registro:0,banco:0,outros:0}),{total:0,ratio:0}));
test('each required blank/invalid/negative and boundary rejected',()=>{for(const id of Object.keys(base))for(const val of ['', ' ',null,undefined,NaN,Infinity,-1,'abc',1e9+1])assert(c({...base,[id]:val}).error,id);assert(c({...base,valor:0}).error);assert(c({...base,valor:.001}).error);});
test('finite max costs, minimum reference, decimals',()=>{const r=c({valor:.01,itbi:1e9,escritura:1e9,registro:1e9,banco:1e9,outros:1e9});assert.equal(r.total,5e9);assert(Number.isFinite(r.ratio));const tiny=c({valor:100,itbi:.1,escritura:.2,registro:0,banco:0,outros:0});assert(Math.abs(tiny.total-.3)<1e-15);});
test('DOM starts blank, errors focused, all edits clear and recovery works',()=>{
 const es={};for(const id of [...Object.keys(base),'res','erro','calcular','total','pct'])es[id]={value:'',hidden:true,textContent:'',events:{},attrs:{},addEventListener(n,f){this.events[n]=f;},setAttribute(k,v){this.attrs[k]=v;},removeAttribute(k){delete this.attrs[k];},focus(){this.focused=true;}};
 vm.runInNewContext(fs.readFileSync(require.resolve('../apps/custo-de-compra/calculadora.js'),'utf8'),{document:{getElementById:id=>es[id]}});
 const click=es.calcular.events.click;click();assert.equal(es.res.hidden,true);assert.equal(es.erro.hidden,false);assert(es.valor.focused);
 for(const id of Object.keys(base))es[id].value=String(base[id]);click();assert.equal(es.res.hidden,false);
 for(const id of Object.keys(base))for(const e of ['input','change']){es[id].events[e]();assert.equal(es.res.hidden,true);click();assert.equal(es.res.hidden,false);}
 es.itbi.value='';click();assert.equal(es.res.hidden,true);assert.equal(es.itbi.attrs['aria-invalid'],'true');es.itbi.value='0';es.itbi.events.input();click();click();assert.equal(es.res.hidden,false);assert.equal(es.erro.hidden,true);assert.equal(es.itbi.attrs['aria-invalid'],undefined);
});
