'use strict';
(function(root){
 const labels={valor:'preço de referência',itbi:'ITBI informado',escritura:'custo de escritura/instrumento',registro:'total de registro',banco:'tarifas bancárias',outros:'outros custos'};
 function calculate(values){
  const v={};for(const id of Object.keys(labels)){
   const raw=values[id],n=typeof raw==='number'?raw:(typeof raw==='string'&&raw.trim()!==''?Number(raw):NaN),min=id==='valor'?.01:0;
   if(!Number.isFinite(n)||n<min||n>1e9)return {error:`Informe ${labels[id]} entre ${id==='valor'?'R$ 0,01':'zero'} e R$ 1 bilhão. O campo não pode ficar vazio.`,field:id};v[id]=n;
  }
  const total=v.itbi+v.escritura+v.registro+v.banco+v.outros,ratio=total/v.valor*100;
  if(!Number.isFinite(total)||!Number.isFinite(ratio))return {error:'Não foi possível calcular valores finitos.',field:'valor'};
  return {total,ratio};
 }
 if(typeof module==='object'&&module.exports)module.exports={calculate};
 if(!root.document)return;
 const get=id=>root.document.getElementById(id),ids=Object.keys(labels);
 function clear(){get('res').hidden=true;get('erro').hidden=true;get('erro').textContent='';ids.forEach(id=>get(id).removeAttribute('aria-invalid'));}
 ids.forEach(id=>{get(id).addEventListener('input',clear);get(id).addEventListener('change',clear);});
 get('calcular').addEventListener('click',()=>{
  clear();const r=calculate(Object.fromEntries(ids.map(id=>[id,get(id).value])));
  if(r.error){get('erro').textContent=r.error;get('erro').hidden=false;get(r.field).setAttribute('aria-invalid','true');get(r.field).focus();return;}
  get('total').textContent=r.total.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
  get('pct').textContent=r.ratio.toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})+'%';
  get('res').hidden=false;
 });
})(typeof window==='undefined'?globalThis:window);
