(() => {
  'use strict';
  const el = id => document.getElementById('referral-' + id);
  const form = document.getElementById('property-referral');
  if (!form) return;
  const channel = el('channel');
  const contact = el('contact');
  const city = el('city');
  const type = el('type');
  const summary = el('summary');
  const preview = el('preview');
  const draft = el('draft');
  const body = el('body');
  const status = el('status');

  function resetDraft() {
    preview.hidden = true;
    draft.removeAttribute('href');
    body.value = '';
    status.textContent = '';
    contact.setCustomValidity('');
    city.setCustomValidity('');
    summary.setCustomValidity('');
  }
  function updateChannel() {
    const byPhone = channel.value === 'whatsapp';
    contact.type = byPhone ? 'tel' : 'email';
    contact.autocomplete = byPhone ? 'tel' : 'email';
    el('contact-label').textContent = byPhone ? 'Seu WhatsApp' : 'Seu e-mail';
    contact.value = '';
    resetDraft();
  }
  form.addEventListener('input', resetDraft);
  channel.addEventListener('change', updateChannel);
  form.addEventListener('submit', event => {
    event.preventDefault();
    resetDraft();
    const byPhone = channel.value === 'whatsapp';
    const ownContact = contact.value.trim();
    if (byPhone && (!/^\+?[0-9 ().-]+$/.test(ownContact) ||
        !/^[0-9]{8,15}$/.test(ownContact.replace(/\D/g, '')))) {
      contact.setCustomValidity('Informe um número de WhatsApp com DDD.');
    }
    if (!city.value.trim()) city.setCustomValidity('Informe a cidade.');
    if (!summary.value.trim()) summary.setCustomValidity('Escreva um resumo sem identificação.');
    if (!form.reportValidity()) return;

    const oneLine = value => value.trim().replace(/[\r\n]+/g, ' ');
    const message = [
      'Contato para retorno (' + (byPhone ? 'WhatsApp' : 'E-mail') + '): ' + oneLine(ownContact),
      'Cidade: ' + oneLine(city.value),
      'Tipo de imóvel: ' + oneLine(type.value),
      'Resumo: ' + oneLine(summary.value),
    ].join('\r\n');
    try {
      draft.href = 'mailto:comercial@praia.digital?subject=' +
        encodeURIComponent('Indicação de imóvel - Afiliado') + '&body=' + encodeURIComponent(message);
      body.value = message;
      preview.hidden = false;
      status.textContent = 'Rascunho preparado. A página não enviou a mensagem.';
      draft.focus();
    } catch {
      status.textContent = 'Não foi possível preparar o rascunho. Use a opção manual abaixo.';
    }
  });
  el('fields').disabled = false;
})();
