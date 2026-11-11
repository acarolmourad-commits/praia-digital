// Run with jsdom installed: node tests/diaria-dom.cjs. No external resources or real emails.
const {JSDOM}=require('jsdom');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const html=fs.readFileSync(path.join(__dirname,'../ferramentas/calculadora-diaria-ideal-airbnb-2026.html'),'utf8');
const dom=new JSDOM(html,{runScripts:'outside-only',url:'https://praia.digital/ferramentas/calculadora-diaria-ideal-airbnb-2026.html'});
const w=dom.window,d=w.document,$=id=>d.getElementById(id);
let revoked=0,blobCount=0,requests=0;
w.URL.createObjectURL=()=>`blob:report-${++blobCount}`;
w.URL.revokeObjectURL=()=>revoked++;
w.HTMLElement.prototype.scrollIntoView=function(){};
w.matchMedia=()=>({matches:true});
w.eval([...d.querySelectorAll('script:not([src])')].map(s=>s.textContent).join('\n'));
const set=(id,v)=>{$(id).value=v;$(id).dispatchEvent(new w.Event('input'));};
const calc=()=>$('form-calculo').dispatchEvent(new w.Event('submit',{cancelable:true}));
const settled=()=>new Promise(r=>setTimeout(r,0));
(async()=>{
 assert.equal($('resultado').hidden,true);calc();
 assert.match($('principal').textContent,/378,77/);assert.match($('detalhes').textContent,/159,59/);
 assert.equal($('baixar-relatorio').hidden,false);assert.match($('baixar-relatorio').href,/^blob:/);
 assert.equal(d.activeElement.id,'resultado');assert.equal(requests,0);
 const report=w.createReport(w.__sim);assert.match(report,/378,77/);assert.match(report,/não representam mercado observado/);assert.doesNotMatch(report,/<li>Comparativo detalhado/);
 for(const id of ['custos','limpeza','lucro','ocupacao','estadia']){
  const old=$(id).value;set(id,old);assert.equal($('resultado').hidden,true);assert.equal(w.__sim,null);assert.equal($('baixar-relatorio').hasAttribute('href'),false);calc();
 }
 set('cidade','Guarujá');assert.equal($('resultado').hidden,true);calc();
 for(const [id,v] of [['custos',''],['custos','NaN'],['custos','Infinity'],['custos','-1'],['custos','100000001'],['limpeza','-1'],['lucro','-1'],['ocupacao','0'],['ocupacao','150'],['ocupacao','-1'],['estadia','0'],['estadia','366'],['estadia','1.001']]){
  const old=$(id).value;set(id,v);calc();assert.equal($('resultado').hidden,true,`${id}=${v}`);assert.equal($('erro-calculo').hidden,false);assert.equal(w.__sim,null);assert.equal(d.activeElement.id,id);set(id,old);calc();
 }
 for(const id of ['custos','limpeza','lucro'])set(id,'0');set('ocupacao','100');set('estadia','365');calc();assert.match($('principal').textContent,/0,00/);
 set('estadia','2.5');set('ocupacao','0.01');calc();assert.equal($('resultado').hidden,false);
 const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length);
 for(const el of d.querySelectorAll('input,select')) assert.ok(d.querySelector(`label[for="${el.id}"]`));
 w.fetch=async()=>{requests++;return {ok:true,json:async()=>({success:false})};};
 set('lead-email','invalid');$('enviar-simulacao').click();await settled();assert.equal(requests,0);
 set('lead-email','test@example.com');$('enviar-simulacao').click();await settled();assert.match($('status-envio').textContent,/Não foi possível/);assert.equal($('baixar-relatorio').hidden,false);
 w.fetch=async()=>({ok:true,json:async()=>({success:'true'})});$('enviar-simulacao').click();await settled();assert.match($('status-envio').textContent,/confirmou a aceitação/);
 let release;w.fetch=()=>new Promise(r=>release=()=>r({ok:true,json:async()=>({success:true})}));
 $('enviar-simulacao').click();assert.equal($('enviar-simulacao').disabled,true);set('custos','1500');calc();release();await settled();
 assert.equal($('pos-envio').style.display,'none');assert.equal($('status-envio').textContent,'');assert.equal($('enviar-simulacao').disabled,false);
 // A stalled network request must settle even if the mock ignores abort.
 const realSetTimeout=w.setTimeout.bind(w);let expire, aborted=false;
 w.setTimeout=(callback,ms)=>ms===15000?(expire=callback,12345):realSetTimeout(callback,ms);
 w.fetch=(url,options)=>{requests++;options.signal.addEventListener('abort',()=>aborted=true);return new Promise(()=>{});};
 const beforeTimeout=requests;$('enviar-simulacao').click();expire();await settled();
 assert.equal(aborted,true);assert.equal($('enviar-simulacao').disabled,false);
 assert.match($('status-envio').textContent,/resultado do envio é incerto/);
 assert.match($('status-envio').textContent,/Não reenviamos automaticamente/);
 assert.equal(requests,beforeTimeout+1);assert.equal($('baixar-relatorio').hidden,false);
 // A timeout for a previous simulation must not expose an old status.
 $('enviar-simulacao').click();set('custos','1600');calc();expire();await settled();
 assert.equal($('pos-envio').style.display,'none');assert.equal($('status-envio').textContent,'');
 assert.equal($('enviar-simulacao').disabled,false);
 w.setTimeout=realSetTimeout;
 assert.ok(revoked>0);assert.equal(blobCount-revoked,1);
 console.log('PASS diária DOM: formulas, ranges, blank/NaN/infinity, zero, decimals, invalidation, download content, focus, labels, mocked email outcomes, stale response and blob cleanup');
 dom.window.close();
})().catch(e=>{dom.window.close();console.error(e);process.exit(1);});
