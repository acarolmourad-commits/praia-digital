'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

// Exercise the actual inline handlers without sending messages or submitting forms.
function loadTool(file) {
  const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
  const nodes = new Map();
  const alerts = [], copied = [];
  function node(value = '') {
    const classes = new Set();
    const listeners = {};
    return { value, textContent: '', innerHTML: '', style: {}, children: [],
      classList: { add: c => classes.add(c), remove: c => classes.delete(c), contains: c => classes.has(c) },
      appendChild(child) { this.children.push(child); }, scrollIntoView() {},
      addEventListener(event, handler) { listeners[event] = handler; }, listeners,
    };
  }
  for (const match of html.matchAll(/\bid=["']([^"']+)["']/g)) nodes.set(match[1], node());
  const tabs = [node(), node(), node(), node()];
  const context = vm.createContext({
    document: {
      getElementById(id) { return nodes.get(id) || null; },
      createElement() { return node(); }, querySelectorAll(selector) { assert.equal(selector, '.tab'); return tabs; },
    },
    navigator: { clipboard: { writeText(text) { copied.push(text); return Promise.resolve(); } } },
    alert(message) { alerts.push(message); }, setTimeout(fn) { fn(); },
    fetch() { throw new Error('Tools must not send data while preparing drafts'); },
  });
  context.window = context;
  context.location = { href: '' };
  for (const [, attrs, code] of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (/\bsrc\s*=|application\/ld\+json/i.test(attrs)) continue;
    new vm.Script(code, { filename: file }).runInContext(context);
  }
  return { context, nodes, tabs, alerts, copied,
    set(values) { for (const [id, value] of Object.entries(values)) nodes.get(id).value = String(value); },
  };
}

async function main() {
  const chat = loadTool('ia/ia-atendimento.html');
  chat.context.sendQuick('Quais cidades atendemos?');
  assert.match(chat.nodes.get('chatWindow').children.at(-1).innerHTML, /Santos/);
  chat.set({chatInput: '<img src=x onerror=alert(1)>'});
  chat.context.sendChat();
  assert.equal(chat.nodes.get('chatInput').value, '');
  assert.match(chat.nodes.get('chatWindow').children.at(-2).innerHTML, /&lt;img/);
  assert.match(chat.nodes.get('chatWindow').children.at(-1).innerHTML, /atendimento personalizado/);
  chat.context.sendQuick('Ver oportunidades');
  assert.match(chat.nodes.get('chatWindow').children.at(-1).innerHTML, /imoveis\.html/);

  const commercial = loadTool('ia/ia-comercial.html');
  commercial.set({leadNome:'<Carol>', leadCanal:'E-mail', leadInteresse:'compra', leadCidade:'santos', leadOrcamento:'1000000', leadPrazo:'imediato'});
  commercial.context.runQualifier();
  const quote = commercial.nodes.get('commercialResult').innerHTML;
  assert.match(quote, /&lt;Carol&gt;/);
  assert.match(quote, /Santos/);
  assert.match(quote, /1\.000\.000/);
  assert.match(quote, /HOT/);
  assert.match(quote, /href="\/imoveis\.html"/);
  assert.match(quote, /Nenhum contato foi salvo ou enviado/);
  assert.doesNotMatch(quote, /ROI estimado|Apto 2q|Pousada 8|oportunidade alinhada/);
  commercial.set({leadNome:'', leadOrcamento:'', leadPrazo:'90d'});
  commercial.context.runQualifier();
  assert.match(commercial.nodes.get('commercialResult').innerHTML, /orçamento a confirmar/);
  assert.match(commercial.nodes.get('commercialResult').innerHTML, /COLD/);
  commercial.set({leadOrcamento:'-1'}); commercial.context.runQualifier();
  assert.match(commercial.nodes.get('commercialResult').textContent, /orçamento válido/);

  const legal = loadTool('ia/ia-juridica.html');
  legal.set({legalParte:'<Carol>', legalObjeto:'Apartamento', legalValor:'500000', legalCidade:'santos'});
  for (const kind of ['contrato','proposta','distrato','recibo','procuracao','checklist']) {
    legal.set({legalTipo:kind}); legal.context.runLegal();
    const output = legal.nodes.get('legalResult').innerHTML;
    assert.match(output, /&lt;Carol&gt;/); assert.match(output, /Santos/);
    assert.doesNotMatch(output, /NaN|undefined/);
  }
  legal.set({legalTipo:'contrato',legalParte:'',legalObjeto:'',legalValor:''}); legal.context.runLegal();
  assert.match(legal.nodes.get('legalResult').innerHTML, /________________/);
  legal.set({legalValor:'-1'}); legal.context.runLegal();
  assert.match(legal.nodes.get('legalResult').textContent, /valor válido/);

  const season = loadTool('ia/ia-temporada.html');
  season.set({sTipo:'apartamento',sCidade:'santos',sBairro:'Gonzaga',sDorms:2,sDiferencial:'Wi-Fi',sDiaria:350});
  season.context.runSeason('publicar');
  assert.match(season.context.__seasonText, /Gonzaga/);
  assert.match(season.context.__seasonText, /R\$ 350\/noite/);
  season.context.copyText(season.context.__seasonText); await Promise.resolve();
  assert.equal(season.copied[0], season.context.__seasonText);
  assert.match(season.nodes.get('seasonResult').innerHTML, /copyText\(window\.__seasonText\)/);
  season.set({pPreco:200,pAlta:450,pOcupacao:70,pDespesa:600}); season.context.runSeason('pricing');
  assert.match(season.context.__seasonText, /Receita mensal estimada: R\$ 6\.825/);
  assert.match(season.context.__seasonText, /Lucro estimado\/mês: R\$ 6\.225/);
  assert.doesNotMatch(season.context.__seasonText, /Yield estimado/);
  season.set({pOcupacao:101}); season.context.runSeason('pricing');
  assert.match(season.context.__seasonText, /ocupação entre 0% e 100%/);
  season.set({pOcupacao:0}); season.context.runSeason('pricing');
  assert.match(season.context.__seasonText, /Receita mensal estimada: R\$ 0/);
  season.set({pOcupacao:70,pDespesa:-1}); season.context.runSeason('pricing');
  assert.match(season.context.__seasonText, /despesas maiores ou iguais a zero/);
  for (const values of [
    {pPreco:'1e308',pAlta:'1e308',pOcupacao:50,pDespesa:0},
    {pPreco:200,pAlta:450,pOcupacao:50,pDespesa:'1e308'},
    {pPreco:Number.MAX_SAFE_INTEGER,pAlta:Number.MAX_SAFE_INTEGER,pOcupacao:100,pDespesa:0},
    {pPreco:'1e-308',pAlta:'1e-308',pOcupacao:50,pDespesa:1},
  ]) {
    season.set(values); season.context.runSeason('pricing');
    assert.match(season.context.__seasonText, /limite de precisão/);
    assert.doesNotMatch(season.context.__seasonText, /Receita mensal estimada|Infinity|NaN/);
    assert.doesNotMatch(season.nodes.get('seasonResult').innerHTML, /Receita mensal estimada|Infinity|NaN/);
  }
  season.set({pPreco:200,pAlta:450,pOcupacao:100,pDespesa:600}); season.context.runSeason('pricing');
  assert.match(season.context.__seasonText, /Receita mensal estimada: R\$ 9\.750/);
  assert.match(season.context.__seasonText, /Lucro estimado\/mês: R\$ 9\.150/);
  season.set({pOcupacao:0}); season.context.runSeason('pricing');
  assert.match(season.context.__seasonText, /Receita mensal estimada: R\$ 0/);
  assert.match(season.context.__seasonText, /Lucro estimado\/mês: R\$ -600/);
  season.set({pPreco:200.5,pAlta:450.5,pOcupacao:50.5,pDespesa:0}); season.context.runSeason('pricing');
  assert.match(season.context.__seasonText, /Ocupação alvo: 50\.5%/);
  assert.match(season.context.__seasonText, /Receita mensal estimada: R\$ 4\.931/);
  assert.doesNotMatch(season.context.__seasonText, /limite de precisão|Infinity|NaN/);
  season.set({rTipo:'regras',aTipo:'positiva'});
  for (const mode of ['respostas','avaliacoes']) {
    season.context.runSeason(mode); assert.match(season.context.__seasonText, /Rascunho: confirme os fatos/);
  }
  season.context.setTab(season.tabs[1], 'pricing');
  assert.equal(season.nodes.get('tab-pricing').style.display, 'block');
  assert.equal(season.nodes.get('tab-publicar').style.display, 'none');

  const posts = loadTool('marketing/gerador-posts-redes-sociais-2026.html');
  posts.context.gerar(); assert.equal(posts.alerts.length, 1);
  for (const channel of ['Instagram','LinkedIn','WhatsApp']) {
    posts.set({tema:'Gestão de temporada',cidade:'Santos',canal:channel}); posts.context.gerar();
    assert.match(posts.nodes.get('resultado').textContent, /Gestão de temporada em Santos/);
    assert.match(posts.nodes.get('resultado').textContent, /https:\/\/praia\.digital/);
    assert.equal(posts.nodes.get('resultado').style.display, 'block');
  }
  const automation = loadTool('automacao-imobiliarias.html');
  assert.equal(automation.nodes.has('y'), false, 'Removed footer year must be optional');
  let prevented = false;
  const event = {preventDefault() { prevented = true; }};
  await automation.nodes.get('automacaoLeadForm').listeners.submit(event);
  assert.equal(prevented, true);
  assert.equal(automation.context.location.href, '');
  assert.match(automation.nodes.get('automacaoFeedback').textContent, /Preencha todos os campos/);
  automation.set({automacaoNome:'Carol & Cia',automacaoImob:'Praia Digital',automacaoCidade:'Santos',automacaoFone:'11999990000'});
  await automation.nodes.get('automacaoLeadForm').listeners.submit(event);
  const draft = new URL(automation.context.location.href);
  assert.equal(draft.protocol, 'mailto:');
  assert.equal(draft.pathname, 'comercial@praia.digital');
  assert.match(draft.searchParams.get('body'), /Nome: Carol & Cia\nImobiliária: Praia Digital/);
  assert.match(automation.nodes.get('automacaoFeedback').textContent, /Rascunho preparado/);
  assert.match(automation.nodes.get('automacaoFeedback').textContent, /nenhum interesse foi registrado automaticamente/);
  console.log('PASS: five replacement tools and automation inquiry prepare valid drafts without sending.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
