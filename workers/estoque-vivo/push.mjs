import {buildPushPayload} from '@block65/webcrypto-web-push';
import {AppError} from './domain.mjs';

export function validSubscription(value){
 if(!value||typeof value!=='object')throw new AppError('Inscrição de notificações inválida.');
 let url;try{url=new URL(value.endpoint);}catch{throw new AppError('Destino de notificações inválido.');}
 const h=url.hostname;
 const allowed=h==='fcm.googleapis.com'||h==='updates.push.services.mozilla.com'||h==='push.services.mozilla.com'||h.endsWith('.push.apple.com')||h.endsWith('.notify.windows.com');
 if(url.protocol!=='https:'||!allowed||url.port||url.username||url.password||url.hash||url.href.length>2048)throw new AppError('Serviço de notificações não suportado.');
 if(!/^[A-Za-z0-9_-]{87}$/.test(value.keys?.p256dh||'')||!/^B/.test(value.keys.p256dh)||!/^[A-Za-z0-9_-]{22}$/.test(value.keys?.auth||''))throw new AppError('Chaves de notificação inválidas.');
 return {endpoint:url.href,expirationTime:null,keys:{p256dh:value.keys.p256dh,auth:value.keys.auth}};
}

export async function sendPush(subscription,data,keys){
 const safe=validSubscription(subscription);
 const payload=await buildPushPayload({data:JSON.stringify(data),options:{ttl:300}},safe,keys);
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),10000);
 try{return (await fetch(safe.endpoint,{...payload,redirect:'manual',signal:controller.signal})).status;}finally{clearTimeout(timer);}
}

export function alertLevel(available,threshold){return available===0?2:available<=threshold?1:0;}
