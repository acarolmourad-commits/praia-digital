const assert=require('node:assert/strict');
const {rental,appreciation}=require('../js/imovel-cenarios.js');
const r=rental(1800000,800,30,25,1800);
assert.equal(r.nights,109.5);assert.equal(r.gross,87600);assert.equal(r.net,44100);assert.equal(r.yield,2.45);
assert.equal(rental(1800000,800,0,25,1800).net,-21600);
assert.equal(rental(1800000,800,0,25,1800).payback,null);
for(const [rate,value] of [[-3,1545721.25],[0,1800000],[3,2086693.33],[6,2408806.04]])assert.equal(Number(appreciation(1800000,rate,5).value.toFixed(2)),value);
assert.equal(Number((1800000/234).toFixed(2)),7692.31);
console.log('House default, loss and compound-price calculations passed.');

for(const value of [NaN,Infinity,-1,101])assert.throws(()=>rental(1800000,800,value,25,1800),RangeError);
for(const years of [NaN,0,31,1.5])assert.throws(()=>appreciation(1800000,3,years),RangeError);
assert.throws(()=>rental(0,800,30,25,1800),RangeError);
assert.equal(appreciation(1800000,-100,5).value,0);
