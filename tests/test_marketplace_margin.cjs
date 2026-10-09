// Run: node tests/test_marketplace_margin.cjs
// Extract the actual calculator functions; do not duplicate production formulas.
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const html=fs.readFileSync(path.resolve(__dirname,'../apps/calculadora-precificacao-shopee/index.html'),'utf8');
const match=html.match(/function taxaShopee[\s\S]*?(?=function calc\()/);
if(!match) throw new Error('Calculator functions not found');
vm.runInThisContext(match[0]);
const assert=require('node:assert/strict');
assert.equal(precoParaMargem(43.2,'shopee',0,0,15),73.39);
assert.equal(precoParaMargem(10,'shopee',0,0,0),18.13);
assert.equal(precoParaMargem(10,'tiktok',0,0,15),15.19);
assert.equal(precoParaMargem(10,'tiktok',100,0,15),null);
assert.equal(precoParaMargem(-1,'shopee',0,0,15),null);
assert.equal(precoParaMargem(10,'shopee',0,0,100),null);
let cases=0;
for(const pl of ['shopee','tiktok']) for(const c of [0,10,43.2,47.5,50,60,100,150,200]) for(const target of [0,10,15,30,70,90]){
 const price=precoParaMargem(c,pl,0,3,target);
 if(price===null) continue;
 assert(lucro(price,c,pl,0,3).lucro/price*100>=target-1e-8);
 for(let cent=1;cent<Math.round(price*100);cent++) assert(lucro(cent/100,c,pl,0,3).lucro/(cent/100)*100<target+1e-8);
 cases++;
}
console.log('PASS: 6 assertions + '+cases+' minimum-price cases verified in cents.');
assert.equal(precoParaMargem(10,'invalid',0,0,15),null);
for (const value of [NaN,Infinity,-Infinity]) assert.equal(precoParaMargem(value,'shopee',0,0,15),null);
console.log('PASS: invalid platform and non-finite costs rejected');
