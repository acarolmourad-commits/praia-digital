const { JSDOM } = require('jsdom');
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const dom=new JSDOM(fs.readFileSync(path.join(root,'apps/simulador-roi-temporada/index.html'),'utf8'),{url:'https://praia.digital/apps/simulador-roi-temporada/',runScripts:'outside-only'});
const w=dom.window,d=w.document;
for(const script of ['roi-temporada-core.js','roi-temporada-ui.js'])w.eval(fs.readFileSync(path.join(root,'js',script),'utf8'));
const field=id=>d.getElementById(id),submit=()=>field('roi-form').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));
const edit=(id,value,event='input')=>{field(id).value=value;field(id).dispatchEvent(new w.Event(event,{bubbles:true}));};
assert.equal(field('result').hidden,true);
submit();assert.equal(field('result').hidden,false);assert.match(field('rLiq').textContent,/18.795,63/);assert.match(field('rRoiL').textContent,/3,2%/);assert.equal(d.activeElement.id,'roi-result-title');
for(const id of ['valor','adr','ocup','noites','custos','plataforma','iptu','cond','ir']){
 assert.equal(field(id).labels.length,1);
 const v=field(id).value;edit(id,'');assert.equal(field('result').hidden,true);submit();assert.equal(field('result').hidden,true);assert.equal(field(id).getAttribute('aria-invalid'),'true');assert.equal(d.activeElement.id,id);assert.ok(field(id+'-error').textContent);edit(id,v);submit();assert.equal(field('result').hidden,false);
}
for(const [id,value]of [['ocup',150],['ocup',-1],['noites',366],['noites',1.5],['valor',0],['plataforma',101],['ir',-1],['adr',-50]]){
 const v=field(id).value;edit(id,String(value));submit();assert.equal(field('result').hidden,true);assert.ok(field(id+'-error').textContent);assert.equal(d.activeElement.id,id);edit(id,v);submit();
}
const adr=field('adr').value,ocup=field('ocup').value;
edit('cidade','Bertioga','change');assert.equal(field('result').hidden,true);assert.equal(field('adr').value,adr);assert.equal(field('ocup').value,ocup);submit();assert.equal(field('rCidade').textContent,'Bertioga');
edit('ocup','0');submit();assert.match(field('rLiq').textContent,/-R\$\s*47.600,00/);assert.equal(field('rPayback').textContent,'Não recuperado neste cenário');assert.match(field('rBig').textContent,/despesas superam/);
edit('custos','0');edit('iptu','0');edit('cond','0');submit();assert.match(field('rBig').textContent,/equilibram/);
assert.equal(d.querySelectorAll('h1').length,1);assert.equal(d.querySelectorAll('main').length,1);
const html=d.documentElement.outerHTML;
assert.doesNotMatch(html,/Excelente investimento|AirDNA|Airbtics|8–14%|900,68|750,55/);
for(const s of d.querySelectorAll('script[type="application/ld+json"]'))JSON.parse(s.textContent);
dom.window.close();console.log('ROI DOM: labels, validation, invalidation, city isolation, results and metadata passed.');
