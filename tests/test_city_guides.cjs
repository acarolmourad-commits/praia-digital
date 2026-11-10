const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),data=require('../data/city-guides.json'),search=require('../js/property-search.js');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const expected=['ubatuba','caraguatatuba','sao-sebastiao','ilhabela','bertioga','guaruja','santos','sao-vicente','cubatao','praia-grande','mongagua','itanhaem','peruibe','iguape','ilha-comprida','cananeia'];
assert.deepEqual(data.cities.map(c=>c.slug).sort(),expected.sort());
assert.deepEqual(Object.values(Object.groupBy(data.cities,c=>c.region)).map(v=>v.length),[4,9,3]);
const titles=new Set(),descriptions=new Set();let checkedLinks=0;
const catalog=JSON.parse(read('js/main.js').match(/const properties = (\[[\s\S]*?\]);/)[1]);
for(const c of data.cities){
 const rel=`cidades/${c.slug}.html`,html=read(rel);
 assert.equal((html.match(/<h1\b/g)||[]).length,1,rel);
 assert.equal((html.match(/<main\b/g)||[]).length,1,rel);
 assert(!html.includes('\ufffd'),rel+' invalid encoding');
 const title=html.match(/<title>(.*?)<\/title>/)[1],desc=html.match(/name="description" content="([^"]+)"/)[1];
 assert(!titles.has(title));assert(!descriptions.has(desc));titles.add(title);descriptions.add(desc);
 assert(html.includes(`rel="canonical" href="https://praia.digital/${rel}"`));
 assert(html.includes(c.region));assert(html.includes('datetime="2026-11-02"'));
 const schema=JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
 const faq=schema['@graph'].find(s=>s['@type']==='FAQPage');
 assert.equal(faq.mainEntity.length,3);
 for(const q of faq.mainEntity){assert(html.includes(q.name));assert(html.includes(q.acceptedAnswer.text));}
 for(const id of ['conteudo','visao-geral','bairros','visita','analise','ferramentas','imoveis','fontes']) assert(html.includes(`id="${id}"`),rel+': '+id);
 const ctas=[...html.matchAll(/href="([^"<>]+)">Ver imóveis em /g)].map(m=>new URL(m[1],'https://praia.digital'));
 assert.equal(ctas.length,2,rel);
 for(const url of ctas){assert.equal(url.pathname,'/imoveis.html');assert.equal(url.searchParams.get('cidade'),c.name);}
 assert(search.cities.includes(c.name));
 assert.equal(search.parse(c.name).cidade,c.name);
 assert.equal(search.parse(search.normalize(c.name)).cidade,c.name);
 const state=search.fromParams(new URLSearchParams({cidade:c.name}));
 const actual=catalog.filter(p=>search.matches(p,state));
 assert(actual.every(p=>p.city===c.name));
 if(['cananeia','cubatao','iguape','ilha-comprida'].includes(c.slug)) assert.equal(actual.length,0);
}
for(const rel of ['cidades/index.html',...data.cities.map(c=>`cidades/${c.slug}.html`)]){
 const html=read(rel);
 for(const m of html.matchAll(/(?:href|src)="([^"<>]+)"/g)){
  const url=new URL(m[1].replace(/&amp;/g,'&'),'https://praia.digital/'+rel);
  if(url.origin!=='https://praia.digital')continue;
  let target=decodeURIComponent(url.pathname).slice(1);if(target.endsWith('/')||!target)target+='index.html';
  assert(fs.existsSync(path.join(root,target)),`${rel} broken target ${target}`);
  if(url.hash)assert(read(target).includes(`id="${url.hash.slice(1)}"`),`${target} missing ${url.hash}`);
  checkedLinks++;
 }
}
const home=read('cidades/index.html');assert.equal((home.match(/class="card city-card"/g)||[]).length,16);
assert(home.includes('Cubatão')&&home.includes('não tenha praia oceânica'));
const casa=catalog.find(p=>p.id===9),lancamento=catalog.find(p=>p.id===10);
assert.equal(casa.price,'R$ 595.000');assert.equal(casa.bedrooms,'2');assert.equal(casa.area,'105m²');
assert.equal(lancamento.price,'R$ 2.500.000');assert.equal(lancamento.bedrooms,'4');
for(const p of [casa,lancamento])assert(!/modelo|fict[ií]ci|demonstra[cç][aã]o/i.test(p.description));
assert(read('cidades/bertioga.html').includes('/imoveis/casas-lancamento-sao-lourenco.html'));
assert(read('cidades/bertioga.html').includes('/casa-condominio-fechado-bertioga.html'));
console.log(`16 guides, regions 4/9/3, metadata, schemas, ${checkedLinks} local targets/anchors, 16 city filters and listing regression passed.`);

// Owner requested withdrawal of the old Bertioga rental, retaining existing offers and adding the authorized apartment.
assert(!catalog.some(p=>p.id===8||p.slug==='apartamento-alto-padrao-bertioga'));
assert.deepEqual(catalog.filter(p=>p.city==='Bertioga').map(p=>p.id).sort((a,b)=>a-b),[9,10,11,12,13,14,15,16]);
assert.equal(catalog.filter(p=>search.matches(p,search.fromParams(new URLSearchParams({cidade:'Bertioga',finalidade:'Aluguel'})))).length,0);
assert.equal(catalog.filter(p=>search.matches(p,search.fromParams(new URLSearchParams({cidade:'Bertioga',finalidade:'Venda'})))).length,8);
assert(!read('imoveis.html').includes('Apartamento alto padrão - Bertioga'));
assert(!read('encontrar-imovel.html').includes('apartamento-alto-padrao-bertioga'));
assert(!read('fix_broken_links.py').includes('apartamento-alto-padrao-bertioga'));
assert(!read('scripts/automation/generate_landings_safe.py').includes('apartamento-alto-padrao-bertioga'));
const withdrawn=read('leads/apartamento-alto-padrao-bertioga.html');
assert(withdrawn.includes('noindex, follow')&&withdrawn.includes('Anúncio removido'));
assert(!/application\/ld\+json|<form|wa.me|Unsplash|8.900|http-equiv="refresh"/i.test(withdrawn));
console.log('Withdrawn Bertioga rental absent; all eight real offers and empty rental filter preserved.');
