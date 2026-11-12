const vm=require('node:vm'),fs=require('fs'),assert=require('node:assert/strict');
const code=fs.readFileSync(require('path').join(__dirname,'../js/lead-capture.js'),'utf8');
(async()=>{
 let assertions=0;
 for(const kind of ['true','string','false','missing','http','json','network','timeout','invalid','honey','blank']){
  let handler,calls=0,body,reset=false,timer;
  const button={disabled:true},status={textContent:'',focus(){}},elements={};
  for(const [k,v] of Object.entries({nome:'Teste',email:'teste@example.com',telefone:'',interesse:'comprar',mensagem:'Teste fictício',consentimento:'Autorizo',_honey:''}))elements[k]={value:v,focus(){}};
  if(kind==='honey')elements._honey.value='bot';if(kind==='blank')elements.nome.value=' ';
  const form={elements,querySelector:s=>s==='[type="submit"]'?button:status,addEventListener:(n,h)=>handler=h,reportValidity:()=>kind!=='invalid',setAttribute(){},removeAttribute(){},reset(){reset=true;}};
  vm.runInNewContext(code,{document:{querySelectorAll:()=>[form]},location:{pathname:'/contato.html',search:'?secret=private'},AbortController,Date,setTimeout:f=>{timer=f;return 1},clearTimeout(){},fetch:async(u,o)=>{calls++;body=JSON.parse(o.body);assert.equal(o.credentials,'omit');assert.equal(o.referrerPolicy,'no-referrer');if(kind==='network')throw Error();if(kind==='timeout'){timer();assert.equal(o.signal.aborted,true);throw Error();}return {ok:kind!=='http',json:async()=>{if(kind==='json')throw Error();return {success:kind==='true'?true:kind==='string'?'true':kind==='missing'?undefined:'false'};}};}});
  const first=handler({preventDefault(){}});await handler({preventDefault(){}});await first;
  if(['invalid','honey','blank'].includes(kind)){assert.equal(calls,0);assert.equal(reset,false);}else{
   assert.equal(calls,1);assert.equal(body.origem,'/contato.html');assert.ok(!JSON.stringify(body).includes('private'));
   const ok=['true','string'].includes(kind);assert.equal(reset,ok);assert.equal(button.disabled,ok);assert.ok(status.textContent.includes(ok?'aceita':'Não conseguimos'));
  }
  assertions++;
 }
 console.log(assertions+' scenarios passed; requests simulated, no network.');
})().catch(e=>{console.error(e);process.exit(1)});
