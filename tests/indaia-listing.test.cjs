const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname,'../imoveis/duas-casas-indaia-432m2.html'),'utf8');
const data = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
let checks=0;
for(const text of ['R$ 1.150.000','432 m²','307,91 m²','7 quartos','6 suítes','12 × 36 m','uma no térreo e três no pavimento superior','três quartos, sendo duas suítes','450 m','Avenida Anchieta','instituição financeira','index, follow','13 fotografias reais']) {assert.ok(html.includes(text),text); checks++;}
assert.equal(data.offers.price,'1150000'); checks++;
assert.equal(data.offers.priceCurrency,'BRL'); checks++;
for(const privateOrWrong of ['Jorge Mansour','542','713.065','2.000.000','864 m²','a 50 m da praia','wa.me','teste-nao-aprovado','libfile_']) {assert.ok(!html.includes(privateOrWrong),privateOrWrong); checks++;}
assert.equal((html.match(/<h1>/g)||[]).length,1); checks++;
assert.ok(html.includes('mailto:comercial@praia.digital')); checks++;
console.log(`${checks} verificações de conteúdo aprovadas; página final com galeria real.`);

assert.equal(data.image.length,13);
assert.ok(!html.includes('data-photo-status'));
