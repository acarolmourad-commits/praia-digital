/* Local search only: never send a budget under a different purpose silently. */
(function () {
  'use strict';
  const form=document.getElementById('smartsearch');
  if(!form) return;
  const search=window.PDPropertySearch;
  const purpose=form.elements.finalidade;
  const query=form.elements.q;
  const status=document.getElementById('home-search-status');
  let previous=purpose.value;
  function changePurpose(next) {
    if(previous && search.budgetUnit(previous)!==search.budgetUnit(next)) {
      query.value=search.withoutBudget(query.value);
      status.textContent='Orçamento limpo: informe o preço de compra ou o aluguel mensal para a nova finalidade.';
    }
    purpose.value=next;
    previous=next;
  }
  purpose.addEventListener('change',function () {
    changePurpose(this.value);
    // The latest explicit selector choice takes precedence over old purpose words.
    query.value=query.value.replace(/\b(?:comprar|compra|venda|alugar|aluguel|loca[cç][aã]o)\b/gi,' ').replace(/\s+/g,' ').trim();
  });
  query.addEventListener('input',function () {
    if(/\b(comprar|compra|venda|alugar|aluguel|locacao)\b/.test(search.normalize(this.value))) changePurpose(search.parse(this.value).finalidade);
  });
})();
