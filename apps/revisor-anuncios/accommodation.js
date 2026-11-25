(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const form = $('accommodation-form');
  const download = $('accommodation-download');
  let revision = 0;
  function invalidate() {
    revision++;
    if (download?.hasAttribute('href')) {
      URL.revokeObjectURL(download.href);
      download.removeAttribute('href');
      download.hidden = true;
    }
    const hadResult = !$('accommodation-result').hidden;
    $('accommodation-result').hidden = true;
    $('accommodation-text').value = '';
    $('accommodation-copy').disabled = false;
    $('accommodation-status').textContent = hadResult ? 'A conferência mudou. Gere um novo resumo antes de compartilhar.' : '';
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', invalidate);
  form.addEventListener('change', invalidate);
  form.addEventListener('reset', invalidate);
  $('accommodation-generate').addEventListener('click', () => {
    invalidate();
    const value = id => $(id).value.trim() || 'Não informado';
    const checks = [...form.querySelectorAll('input[type="checkbox"]')];
    $('accommodation-text').value = [
      'PRAIA DIGITAL — CONFERÊNCIA MANUAL DA ACOMODAÇÃO',
      `Resumo gerado em ${new Date().toLocaleString('pt-BR')}`,
      `Categoria: ${value('accommodation-name')}`,
      `Canal / fonte 1: ${value('accommodation-source-one')}`,
      `Canal / fonte 2: ${value('accommodation-source-two')}`,
      '',
      ...checks.map(input => `${input.checked ? 'MARCADO COMO CONFERIDO' : 'PENDENTE'}: ${input.closest('label').querySelector('span').textContent.trim()}`),
      '', `Pendências e próximo passo: ${value('accommodation-notes')}`, '',
      'Registro das marcações do usuário; não é verificação automática dos canais nem aprovação para publicar.',
      'Fontes não informadas continuam pendentes. Dados não enviados nem salvos entre sessões.',
      'https://praia.digital/apps/revisor-anuncios/#conferencia-hospedagem'
    ].join('\n');
    if (download && typeof URL.createObjectURL === 'function') {
      const file = new Blob([$('accommodation-text').value], { type: 'text/plain;charset=utf-8' });
      download.href = URL.createObjectURL(file);
      download.hidden = false;
    }
    $('accommodation-result').hidden = false;
    $('accommodation-text').focus();
    $('accommodation-status').textContent = 'Resumo gerado. Confira as fontes antes de compartilhar.';
  });
  $('accommodation-copy').addEventListener('click', async () => {
    if ($('accommodation-result').hidden || $('accommodation-copy').disabled) return;
    const request = revision;
    $('accommodation-copy').disabled = true;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText($('accommodation-text').value);
      if (request === revision) $('accommodation-status').textContent = 'Resumo da acomodação copiado.';
    } catch {
      if (request !== revision) return;
      $('accommodation-text').focus(); $('accommodation-text').select();
      $('accommodation-status').textContent = 'Texto selecionado. Use o comando Copiar do seu dispositivo (Ctrl+C ou ⌘C no computador).';
    } finally {
      if (request === revision) $('accommodation-copy').disabled = false;
    }
  });
  $('accommodation-generate').disabled = false;
})();
