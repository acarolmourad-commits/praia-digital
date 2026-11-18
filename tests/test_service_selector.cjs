'use strict';
const assert=require('node:assert/strict');
const {choices,recommend}=require('../js/servicos-seletor.js');
assert.equal(recommend('temporada','','ajuda'),null);
assert.equal(recommend('venda','precos','ajuda'),null);
assert.equal(recommend('temporada','anuncio',''),null);
assert.equal(recommend('__proto__','constructor','ajuda'),null);
assert.equal(recommend('temporada','anuncio','ajuda').href,'/servicos/anuncios-airbnb-booking.html');
assert.equal(recommend('venda','anuncio','ajuda').href,'/servicos/propaganda-imobiliaria.html');
assert.equal(recommend('temporada','precos','ajuda').href,'/anfitrioes/central-priceplabs.html#gestao-pricelabs');
let count=0;
for(const [objective,needs] of Object.entries(choices)) for(const [need,item] of Object.entries(needs)){
 for(const start of ['sozinho','ajuda']){
  const r=recommend(objective,need,start);
  assert.ok(r && r.href.startsWith('/') && !r.href.startsWith('//'));
  assert.equal(r.href,start==='sozinho'?item.free:item.paid);
  assert.ok(!r.href.includes('stripe')&&!r.href.includes('mailto'));
  count++;
 }
}
console.log('Rotas validadas: '+count+'; entradas incompletas e prioridades incompatíveis rejeitadas.');
