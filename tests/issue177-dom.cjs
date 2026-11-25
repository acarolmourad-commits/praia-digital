// Offline behavior tests: execute the shipped scripts with controlled DOM/network adapters.
// No service requests, messages, or browser rendering occur. Run: node --test tests/issue177-dom.cjs
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(process.env.ISSUE177_ROOT || path.join(__dirname,'..'));
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const search=require(path.join(root,'js/property-search.js'));
const houseUrl='https://praia.digital/casa-condominio-fechado-bertioga.html';
const classic=read('home-classica.html');
const house=read('casa-condominio-fechado-bertioga.html');
const listingData=()=>vm.runInNewContext(classic.match(/const listings = (\[[\s\S]*?\n\]);/)[1]);

class Element {
  constructor(id='',tagName='DIV'){Object.assign(this,{id,tagName,value:'',textContent:'',children:[],options:[],listeners:{},attributes:{},hidden:false});this.classes=new Set();this.classList={add:c=>this.classes.add(c),remove:c=>this.classes.delete(c)};}
  set innerHTML(value){this.html=value;if(this.tagName==='SELECT')this.options=[...value.matchAll(/<option value="([^"]*)">([^<]*)<\/option>/g)].map(m=>({value:m[1],text:m[2]}));}
  get innerHTML(){return this.html || '';}
  add(option){this.options.push(option);}
  addEventListener(name,fn){this.listeners[name]=fn;}
  fire(name){return this.listeners[name]?.call(this,{preventDefault(){}});}
  set href(v){this.attributes.href=v;} get href(){return this.attributes.href;}
  getAttribute(k){return this.attributes[k]??null;}
  removeAttribute(k){delete this.attributes[k];}
  checkValidity(){return this.valid!==false;}
  reportValidity(){return this.checkValidity();}
  focus(){}
  replaceChildren(...nodes){this.children=nodes;}
  appendChild(node){this.children.push(node);}
}
function qrHarness(){
  const els=Object.fromEntries(['qrListingId','qrPreview','qrResultUrl','qrStatus'].map(id=>[id,new Element(id)]));
  const listings=listingData();
  const ctx={URL,Number,listings,document:{getElementById:id=>els[id],createElement:()=>new Element()}};
  vm.createContext(ctx);
  vm.runInContext(classic.slice(classic.indexOf('function listingPageUrl('),classic.indexOf('// EMBED CODE')),ctx);
  return {ctx,els,listings,generate(value){els.qrListingId.value=value;ctx.generateQR();}};
}
function catalogueHarness(query=''){
  const els={};
  for(const id of ['lista-imoveis','search-status','busca','preco-label','limpar-busca','preco-filtro','quartos-filtro','cidade-filtro','tipo-filtro','categoria-filtro']) els[id]=new Element(id,/(cidade|tipo|categoria)-filtro/.test(id)?'SELECT':'INPUT');
  let ready;
  const location={href:'https://praia.digital/imoveis.html'+query,search:query};
  const ctx={URL,URLSearchParams,Option:function(text,value){return {text,value};},location,history:{replaceState(_a,_b,u){location.href=String(u);location.search=u.search;},pushState(_a,_b,u){location.href=String(u);location.search=u.search;}},document:{getElementById:id=>els[id],addEventListener:(e,fn)=>{if(e==='DOMContentLoaded')ready=fn;}},window:{PDPropertySearch:search,addEventListener(){}},console};
  vm.createContext(ctx);
  vm.runInContext(read('js/main.js').replace(/\}\)\(\);\s*$/, 'globalThis.catalogue={properties,propertyCardTemplate,restoreSearch};})();'),ctx);
  ready();
  return {ctx,els,edit(value){els.busca.value=value;els.busca.fire('input');}};
}
test('classic 25 and current 9 share a stable URL, title, price and documented characteristics',()=>{
  const {ctx}=catalogueHarness();const c=listingData().find(p=>p.id===25);const p=ctx.catalogue.properties.find(p=>p.id===9);
  assert.equal(new URL(c.url,'https://praia.digital/').href,houseUrl);
  assert.equal('https://praia.digital/'+p.slug.slice(3)+'.html',houseUrl);
  assert.equal(p.title,c.titulo);assert.equal(search.money(p.price),c.preco);assert.equal(c.preco,595000);
  assert.equal(Number(p.bedrooms),2);assert.equal(c.dormitorios,2);assert.equal(c.area,105);
  assert.match(p.description,/2 banheiros e 1 vaga/);assert.match(p.description,/710/);assert.match(p.description,/105/);
  assert.equal(c.roi,null);assert.doesNotMatch(c.aiReason,/19,4|11,3|AirDNA/);
  assert(house.includes(p.title));assert(house.includes('R$ 595.000'));
});
test('QR for ID 25 uses the individual page and the same conventional link',()=>{
  const {els,generate}=qrHarness();generate('25');
  assert.equal(els.qrResultUrl.href,houseUrl);
  assert.equal(new URL(els.qrPreview.children[0].src).searchParams.get('data'),houseUrl);
  assert.equal(new URL(els.qrPreview.children[0].src).searchParams.get('size'),'224x224');
  assert(els.qrResultUrl.classes.has('visible'));
});
test('QR accepts an existing record beyond 25 without hardcoded upper bounds',()=>{
  const h=qrHarness();h.listings.push({id:26,titulo:'Test record',url:'casa-condominio-fechado-bertioga.html'});h.generate('26');
  assert.equal(h.els.qrResultUrl.href,houseUrl);
});
test('QR rejects absent IDs, fractions, empty input and a classic record without URL; clears old results',()=>{
  for(const id of ['999','25.5','','0','-1','9']){
    const h=qrHarness();h.generate('25');h.generate(id);
    assert.equal(h.els.qrResultUrl.href,undefined,id);assert.equal(h.els.qrPreview.children.length,0,id);assert(h.els.qrStatus.textContent,id);
  }
});
test('QR refuses external destinations, fragments and malformed URLs; image failure preserves ordinary link',()=>{
  const h=qrHarness();
  for(const url of ['https://example.com/a.html','/#imovel-25','casa.html#fragment','casa.html?x=1','javascript:alert(1)','http://[']) assert.equal(h.ctx.listingPageUrl({url}),null,url);
  h.generate('25');h.els.qrPreview.children[0].onerror();assert.equal(h.els.qrResultUrl.href,houseUrl);assert.match(h.els.qrStatus.textContent,/Use o link/);
});
test('opening classic ID 25 navigates directly to the individual page',()=>{
  let destination;const ctx={listings:listingData(),window:{location:{assign:url=>destination=url}},listingPageUrl:qrHarness().ctx.listingPageUrl};
  vm.createContext(ctx);vm.runInContext(classic.slice(classic.indexOf('function openModal('),classic.indexOf('function closeModal(')),ctx);
  ctx.openModal(25);assert.equal(destination,houseUrl);
});
test('search for Bertioga house, two bedrooms, budget and games room finds the documented house',()=>{
  const h=catalogueHarness();h.edit('comprar casa em Bertioga com 2 quartos até R$ 600 mil sala de jogos');
  assert.match(h.els['search-status'].textContent,/^1 imóvel/);assert(h.els['lista-imoveis'].innerHTML.includes('casa-condominio-fechado-bertioga.html'));
});
test('suite queries display limitation and never present unverified matches, including URL restoration',()=>{
  const h=catalogueHarness('?q=comprar+casa+com+2+su%C3%ADtes&quartos=2');
  assert.match(h.els['search-status'].textContent,/suítes não verificada/);
  assert.doesNotMatch(h.els['lista-imoveis'].innerHTML,/property-card/);
  h.els['quartos-filtro'].value='2';h.els['quartos-filtro'].fire('change');
  assert.doesNotMatch(h.els['lista-imoveis'].innerHTML,/property-card/);
  h.edit('comprar casa em Bertioga com 2 quartos até R$ 600 mil');
  assert.match(h.els['search-status'].textContent,/^1 imóvel/);
  h.els['limpar-busca'].fire('click');assert.match(h.els['lista-imoveis'].innerHTML,/property-card/);
});
test('catalogue and detail email drafts include title, price, URL and correct destination',()=>{
  const {ctx}=catalogueHarness();const p=ctx.catalogue.properties.find(p=>p.id===9);
  const card=ctx.catalogue.propertyCardTemplate(p);const cardLink=card.match(/class="btn-whatsapp" href="([^"]+)"/)[1];
  const detailLink=house.match(/class="btn-whatsapp" href="([^"]+)"/)[1];
  for(const link of [cardLink,detailLink]){const url=new URL(link.replaceAll('&amp;', '&'));assert.equal(url.protocol,'mailto:');assert.equal(url.pathname,'comercial@praia.digital');const message=url.searchParams.get('body');assert(message.includes(houseUrl));assert(message.includes(p.title));assert(message.includes(p.price));}
});

function formHarness(fetchImpl){
  const form=new Element('leadForm');const status=new Element('formStatus');const fallback=new Element('interestFallback');const button=new Element();
  const fields=[{id:'name',value:'Teste local'},{id:'phone',value:'11900000000'},...Array.from(house.matchAll(/<input type="hidden" id="([^"]+)" value="([^"]+)"/g),m=>({id:m[1],value:m[2]}))];
  form.querySelectorAll=()=>fields;form.querySelector=()=>button;
  const timers=new Map();let timerId=0;const events=[];
  const ctx={document:{getElementById:id=>({leadForm:form,formStatus:status,interestFallback:fallback})[id]},fetch:fetchImpl,AbortController,setTimeout:fn=>{timers.set(++timerId,fn);return timerId;},clearTimeout:id=>timers.delete(id),localStorage:{getItem:()=>null,setItem(){}},location:{pathname:'/casa-condominio-fechado-bertioga.html'},window:{dispatchEvent:event=>events.push(event)},CustomEvent:function(type,init){Object.assign(this,{type,...init});},console};
  vm.createContext(ctx);
  const script=Array.from(house.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g),m=>m[1]).find(s=>s.includes("const form = document.getElementById('leadForm')"));
  assert(script,'interest script exists');vm.runInContext(script,ctx);
  return {form,status,fallback,button,timers,events,submit:()=>form.fire('submit')};
}
test('interest submission carries property context and only confirms service acceptance after a successful response',async()=>{
  let request;let respond;
  const h=formHarness((url,options)=>{request={url,...options};return new Promise(resolve=>respond=resolve);});
  const pending=h.submit();assert.equal(h.button.disabled,true);assert.match(h.status.textContent,/Enviando/);
  await h.submit(); // Prevent accidental duplicate request while pending.
  assert.equal(h.events.length,1);
  const body=JSON.parse(request.body);assert.equal(request.url,'https://academy.praia.digital/leads');assert.equal(body.property_url,houseUrl);assert.equal(body.property_price,'R$ 595.000');assert.equal(body.property_title,'Casa com 2 quartos em condomínio fechado em Bertioga');
  respond({ok:true});await pending;assert.match(h.status.textContent,/aceitou/);assert.equal(h.button.disabled,false);assert.equal(h.fallback.hidden,true);assert.equal(h.timers.size,0);
});
for(const mode of ['http-error','network-error','timeout'])test('interest '+mode+' preserves reviewable email alternative without claiming receipt',async()=>{
  const h=formHarness((_url,opts)=>mode==='http-error'?Promise.resolve({ok:false}):mode==='network-error'?Promise.reject(new Error('offline')):new Promise((_,reject)=>opts.signal.addEventListener('abort',()=>reject(new Error('timeout')))));
  const pending=h.submit();if(mode==='timeout')for(const fn of [...h.timers.values()])fn();await pending;
  assert.equal(h.fallback.hidden,false);assert.match(h.status.textContent,/Não foi possível confirmar/);assert.doesNotMatch(h.status.textContent,/aceitou|Recebido/);
  const message=new URL(h.fallback.href).searchParams.get('body');assert(message.includes(houseUrl));assert(message.includes('R$ 595.000'));assert(message.includes('Teste local'));assert.equal(h.button.disabled,false);
});
test('invalid interest form cannot submit',async()=>{let calls=0;const h=formHarness(()=>{calls++;return Promise.resolve({ok:true});});h.form.valid=false;await h.submit();assert.equal(calls,0);});
test('modified HTML has parseable JSON-LD and JavaScript; guide describes actual controls',()=>{
  for(const file of ['home-classica.html','imoveis.html','encontrar-imovel.html','casa-condominio-fechado-bertioga.html']) {
    for(const m of read(file).matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)) {
      if(m[1].includes('application/ld+json'))JSON.parse(m[2]);else if(!/\bsrc=/.test(m[1]))new vm.Script(m[2],{filename:file});
    }
  }
  const guide=read('encontrar-imovel.html');assert.doesNotMatch(guide,/ranqueados por score|Compare pelo score|preço e área/);assert.match(guide,/Abrir busca com filtros/);assert.match(guide,/mínimo de quartos/);
});
