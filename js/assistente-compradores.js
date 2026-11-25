/* Buyer guidance is local and rule-based. No inventory, credit or messaging API. */
(function (root) {
  'use strict';
  const clean = (value, limit = 2000) => String(value || '').trim().slice(0, limit);
  const normalize = value => clean(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const money = value => Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
  function summary(profile) {
    const budget = Number(profile.budget);
    return ['Olá! Gostaria de orientação para comprar um imóvel.',
      'Cidade/bairro: ' + (clean(profile.city, 100) || 'a definir'),
      'Orçamento máximo: ' + (Number.isFinite(budget) && budget >= 1 && budget <= 1e9 ? money(budget) : 'a definir'),
      'Tipo: ' + (clean(profile.type, 100) || 'a definir'),
      'Objetivo: ' + (clean(profile.goal, 100) || 'a definir'),
      'Financiamento: ' + (clean(profile.payment, 100) || 'a definir'),
      'Prazo: ' + (clean(profile.time, 100) || 'a definir'),
      'Preferências: ' + (clean(profile.notes, 600) || 'a definir'),
      'Quero confirmar disponibilidade e condições antes de agendar uma visita.'].join('\n');
  }
  function guidance(question) {
    const m = normalize(question);
    const items = [];
    const add = (text, label, url) => items.push({ text, label, url });
    if (/bertioga|riviera/.test(m)) add('Para Bertioga ou Riviera, registre bairro, tipo e orçamento no perfil. Consulte os anúncios e confirme disponibilidade com a equipe; esta orientação não seleciona um imóvel.', 'Consultar catálogo', '/imoveis.html');
    const withoutCredit = /\b(sem |nao (?:quero |vou |pretendo )?)(?:financ\w*|credito)|\ba vista\b/.test(m);
    if (/(financ|fgts|credito|parcela|entrada|selic|juros)/.test(m) && (!withoutCredit || /fgts/.test(m))) add('Financiamento depende da análise da instituição. Compare o Custo Efetivo Total, prazo e condições de propostas equivalentes. O FGTS tem requisitos próprios; este orientador não confirma elegibilidade nem aprovação.', 'Conferir fontes oficiais', '#fontes');
    if (withoutCredit) add('Você mencionou compra sem financiamento ou à vista. Registre essa preferência no perfil e considere também os custos da aquisição, sem assumir uma taxa fixa.', 'Organizar perfil', '#perfil');
    if (/(document|escritura|itbi|registro|cartorio|contrato)/.test(m)) add('Peça orientação sobre matrícula atualizada, situação do imóvel e documentos das partes antes de contratar. Confirme tributos e emolumentos com prefeitura, cartório e profissional responsável; não aplicamos um percentual genérico.', 'Preparar atendimento', '#perfil');
    if (/(temporada|airbnb|invest|rentabilidade|locacao|renda)/.test(m)) add('Para locação, planeje cenários de receita, vacância e despesas, incluindo manutenção e gestão. Não há retorno garantido nem estimativa automática nesta página.', 'Organizar objetivo de investimento', '#perfil');
    if (/(cidade|melhor|custo|barata|onde)/.test(m)) add('Compare bairros e cidades pelas suas prioridades: deslocamento, serviços, características do imóvel e orçamento. Não existe uma cidade melhor para todos os perfis.', 'Consultar catálogo', '/imoveis.html');
    if (!items.length) add('Preencha o perfil com cidade, orçamento e preferências para preparar um resumo fiel ao que procura. Este orientador não consulta ofertas em tempo real nem interpreta todos os detalhes de uma conversa.', 'Organizar perfil', '#perfil');
    return items;
  }
  const api = { summary, guidance };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (!root.document) return;
  const d = root.document, get = id => d.getElementById(id);
  if (!get('buyer-profile')) return;
  const status = text => { get('buyer-status').textContent = text; };
  const fields = ['city', 'budget', 'type', 'goal', 'payment', 'time', 'notes'];
  get('buyer-profile').addEventListener('submit', event => {
    event.preventDefault();
    if (!get('buyer-profile').reportValidity()) return;
    get('buyer-summary').value = summary(Object.fromEntries(fields.map(key => [key, get('buyer-' + key).value])));
    get('buyer-preview').hidden = false;
    status('Resumo preparado. Revise antes de compartilhar; nada foi enviado.');
    get('buyer-summary').focus();
  });
  get('buyer-profile').addEventListener('input', () => {
    if (!get('buyer-preview').hidden) {
      get('buyer-preview').hidden = true;
      get('buyer-summary').value = '';
      status('Perfil alterado. Prepare novamente o resumo para compartilhar os dados atuais.');
    }
  });
  get('buyer-whatsapp').addEventListener('click', () => {
    const text = clean(get('buyer-summary').value, 2400);
    if (!text) { status('Preencha o resumo antes de preparar o e-mail.'); return; }
    root.open('mailto:comercial@praia.digital?subject=Perfil%20de%20compra&body=' + encodeURIComponent(text), '_blank', 'noopener,noreferrer');
    status('Revise e envie o e-mail para comercial@praia.digital. O site não confirma entrega.');
  });
  get('buyer-copy').addEventListener('click', async () => {
    const text = clean(get('buyer-summary').value, 2400);
    if (!text) { status('Preencha o resumo antes de copiar.'); return; }
    try {
      await root.navigator.clipboard.writeText(text);
      status('Resumo copiado. Nenhuma mensagem foi enviada.');
    } catch (_) {
      get('buyer-summary').focus(); get('buyer-summary').select();
      status('Cópia automática indisponível. O texto foi selecionado para você copiar manualmente.');
    }
  });
  function ask() {
    const text = clean(get('msg').value);
    if (!text) { get('msg').focus(); return; }
    const user = d.createElement('div'); user.className = 'msg user'; user.textContent = text;
    get('chat').appendChild(user);
    guidance(text).forEach(item => {
      const message = d.createElement('div'); message.className = 'msg bot';
      const p = d.createElement('p'); p.textContent = item.text;
      const a = d.createElement('a'); a.textContent = item.label; a.href = item.url;
      message.append(p, a); get('chat').appendChild(message);
    });
    // Bound the local transcript; do not persist questions in browser storage.
    while (get('chat').children.length > 36) get('chat').firstElementChild.remove();
    get('msg').value = ''; get('msg').focus();
  }
  get('buyer-ask').addEventListener('click', ask);
  get('msg').addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); ask(); }
  });
  d.querySelectorAll('[data-q]').forEach(button => button.addEventListener('click', () => {
    get('msg').value = button.dataset.q; get('msg').focus();
  }));
  const initial = new URLSearchParams(root.location.search).get('q');
  if (initial) get('msg').value = clean(initial);
  get('buyer-clear').addEventListener('click', () => {
    get('buyer-profile').reset(); get('buyer-summary').value = ''; get('buyer-preview').hidden = true;
    get('chat').replaceChildren(); get('msg').value = '';
    status('Perfil, resumo e orientações apagados deste formulário.'); get('buyer-city').focus();
  });
})(typeof window !== 'undefined' ? window : globalThis);
