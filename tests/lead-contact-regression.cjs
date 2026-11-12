// Run contact handlers offline: window.open/location are captured, never used.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const cities = ['bertioga', 'guaruja', 'itanhaem', 'mongagua', 'peruibe', 'praia-grande', 'santos', 'sao-vicente'];
const servicePages = cities.map(city => `litoral-prime-imoveis/servicos/cidade-servico/${city}-avaliacao.html`);
for (const city of ['itanhaem', 'praia-grande', 'sao-vicente']) {
  for (const service of ['automacao', 'captacao', 'consultoria', 'descricao-ia', 'venda-imovel']) {
    servicePages.push(`litoral-prime-imoveis/servicos/cidade-servico/${city}-${service}.html`);
  }
}
let cases = 0;

function scriptContaining(html, marker) {
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)]
    .map(match => match[1]).filter(script => script.includes(marker));
  assert.equal(scripts.length, 1, `Expected one script containing ${marker}`);
  return scripts[0];
}

for (const file of servicePages) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const title = html.match(/<title>([^<]+)<\/title>/)[1];
  const script = scriptContaining(html, 'function handlePageLead');
  for (const omitted of [null, 'nome', 'telefone', 'tipo', 'all-controls']) {
    const alerts = [], opened = [];
    const values = { nome: '  Ana & João  ', telefone: '  +55 11 99999-0000  ', tipo: '  Avaliação & visita  ' };
    if (omitted && omitted !== 'all-controls') values[omitted] = '   ';
    const context = {
      document: { title }, alert: message => alerts.push(message),
      window: { open: (...args) => opened.push(args) },
    };
    vm.createContext(context);
    vm.runInContext(script, context, { filename: file });
    assert.deepEqual(opened, [], 'Loading the form must not open WhatsApp');
    let prevented = false;
    const result = context.handlePageLead({
      preventDefault() { prevented = true; },
      target: { querySelector(selector) {
        if (omitted === 'all-controls') return null;
        const key = { 'input[type="text"]': 'nome', 'input[type="tel"]': 'telefone', select: 'tipo' }[selector];
        assert.ok(key, `Unexpected selector ${selector}`);
        return { value: values[key] };
      } },
    });
    assert.equal(result, false);
    assert.equal(prevented, true);
    if (omitted) {
      assert.deepEqual(opened, []);
      assert.deepEqual(alerts, ['Preencha nome, telefone e tipo de interesse.']);
    } else {
      assert.deepEqual(alerts, []);
      assert.equal(opened.length, 1);
      assert.equal(opened[0][1], '_blank');
      const url = new URL(opened[0][0]);
      assert.equal(url.origin, 'https://wa.me');
      assert.equal(url.pathname, '/5511954346288');
      assert.equal(url.searchParams.get('text'), `Olá! Tenho interesse em Avaliação & visita no serviço: ${title.split('|')[0].trim()}. Nome: Ana & João, Telefone: +55 11 99999-0000`);
    }
    cases++;
  }
}

const leadFile = 'leads/sobrado-geminado-peruibe.html';
const leadHtml = fs.readFileSync(path.join(root, leadFile), 'utf8');
const leadTitle = leadHtml.match(/<title>([^<]+)<\/title>/)[1];
const leadScript = scriptContaining(leadHtml, "const form = document.getElementById('lead-form')");
for (const scenario of ['missing-name', 'missing-phone', 'empty-time', 'chosen-time']) {
  const alerts = [];
  let handler;
  const fields = {
    'lead-nome': { value: scenario === 'missing-name' ? ' ' : '  Ana & João  ' },
    'lead-telefone': { value: scenario === 'missing-phone' ? ' ' : '  +55 11 99999-0000  ' },
    'lead-horario': { value: scenario === 'chosen-time' ? '  Tarde  ' : '' },
  };
  const context = {
    document: {
      title: leadTitle,
      getElementById(id) {
        if (id === 'lead-form') return { addEventListener(event, callback) {
          assert.equal(event, 'submit'); handler = callback;
        } };
        assert.ok(fields[id], `Unexpected field ${id}`);
        return fields[id];
      },
    },
    window: { location: { href: 'about:blank' } },
    alert: message => alerts.push(message),
  };
  vm.createContext(context);
  vm.runInContext(leadScript, context, { filename: leadFile });
  assert.equal(typeof handler, 'function');
  let prevented = false;
  handler({ preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  if (scenario.startsWith('missing-')) {
    assert.equal(context.window.location.href, 'about:blank');
    assert.deepEqual(alerts, ['Preencha nome e WhatsApp.']);
  } else {
    assert.deepEqual(alerts, []);
    const url = new URL(context.window.location.href);
    assert.equal(url.origin, 'https://wa.me');
    assert.equal(url.pathname, '/5511954346288');
    assert.equal(url.searchParams.get('text'), `Olá! Tenho interesse no imóvel: Sobrado geminado - Peruíbe. Nome: Ana & João, WhatsApp: +55 11 99999-0000, Horário: ${scenario === 'chosen-time' ? 'Tarde' : 'Não informado'}`);
  }
  cases++;
}

const quickFile = 'litoral-prime-imoveis/servicos/captura-rapida.html';
const quickHtml = fs.readFileSync(path.join(root, quickFile), 'utf8');
const quickScript = scriptContaining(quickHtml, "const form = document.getElementById('lead-form')");
assert.match(quickHtml, /Revise e envie para solicitar atendimento/);
for (const scenario of ['missing-name', 'missing-phone', 'empty-interest', 'chosen-interest', 'missing-form']) {
  const alerts = [];
  let handler;
  const fields = {
    'lead-nome': { value: scenario === 'missing-name' ? ' ' : '  Ana & João  ' },
    'lead-telefone': { value: scenario === 'missing-phone' ? ' ' : '  +55 11 99999-0000  ' },
    'lead-interesse': { value: scenario === 'chosen-interest' ? '  Avaliação & visita + consultoria?  ' : '' },
  };
  const context = {
    document: {
      getElementById(id) {
        if (id === 'lead-form') {
          if (scenario === 'missing-form') return null;
          return { addEventListener(event, callback) {
            assert.equal(event, 'submit'); handler = callback;
          } };
        }
        assert.ok(fields[id], `Unexpected field ${id}`);
        return fields[id];
      },
    },
    window: { location: { href: 'about:blank' } },
    alert: message => alerts.push(message),
  };
  vm.createContext(context);
  vm.runInContext(quickScript, context, { filename: quickFile });
  assert.equal(context.window.location.href, 'about:blank', 'Loading the form must not open WhatsApp');
  if (scenario === 'missing-form') {
    assert.equal(handler, undefined);
    assert.deepEqual(alerts, []);
  } else {
    assert.equal(typeof handler, 'function');
    let prevented = false;
    handler({ preventDefault() { prevented = true; } });
    assert.equal(prevented, true);
    if (scenario.startsWith('missing-')) {
      assert.equal(context.window.location.href, 'about:blank');
      assert.deepEqual(alerts, ['Preencha nome e WhatsApp.']);
    } else {
      assert.deepEqual(alerts, []);
      const url = new URL(context.window.location.href);
      assert.equal(url.origin, 'https://wa.me');
      assert.equal(url.pathname, '/5511954346288');
      assert.equal([...url.searchParams.keys()].length, 1, 'Input must remain inside the message parameter');
      const interest = scenario === 'chosen-interest' ? 'Avaliação & visita + consultoria?' : 'Não informado';
      assert.equal(url.searchParams.get('text'), `Olá! Tenho interesse: ${interest}. Nome: Ana & João, WhatsApp: +55 11 99999-0000`);
    }
  }
  cases++;
}

console.log(`Passed ${cases} offline contact-form cases across ${servicePages.length + 2} pages; no network requests.`);
