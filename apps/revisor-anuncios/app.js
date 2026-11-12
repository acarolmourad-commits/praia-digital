(function () {
  'use strict';
  const { MODES, FIELDS, review } = window.PraiaConsistency;
  const $ = id => document.getElementById(id);
  const records = [
    { id: 'ref', title: 'Ficha de referência', help: 'Dados conferidos com a fonte responsável. Essa é a base da comparação.' },
    { id: 'v1', title: 'Versão 1 do anúncio', help: 'Transcreva os mesmos campos da primeira versão que deseja revisar.' },
    { id: 'v2', title: 'Versão 2 do anúncio', help: 'Transcreva os campos da segunda versão. Não complete dados por suposição.' }
  ];
  let isDemo = false;
  let currentText = '';

  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  for (const record of records) {
    const box = element('fieldset', undefined, 'record');
    box.append(element('legend', record.title), element('p', record.help));
    if (record.id !== 'ref') {
      const label = element('label', 'Nome da versão (opcional)');
      label.htmlFor = `${record.id}-name`;
      const input = element('input');
      input.id = `${record.id}-name`; input.type = 'text'; input.maxLength = 120;
      input.placeholder = record.id === 'v1' ? 'Ex.: portal A' : 'Ex.: material da equipe';
      input.autocomplete = 'off'; label.append(input); box.append(label);
    }
    for (const field of FIELDS) {
      const text = field.key === 'area' ? 'Área (mesmo tipo em todas as fichas)' : field.key === 'price' ? 'Preço pedido (R$)' : field.label;
      const label = element('label', text);
      label.htmlFor = `${record.id}-${field.key}`;
      const input = element(field.key === 'mode' ? 'select' : 'input');
      input.id = `${record.id}-${field.key}`; input.name = input.id;
      if (field.key === 'mode') {
        const empty = element('option', 'Não informado'); empty.value = ''; input.append(empty);
        for (const [value, title] of Object.entries(MODES)) {
          const option = element('option', title); option.value = value; input.append(option);
        }
      } else {
        input.type = 'text'; input.autocomplete = 'off'; input.maxLength = 30;
        input.inputMode = ['rooms', 'parking'].includes(field.key) ? 'numeric' : 'decimal';
        input.placeholder = 'Não informado'; input.setAttribute('aria-describedby', 'format-help');
      }
      label.append(input); box.append(label);
    }
    $('record-fields').append(box);
  }

  function readRecord(id) {
    const data = Object.fromEntries(FIELDS.map(f => [f.key, $(`${id}-${f.key}`).value]));
    data.name = id === 'ref' ? 'Ficha de referência' : $(`${id}-name`).value;
    return data;
  }

  function removeErrors() {
    $('errors').hidden = true; $('errors').replaceChildren();
    document.querySelectorAll('[aria-invalid]').forEach(e => e.removeAttribute('aria-invalid'));
  }

  function invalidate() {
    if (!$('report').hidden) $('live-status').textContent = 'Os campos mudaram. Compare novamente para gerar um relatório atualizado.';
    $('report').hidden = true; currentText = ''; $('report-text').value = '';
    $('copy-status').textContent = ''; removeErrors();
  }
  $('review-form').addEventListener('input', invalidate);
  $('review-form').addEventListener('change', invalidate);

  const statusNames = {
    match: 'Coincide', different: 'Diferença', reference_missing: 'Referência incompleta',
    missing: 'Não informado na versão', incomparable: 'Preço não comparável'
  };

  $('review-form').addEventListener('submit', event => {
    event.preventDefault(); removeErrors();
    const result = review(readRecord('ref'), [readRecord('v1'), readRecord('v2')], $('confirmed').checked);
    if (!result.ok) {
      $('report').hidden = true;
      $('errors').append(element('strong', 'Confira os campos antes de comparar:'));
      const list = element('ul'); let firstInput;
      for (const error of result.errors) {
        const fieldLabel = FIELDS.find(f => f.key === error.field)?.label || 'Confirmação';
        list.append(element('li', `${error.record} — ${fieldLabel}: ${error.message}`));
        const id = error.field === 'confirmed' ? 'confirmed' : `${error.record === 'Ficha de referência' ? 'ref' : error.record === 'Versão 1' ? 'v1' : 'v2'}-${error.field}`;
        const input = $(id); input.setAttribute('aria-invalid', 'true');
        if (!firstInput) firstInput = input;
      }
      $('errors').append(list); $('errors').hidden = false;
      $('live-status').textContent = ''; firstInput?.focus(); return;
    }

    const identification = $('property').value.trim() || 'Sem identificação';
    const date = new Date().toLocaleString('pt-BR');
    $('report-meta').textContent = `${identification} · Gerado em ${date}`;
    $('report-demo').hidden = !isDemo;
    $('different-count').textContent = result.counts.different;
    $('pending-count').textContent = result.counts.pending;
    $('matching-count').textContent = result.counts.matching;
    $('report-tables').replaceChildren();
    const text = [
      'PRAIA DIGITAL — RELATÓRIO DE CONSISTÊNCIA',
      `${identification} · Gerado em ${date}`,
      ...(isDemo ? ['DEMONSTRAÇÃO COM DADOS FICTÍCIOS.'] : []),
      `Diferenças: ${result.counts.different}. Itens sem conclusão: ${result.counts.pending}. Campos coincidentes: ${result.counts.matching}.`,
      'Contagem por campo e por versão. Coincidência não comprova a correção do dado no mundo real.', ''
    ];
    for (let i = 0; i < 2; i++) {
      const rows = result.rows.filter(r => r.version === i);
      const section = element('section', undefined, 'table-section');
      const title = element('h3', rows[0].name); title.id = `version-heading-${i}`; section.append(title);
      const wrap = element('div', undefined, 'table-wrap');
      wrap.tabIndex = 0; wrap.setAttribute('role', 'region'); wrap.setAttribute('aria-labelledby', title.id);
      const table = element('table');
      const caption = element('caption', `${rows[0].name}: cinco campos comparados à ficha de referência`);
      caption.className = 'sr-only'; table.append(caption);
      const thead = element('thead'); const head = element('tr');
      for (const label of ['Campo', 'Referência', 'Esta versão', 'Resultado']) { const th = element('th', label); th.scope = 'col'; head.append(th); }
      thead.append(head); table.append(thead);
      const tbody = element('tbody'); text.push(rows[0].name.toUpperCase());
      for (const row of rows) {
        const tr = element('tr'); const label = element('th', row.label); label.scope = 'row';
        const outcome = element('td');
        outcome.append(element('span', statusNames[row.status], `status ${row.status === 'match' || row.status === 'different' ? row.status : 'pending'}`), element('p', row.detail));
        tr.append(label, element('td', row.reference), element('td', row.value), outcome); tbody.append(tr);
        text.push(`${row.label}: referência ${row.reference}; versão ${row.value}. ${statusNames[row.status]}. ${row.detail}`);
      }
      text.push(''); table.append(tbody); wrap.append(table); section.append(wrap); $('report-tables').append(section);
    }
    text.push('Confira diferenças com a fonte responsável e compare novamente após corrigir.',
      'Limites: não lê portais ou documentos; não confirma disponibilidade, taxas, propriedade ou validade jurídica; não substitui vistoria ou avaliação.',
      'Regras locais. Dados não enviados nem salvos entre sessões.', 'https://praia.digital/');
    currentText = text.join('\n'); $('report-text').value = currentText;
    $('report').hidden = false; $('report-title').focus();
    $('live-status').textContent = `Comparação concluída: ${result.counts.different} diferenças e ${result.counts.pending} itens sem conclusão.`;
  });

  $('clear').addEventListener('click', () => {
    $('review-form').reset(); isDemo = false; $('demo-status').hidden = true;
    invalidate(); $('live-status').textContent = 'Todos os campos foram limpos.'; $('property').focus();
  });
  $('example').addEventListener('click', () => {
    invalidate(); isDemo = true; $('demo-status').hidden = false;
    $('property').value = 'DEMO-001 · apartamento fictício';
    const examples = {
      ref: { mode: 'venda', area: '70,53', rooms: '2', parking: '1', price: '600.000,00' },
      v1: { name: 'Portal A — exemplo fictício', mode: 'venda', area: '70,53', rooms: '3', parking: '1', price: '595.000,00' },
      v2: { name: 'Versão da equipe — exemplo fictício', mode: 'mensal', area: '70,53', rooms: '2', parking: '', price: '3.200,00' }
    };
    for (const [id, fields] of Object.entries(examples)) for (const [key, value] of Object.entries(fields)) $(`${id}-${key}`).value = value;
    $('confirmed').checked = true;
    $('live-status').textContent = 'Exemplo fictício carregado. Clique em Comparar as versões para ver o resultado.';
  });
  $('print').addEventListener('click', () => { if (currentText) window.print(); });
  $('copy').addEventListener('click', async () => {
    if (!currentText) return;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(currentText); $('copy-status').textContent = 'Relatório copiado.';
    } catch {
      const box = $('report-text'); box.closest('details').open = true; box.focus(); box.select();
      $('copy-status').textContent = 'Texto selecionado. Use o comando Copiar do seu dispositivo (Ctrl+C ou ⌘C no computador).';
    }
  });
})();
