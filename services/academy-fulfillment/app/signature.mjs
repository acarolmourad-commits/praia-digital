export async function verifiedEvent(request,secret,now=Math.floor(Date.now()/1000),cryptoApi=crypto){
 if(!secret?.startsWith('whsec_'))throw Error('NOT_CONFIGURED');
 const header=request.headers.get('stripe-signature')||'';if(header.length>2048)throw Error('BAD_SIGNATURE');
 const parts=header.split(',').map(x=>x.trim().split('='));const times=parts.filter(x=>x[0]==='t');const sigs=parts.filter(x=>x[0]==='v1').map(x=>x[1]);
 if(times.length!==1||!/^\d+$/.test(times[0][1])||Math.abs(now-Number(times[0][1]))>300||sigs.length>8)throw Error('BAD_SIGNATURE');
 const reader=request.body?.getReader();if(!reader)throw Error('EMPTY');let size=0,blocks=[];while(true){const r=await reader.read();if(r.done)break;size+=r.value.length;if(size>131072){await reader.cancel();throw Error('BODY_LIMIT');}blocks.push(r.value);}
 const raw=new Uint8Array(size);let offset=0;for(const b of blocks){raw.set(b,offset);offset+=b.length;}
 const prefix=new TextEncoder().encode(times[0][1]+'.');const bytes=new Uint8Array(prefix.length+size);bytes.set(prefix);bytes.set(raw,prefix.length);
 const key=await cryptoApi.subtle.importKey('raw',new TextEncoder().encode(secret),{name:'HMAC',hash:'SHA-256'},false,['verify']);let valid=false;
 for(const sig of sigs){if(!/^[a-f0-9]{64}$/.test(sig||''))continue;if(await cryptoApi.subtle.verify('HMAC',key,Uint8Array.from(sig.match(/../g),x=>parseInt(x,16)),bytes)){valid=true;break;}}
 if(!valid)throw Error('BAD_SIGNATURE');return JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(raw));
}
