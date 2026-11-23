'use strict';
(function(root){
 const fields={valor:[.01,1e9,'Informe valor do imóvel entre R$ 0,01 e R$ 1 bilhão.'],diaria:[0,1e9,'Informe diária entre zero e R$ 1 bilhão.'],noites:[0,31,'Informe noites inteiras entre 0 e 31.'],taxa:[0,100,'Informe taxa entre 0% e 100%.'],custos:[0,1e9,'Informe despesas da temporada entre zero e R$ 1 bilhão.'],anual:[0,1e9,'Informe receita mensal do contrato anual entre zero e R$ 1 bilhão.'],custosAnual:[0,1e9,'Informe despesas mensais do contrato anual entre zero e R$ 1 bilhão.']};
 function calculate(values){
  const v={};for(const [id,[min,max,message]] of Object.entries(fields)){
   const raw=values[id],n=typeof raw==='number'?raw:(typeof raw==='string'&&raw.trim()!==''?Number(raw):NaN);
   if(!Number.isFinite(n)||n<min||n>max||(id==='noites'&&!Number.isInteger(n)))return {error:message,field:id};v[id]=n;
  }
  const gross=v.diaria*v.noites,season=gross*(1-v.taxa/100)-v.custos,annual=v.anual-v.custosAnual;
  const result={gross,annualGross:v.anual,season,annual,season12:season*12,annual12:annual*12,seasonRatio:season*12/v.valor*100,annualRatio:annual*12/v.valor*100};
  if(!Object.values(result).every(Number.isFinite))return {error:'Não foi possível calcular valores finitos.',field:'valor'};
  result.outcome=Math.round(season*100)===Math.round(annual*100)?'tie':season>annual?'season':'annual';return result;
 }
 if(typeof module==='object'&&module.exports)module.exports={calculate};
 if(!root.document)return;
 const get=id=>root.document.getElementById(id),ids=Object.keys(fields);
 function clear(){get('res').hidden=true;get('erro').hidden=true;get('erro').textContent='';ids.forEach(id=>get(id).removeAttribute('aria-invalid'));}
 ids.forEach(id=>{get(id).addEventListener('input',clear);get(id).addEventListener('change',clear);});
 get('calcular').addEventListener('click',()=>{
  clear();const r=calculate(Object.fromEntries(ids.map(id=>[id,get(id).value])));
  if(r.error){get('erro').textContent=r.error;get('erro').hidden=false;get(r.field).setAttribute('aria-invalid','true');get(r.field).focus();return;}
  const fmt=n=>n.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
  for(const [id,key] of Object.entries({bt:'gross',ba:'annualGross',lt:'season',la:'annual',at:'season12',aa:'annual12'}))get(id).textContent=fmt(r[key]);
  get('yt').textContent=r.seasonRatio.toLocaleString('pt-BR',{maximumFractionDigits:1})+'%';get('ya').textContent=r.annualRatio.toLocaleString('pt-BR',{maximumFractionDigits:1})+'%';
  get('dica').textContent=r.outcome==='tie'?'Os saldos do mês são iguais na precisão exibida.':r.outcome==='season'?'A temporada tem saldo maior neste mês hipotético, considerando apenas as despesas informadas.':'O contrato anual tem saldo maior neste mês hipotético, considerando apenas as despesas informadas.';
  get('res').hidden=false;
 });
})(typeof window==='undefined'?globalThis:window);
