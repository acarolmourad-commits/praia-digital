import {Miniflare,convertV4MiniflareOptions} from 'miniflare';
const mf=new Miniflare(convertV4MiniflareOptions({host:'127.0.0.1',port:Number(process.env.PORT||4173),modules:['dist/worker.mjs'].map(file=>({type:'ESModule',path:new URL(file,import.meta.url).pathname})),compatibilityDate:'2026-11-13',durableObjects:{ROOMS:{className:'InventoryRoom',useSQLite:true}},durableObjectsPersist:new URL('./.dev-state',import.meta.url).pathname}));
console.log('Inventory development server',String(await mf.ready));
