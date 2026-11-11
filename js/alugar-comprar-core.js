/* Pure, deterministic rent-versus-buy model. Rates and balances are nominal BRL. */
(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PDRentBuy = api;
})(typeof globalThis === 'object' ? globalThis : this, function () {
  'use strict';
  const fields = Object.freeze({
    price: { id: 'valor', label: 'Valor do imóvel', min: 1, max: 100000000, value: 595000 },
    rent: { id: 'aluguel', label: 'Aluguel mensal', min: 0, max: 1000000, value: 2800 },
    downPayment: { id: 'entrada', label: 'Entrada', min: 0, max: 100000000, value: 120000 },
    annualInterest: { id: 'taxa', label: 'Juros do financiamento', min: 0, max: 100, value: 11.19 },
    loanYears: { id: 'anos', label: 'Prazo do financiamento', min: 1, max: 50, integer: true, value: 20 },
    horizonYears: { id: 'horizonte', label: 'Horizonte da comparação', min: 1, max: 50, integer: true, value: 10 },
    appreciation: { id: 'valoriz', label: 'Valorização do imóvel', min: -50, max: 100, value: 4 },
    rentGrowth: { id: 'reajAluguel', label: 'Reajuste do aluguel', min: -50, max: 100, value: 4 },
    investmentReturn: { id: 'rendimento', label: 'Retorno líquido dos investimentos', min: -50, max: 100, value: 6 },
    purchaseCostPct: { id: 'custoCompra', label: 'Custos de aquisição', min: 0, max: 30, value: 4 },
    saleCostPct: { id: 'custoVenda', label: 'Custos de venda', min: 0, max: 30, value: 6 },
    annualMaintenance: { id: 'manutencao', label: 'Manutenção anual', min: 0, max: 20, value: 1 },
    ownerMonthly: { id: 'custoProprietario', label: 'Outros custos mensais da compra', min: 0, max: 1000000, value: 0 },
    renterMonthly: { id: 'custoInquilino', label: 'Outros custos mensais do aluguel', min: 0, max: 1000000, value: 0 },
    expenseGrowth: { id: 'reajCustos', label: 'Reajuste dos demais custos', min: -50, max: 100, value: 4 },
    loanMonthly: { id: 'seguros', label: 'Seguros e tarifas mensais do financiamento', min: 0, max: 1000000, value: 0 },
    balanceIndex: { id: 'indexador', label: 'Correção anual do saldo devedor', min: 0, max: 30, value: 0 },
    saleTax: { id: 'impostoVenda', label: 'Provisão de imposto na venda', min: 0, max: 1000000000, value: 0 }
  });
  const defaults = Object.freeze(Object.assign(
    Object.fromEntries(Object.entries(fields).map(([key, field]) => [key, field.value])),
    { rateType: 'nominal', amortization: 'PRICE' }
  ));
  const br = value => value.toLocaleString('pt-BR');

  function validate(raw) {
    const values = {};
    const errors = {};
    for (const [key, field] of Object.entries(fields)) {
      const value = raw && raw[key];
      const number = typeof value === 'number' ? value :
        typeof value === 'string' && value.trim() !== '' ? Number(value) : NaN;
      if (!Number.isFinite(number)) errors[key] = 'Informe um número válido.';
      else if (number < field.min || number > field.max) errors[key] = `Use um valor entre ${br(field.min)} e ${br(field.max)}.`;
      else if (field.integer && !Number.isInteger(number)) errors[key] = 'Informe um número inteiro de anos.';
      else values[key] = number;
    }
    if (values.downPayment > values.price) errors.downPayment = 'A entrada não pode superar o valor do imóvel. Para compra à vista, use o valor integral.';
    for (const [key, options] of Object.entries({ rateType: ['nominal', 'effective'], amortization: ['PRICE', 'SAC'] })) {
      if (!raw || !options.includes(raw[key])) errors[key] = 'Selecione uma opção válida.';
      else values[key] = raw[key];
    }
    return { valid: Object.keys(errors).length === 0, values, errors };
  }

  function monthlyEffective(annualPct) { return Math.expm1(Math.log1p(annualPct / 100) / 12); }
  function payment(principal, rate, months) {
    if (principal === 0) return 0;
    if (rate === 0) return principal / months;
    return principal * rate / -Math.expm1(-months * Math.log1p(rate));
  }

  function calculate(raw) {
    const checked = validate(raw);
    if (!checked.valid) return { valid: false, errors: checked.errors };
    const p = checked.values;
    const months = p.horizonYears * 12;
    const loanMonths = p.loanYears * 12;
    const interestRate = p.rateType === 'nominal' ? p.annualInterest / 1200 : monthlyEffective(p.annualInterest);
    const investmentRate = monthlyEffective(p.investmentReturn);
    const propertyRate = monthlyEffective(p.appreciation);
    const indexRate = monthlyEffective(p.balanceIndex);
    const purchaseCosts = p.price * p.purchaseCostPct / 100;
    const initialCash = p.downPayment + purchaseCosts;
    const financed = p.price - p.downPayment;
    let debt = financed;
    let property = p.price;
    let ownerInvestments = 0;
    let renterInvestments = initialCash;
    let ownerContributions = 0;
    let renterContributions = 0;
    let totalRent = 0;
    let totalOwnerHousing = 0;
    let totalRenterHousing = 0;
    let totalLoanPayments = 0;
    let totalInterest = 0;
    let totalIndexation = 0;
    let firstPayment = 0;
    let firstOwnerCost = 0;
    let firstRenterCost = 0;
    let lastPayment = 0;
    const yearly = [];
    function snapshot(month) {
      const sellingCosts = property * p.saleCostPct / 100;
      const netEquity = property - sellingCosts - p.saleTax - debt;
      const ownerWealth = netEquity + ownerInvestments;
      return { month, year: month / 12, property, debt, sellingCosts, saleTax: p.saleTax,
        netEquity, ownerInvestments, renterInvestments, ownerWealth,
        renterWealth: renterInvestments, difference: ownerWealth - renterInvestments };
    }
    for (let month = 1; month <= months; month += 1) {
      const yearIndex = Math.floor((month - 1) / 12);
      const costFactor = Math.pow(1 + p.expenseGrowth / 100, yearIndex);
      const rent = p.rent * Math.pow(1 + p.rentGrowth / 100, yearIndex);
      let installment = 0;
      const loanActive = financed > 0 && month <= loanMonths;
      if (loanActive) {
        const correction = debt * indexRate;
        debt += correction;
        totalIndexation += correction;
        const remaining = loanMonths - month + 1;
        const interest = debt * interestRate;
        const amortization = remaining === 1 ? debt : Math.min(debt, Math.max(0,
          p.amortization === 'SAC' ? debt / remaining : payment(debt, interestRate, remaining) - interest));
        installment = interest + amortization;
        debt = Math.max(0, debt - amortization);
        totalInterest += interest;
        totalLoanPayments += installment;
      }
      const ownerCost = installment + property * p.annualMaintenance / 1200 +
        p.ownerMonthly * costFactor + (loanActive ? p.loanMonthly * costFactor : 0);
      const renterCost = rent + p.renterMonthly * costFactor;
      const commonBudget = Math.max(ownerCost, renterCost);
      const ownerSaving = commonBudget - ownerCost;
      const renterSaving = commonBudget - renterCost;
      // Existing investments earn first; each month's savings are added at month end.
      ownerInvestments = ownerInvestments * (1 + investmentRate) + ownerSaving;
      renterInvestments = renterInvestments * (1 + investmentRate) + renterSaving;
      ownerContributions += ownerSaving;
      renterContributions += renterSaving;
      totalOwnerHousing += ownerCost;
      totalRenterHousing += renterCost;
      totalRent += rent;
      property *= 1 + propertyRate;
      if (month === 1) { firstPayment = installment; firstOwnerCost = ownerCost; firstRenterCost = renterCost; }
      lastPayment = installment;
      if (month % 12 === 0) yearly.push(snapshot(month));
    }
    const final = snapshot(months);
    const result = { valid: true, params: p, months, loanMonths, financed, purchaseCosts, initialCash,
      interestRate, firstPayment, lastPayment, firstOwnerCost, firstRenterCost,
      totalRent, totalOwnerHousing, totalRenterHousing, totalLoanPayments, totalInterest, totalIndexation,
      ownerContributions, renterContributions, ownerOutlay: initialCash + totalOwnerHousing,
      renterOutlay: totalRenterHousing, ...final, yearly,
      outcome: Math.abs(final.difference) <= 1 ? 'close' : final.difference > 0 ? 'buy' : 'rent' };
    if (!Object.values(result).filter(value => typeof value === 'number').every(Number.isFinite) ||
        !yearly.every(row => Object.values(row).every(Number.isFinite))) {
      return { valid: false, errors: { price: 'Os valores excedem o limite da simulação. Reduza as taxas ou o prazo.' } };
    }
    return result;
  }

  function sensitivity(raw) {
    const base = calculate(raw);
    if (!base.valid) return [];
    const variants = [
      { label: 'Valorização 2 p.p. menor', key: 'appreciation', delta: -2 },
      { label: 'Cenário informado', key: 'appreciation', delta: 0 },
      { label: 'Valorização 2 p.p. maior', key: 'appreciation', delta: 2 },
      { label: 'Retorno líquido 2 p.p. menor', key: 'investmentReturn', delta: -2 },
      { label: 'Retorno líquido 2 p.p. maior', key: 'investmentReturn', delta: 2 }
    ];
    return variants.map(variant => {
      const params = { ...base.params, [variant.key]: base.params[variant.key] + variant.delta };
      return { ...variant, rate: params[variant.key], result: calculate(params) };
    });
  }
  return Object.freeze({ fields, defaults, validate, monthlyEffective, payment, calculate, sensitivity });
});
