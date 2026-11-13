import assert from 'node:assert/strict';import {createHmac}from'node:crypto';
const secret='whsec_local_runtime_fixture';
const base=process.env.RUNTIME_BASE_URL||'http://127.0.0.1:8797';
const mf={dispatchFetch:(url,opts)=>fetch(base+new URL(url).pathname,opts),dispose:async()=>{}};
try{
 const health=await mf.dispatchFetch('http://localhost/health');assert.equal(health.status,200);assert.equal((await health.json()).automatic_delivery,false);
 const body=JSON.stringify({id:'evt_fixture',type:'checkout.session.completed',livemode:false,created:Math.floor(Date.now()/1000),data:{object:{id:'cs_fixture'}}});const timestamp=Math.floor(Date.now()/1000);const sig='t='+timestamp+',v1='+createHmac('sha256',secret).update(timestamp+'.'+body).digest('hex');
 for(let i=0;i<2;i++){const r=await mf.dispatchFetch('http://localhost/stripe-webhook',{method:'POST',headers:{'stripe-signature':sig},body});assert.equal(r.status,200,await r.text());}
 const bad=await mf.dispatchFetch('http://localhost/stripe-webhook',{method:'POST',headers:{'stripe-signature':sig},body:body+' '});assert.notEqual(bad.status,200);
 console.log('PASS local workerd Worker/SQLite intake duplicate + invalid signature + delivery disabled');
}finally{await mf.dispose();}
