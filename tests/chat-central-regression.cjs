'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const file = 'ia/chat-central.html';
const html = fs.readFileSync(path.join(root, file), 'utf8');
const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)]
  .filter(([, attrs]) => !/\bsrc\s*=|ld\+json/i.test(attrs)).map(([, , code]) => code);
let checks = 0;
async function test(name, fn) { await fn(); checks++; }
function setup({hostname = 'praia.digital', backend = false, response, rejected = false} = {}) {
  const nodes = new Map();
  function node() { return {value: '', innerHTML: '', children: [], scrollHeight: 50,
    appendChild(child) { this.children.push(child); }}; }
  for (const [, id] of html.matchAll(/\bid="([^"]+)"/g)) nodes.set(id, node());
  const requests = [], opened = [];
  const context = vm.createContext({
    document: { getElementById(id) { return nodes.get(id); }, createElement: node },
    location: {hostname}, setTimeout(fn) { fn(); },
    open(...args) { opened.push(args); },
    // This stub is the only network capability in the VM; no real request is made.
    async fetch(url, options) {
      requests.push({url, options});
      if (!options) return {ok: backend};
      if (rejected) throw new Error('Synthetic network failure');
      return response || {ok: true, async json() { return {output: 'Synthetic reply'}; }};
    }
  });
  context.window = context;
  for (const script of scripts) new vm.Script(script, {filename: file}).runInContext(context);
  return {context, nodes, requests, opened,
    async ready() { await new Promise(resolve => setImmediate(resolve)); },
    async send(text) { nodes.get('chatInput').value = text; await context.sendChat(); },
    lastMessage() { return nodes.get('chatWindow').children.at(-1)?.innerHTML || ''; }};
}
(async () => {
  await test('inline scripts and event handlers compile', () => {
    for (const script of scripts) new vm.Script(script, {filename: file});
    for (const [, handler] of html.matchAll(/\bon(?:click|keydown)="([^"]+)"/g)) new vm.Script(handler, {filename: file});
  });
  await test('backend detection failure retains local fallback', async () => {
    const app = setup(); await app.ready();
    assert.equal(app.context.__pdBackend, false);
    await app.send('ROI');
    assert.match(app.lastMessage(), /\/ia\/ia-investidores\.html/);
    assert.equal(app.requests.length, 1, 'fallback must not post a message');
  });
  await test('backend detection success uses the configured API', async () => {
    const app = setup({backend: true}); await app.ready();
    assert.equal(app.context.__pdBackend, 'https://api.praia.digital');
    await app.send('Synthetic question');
    assert.equal(app.requests.length, 2);
    const request = app.requests[1];
    assert.equal(request.url, 'https://api.praia.digital/api/chat.js');
    assert.equal(request.options.method, 'POST');
    assert.deepEqual(JSON.parse(request.options.body), {agent: 'comercial', input: 'Synthetic question', context: {}});
    assert.match(app.lastMessage(), /Synthetic reply/);
    assert.equal(app.nodes.get('chatInput').value, '');
  });
  for (const [name, output] of [['missing', undefined], ['object', {}], ['null', null], ['blank', '   ']]) {
    await test(`backend ${name} output is handled`, async () => {
      const app = setup({backend: true, response: {ok: true, async json() { return {output}; }}});
      await app.ready(); await app.send('Synthetic question'); assert.match(app.lastMessage(), /Sem resposta/);
    });
  }
  for (const [name, config] of [
    ['HTTP error', {response: {ok: false, async json() { throw new Error('must not parse failed response'); }}}],
    ['invalid JSON', {response: {ok: true, async json() { throw new SyntaxError('Synthetic invalid JSON'); }}}],
    ['network failure', {rejected: true}]
  ]) {
    await test(name, async () => {
      const app = setup({backend: true, ...config}); await app.ready(); await app.send('Synthetic question');
      assert.match(app.lastMessage(), /Backend indisponível/);
    });
  }
  await test('user and backend markup are rendered literally', async () => {
    const app = setup({backend: true, response: {ok: true, async json() { return {output: '<img src=x onerror=alert(1)>'}; }}});
    await app.ready(); await app.send('<script>synthetic</script>');
    assert.match(app.nodes.get('chatWindow').children.at(-2).innerHTML, /&lt;script&gt;/);
    assert.match(app.lastMessage(), /&lt;img/);
  });
  const routes = {
    marketing: 'ia-marketing.html', preço: 'ia-avaliacao.html', captação: 'ia-captacao.html', contrato: 'ia-juridica.html',
    airbnb: 'ia-temporada.html', roi: 'ia-investidores.html', seo: 'ia-portais.html', gestão: 'ia-gestao.html',
    atendimento: 'ia-atendimento.html', conteúdo: 'ia-conteudo.html', mercado: 'ia-mercado.html', imagem: 'ia-imagens.html',
    vídeo: 'ia-videos.html', comercial: 'ia-comercial.html'
  };
  for (const [question, route] of Object.entries(routes)) {
    await test(`GitHub Pages fallback: ${route}`, async () => {
      const app = setup({hostname: 'acarolmourad-commits.github.io'}); await app.ready(); await app.send(question);
      assert.equal(app.opened.length, 1);
      assert.deepEqual(app.opened[0], ['/ia/' + route, '_blank', 'noopener']);
      assert(fs.existsSync(path.join(root, 'ia', route)));
      assert.equal(app.nodes.get('chatInput').value, '');
      assert.equal(app.requests.length, 1, 'fallback must not post a message');
    });
  }
  await test('unknown GitHub Pages topic offers guidance without opening a URL', async () => {
    const app = setup({hostname: 'acarolmourad-commits.github.io'}); await app.ready(); await app.send('Olá');
    assert.equal(app.opened.length, 0); assert.match(app.lastMessage(), /palavras-chave/);
  });
  for (const [question, route] of [['marketing', 'ia-marketing'], ['contrato', 'ia-juridica'], ['cap rate', 'ia-investidores'], ['Olá', null]]) {
    await test(`local fallback ${question}`, async () => {
      const app = setup(); await app.ready(); await app.send(question);
      assert.match(app.lastMessage(), route ? new RegExp('/ia/' + route + '\\.html') : /Abra o agente direto/);
    });
  }
  await test('blank input sends and opens nothing', async () => {
    const app = setup({backend: true}); await app.ready(); await app.send('   ');
    assert.equal(app.requests.length, 1); assert.equal(app.opened.length, 0); assert.equal(app.lastMessage(), '');
  });
  console.log(JSON.stringify({checks, passed: checks, network: 'stubbed; no external request'}));
})().catch(error => { console.error(error); process.exitCode = 1; });
