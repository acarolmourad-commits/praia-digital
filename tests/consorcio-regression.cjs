const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('apps/calculadora-consorcio/index.html','utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('function calcular'));
function run(values){const nodes={};for(const id of ['credito','prazo','taxa','lance','taxaFin','rParc','rTotC','rParcF','rTotF','rSave','rLance','result'])nodes[id]={value:String(values[id]??0),textContent:'',style:{}};
 const alerts=[];const ctx={document:{getElementById:id=>nodes[id]},alert:s=>alerts.push(s)};vm.createContext(ctx);vm.runInContext(script,ctx);ctx.calcular();return {nodes,alerts};}
const base={credito:120000,prazo:120,taxa:20,lance:25,taxaFin:0};
let r=run(base);assert.equal(r.alerts.length,0);assert.equal(r.nodes.rTotC.textContent,'R$ 144.000');assert.equal(r.nodes.rTotF.textContent,'R$ 120.000');assert.equal(r.nodes.rLance.textContent,'R$ 30.000');assert.match(r.nodes.rSave.textContent,/-24\.000/,'negative difference must not be hidden');
for(const change of [{lance:101},{taxa:-1},{taxaFin:-1},{prazo:1.5},{credito:0}]){r=run({...base,...change});assert.equal(r.alerts.length,1);assert.equal(r.nodes.result.style.display,undefined);}
console.log('Consorcio: zero interest, signed difference, separate bid and five invalid inputs passed');
