(() => {
  'use strict';
  const boxes = [...document.querySelectorAll('.guide-route input[type="checkbox"]')];
  const progress = document.getElementById('guide-progress');
  const reset = document.getElementById('guide-reset');
  const undo = document.createElement('button');
  undo.type = 'button';
  undo.textContent = 'Desfazer limpeza';
  reset.after(undo);
  let cleared = [];

  const update = () => {
    const count = boxes.filter(box => box.checked).length;
    if (count) cleared = [];
    undo.hidden = cleared.length === 0;
    reset.disabled = count === 0;
    progress.textContent = `${count} de ${boxes.length} conferências marcadas`;
  };
  boxes.forEach(box => box.addEventListener('change', update));
  // Back/forward navigation can restore checkbox state without firing change.
  window.addEventListener('pageshow', update);
  reset.addEventListener('click', () => {
    cleared = boxes.filter(box => box.checked);
    cleared.forEach(box => { box.checked = false; });
    update();
    undo.focus();
  });
  undo.addEventListener('click', () => {
    cleared.forEach(box => { box.checked = true; });
    update();
    reset.focus();
  });
  document.getElementById('guide-print').addEventListener('click', () => window.print());
  document.getElementById('guide-download').addEventListener('click', () => {
    const selected = document.getElementById('guide-export-route').value;
    const routes = [...document.querySelectorAll('.guide-route')].filter(route => !selected || route.id === selected);
    const now = new Date();
    const timestamp = new Intl.DateTimeFormat('pt-BR', {
      dateStyle: 'short', timeStyle: 'short', timeZone: 'America/Sao_Paulo'
    }).format(now);
    const fileDate = new Intl.DateTimeFormat('sv-SE', {
      timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit'
    }).format(now);
    const lines = [
      'Praia Digital — checklist dos aplicativos',
      `Exportado em ${timestamp} (America/Sao_Paulo).`,
      'https://praia.digital/apps/guia-de-uso.html',
      '',
      'As marcações registram esta consulta. Não comprovam aprovação, execução ou resultado.',
      'Um item não marcado pode não ter sido analisado. Confirme seu estado antes de encaminhar.',
      ''
    ];
    routes.forEach(route => {
      lines.push(route.querySelector('h2').textContent.trim());
      lines.push(`https://praia.digital/apps/guia-de-uso.html#${route.id}`);
      route.querySelectorAll('input[type="checkbox"]').forEach(box => {
        const text = box.closest('label').textContent.trim();
        lines.push(`${box.checked ? '[x] Marcado nesta consulta' : '[ ] A conferir (não marcado)'} — ${text}`);
      });
      lines.push('Fonte e data: não informado', 'Responsável: não identificado',
        'Próxima ação e prazo combinado: não informado', '');
    });
    lines.push('Revise o arquivo antes de compartilhar. Complete os campos somente com informações confirmadas.',
      'Os dados não são transferidos automaticamente entre os aplicativos.');
    const status = document.getElementById('guide-download-status');
    let url;
    let anchor;
    try {
      url = URL.createObjectURL(new Blob(['\uFEFF' + lines.join('\n') + '\n'], {type: 'text/plain;charset=utf-8'}));
      anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = `praia-digital-checklist${selected ? `-${selected}` : ''}-${fileDate}.txt`;
      document.body.appendChild(anchor);
      anchor.click();
      status.textContent = `${selected ? 'Arquivo do roteiro “' + routes[0].querySelector('h2').textContent.trim() + '” preparado.' : 'Arquivo dos quatro roteiros preparado.'} Confira os downloads do navegador antes de fechar esta página.`;
    } catch {
      status.textContent = 'Não foi possível preparar o arquivo. Use Imprimir ou salvar em PDF para guardar suas marcações.';
    } finally {
      anchor?.remove();
      if (url) setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
  });
  document.getElementById('guide-actions').hidden = false;
  update();
})();
