/* Contact requests only. No newsletter enrollment, cookies, PII analytics or local storage. */
(() => {
  'use strict';
  const endpoint = 'https://formsubmit.co/ajax/comercial@praia.digital';
  document.querySelectorAll('form[data-pd-lead]').forEach(form => {
    const button = form.querySelector('[type="submit"]');
    const status = form.querySelector('[data-lead-status]');
    let busy = false;
    let sent = false;
    button.disabled = false;
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (busy || sent || !form.reportValidity()) return;
      if (form.elements._honey.value) return;
      const nome = form.elements.nome.value.trim();
      if (!nome) { status.textContent = 'Informe seu nome.'; form.elements.nome.focus(); return; }
      busy = true; button.disabled = true; form.setAttribute('aria-busy', 'true');
      status.textContent = 'Enviando sua solicitação…';
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 15000);
      // Only the pathname is recorded: query strings may contain private information.
      const payload = {
        _subject: 'Solicitação de contato — Praia Digital', _template: 'table', _honey: '',
        nome, email: form.elements.email.value.trim(),
        telefone: form.elements.telefone.value.trim(), interesse: form.elements.interesse.value,
        mensagem: form.elements.mensagem.value.trim(), origem: location.pathname,
        consentimento: form.elements.consentimento.value,
        data_consentimento: new Date().toISOString(), versao_formulario: '2026-11-12'
      };
      try {
        const response = await fetch(endpoint, {
          method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(payload), signal: controller.signal, credentials: 'omit', referrerPolicy: 'no-referrer'
        });
        const data = await response.json();
        if (!response.ok || !(data.success === true || data.success === 'true')) throw new Error('unconfirmed');
        sent = true;
        status.textContent = 'Solicitação aceita pelo serviço de envio. A entrega na caixa de e-mail ainda depende do provedor. Se precisar, fale conosco pelo WhatsApp.';
        button.textContent = 'Solicitação enviada';
        form.reset();
      } catch (_) {
        status.textContent = 'Não conseguimos confirmar o envio. Seus dados foram preservados nesta página. A solicitação pode ter sido recebida: não reenviamos automaticamente. Use o WhatsApp ou e-mail para confirmar antes de tentar novamente.';
      } finally {
        clearTimeout(timeout); busy = false; button.disabled = sent;
        form.removeAttribute('aria-busy'); status.focus();
      }
    });
  });
})();
