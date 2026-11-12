const {test} = require('node:test');
const assert = require('node:assert/strict');
const {search} = require('../js/content-discovery.js');
const items = [
  {url:'/cidades/sao-sebastiao.html',title:'São Sebastião — guia local',category:'Cidades e bairros'},
  {url:'/blog/financiamento.html',title:'Financiamento: perguntas e respostas',category:'Artigos'},
  {url:'/guias/ficha.html',title:'Comparação de bairros',category:'Guias e checklists'}
];
test('accent-insensitive search and multiple words narrow results',()=>{
  assert.deepEqual(search(items,'sao sebastiao',''),[items[0]]);
  assert.deepEqual(search(items,'comparação bairros',''),[items[2]]);
});
test('category intersects the query rather than broadening it',()=>{
  assert.deepEqual(search(items,'financiamento','Cidades e bairros'),[]);
  assert.deepEqual(search(items,'','Artigos'),[items[1]]);
});
test('empty query, no match and punctuation are safe',()=>{
  assert.deepEqual(search(items,'',''),items);
  assert.deepEqual(search(items,'inexistente',''),[]);
  assert.deepEqual(search(items,'<script>',''),[]);
});
test('title matches precede matches in the path',()=>{
  const catalog=[{url:'/blog/bairro.html',title:'Outro assunto',category:'Artigos'}, {url:'/blog/guia.html',title:'Bairro: como comparar',category:'Artigos'}];
  assert.deepEqual(search(catalog,'bairro',''),[catalog[1],catalog[0]]);
});
