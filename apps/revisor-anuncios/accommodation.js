(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const form = $('accommodation-form');
  const download = $('accommodation-download');
  const pending = $('accommodation-pending');
  let revision = 0;
  let firstPendingField;
  function invalidate() {
    revision++;
    firstPendingField = null;
    if (download?.hasAttribute('href')) {
      URL.revokeObjectURL(download.href);
      download.removeAttribute('href');
      download.hidden = true;
    }
    const hadResult = !$('accommodation-result').hidden;
    $('accommodation-result').hidden = true;
    $('accommodation-text').value = '';
    $('accommodation-copy').disabled = false;
    if (pending) {
      pending.value = '';
      $('accommodation-pending-panel').hidden = true;
      $('accommodation-copy-pending').disabled = false;
    }
    $('accommodation-status').textContent = hadResult ? 'A conferência mudou. Gere um novo resumo antes de compartilhar.' : '';
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', invalidate);
  form.addEventListener('change', invalidate);
  form.addEventListener('reset', invalidate);
  $('accommodation-generate').addEventListener('click', () => {
    invalidate();
    const value = id => $(id).value.trim() || 'Não informado';
    const date = id => {
      const iso = $(id).value;
      return iso ? iso.split('-').reverse().join('/') : 'Não informada';
    };
    const checks = [...form.querySelectorAll('input[type="checkbox"]')];
    $('accommodation-text').value = [
      'PRAIA DIGITAL — CONFERÊNCIA MANUAL DA ACOMODAÇÃO',
      `Resumo gerado em ${new Date().toLocaleString('pt-BR')}`,
      `Categoria: ${value('accommodation-name')}`,
      `Canal / fonte 1: ${value('accommodation-source-one')}`,
      `Consulta à fonte 1: ${date('accommodation-date-one')}`,
      `Canal / fonte 2: ${value('accommodation-source-two')}`,
      `Consulta à fonte 2: ${date('accommodation-date-two')}`,
      '',
      ...checks.map(input => `${input.checked ? 'MARCADO COMO CONFERIDO' : 'PENDENTE'}: ${input.closest('label').querySelector('span').textContent.trim()}`),
      '', `Pendências e próximo passo: ${value('accommodation-notes')}`, '',
      'Registro das marcações do usuário; não é verificação automática dos canais nem aprovação para publicar.',
      'Fontes não informadas continuam pendentes. Dados não enviados nem salvos entre sessões.',
      'Datas de consulta informadas pelo usuário; não confirmam disponibilidade atual.',
      'https://praia.digital/apps/revisor-anuncios/#conferencia-hospedagem'
    ].join('\n');
    if (download && typeof URL.createObjectURL === 'function') {
      const file = new Blob([$('accommodation-text').value], { type: 'text/plain;charset=utf-8' });
      download.href = URL.createObjectURL(file);
      download.hidden = false;
    }
    if (pending) {
      const items = [];
      function addPending(field, message) {
        if (!firstPendingField) firstPendingField = field;
        items.push(message);
      }
      for (const [id, message] of [
        ['accommodation-source-one', 'Identificar a primeira fonte.'],
        ['accommodation-source-two', 'Identificar a segunda fonte.'],
        ['accommodation-date-one', 'Registrar quando a primeira fonte foi consultada.'],
        ['accommodation-date-two', 'Registrar quando a segunda fonte foi consultada.']
      ]) {
        const field = $(id);
        if (!field.value.trim()) addPending(field, message);
      }
      for (const input of checks.filter(input => !input.checked)) {
        const label = input.closest('label').querySelector('span').textContent.trim();
        addPending(input, 'Confirmar se ' + label.charAt(0).toLowerCase() + label.slice(1));
      }
      if (items.length) {
        const category = $('accommodation-name').value.trim();
        if (category) items.unshift('Categoria: ' + category);
        pending.value = items.join('\n');
        $('accommodation-pending-panel').hidden = false;
      }
    }
    $('accommodation-result').hidden = false;
    $('accommodation-text').focus();
    $('accommodation-status').textContent = 'Resumo gerado. Confira as fontes antes de compartilhar.';
  });
  async function copyText(field, button, confirmation) {
    if ($('accommodation-result').hidden || button.disabled || !field.value) return;
    const request = revision;
    button.disabled = true;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(field.value);
      if (request === revision) $('accommodation-status').textContent = confirmation;
    } catch {
      if (request !== revision) return;
      field.focus();
      field.select();
      $('accommodation-status').textContent = 'Texto selecionado. Use o comando Copiar do seu dispositivo (Ctrl+C ou ⌘C no computador).';
    } finally {
      if (request === revision) button.disabled = false;
    }
  }
  $('accommodation-first-pending')?.addEventListener('click', () => {
    firstPendingField?.focus();
  });
  $('accommodation-copy').addEventListener('click', event => {
    copyText($('accommodation-text'), event.currentTarget, 'Resumo da acomodação copiado.');
  });
  $('accommodation-copy-pending')?.addEventListener('click', event => {
    copyText(pending, event.currentTarget, 'Pendências copiadas. Cole os itens desejados no relatório.');
  });
  $('accommodation-generate').disabled = false;
})();
