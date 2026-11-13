import assert from'node:assert/strict';import{createHash}from'node:crypto';import{Composio}from'./composio.mjs';
const bytes=new Uint8Array([80,75,3,4,1,2]);const offer={file_id:'file_fixture',bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')};
function fixture(){const c=new Composio({COMPOSIO_DOWNLOAD_HOSTS_JSON:'["files.example.invalid"]'},async()=>new Response(bytes));let checks=0;c.privateMetadata=async()=>{checks++;return{size:String(bytes.length)};};c.call=async()=>({binary_data:{url:'https://files.example.invalid/signed',size:bytes.length}});return{c,count:()=>checks};}
const f=fixture();assert.deepEqual(await f.c.downloadVerifiedZip(offer),bytes);assert.equal(f.count(),2);console.log('PASS download hash + before/after permissions');
await assert.rejects(()=>fixture().c.downloadVerifiedZip({...offer,sha256:'0'.repeat(64)}),/HASH/);console.log('PASS corrupted package blocked');
const g=fixture();g.c.call=async()=>({binary_data:{url:'https://unapproved.example.invalid/x',size:bytes.length}});await assert.rejects(()=>g.c.downloadVerifiedZip(offer),/ORIGIN/);console.log('PASS unapproved staging origin blocked');
const h=fixture();h.c.fetcher=async()=>new Response(new Uint8Array(99));await assert.rejects(()=>h.c.downloadVerifiedZip(offer),/TOO_LARGE/);console.log('PASS oversized download blocked');
console.log('4 Drive adapter tests passed');
