self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('push',event=>{
 let data={title:'Estoque Vivo',body:'Há uma atualização de estoque. Abra o painel para conferir.',tag:'stock-update',url:'/'};
 try{Object.assign(data,event.data.json());}catch{}
 event.waitUntil(self.registration.showNotification(data.title,{body:data.body,tag:data.tag,icon:'/icon-192.png',badge:'/icon-192.png',data:{url:'/'},timestamp:data.at?Date.parse(data.at):Date.now()}));
});
self.addEventListener('notificationclick',event=>{event.notification.close();event.waitUntil((async()=>{const tabs=await self.clients.matchAll({type:'window',includeUncontrolled:true});for(const tab of tabs)if(new URL(tab.url).origin===self.location.origin){await tab.focus();return;}await self.clients.openWindow('/');})());});
