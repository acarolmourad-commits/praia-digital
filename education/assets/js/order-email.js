(() => {
  'use strict';
  // Keep the original mailto available when JavaScript or clipboard access fails.
  document.querySelectorAll('[data-kit], [data-bundle]').forEach(card => {
    const link = card.querySelector('a.cta[href^="mailto:"]');
    if (!link) return;
    const url = new URL(link.href);
    const recipient = decodeURIComponent(url.pathname);
    const subject = url.searchParams.get('subject');
    const body = url.searchParams.get('body');
    if (recipient !== 'comercial@praia.digital' || !subject || !body) return;
    const title = card.querySelector('h2, h3').textContent.trim();
    const text = `Para: ${recipient}\nAssunto: ${subject}\n\n${body}`;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'cta secondary copy-order';
    button.textContent = 'Copiar pedido';
    button.setAttribute('aria-label', `Copiar pedido: ${title}`);
    const status = document.createElement('p');
    status.className = 'order-status';
    status.setAttribute('role', 'status');
    status.hidden = true;
    let fallback;
    button.addEventListener('click', async () => {
      button.disabled = true;
      status.hidden = false;
      status.textContent = 'Preparando o pedido…';
      try {
        await navigator.clipboard.writeText(text);
        if (fallback) fallback.hidden = true;
        status.textContent = 'Pedido copiado. Abra seu e-mail, preencha o destinatário e o assunto indicados e envie a mensagem. O pedido ainda não foi enviado.';
      } catch {
        if (!fallback) {
          fallback = document.createElement('textarea');
          fallback.className = 'order-copy-text';
          fallback.readOnly = true;
          fallback.rows = 9;
          fallback.value = text;
          fallback.setAttribute('aria-label', `Texto do pedido para copiar: ${title}`);
          status.after(fallback);
        }
        fallback.hidden = false;
        fallback.focus();
        fallback.select();
        status.textContent = 'A cópia automática não está disponível. Copie o texto selecionado e envie pelo seu e-mail ao destinatário indicado. O pedido ainda não foi enviado.';
      } finally {
        button.disabled = false;
      }
    });
    link.after(button, status);
  });
})();
