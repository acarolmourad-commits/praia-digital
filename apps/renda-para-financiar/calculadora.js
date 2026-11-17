'use strict';
(function(root){
  const fields={valor:[0.01,1e9,'Informe um valor de imóvel entre R$ 0,01 e R$ 1 bilhão.'],entrada:[0,100,'Informe entrada entre 0% e 100%.'],taxa:[0,100,'Informe taxa anual entre 0% e 100%.'],prazo:[1,600,'Informe prazo inteiro entre 1 e 600 meses.'],pct:[0.01,100,'Informe percentual da renda entre 0,01% e 100%.']};
  function calculate(values){
    const v={};
    for(const [id,[min,max,message]] of Object.entries(fields)){
      const raw=values[id]; const n=typeof raw==='number'?raw:(typeof raw==='string'&&raw.trim()!==''?Number(raw):NaN);
      if(!Number.isFinite(n)||n<min||n>max||(id==='prazo'&&!Number.isInteger(n)))return {error:message,field:id};
      v[id]=n;
    }
    if(!['nominal','efetiva'].includes(values.tipoTaxa))return {error:'Selecione a convenção da taxa.',field:'tipoTaxa'};
    const i=values.tipoTaxa==='nominal'?v.taxa/1200:Math.expm1(Math.log1p(v.taxa/100)/12);
    const F=v.valor*(1-v.entrada/100),n=v.prazo;
    const sac=F/n+F*i;
    const price=i===0?F/n:F*i/(-Math.expm1(-n*Math.log1p(i)));
    const result={sac,price,rsac:sac/(v.pct/100),rprice:price/(v.pct/100),financed:F};
    if(!Object.values(result).every(Number.isFinite))return {error:'Não foi possível calcular com esses valores.',field:'valor'};
    return result;
  }
  if(typeof module==='object'&&module.exports)module.exports={calculate};
  if(!root.document)return;
  const d=root.document,ids=[...Object.keys(fields),'tipoTaxa'];
  const get=id=>d.getElementById(id);
  function clear(){get('res').hidden=true;get('erro').hidden=true;get('erro').textContent='';ids.forEach(id=>get(id).removeAttribute('aria-invalid'));}
  ids.forEach(id=>{get(id).addEventListener('input',clear);get(id).addEventListener('change',clear);});
  get('calcular').addEventListener('click',()=>{
    clear();const result=calculate(Object.fromEntries(ids.map(id=>[id,get(id).value])));
    if(result.error){get('erro').textContent=result.error;get('erro').hidden=false;get(result.field).setAttribute('aria-invalid','true');get(result.field).focus();return;}
    const fmt=v=>v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
    for(const [id,key] of Object.entries({sac1:'sac',price:'price',rsac:'rsac',rprice:'rprice'}))get(id).textContent=fmt(result[key]);
    get('dica').textContent=result.financed===0?'Entrada de 100%: não há saldo financiado neste cenário.':'Renda indicativa apenas para principal e juros. Inclua custos e outros compromissos na análise com a instituição.';
    get('res').hidden=false;
  });
})(typeof window==='undefined'?globalThis:window);
