const fs=require('node:fs');
const assert=require('node:assert/strict');
const main=fs.readFileSync('js/main.js','utf8');
const properties=JSON.parse(main.match(/const properties = (\[[\s\S]*?\n    \]);/)[1]);
const removed=['apartamento-vista-mar-santos','casa-duplex-guaruja','studio-moderno-praia-grande','cobertura-duplex-sao-vicente','casa-terrea-itanhaem','apartamento-compacto-mongagua'];
assert(properties.every(p=>![1,2,3,4,5,6].includes(p.id)));
for(const id of [9,10,11,12,13]) assert(properties.some(p=>p.id===id&&p.city==='Bertioga'));
for(const path of ['imoveis.html','encontrar-imovel.html']) {
 const html=fs.readFileSync(path,'utf8');
 for(const match of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
  const data=JSON.parse(match[1]);
  if(data['@type']==='ItemList') for(const item of data.itemListElement) assert(!removed.some(slug=>item.url.endsWith('/'+slug+'.html')));
 }
}
console.log('Confirmed catalog removal and retained Bertioga listings: passed');
