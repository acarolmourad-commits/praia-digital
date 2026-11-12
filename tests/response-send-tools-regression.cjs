const fs=require('node:fs'), path=require('node:path'), vm=require('node:vm'), assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const files=['outreach/auto-respostas/modelo-resposta-automatica-lead.html','docs/sales/send-execution-tracker-2026.html'];
function scripts(file){return [...fs.readFileSync(path.join(root,file),'utf8').matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)].filter(m=>!(/ld\+json|\bsrc\s*=/.test(m[1]))).map(m=>m[2]);}
let checks=0;const test=(name,fn)=>{fn();checks++;};
function setup(file,marker,initial={}){
 const elements=new Map(),store=new Map(Object.entries(initial)),alerts=[];
 function el(id){if(!elements.has(id))elements.set(id,{value:'',innerHTML:'',innerText:'',textContent:'',offsetTop:150,classList:{values:new Set(),add(x){this.values.add(x)},remove(x){this.values.delete(x)}},querySelector(){return el(id+'-text')},click(){}});return elements.get(id);}
 const c={document:{getElementById:el,querySelectorAll(){return Array.from(elements.entries()).filter(([key])=>/^resposta\d$/.test(key)).map(([,e])=>e)},createElement(){return el('download')},body:{appendChild(){},removeChild(){}}},localStorage:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)},alert:m=>alerts.push(m),confirm:()=>true,setTimeout(){},Date,Math,JSON,Blob,URL,URLSearchParams,location:{search:'?lead=%3Cb%3ESynthetic%3C%2Fb%3E&city=Test',href:''},scrollTo(){},navigator:{clipboard:{async writeText(text){c.copied=text}}}};
 c.window=c;vm.createContext(c);const src=scripts(file).find(s=>s.includes(marker));assert(src);vm.runInContext(src,c);return {c,el,store,alerts,eval:s=>vm.runInContext(s,c)};
}
test('all inline scripts parse',()=>{for(const f of files)for(const s of scripts(f))new vm.Script(s,{filename:f});});
const response=setup(files[0],'function mostrarResposta(');
test('query values render literally',()=>{assert.equal(response.el('leadNameDisplay').textContent,'<b>Synthetic</b>');assert.equal(response.el('leadCityDisplay').textContent,'Test');});
test('scenario navigation selects one response',()=>{response.el('resposta1');response.el('resposta2');response.c.mostrarResposta(1);assert(response.el('resposta1').classList.values.has('active'));response.c.mostrarResposta(2);assert(!response.el('resposta1').classList.values.has('active'));assert(response.el('resposta2').classList.values.has('active'));});
const send=setup(files[1],'let queue =',{praiaSendQueue:JSON.stringify([{leadName:'Synthetic queue',city:'Test',type:'Primeiro contato'}]),praiaSentLog:JSON.stringify([{leadName:'Retained record',city:'Test',date:'2000-01-01'}])});
test('tracker starts and preserves existing records',()=>{assert.equal(send.el('statPending').textContent,1);assert.equal(send.el('statSent').textContent,0);assert(send.el('queueList').innerHTML.includes('Synthetic queue'));});
test('tracker validates manual registration',()=>{send.c.markSent();assert.equal(send.el('toast').textContent,'Preencha nome e cidade');assert.equal(send.eval('sent.length'),1);});
test('tracker records manual sends locally without sending messages',()=>{send.el('leadName').value='Synthetic manual';send.el('leadCity').value='Test';send.el('sendType').value='Primeiro contato';send.c.markSent();const saved=JSON.parse(send.store.get('praiaSentLog'));assert.equal(saved.length,2);assert.equal(saved[0].leadName,'Retained record');assert.equal(saved[1].leadName,'Synthetic manual');assert.equal(send.el('statSent').textContent,1);assert(send.el('toast').textContent.includes('Envio registrado'));send.c.markSentById(0);assert.equal(send.el('statPending').textContent,0);assert.equal(JSON.parse(send.store.get('praiaSentLog')).length,3);});
test('daily action opens checklist without fabricating completion',()=>{const before=send.store.get('praiaTodayLog');send.c.runDailyRoutine();assert.equal(send.c.location.href,'/docs/sales/checklist-operacional-2026.html');assert.equal(send.store.get('praiaTodayLog'),before);});
test('tracker shortcut buttons resolve to existing pages from the nested page URL',()=>{
 const html=fs.readFileSync(path.join(root,files[1]),'utf8');
 const handlers=[...html.matchAll(/onclick="(window\.open\([^"]+\))"/g)].map(match=>match[1]);
 assert.equal(handlers.length,3,'all three tracker shortcuts are exercised');
 for(const handler of handlers){
  let destination;
  vm.runInNewContext(handler,{window:{open(url){destination=url;}}});
  const resolved=new URL(destination,'https://praia.digital/'+files[1]);
  assert.equal(resolved.origin,'https://praia.digital');
  assert(fs.existsSync(path.join(root,decodeURIComponent(resolved.pathname.slice(1)))),`Missing shortcut destination: ${resolved.pathname}`);
 }
});
(async()=>{response.el('resposta1-text').innerText='Synthetic response body';await response.c.copiar(1);test('copy contains only response body',()=>{assert.equal(response.c.copied,'Synthetic response body');assert(response.alerts.at(-1).includes('Revise os dados'));});response.c.navigator.clipboard.writeText=async()=>{throw new Error('denied')};await response.c.copiar(1);test('clipboard rejection provides manual recovery',()=>{assert(response.alerts.at(-1).includes('copie manualmente'));});console.log(JSON.stringify({checks,passed:checks}));})().catch(e=>{console.error(e);process.exitCode=1});
