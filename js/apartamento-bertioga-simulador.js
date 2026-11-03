/* Cenários matemáticos ilustrativos. Sem pressupor renda observada. */
(function(root){
  'use strict';
  function valid(n,min,max){ return typeof n === 'number' && Number.isFinite(n) && n>=min && n<=max; }
  function rental(price,daily,occupancy,variable,fixed){
    if(!valid(price,1,1e8)||!valid(daily,0,1e5)||!valid(occupancy,0,100)||!valid(variable,0,100)||!valid(fixed,0,1e6)) throw new RangeError('Revise os campos e respeite os limites indicados.');
    const nights=365*occupancy/100, gross=nights*daily, net=gross*(1-variable/100)-fixed*12;
    return {nights,gross,net,yield:net/price*100,payback:net>0?price/net:null};
  }
  function appreciation(price,rate,years){
    if(!valid(price,1,1e8)||!valid(rate,-100,100)||!valid(years,1,30)||!Number.isInteger(years)) throw new RangeError('Informe um preço válido, taxa entre −100% e 100% e prazo inteiro de 1 a 30 anos.');
    const value=price*Math.pow(1+rate/100,years);
    return {value,change:value-price,percentage:(value/price-1)*100};
  }
  if(typeof module==='object' && module.exports) module.exports={rental,appreciation};
  if(!root.document) return;
  const d=root.document, el=id=>d.getElementById(id), number=id=>{const v=el(id).value.trim();return v===''?NaN:Number(v);};
  const money=n=>n.toLocaleString('pt-BR',{style:'currency',currency:'BRL'}), num=n=>n.toLocaleString('pt-BR',{maximumFractionDigits:2});
  function result(target,rows){
    el(target).replaceChildren(...rows.map(([label,value])=>{const box=d.createElement('div'),small=d.createElement('small'),strong=d.createElement('strong');box.className='result';small.textContent=label;strong.textContent=value;box.append(small,strong);return box;}));
  }
  function calculateRental(){
    try{const x=rental(number('price'),number('daily'),number('occupancy'),number('variable'),number('fixed'));el('rental-error').textContent='';result('rental-results',[
      ['Noites equivalentes por ano',num(x.nights)],['Receita bruta anual',money(x.gross)],['Resultado operacional anual',money(x.net)],['Retorno operacional sobre o preço',num(x.yield)+'% a.a.'],['Retorno simples do preço',x.payback===null?'Não há retorno com resultado não positivo':num(x.payback)+' anos']]);
    }catch(e){el('rental-results').replaceChildren();el('rental-error').textContent=e.message;}
  }
  function calculateValue(){
    try{const x=appreciation(number('price'),number('rate'),number('years'));el('value-error').textContent='';result('value-results',[['Preço no cenário hipotético',money(x.value)],['Variação nominal',money(x.change)],['Variação acumulada',num(x.percentage)+'%']]);
    }catch(e){el('value-results').replaceChildren();el('value-error').textContent=e.message;}
  }
  el('rental-form').addEventListener('submit',event=>{event.preventDefault();calculateRental();calculateValue();});
  el('value-form').addEventListener('submit',event=>{event.preventDefault();calculateValue();});
  for(const id of ['price','daily','occupancy','variable','fixed']) el(id).addEventListener('input',()=>{calculateRental();if(id==='price')calculateValue();});
  for(const id of ['rate','years']) el(id).addEventListener('input',calculateValue);
  calculateRental();calculateValue();
})(typeof globalThis!=='undefined'?globalThis:this);
