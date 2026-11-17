'use strict';
(function(root){
const fields={valor:[.01,1e9,'Informe valor inicial entre R$ 0,01 e R$ 1 bilhão.'],taxa:[-100,100,'Informe variação anual do imóvel entre −100% e 100%.'],anos:[1,50,'Informe prazo inteiro entre 1 e 50 anos.'],cdi:[-100,100,'Informe taxa anual comparativa entre −100% e 100%.']};
function calculate(values){
 const v={};for(const [id,[min,max,message]] of Object.entries(fields)){
 const raw=values[id],n=typeof raw==='number'?raw:(typeof raw==='string'&&raw.trim()!==''?Number(raw):NaN);
 if(!Number.isFinite(n)||n<min||n>max||(id==='anos'&&!Number.isInteger(n)))return {error:message,field:id};v[id]=n;
 }
 const future=rate=>rate===-100?0:v.valor*Math.exp(v.anos*Math.log1p(rate/100));
 const property=future(v.taxa),comparison=future(v.cdi);
 const delta=rate=>rate===-100?-v.valor:v.valor*Math.expm1(v.anos*Math.log1p(rate/100));
 const result={property,comparison,propertyGain:delta(v.taxa),comparisonGain:delta(v.cdi),years:v.anos};
 if(!Object.values(result).every(Number.isFinite))return {error:'Não foi possível calcular valores finitos.',field:'valor'};
 result.outcome=Math.round(property*100)===Math.round(comparison*100)?'tie':property>comparison?'property':'comparison';return result;
}
if(typeof module==='object'&&module.exports)module.exports={calculate};
if(!root.document)return;
const get=id=>root.document.getElementById(id),ids=[...Object.keys(fields),'cenario'];
function clear(){get('res').hidden=true;get('erro').hidden=true;get('erro').textContent='';ids.forEach(id=>get(id).removeAttribute('aria-invalid'));}
ids.forEach(id=>{get(id).addEventListener('input',clear);get(id).addEventListener('change',clear);});
for(const event of ['input','change'])get('taxa').addEventListener(event,()=>{get('cenario').value='custom';});
get('cenario').addEventListener('change',()=>{const c=get('cenario').value;if(['-5','0','5'].includes(c))get('taxa').value=c;});
get('calcular').addEventListener('click',()=>{
 clear();const r=calculate(Object.fromEntries(Object.keys(fields).map(id=>[id,get(id).value])));
 if(r.error){get('erro').textContent=r.error;get('erro').hidden=false;get(r.field).setAttribute('aria-invalid','true');get(r.field).focus();return;}
 const fmt=n=>n.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
 get('prazo').textContent=r.years;
 for(const [id,key] of Object.entries({vfImo:'property',vfCdi:'comparison',gImo:'propertyGain',gCdi:'comparisonGain'}))get(id).textContent=fmt(r[key]);
 get('dica').textContent=r.outcome==='tie'?'Os cenários têm o mesmo valor projetado na precisão exibida.':r.outcome==='property'?'O valor projetado do imóvel é maior nesta hipótese; isso não indica maior retorno líquido ou melhor investimento.':'O valor projetado do comparativo é maior nesta hipótese; isso não indica maior retorno líquido ou melhor investimento.';
 get('res').hidden=false;
});
})(typeof window==='undefined'?globalThis:window);
