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
assert.deepEqual(catalog.filter(p=>p.city==='Bertioga').map(p=>p.id).sort((a,b)=>a-b),[9,10,11,12,13,14,15,16,17,18,19,20,21,22]);
assert.equal(catalog.filter(p=>search.matches(p,search.fromParams(new URLSearchParams({cidade:'Bertioga',finalidade:'Aluguel'})))).length,0);
assert.equal(catalog.filter(p=>search.matches(p,search.fromParams(new URLSearchParams({cidade:'Bertioga',finalidade:'Venda'})))).length,14);
assert(!read('imoveis.html').includes('Apartamento alto padrão - Bertioga'));
assert(!read('encontrar-imovel.html').includes('apartamento-alto-padrao-bertioga'));
assert(!read('fix_broken_links.py').includes('apartamento-alto-padrao-bertioga'));
assert(!read('scripts/automation/generate_landings_safe.py').includes('apartamento-alto-padrao-bertioga'));
const withdrawn=read('leads/apartamento-alto-padrao-bertioga.html');
assert(withdrawn.includes('noindex, follow')&&withdrawn.includes('Anúncio removido'));
assert(!/application\/ld\+json|<form|wa.me|Unsplash|8.900|http-equiv="refresh"/i.test(withdrawn));
const sobrado=catalog.find(p=>p.id===21);
assert.equal(sobrado.slug,'sobrado-indaia-94m2');
const matches=params=>search.matches(sobrado,search.fromParams(new URLSearchParams(params)));
assert(matches({cidade:'Bertioga',finalidade:'Venda',tipo:'casa',quartos:'2',preco_max:'1500000'}));
assert(matches({q:'sobrado Indaiá 2 dormitórios',finalidade:'Venda'}));
assert(!matches({cidade:'Bertioga',finalidade:'Aluguel'}));
assert(!matches({cidade:'Bertioga',finalidade:'Venda',quartos:'3'}));
assert(!matches({cidade:'Bertioga',finalidade:'Venda',preco_max:'1499999'}));
const saoc=catalog.find(p=>p.id===22);
assert.equal(saoc.slug,'apartamento-vicente-carvalho-ii-saoc-45m2');
const matchesSaoc=params=>search.matches(saoc,search.fromParams(new URLSearchParams(params)));
assert(matchesSaoc({cidade:'Bertioga',finalidade:'Venda',tipo:'apartamento',quartos:'2',preco_max:'235000'}));
assert(!matchesSaoc({cidade:'Bertioga',finalidade:'Venda',tipo:'casa'}));
assert(!matchesSaoc({cidade:'Bertioga',finalidade:'Aluguel'}));
assert(!matchesSaoc({cidade:'Bertioga',finalidade:'Venda',preco_max:'234999'}));
console.log('Withdrawn Bertioga rental absent; fourteen real sale offers and the empty rental filter checked.');

const accessibleGuides=data.cities.filter(c=>c.accessibleBeachService);
assert.deepEqual(accessibleGuides.map(c=>c.slug),['caraguatatuba']);
const caragua=read('cidades/caraguatatuba.html');
const visitorSection=caragua.match(/<section id="visita">([\s\S]*?)<\/section>/)?.[1];
assert(visitorSection,'public visitor section is required');
assert.equal((caragua.match(/id="praia-acessivel"/g)||[]).length,1);
assert(visitorSection.includes('<article class="card" id="praia-acessivel" aria-labelledby="praia-acessivel-titulo">'));
assert(visitorSection.includes('<h3 id="praia-acessivel-titulo">Praia Acessível na Praia do Centro</h3>'));
for(const term of ['Praça da Cultura','banho de mar assistido e gratuito','pessoas com deficiência ou pessoas idosas','sábados e domingos, das 9h às 16h','cadastro simples no local','agendar com antecedência na SEPEDI','condições no dia'])
 assert(visitorSection.includes(term),'missing Praia Acessível visitor detail: '+term);
assert(visitorSection.includes('href="https://www.caraguatatuba.sp.gov.br/pmc/2025/06/praia-acessivel/"'));
assert(!/29\/11|Navegar Experience/i.test(visitorSection));
console.log('Praia Acessível municipal guidance present in Caraguatatuba visitor section only.');

const historicTourCities=data.cities.filter(c=>c.historicCenterTour);
assert.deepEqual(historicTourCities.map(c=>c.slug),['sao-sebastiao']);
const saoSebastiao=read('cidades/sao-sebastiao.html');
const saoSebastiaoVisit=saoSebastiao.match(/<section id="visita">([\s\S]*?)<\/section>/)?.[1];
assert(saoSebastiaoVisit,'public visitor section is required');
assert.equal((saoSebastiao.match(/id="visitas-centro-historico"/g)||[]).length,1);
for(const term of ['Visitas monitoradas ao Centro Histórico','gratuitas para grupos de turistas','Igreja Matriz','Casa da Cultura','Confirme os horários e a disponibilidade'])
 assert(saoSebastiaoVisit.includes(term),'missing Centro Histórico visitor detail: '+term);
assert(saoSebastiaoVisit.includes('href="tel:+551238924604">(12) 3892-4604'));
assert(saoSebastiaoVisit.includes('href="https://www.turismosaosebastiao.com.br/noticias/prefeitura-de-sao-sebastiao-oferece-visitas-monitoradas-pelo-centro-historico-para-estudantes-e-turistas"'));
assert(!/escolar|Seduc|(?:\d{1,2}h\b)/i.test(saoSebastiaoVisit.slice(saoSebastiaoVisit.indexOf('id="visitas-centro-historico"'))));
console.log('São Sebastião Centro Histórico visitor guidance present once with the official source and phone.');

const ilhaDianaCities=data.cities.filter(c=>c.ilhaDianaVisit);
assert.deepEqual(ilhaDianaCities.map(c=>c.slug),['santos']);
const santos=read('cidades/santos.html');
const ilhaDiana=santos.match(/<section id="visita">[\s\S]*?(<article class="card" id="ilha-diana"[\s\S]*?<\/article>)/)?.[1];
assert(ilhaDiana,'Ilha Diana card in public visitor section');
assert.equal((santos.match(/id="ilha-diana"/g)||[]).length,1);
for(const term of ['passeios agendados','conduzidos por moradores','manguezais','educação ambiental','atrás da Alfândega','Praça da República','confirme a ida e a volta'])
 assert(ilhaDiana.includes(term),'missing Ilha Diana detail: '+term);
assert.deepEqual([...ilhaDiana.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['https://www.turismosantos.com.br/pt-br/ilhadiana','https://www.santos.sp.gov.br/?q=node/163190']);
assert(!/\bR\$|\b\d{1,2}h\b|festival|gratuit|tel:|wa\.me|cetsantos\.com/i.test(ilhaDiana));
console.log('Ilha Diana visitor guidance present only in Santos, with stable official source links.');

assert.deepEqual(data.cities.filter(c=>c.localEntrepreneursCatalog).map(c=>c.slug),['ilhabela']);
const ilhabela=read('cidades/ilhabela.html');
const ilhabelaVisit=ilhabela.match(/<section id="visita">([\s\S]*?)<\/section>/)?.[1];
assert(ilhabelaVisit?.includes('Perequê é uma referência'));
const localCatalog=ilhabelaVisit.match(/<article class="card" id="o-negocio-delas"[\s\S]*?<\/article>/)?.[0];
assert(localCatalog,'Ilhabela public visitor section should include the local catalog');
assert.equal((ilhabela.match(/id="o-negocio-delas"/g)||[]).length,1);
assert(localCatalog.includes('aria-labelledby="o-negocio-delas-titulo"'));
for(const term of ['catálogo digital gratuito','produtos e serviços','liderados por mulheres','Organizado por município','Sebrae em parceria com a Prefeitura de Ilhabela']) assert(localCatalog.includes(term),term);
assert.deepEqual([...localCatalog.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['https://www.ilhabela.sp.gov.br/portal/noticias/0/3/18642/ilhabela-lanca-catalogo-digital-de-empreendedoras-da-regiao']);
console.log('O Negócio Delas visitor guidance is present only in Ilhabela, with municipal source.');

assert.deepEqual(data.cities.filter(c=>c.itaguareTrail).map(c=>c.slug),['bertioga']);
const bertiogaTrailPage=read('cidades/bertioga.html');
const bertiogaVisit=bertiogaTrailPage.match(/<section id="visita">([\s\S]*?)<\/section>/)?.[1];
const bertiogaTrail=bertiogaVisit?.match(/<article class="card" id="trilha-itaguare"[\s\S]*?<\/article>/)?.[0];
assert(bertiogaTrail,'Trail card should be inside Referências locais');
assert.equal((bertiogaTrailPage.match(/id="trilha-itaguare"/g)||[]).length,1);
assert(bertiogaTrail.includes('aria-labelledby="trilha-itaguare-titulo"'));
assert(bertiogaTrail.includes('<h3 id="trilha-itaguare-titulo">Trilha do Itaguaré: Relíquias do Passado</h3>'));
for(const term of ['1 a 2 km','duração estimada de 1h30 a 2h','A monitoria é opcional','Confira as condições de acesso'])
 assert(bertiogaTrail.includes(term),term);
assert.deepEqual([...bertiogaTrail.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['https://www.bertioga.sp.gov.br/turismo/pontos-turisticos/trilhas/trilha-do-veu-da-noiva']);
console.log('Itaguaré Trail visitor guidance is linked only from Bertioga with practical checks and time estimates.');

const bertiogaAgenda='/eventos-litoral-paulista-2026-2027/agenda-eventos-bertioga.html';
assert.deepEqual(data.cities.filter(c=>c.visitAgenda).map(c=>c.slug),['bertioga']);
assert.equal((bertiogaTrailPage.split('href="'+bertiogaAgenda+'"').length-1),1);
assert(bertiogaVisit.includes('<a href="'+bertiogaAgenda+'">Agenda de Bertioga</a>'),'Agenda shortcut must be visible in the visit section');
const bertiogaAgendaPage=read(bertiogaAgenda.slice(1));
assert(bertiogaAgendaPage.includes('id="dezembro-2026"'));
assert(bertiogaAgendaPage.includes('href="#dezembro-2026"'));
assert(bertiogaAgendaPage.includes('<a href="/cidades/bertioga.html">Guia local de Bertioga</a>'),'Keep the existing return link');
console.log('Bertioga city guide and agenda are connected in both directions.');
