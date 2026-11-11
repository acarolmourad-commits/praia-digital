const test = require('node:test');
const assert = require('node:assert/strict');
const { calculate } = require('../js/roi-temporada-core.js');
const base = { valor:595000,adr:750,ocup:55,noites:200,custos:38000,plataforma:15.5,iptu:2400,cond:7200,ir:15 };
const calc = changes => calculate({...base,...changes});
const close = (a,b) => assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
test('Independent baseline: 110 nights, gross 82500, net 18795.625',()=>{
 const r=calc({});assert.equal(r.valid,true);close(r.nights,110);close(r.gross,82500);close(r.platformFee,12787.5);
 close(r.costs,47600);close(r.beforeTax,22112.5);close(r.tax,3316.875);close(r.net,18795.625);
 close(r.grossYield,13.865546218487394);close(r.netYield,3.1589285714285715);close(r.payback,4760000/150365);
});
test('City cannot silently inject benchmark values',()=>assert.deepEqual(calc({cidade:'Bertioga'}),calc({cidade:'Santos'})));
test('Zero occupied or available nights correctly reports loss and unavailable payback',()=>{
 for(const changes of [{ocup:0},{noites:0},{adr:0}]){const r=calc(changes);assert.equal(r.valid,true);close(r.gross,0);close(r.tax,0);close(r.net,-47600);assert.equal(r.payback,null);}
});
test('100% occupancy and 365 nights are valid without artificial yield caps',()=>{const r=calc({valor:1000,ocup:100,noites:365});assert.equal(r.valid,true);close(r.nights,365);assert.ok(r.netYield>100);});
test('No fees, taxes or costs uses gross as net',()=>{const r=calc({plataforma:0,custos:0,iptu:0,cond:0,ir:0});close(r.gross,r.net);});
test('Zero saldo and 100% tax have no infinite payback',()=>{for(const changes of [{custos:69712.5,iptu:0,cond:0},{ir:100}]){const r=calc(changes);close(r.net,0);assert.equal(r.payback,null);}});
test('100% platform fee leaves costs, no negative simulated tax',()=>{const r=calc({plataforma:100});close(r.net,-47600);close(r.tax,0);});
test('Inputs remain unchanged',()=>{const data={...base};calculate(data);assert.deepEqual(data,base);});
for(const key of Object.keys(base))for(const value of [NaN,Infinity,-Infinity,undefined,null,'', '55', -1]){
 test(`Reject ${key}=${String(value)}`,()=>{const r=calc({[key]:value});assert.equal(r.valid,false);assert.ok(r.errors[key]);});
}
for(const [key,value]of [['valor',0],['ocup',150],['plataforma',101],['ir',101],['noites',366],['noites',1.5]])test(`Range ${key}=${value}`,()=>{const r=calc({[key]:value});assert.equal(r.valid,false);assert.ok(r.errors[key]);});
test('Huge finite input or tiny denominator cannot produce Infinity',()=>{for(const changes of [{adr:Number.MAX_VALUE},{valor:Number.MIN_VALUE}])assert.equal(calc(changes).valid,false);});
