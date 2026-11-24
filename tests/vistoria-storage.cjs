const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const {createStore,KEY,GROUPS}=require('../apps/checklist-vistoria/checklist.js');
function storage(raw=null){return {raw,writes:0,removes:0,getItem(){return this.raw;},setItem(k,v){assert.equal(k,KEY);this.raw=v;this.writes++;},removeItem(k){assert.equal(k,KEY);this.raw=null;this.removes++;}};}
test('valid legacy key hydration, toggle/unmark and reload',()=>{const mem=storage('{"0_0":"ok","1_0":"bad"}');const s=createStore(()=>mem);assert.equal(s.snapshot().session,false);assert.equal(Object.keys(s.snapshot().state).length,2);s.mark('0_0','ok');assert(!('0_0'in s.snapshot().state));s.mark('0_1','bad');assert.equal(createStore(()=>mem).snapshot().state['0_1'],'bad');s.mark('0_1','ok');assert.equal(s.snapshot().state['0_1'],'ok');});
test('corrupt/null/array/primitives preserved unchanged during session',()=>{for(const raw of ['{','null','[]','"str"','true','3','']){const mem=storage(raw),s=createStore(()=>mem);assert(s.snapshot().session);assert.deepEqual(s.snapshot().state,{});s.mark('0_0','ok');assert.equal(mem.raw,raw);assert.equal(mem.writes,0);assert.match(s.snapshot().status,/Modo sessão/);}});
test('whitelist keys and only ok/bad; retain valid subset without rewriting invalid',()=>{const raw='{"0_0":"ok","0_1":"bad","99_0":"ok","0_2":"yes","__proto__":"ok","constructor":"bad"}',mem=storage(raw),s=createStore(()=>mem);assert.deepEqual(s.snapshot().state,{'0_0':'ok','0_1':'bad'});assert.equal(s.snapshot().total,GROUPS.reduce((n,g)=>n+g.items.length,0));s.mark('0_3','ok');s.mark('100_0','ok');s.mark('0_4','yes');assert.equal(Object.keys(s.snapshot().state).length,3);assert.equal(mem.raw,raw);});
test('storage getter/read exceptions keep functioning in session',()=>{for(const access of [()=>{throw Error('denied')},()=>({getItem(){throw Error('denied')}})]){const s=createStore(access);s.mark('0_0','bad');assert.equal(s.snapshot().state['0_0'],'bad');assert(s.snapshot().session);s.reset();assert.match(s.snapshot().status,/não foi possível remover/i);}});
test('write denied preserves current state and old stored data',()=>{const mem=storage('{"0_0":"ok"}');mem.setItem=()=>{throw Error('quota')};const s=createStore(()=>mem);s.mark('0_1','bad');assert.equal(s.snapshot().state['0_1'],'bad');assert.equal(mem.raw,'{"0_0":"ok"}');assert.match(s.snapshot().status,/não foi possível salvar/i);});
test('explicit reset recovers corrupt data or warns on removal failure',()=>{const mem=storage('{'),s=createStore(()=>mem);s.mark('0_0','ok');s.reset();assert.equal(mem.raw,null);assert.equal(s.snapshot().session,false);s.mark('0_1','bad');assert.equal(mem.writes,1);mem.removeItem=()=>{throw Error('denied')};s.reset();assert.deepEqual(s.snapshot().state,{});assert(s.snapshot().session);assert.match(s.snapshot().status,/podem reaparecer/);});
test('UI neutral progress, reset cancel/confirm and no exception on blocked access',()=>{
 const mem=storage('{"0_0":"ok"}'),es={};for(const id of ['groups','bar','score','verdict','storage-status','visit-problems-list','visit-problems-empty'])es[id]={innerHTML:'',textContent:'',style:{}};
 let yes=false;const ctx={document:{getElementById:id=>es[id]},localStorage:mem,confirm:()=>yes};vm.runInNewContext(fs.readFileSync(require.resolve('../apps/checklist-vistoria/checklist.js'),'utf8'),ctx);
 assert.match(es.verdict.textContent,/1\/26/);ctx.resetAll();assert.equal(mem.removes,0);assert.match(es.verdict.textContent,/1\/26/);yes=true;ctx.resetAll();assert.equal(mem.removes,1);assert.match(es.verdict.textContent,/0\/26/);
 for(let g=0;g<GROUPS.length;g++)for(let i=0;i<GROUPS[g].items.length;i++)ctx.mark(g+'_'+i,'bad');assert.equal(es.score.textContent,'100%');assert.match(es.verdict.textContent,/26 com problema/);
 assert.equal((es['visit-problems-list'].innerHTML.match(/<li>/g)||[]).length,26);
 assert.equal(es['visit-problems-empty'].hidden,true);
 assert(!/pode avançar|ótimo estado|negocie/.test(es.verdict.textContent));
});

test('render restores only the focused checklist button without scrolling or stealing outside focus',()=>{
 const mem=storage(),es={};for(const id of ['groups','bar','score','verdict','storage-status','visit-problems-list','visit-problems-empty'])es[id]={innerHTML:'',textContent:'',style:{}};
 const doc={activeElement:null,getElementById:id=>es[id]};
 let focusCalls=0;
 Object.defineProperty(es.groups,'innerHTML',{set(html){
   if(doc.activeElement?.id?.startsWith('vistoria-'))doc.activeElement=null;
   for(const match of html.matchAll(/id="(vistoria-[^"]+)"/g)){
     const id=match[1];es[id]={id,focus(options){assert.equal(options.preventScroll,true);doc.activeElement=this;focusCalls++;}};
   }
 }});
 const ctx={document:doc,localStorage:mem,confirm:()=>true};
 vm.runInNewContext(fs.readFileSync(require.resolve('../apps/checklist-vistoria/checklist.js'),'utf8'),ctx);
 assert(es['vistoria-0_0-ok']);doc.activeElement=es['vistoria-0_0-ok'];
 ctx.mark('0_0','ok');assert.equal(doc.activeElement.id,'vistoria-0_0-ok');assert.equal(focusCalls,1);
 ctx.mark('0_0','ok');assert.equal(doc.activeElement.id,'vistoria-0_0-ok');assert.equal(focusCalls,2);
 doc.activeElement={id:'reset'};ctx.resetAll();assert.equal(doc.activeElement.id,'reset');assert.equal(focusCalls,2);
});

test('orientação editorial usa fontes primárias e não promete conformidade ou preço de laudo',()=>{
 const html=fs.readFileSync(require.resolve('../apps/checklist-vistoria/index.html'),'utf8');
 assert.match(html,/quando solicitado/);assert.match(html,/desgaste do uso normal/);
 assert.match(html,/www2\.camara\.leg\.br/);assert.match(html,/legislacao\.prefeitura\.sp\.gov\.br/);assert.match(html,/www\.stj\.jus\.br/);
 for(const claim of ['vistoria é obrigatória e não pode ser cobrada','veda cobrar tarifa','obrigam inspeção predial periódica','R$ 800–2.500','instalações hidráulicas/elétricas (3 anos)','score de qualidade'])assert(!html.includes(claim),claim);
 assert(!JSON.stringify(GROUPS).includes('Lei SP 16.642/2017'));
});
