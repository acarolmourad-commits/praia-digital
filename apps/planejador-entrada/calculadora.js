'use strict';
(function(root){
  const HORIZON=1200;
  const fields={valor:[0.01,1e9,'Informe valor do imóvel entre R$ 0,01 e R$ 1 bilhão.'],pct:[0,100,'Informe entrada entre 0% e 100%.'],guardado:[0,1e9,'Informe saldo reservado entre zero e R$ 1 bilhão.'],mensal:[0,1e9,'Informe aporte mensal entre zero e R$ 1 bilhão.'],rend:[0,100,'Informe rendimento mensal hipotético entre 0% e 100%.']};
  function calculate(values){
    const v={};
    for(const [id,[min,max,message]] of Object.entries(fields)){
      const raw=values[id],n=typeof raw==='number'?raw:(typeof raw==='string'&&raw.trim()!==''?Number(raw):NaN);
      if(!Number.isFinite(n)||n<min||n>max)return {error:message,field:id};
      v[id]=n;
    }
    const target=v.valor*v.pct/100,rate=v.rend/100;
    // Machine-precision tolerance only; never round each month's balance to currency.
    const reached=balance=>balance>=target||target-balance<=Number.EPSILON*Math.max(1,target)*32;
    let balance=v.guardado,elapsed=0;
    while(!reached(balance)&&elapsed<HORIZON){balance=balance*(1+rate)+v.mensal;elapsed++;}
    const contributed=v.guardado+elapsed*v.mensal;
    return {target,missing:Math.max(0,target-v.guardado),reached:reached(balance),months:reached(balance)?elapsed:null,elapsed,balance,contributed,interest:Math.max(0,balance-contributed)};
  }
  if(typeof module==='object'&&module.exports)module.exports={calculate,HORIZON};
  if(!root.document)return;
  const d=root.document,get=id=>d.getElementById(id),ids=Object.keys(fields);
  function clear(){get('res').hidden=true;get('erro').hidden=true;get('erro').textContent='';ids.forEach(id=>get(id).removeAttribute('aria-invalid'));}
  ids.forEach(id=>{get(id).addEventListener('input',clear);get(id).addEventListener('change',clear);});
  get('calcular').addEventListener('click',()=>{
    clear();const r=calculate(Object.fromEntries(ids.map(id=>[id,get(id).value])));
    if(r.error){get('erro').textContent=r.error;get('erro').hidden=false;get(r.field).setAttribute('aria-invalid','true');get(r.field).focus();return;}
    const fmt=n=>n.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
    for(const [id,key] of Object.entries({meta:'target',falta:'missing',guard:'contributed',juros:'interest',saldo:'balance'}))get(id).textContent=fmt(r[key]);
    get('tempo').textContent=!r.reached?'Não atingida em 1.200 meses':r.months===0?'Meta já coberta (0 meses)':r.months+' mês(es)';
    get('periodo').textContent=r.elapsed+' mês(es)';
    get('dica').textContent=!r.reached?'O horizonte terminou sem atingir a meta. Não foi calculada uma data de conclusão.':r.months===0?'A reserva informada já cobre a meta de entrada, não necessariamente os demais custos.':'Meta atingida apenas na projeção com estas premissas, sem garantia de resultado futuro.';
    get('res').hidden=false;
  });
})(typeof window==='undefined'?globalThis:window);
