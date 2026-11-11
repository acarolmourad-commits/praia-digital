(function () {
  'use strict';
  const form = document.getElementById('compra-form');
  if (!form || !window.CompraViabilidade) return;
  const core = window.CompraViabilidade;
  const $ = id => document.getElementById(id);
  const currency = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 2 });
  const decimal = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 });
  const money = n => currency.format(Math.abs(n) < 0.005 ? 0 : n);
  const pct = n => decimal.format(n) + '%';
  const escape = text => String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  let edited = false;
  let announcement;
  function values() {
    const v = {};
    form.querySelectorAll('input, select').forEach(el => { v[el.id] = el.type === 'number' ? el.valueAsNumber : el.value; });
    return v;
  }
  function visibility(id, show) {
    const group = $(id);
    group.hidden = !show;
    group.querySelectorAll('input, select').forEach(el => { el.disabled = !show; });
  }
  function syncSections() {
    const financed = $('purchase').value === 'financiado';
    const housing = $('goal').value === 'moradia';
    visibility('financing-fields', financed);
    $('entry').disabled = !financed;
    $('entry').closest('.v-field').hidden = !financed;
    visibility('housing-fields', housing);
    visibility('rental-fields', !housing);
    visibility('season-fields', !housing && $('goal').value === 'temporada');
    visibility('annual-fields', !housing && $('goal').value === 'anual');
  }
  const metric = (label, value, hint = '') => '<div class="v-metric"><span>' + label + '</span><strong>' + value + '</strong>' + (hint ? '<small>' + hint + '</small>' : '') + '</div>';
  const row = (label, value) => '<div><dt>' + label + '</dt><dd>' + value + '</dd></div>';
  const list = rows => '<dl class="v-breakdown">' + rows.join('') + '</dl>';
  function common(v, r) {
    const benchmark = r.reference
      ? '<p>Referência municipal: <strong>' + money(r.reference) + '/m²</strong>. Seu preço está ' + pct(Math.abs(r.m2Deviation)) + (r.m2Deviation >= 0 ? ' acima' : ' abaixo') + ' desse valor.</p><p class="v-hint">FipeZAP, outubro/2026, preços anunciados. Diferenças de bairro, padrão e conservação não estão ajustadas. Isso não indica, por si só, oportunidade ou sobrepreço.</p>'
      : '<p class="v-hint">Sem benchmark verificado para esta cidade nesta versão. Compare imóveis semelhantes no mesmo bairro.</p>';
    const debt = r.principal > 0
      ? list([row('Primeira parcela-base', money(r.firstPayment)), row('Última parcela-base', money(r.lastPayment)), row('Seguros/tarifas mensais informados', money(v.financeFees)), row('Juros totais no prazo', money(r.totalInterest))]) + '<p class="v-hint">' + (v.system === 'sac' ? 'SAC' : 'Price') + ' · ' + v.months + ' meses · ' + pct(v.annualRate) + ' efetivos a.a. Sem TR/IPCA; não é proposta de crédito.</p>'
      : '<p class="v-hint">Compra sem saldo financiado. Não há parcela ou encargos de financiamento neste cenário.</p>';
    return '<section class="v-summary-section"><h3>Capital inicial e financiamento</h3>' + list([row('Entrada / pagamento do imóvel', money(v.purchase === 'avista' ? v.price : v.entry)), row('Custos de aquisição', money(r.acquisition)), row('Reforma e mobília', money(v.upfront)), row('Total inicial necessário', money(r.upfront)), row('Saldo a financiar', money(r.principal))]) + debt + (r.principal > 0 && r.entryPercent < 20 ? '<p class="v-result-warning">Entrada inferior a 20%. Verifique a cota financiável e a aprovação com a instituição; esta simulação não garante crédito.</p>' : '') + '</section><section class="v-summary-section"><h3>Preço por m² · ' + escape(v.city) + '</h3><p><strong>' + money(r.pricePerM2) + '/m²</strong> no imóvel informado</p>' + benchmark + '</section>';
  }
  function housing(v, r) {
    const h = r.housing;
    const difference = r.ownerFirstMonth - r.renterFirstMonth;
    const comparison = Math.abs(h.difference) < 1 ? 'Os patrimônios simulados ficam próximos.' : (h.difference > 0 ? 'Comprar' : 'Alugar e investir') + ' apresenta maior patrimônio neste cenário, por ' + money(Math.abs(h.difference)) + '.';
    return '<div class="v-result-main"><p class="v-result-caption">Desembolso da compra · primeiro mês</p><p class="v-result-amount" data-result="owner-month">' + money(r.ownerFirstMonth) + '</p><p>' + money(Math.abs(difference)) + (difference >= 0 ? ' a mais' : ' a menos') + ' que alugar um imóvel equivalente.</p></div><div class="v-metrics">' + metric('Alugar · primeiro mês', money(r.renterFirstMonth), 'Aluguel + encargos informados') + metric('Capital inicial da compra', money(r.upfront), 'Entrada + aquisição + extras') + '</div><section class="v-summary-section"><h3>De onde vem o desembolso</h3>' + list([row('Parcela-base', money(r.firstPayment)), row('Seguros/tarifas da operação', money(r.principal > 0 ? v.financeFees : 0)), row('Custos mensais do proprietário', money(r.fixedCosts))]) + '</section><section class="v-summary-section"><h3>Patrimônio em ' + v.years + ' anos</h3><p class="v-hint">Mesmo capital inicial e orçamento mensal. Valores nominais, com venda hipotética do imóvel ao final.</p><div class="v-metrics">' + metric('Comprar e investir sobras', money(h.buyerAfterSale)) + metric('Alugar e investir sobras', money(h.renterInvestments)) + '</div><p class="v-callout">' + comparison + ' O resultado depende das premissas, não mede liquidez nem prevê o mercado.</p><details class="v-details"><summary>Ver a composição do patrimônio</summary>' + list([row('Imóvel no horizonte', money(h.propertyValue)), row('Investimentos de quem compra', money(h.buyerInvestments)), row('Dívida restante', money(h.residualDebt)), row('Custos da venda hipotética', money(h.saleCosts)), row('Patrimônio comprador sem vender', money(h.buyerBeforeSale))]) + '</details><details class="v-details"><summary>Se a valorização mudar?</summary><p class="v-hint">Todas as outras premissas são mantidas. A coluna da direita é patrimônio comprador menos patrimônio de quem aluga, após venda.</p><div class="v-table-wrap"><table class="v-sensitivity"><caption>Sensibilidade à valorização anual</caption><thead><tr><th scope="col">Valorização a.a.</th><th scope="col">Diferença patrimonial</th></tr></thead><tbody>' + r.sensitivity.map(s => '<tr><td>' + pct(s.appreciation) + '</td><td>' + money(s.difference) + '</td></tr>').join('') + '</tbody></table></div></details></section>' + common(v, r);
  }
  function rental(v, r) {
    const a = r.rental;
    const cash = a.cashflow / 12;
    const flow = cash < 0 ? 'O cenário exige aportes para cobrir os custos e a dívida.' : 'Saldo após as despesas e parcelas informadas. Não é uma garantia de renda.';
    let occupancy = '';
    if (v.goal === 'temporada') {
      const nights = a.breakEvenNights;
      occupancy = '<section class="v-summary-section"><h3>Ocupação e ponto de equilíbrio</h3>' + list([row('Ocupação informada', v.nights + ' noites / ano (' + pct(v.nights / 365 * 100) + ')'), row('Noites para cobrir custos e dívida', nights === null ? 'Não calculável com estas premissas' : nights + ' / ano')]) + (nights > 365 ? '<p class="v-result-warning">Seriam necessárias mais de 365 noites. Este cenário não cobre custos e dívida mesmo com ocupação integral.</p>' : '<p class="v-hint">Diária e custos constantes. Desconte dias de uso próprio e indisponibilidade ao avaliar se a ocupação é possível.</p>') + '</section>';
    }
    return '<div class="v-result-main"><p class="v-result-caption">Fluxo de caixa mensal médio · primeiro ano</p><p class="v-result-amount" data-result="cashflow-month">' + money(cash) + '</p><p>' + flow + '</p></div><div class="v-metrics">' + metric('Rendimento bruto', pct(a.grossYield) + ' a.a.', 'Receita anual ÷ preço do imóvel') + metric('Líquido operacional', pct(a.operatingYield) + ' a.a.', 'Antes do financiamento; despesas informadas') + '</div><section class="v-summary-section"><h3>As contas do primeiro ano</h3>' + list([row('Receita estimada' + (v.goal === 'anual' ? ' após vacância' : ''), money(a.gross)), row('Despesas variáveis (' + pct(v.variableRate) + ')', money(a.variableCosts)), row('Custos fixos anuais', money(r.fixedCosts * 12)), row('Resultado operacional', money(a.operatingNet)), row('Parcelas + encargos da dívida', money(a.firstYearDebt)), row('Caixa após dívida', money(a.cashflow))]) + '<p class="v-hint">Rendimento operacional sobre custo total da compra: <strong>' + pct(a.yieldOnTotalCost) + ' a.a.</strong> Base: preço + aquisição + reforma/mobília. Não é retorno líquido sobre seu capital próprio.</p><p class="v-result-warning">Não inclui despesas ou tributos que você deixou de informar. Sazonalidade pode gerar meses negativos mesmo com média anual positiva.</p></section>' + occupancy + common(v, r);
  }
  function render(announce = false) {
    clearTimeout(announcement);
    syncSections();
    const v = values();
    const r = core.calculate(v);
    form.querySelectorAll('input,select').forEach(el => {
      const error = r.errors[el.id];
      el.setAttribute('aria-invalid', error ? 'true' : 'false');
      const line = $(el.id + '-error');
      if (line) line.textContent = error || '';
    });
    $('result-label').textContent = edited ? 'Suas premissas' : 'Exemplo ilustrativo';
    $('form-errors').hidden = r.valid;
    if (!r.valid) {
      const count = Object.keys(r.errors).length;
      $('principal').textContent = 'Confira os valores';
      $('form-errors').textContent = 'Revise ' + count + (count === 1 ? ' campo indicado' : ' campos indicados') + ' para atualizar a análise.';
      $('result').innerHTML = '<div class="v-empty"><h3>Vamos conferir os dados?</h3><p>Corrija os campos indicados. O resultado anterior foi removido para evitar uma leitura incorreta.</p></div>';
      $('result-title').textContent = 'Análise aguardando dados';
      $('result-live').textContent = 'Análise indisponível. Há campos que precisam de correção.';
      return r;
    }
    $('principal').textContent = money(r.principal);
    $('result-title').textContent = v.goal === 'moradia' ? 'Comprar ou alugar' : (v.goal === 'temporada' ? 'Renda de temporada' : 'Renda de aluguel anual');
    $('result').innerHTML = v.goal === 'moradia' ? housing(v, r) : rental(v, r);
    if (announce) announcement = setTimeout(() => {
      $('result-live').textContent = 'Análise atualizada. ' + (v.goal === 'moradia' ? 'Desembolso da compra no primeiro mês: ' + money(r.ownerFirstMonth) + '. Aluguel e encargos: ' + money(r.renterFirstMonth) : 'Fluxo de caixa mensal médio no primeiro ano: ' + money(r.rental.cashflow / 12)) + '.';
    }, 500);
    return r;
  }
  form.addEventListener('input', () => { edited = true; render(true); });
  form.addEventListener('change', () => { edited = true; render(true); });
  form.addEventListener('submit', event => {
    event.preventDefault();
    const r = render(true);
    if (r.valid) {
      $('result-title').focus();
      $('result-title').scrollIntoView({ block: 'start', behavior: 'auto' });
    } else {
      const field = $(Object.keys(r.errors)[0]);
      const details = field.closest('details');
      if (details) details.open = true;
      field.focus();
    }
  });
  form.addEventListener('reset', () => { setTimeout(() => { edited = false; render(true); }, 0); });
  function labelFooter() {
    if ($('pdFlNome')) $('pdFlNome').setAttribute('aria-label', 'Seu nome para receber novidades');
    if ($('pdFlEmail')) $('pdFlEmail').setAttribute('aria-label', 'Seu e-mail para receber novidades');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', labelFooter);
  else labelFooter();
  render();
  form.querySelector('[type="submit"]').disabled = false;
}());
