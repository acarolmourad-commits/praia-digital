// Run: node tests/test_city_comparator.cjs
// Exercise the actual production functions and DOM output, not a duplicate formula.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const html=fs.readFileSync(path.join(__dirname,'../apps/comparador-cidades/index.html'),'utf8');
const source=html.match(/<script>\s*(const CIDADES[\s\S]*?)<\/script>/)[1];
const elements=Object.fromEntries(['profile-weights','comparison-caption','tbody','ranking-status'].map(id=>[id,{textContent:'',innerHTML:''}]));
const buttons=['investidor','temporada','morar'].map(p=>({dataset:{p},attributes:{},classList:{toggle(){}},setAttribute(k,v){this.attributes[k]=v}}));
const context=vm.createContext({Intl,document:{getElementById:id=>elements[id],querySelectorAll:()=>buttons}});
vm.runInContext(source,context);
const run=code=>JSON.parse(JSON.stringify(vm.runInContext(code,context)));
const data=run('CIDADES');
assert.equal(data.length,12);
assert.equal(new Set(data.map(c=>c.nome)).size,12);
const caragua=data.find(c=>c.nome==='Caraguatatuba');
assert.equal(caragua.m2,3400);
for(const key of ['ocup','adr','valor','liq','infra']) assert.equal(caragua[key],null,key);
const expected={investidor:['Bertioga','São Sebastião','Itanhaém'],temporada:['São Sebastião','Bertioga','Ubatuba'],morar:['São Vicente','Santos','Guarujá']};
for(const profile of Object.keys(expected)){
 const rows=run(`rankCities(CIDADES,'${profile}')`);
 assert.deepEqual(rows.slice(0,3).map(c=>c.nome),expected[profile]);
 assert.equal(rows.at(-1).nome,'Caraguatatuba');assert.equal(rows.at(-1).score,null);
 assert.equal(rows.filter(c=>c.score!==null).length,11);
 for(const row of rows.slice(0,-1)) assert(row.score>=0&&row.score<=100);
 const weights=run(`PERFIS.${profile}`);
 assert.equal(Object.values(weights).reduce((sum,n)=>sum+Math.abs(n),0),1);
 vm.runInContext(`setProfile(document.querySelectorAll('.prof')[${Object.keys(expected).indexOf(profile)}])`,context);
 assert.equal(buttons.filter(b=>b.attributes['aria-pressed']==='true').length,1);
 assert(elements['ranking-status'].textContent.includes('12 cidades; 1 sem score'));
 assert.equal((elements.tbody.innerHTML.match(/<tr/g)||[]).length,12);
 assert.equal((elements.tbody.innerHTML.match(/Sem score/g)||[]).length,1);
 assert(!/NaN|Infinity|undefined/.test(elements.tbody.innerHTML));
 assert(elements['profile-weights'].textContent.includes(profile==='morar'?'infraestrutura 50%':'ocupação'));
}
assert.equal(run('norm(2,[2,2],false)'),0.5);
assert.equal(run('norm(2,[2,2],true)'),0.5);
assert.equal(run('norm(2,[2,10],true)'),1);
assert.equal(run('formatMetric(null)'), 'Indisponível');
assert.equal(run("formatMetric(1100,'R$ ')"), 'R$ 1.100');
assert.equal(run("formatMetric(12.1,'+','%')"), '+12,1%');
assert.deepEqual(run("rankCities(CIDADES,'unknown')"),[]);
assert.deepEqual(run("rankCities([],'morar')"),[]);
assert.equal(run("rankCities([{nome:'A',m2:null,ocup:null,valor:null,liq:null,infra:null}],'investidor')[0].score"),null);
assert.equal(run("rankCities([{nome:'A',m2:1,ocup:1,valor:1,liq:1,infra:null}],'investidor')[0].score"),50);
assert.equal(run("rankCities([{nome:'A',m2:1,ocup:1,valor:1,liq:1,infra:null}],'morar')[0].score"),null);
// Metadata/FAQ stay aligned with the cautious on-page content.
const schemas=[...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m=>JSON.parse(m[1]));
const faq=schemas.find(s=>s['@type']==='FAQPage');
assert.equal(faq.mainEntity.length,4);
for(const q of faq.mainEntity){assert(html.includes('<summary>'+q.name+'</summary>'));assert(html.includes('<p>'+q.acceptedAnswer.text+'</p>'));}
for(const id of ['ranking-title','references-title','metodologia','ranking-status']) assert(html.includes(`id="${id}"`));
assert.equal((html.match(/class="table-scroll"/g)||[]).length,2);
assert.equal((html.match(/<button[^>]*aria-pressed="(?:true|false)"/g)||[]).length,3);
assert(html.includes('role="status" aria-live="polite" aria-atomic="true"'));
assert(html.includes('<noscript>'));
assert(!html.includes('🥇'));
console.log('PASS: 12 cities, all profiles, unchanged top 3, null handling, score boundaries, formatting, accessible selection, tables and aligned FAQ schema.');
