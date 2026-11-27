/* Progressive enhancement: the complete directory remains usable without JS. */
(function () {
  'use strict';
  const form = document.getElementById('catalog-search-form');
  const catalog = document.getElementById('catalogo-apps');
  if (!form || !catalog) return;
  const query = document.getElementById('app-query');
  const goal = document.getElementById('app-goal');
  const clear = document.getElementById('app-clear');
  const status = document.getElementById('app-results');
  const resourceResults = document.getElementById('app-resource-results');
  const resourceList = document.getElementById('app-resource-list');
  const onlyResult = document.getElementById('app-only-result');
  const jumpToResults = document.getElementById('app-jump-results');
  const empty = document.getElementById('app-empty');
  const broaden = document.getElementById('app-search-all');
  const keepGoal = document.getElementById('app-keep-goal');
  const printSelection = document.getElementById('app-print');
  const shareLink = document.getElementById('app-share-link');
  const includeQuery = document.getElementById('app-share-query');
  const copySelection = document.getElementById('app-copy');
  const copyStatus = document.getElementById('app-copy-status');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR').replace(/[^a-z0-9]+/g, ' ').trim();
  const groups = Array.from(catalog.querySelectorAll('.pd-catalog-group')).map(section => ({
    section,
    id: section.getAttribute('aria-labelledby'),
    cards: Array.from(section.querySelectorAll('a.card')).map(card => ({
      card,
      text: normalize(card.textContent + ' ' + card.getAttribute('href') + ' ' + section.querySelector('h2').textContent)
    }))
  }));
  const total = groups.reduce((sum, group) => sum + group.cards.length, 0);
  const resources = resourceResults && resourceList
    ? Array.from(document.querySelectorAll('a[data-catalog-resource]'), link => {
      const title = link.querySelector('.info b')?.textContent.trim() || link.textContent.trim();
      const description = link.querySelector('.info small')?.textContent || '';
      return {title, href: link.getAttribute('href'), group: link.dataset.catalogResource,
        text: normalize(title + ' ' + description)};
    })
    : [];
  function shareUrl() {
    const url = new URL('/apps/', window.location.origin);
    if (goal.value) url.searchParams.set('objetivo', goal.value.slice('grupo-'.length));
    if (includeQuery?.checked) url.searchParams.set('busca', query.value.trim());
    url.hash = 'buscar-apps';
    return url.href;
  }
  function filter() {
    const terms = normalize(query.value).split(' ').filter(Boolean);
    let count = 0;
    let otherMatches = 0;
    let matchedCard;
    for (const group of groups) {
      let visible = 0;
      for (const item of group.cards) {
        const matchesText = terms.every(term => item.text.includes(term));
        const match = matchesText && (!goal.value || group.id === goal.value);
        if (matchesText && !match) otherMatches++;
        item.card.hidden = !match;
        if (match) {
          visible++;
          matchedCard = item.card;
        }
      }
      group.section.hidden = visible === 0;
      count += visible;
    }
    const related = [];
    let otherResources = 0;
    for (const resource of resources) {
      if (!terms.length || !terms.every(term => resource.text.includes(term))) continue;
      if (!goal.value || resource.group === goal.value) related.push(resource);
      else otherResources++;
    }
    if (resourceResults && resourceList) {
      resourceResults.hidden = related.length === 0;
      resourceList.replaceChildren(...related.map(resource => {
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = resource.href;
        link.textContent = resource.title;
        item.append(link);
        return item;
      }));
    }
    status.textContent = count === 1 ? '1 de ' + total + ' aplicativos encontrado.' : count + ' de ' + total + ' aplicativos encontrados.';
    if (related.length) status.textContent += related.length === 1
      ? ' 1 recurso complementar encontrado.'
      : ' ' + related.length + ' recursos complementares encontrados.';
    if (jumpToResults) jumpToResults.hidden = count < 2 || (!goal.value && terms.length === 0);
    if (onlyResult) {
      onlyResult.hidden = count !== 1;
      if (count === 1) {
        onlyResult.href = matchedCard.href;
        const title = matchedCard.querySelector('.info b').cloneNode(true);
        title.querySelector('.badge')?.remove();
        onlyResult.textContent = 'Abrir ' + title.textContent.trim();
      } else {
        onlyResult.removeAttribute('href');
        onlyResult.textContent = '';
      }
    }
    const noMatches = count === 0 && related.length === 0;
    empty.hidden = !noMatches;
    if (keepGoal) keepGoal.hidden = !noMatches || !goal.value;
    if (broaden) {
      broaden.hidden = !noMatches || otherMatches + otherResources === 0;
      if (!broaden.hidden) {
        if (otherMatches) status.textContent += otherMatches === 1
          ? ' Há uma ferramenta correspondente em outro objetivo.'
          : ' Há ' + otherMatches + ' ferramentas correspondentes em outros objetivos.';
        if (otherResources) status.textContent += otherResources === 1
          ? ' Há um recurso complementar em outro objetivo.'
          : ' Há ' + otherResources + ' recursos complementares em outros objetivos.';
      }
    }
    if (printSelection) printSelection.disabled = count === 0;
    if (includeQuery) {
      includeQuery.disabled = terms.length === 0;
      if (includeQuery.disabled) includeQuery.checked = false;
    }
    if (shareLink) shareLink.value = shareUrl();
    if (copySelection) copySelection.textContent = includeQuery?.checked ? 'Copiar link da busca' : 'Copiar link do objetivo';
    if (copyStatus) copyStatus.textContent = '';
  }
  function readObjective() {
    const name = new URLSearchParams(window.location.search).get('objetivo');
    const id = 'grupo-' + name;
    goal.value = groups.some(group => group.id === id) ? id : '';
  }

  function removeIncomingQuery() {
    const url = new URL(window.location.href);
    if (!url.searchParams.has('busca')) return;
    url.searchParams.delete('busca');
    window.history.replaceState(window.history.state, '', url);
  }

  function saveObjective() {
    const url = new URL(window.location.href);
    if (goal.value) url.searchParams.set('objetivo', goal.value.slice('grupo-'.length));
    else url.searchParams.delete('objetivo');
    if (url.href !== window.location.href) window.history.replaceState(window.history.state, '', url);
  }

  function reset() {
    query.value = '';
    if (includeQuery) includeQuery.checked = false;
    removeIncomingQuery();
    goal.value = '';
    saveObjective();
    filter();
  }
  if (printSelection) printSelection.addEventListener('click', () => window.print());
  jumpToResults?.addEventListener('click', () => {
    catalog.querySelector('.pd-catalog-group:not([hidden]) a.card:not([hidden])')?.focus();
  });
  if (copySelection && shareLink && copyStatus) copySelection.addEventListener('click', async () => {
    const value = shareLink.value;
    try {
      await navigator.clipboard.writeText(value);
      if (shareLink.value === value) copyStatus.textContent = 'Link copiado. Cole na conversa ou guarde para depois.';
    } catch (_) {
      if (shareLink.value !== value) return;
      shareLink.focus();
      shareLink.select();
      copyStatus.textContent = 'Selecione e copie o endereço no campo Link para compartilhar.';
    }
  });
  query.addEventListener('input', () => {
    removeIncomingQuery();
    if (includeQuery) includeQuery.checked = false;
    filter();
  });
  function clearSearch() {
    query.value = '';
    removeIncomingQuery();
    filter();
    query.focus();
  }
  query.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || event.isComposing || !query.value) return;
    event.preventDefault();
    clearSearch();
  });
  includeQuery?.addEventListener('change', filter);
  goal.addEventListener('change', () => {
    saveObjective();
    filter();
  });
  form.addEventListener('submit', event => event.preventDefault());
  clear.addEventListener('click', () => { reset(); query.focus(); });
  if (keepGoal) keepGoal.addEventListener('click', clearSearch);
  if (broaden) broaden.addEventListener('click', () => {
    goal.value = '';
    saveObjective();
    filter();
    query.focus();
  });
  const objectives = document.getElementById('objetivos-apps');
  let handledHash = window.location.hash;
  if (objectives) objectives.addEventListener('click', event => {
    // Preserve the current tab when opening a group in another tab/window.
    if (event.defaultPrevented || event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const link = event.target.closest('a[href^="#grupo-"]');
    if (link) {
      reset();
      handledHash = link.getAttribute('href');
    }
  });
  window.addEventListener('hashchange', () => {
    // The click already restored the target; do not erase a subsequent query.
    if (window.location.hash === handledHash) return;
    handledHash = window.location.hash;
    if (groups.some(group => '#' + group.id === window.location.hash)) reset();
  });
  // Browsers may restore form values when returning from an app.
  window.addEventListener('pageshow', () => {
    readObjective();
    filter();
  });
  window.addEventListener('popstate', () => {
    readObjective();
    filter();
  });
  readObjective();
  const incomingQuery = new URLSearchParams(window.location.search).get('busca');
  if (incomingQuery) query.value = incomingQuery.slice(0, query.maxLength);
  form.hidden = false;
  filter();
  // A direct group fragment must still locate its heading after applying filters.
  const initialGroup = groups.find(group => '#' + group.id === window.location.hash);
  if (initialGroup?.section.hidden) {
    reset();
    initialGroup.section.querySelector('h2')?.scrollIntoView();
  }
})();
