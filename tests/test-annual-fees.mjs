import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html=fs.readFileSync(process.argv[2]||'ferramentas/estimativa-faturamento-anual-airbnb-2026.html','utf8');
const script=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('function calculate()'));
assert.ok(script,'Annual calculator script must exist');
async function run(mode,platform,admin){
 const elements={};const values={noites:'365',estadia:'3',cenario:'base',quartos:'2',hospedes:'4',modo:mode,diaria:'320',ocupacao:'60',taxa:String(platform),admin:String(admin),limpeza:'0',lavanderia:'0',condominio:'0',energia:'0',agua:'0',internet:'0',manutencao:'0',reposicao:'0',iptu:'0',seguro:'0',outros:'0'};
 [[90,450,75],[90,320,60],[150,240,40],[35,550,80]].forEach((x,i)=>{values['dias'+i]=String(x[0]);values['d'+i]=String(x[1]);values['o'+i]=String(x[2]);});
 const el=id=>elements[id]??= {value:values[id]??'',validity:{valid:true},textContent:'',innerHTML:'',listeners:{},addEventListener(t,fn){this.listeners[t]=fn;}};
 const copied=[];vm.runInNewContext(script,{document:{getElementById:el,querySelector:()=>({textContent:'field'})},Intl,window:{print(){}},navigator:{clipboard:{writeText:async s=>copied.push(s)}}});
 const submit=()=>el('sim').listeners.submit({preventDefault(){}});
 submit();submit();
 if(Number(platform)+Number(admin)>100){assert.match(el('erro').textContent,/não pode ultrapassar 100%/);assert.doesNotMatch(el('resultado').innerHTML,/class="metric"/);await el('compartilhar').listeners.click();assert.equal(copied.length,0);el('taxa').value='16';el('admin').value='0';submit();assert.equal(el('erro').textContent,'');assert.match(el('resultado').innerHTML,/class="metric"/);el('admin').value='85';submit();await el('compartilhar').listeners.click();assert.equal(copied.length,0,'Must clear stale summary after invalid resubmit');}
 else {assert.equal(el('erro').textContent,'');assert.match(el('resultado').innerHTML,/class="metric"/);await el('compartilhar').listeners.click();assert.equal(copied.length,1);}
}
for(const mode of ['simples','sazonal'])for(const pair of [[16,85],[100,100],[16,84],[0,0],[16,0],[16.1,84]])await run(mode,...pair);
console.log('PASS 12 scenarios: combined fee limits, boundary, repeated submit, recovery and stale-summary suppression');
