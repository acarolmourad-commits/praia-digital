(() => {
  'use strict';
  const names = {name: 'Nome', nome: 'Nome', text: 'Nome', email: 'E-mail', phone: 'Telefone', city: 'Cidade', company: 'Empresa', source: 'Origem', magnet: 'Material', course: 'Curso', faixa_preco: 'Faixa de preço', prazo_interesse: 'Prazo'};
  document.querySelectorAll('form[data-pd-email-form]').forEach((form) => {
    if (form.dataset.emailReady) return;
    form.dataset.emailReady = 'true';
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();
      const address = new URL(form.getAttribute('action'));
      const lines = [];
      for (const field of form.elements) {
        if (!['INPUT','TEXTAREA','SELECT'].includes(field.tagName) || field.disabled ||
            ['password','file','submit','button','reset'].includes(field.type) ||
            (['checkbox','radio'].includes(field.type) && !field.checked)) continue;
        const key = field.name || field.id;
        const value = field.value.trim();
        if (!key || !value) continue;
        const title = field.labels?.[0]?.textContent.trim() || names[key] || field.placeholder || key;
        lines.push(title + ': ' + value);
      }
      const subject = address.searchParams.get('subject') || document.title;
      const text = lines.join('\r\n');
      const status = form.querySelector('[role="status"]') || document.getElementById('formStatus') || document.getElementById('courseFormStatus');
      if (status) status.textContent = 'Revise e envie a mensagem no seu aplicativo de e-mail.';
      window.location.href = 'mailto:comercial@praia.digital?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(text);
    }, true);
    const help = document.createElement('p');
    const link = document.createElement('a');
    link.href = form.getAttribute('action');
    link.textContent = 'comercial@praia.digital';
    help.append('O envio é feito pelo seu aplicativo de e-mail. Você também pode escrever para ', link, '.');
    form.append(help);
  });
})();
