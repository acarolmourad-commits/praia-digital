'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const core = require('../js/alugar-comprar-core.js');

const input = overrides => ({ ...core.defaults, ...overrides });
const neutral = overrides => input({
  price: 120000, downPayment: 20000, rent: 1000,
  annualInterest: 0, loanYears: 1, horizonYears: 1,
  appreciation: 0, rentGrowth: 0, investmentReturn: 0,
  purchaseCostPct: 0, saleCostPct: 0, annualMaintenance: 0,
  ownerMonthly: 0, renterMonthly: 0, expenseGrowth: 0,
  loanMonthly: 0, balanceIndex: 0, saleTax: 0,
  ...overrides
});
function close(actual, expected, label = '', abs = 0.000001, rel = 0.00000000002) {
  assert.ok(Number.isFinite(actual), `${label}: non-finite actual ${actual}`);
  assert.ok(Number.isFinite(expected), `${label}: non-finite expected ${expected}`);
  const tolerance = Math.max(abs, Math.abs(expected) * rel);
  assert.ok(Math.abs(actual - expected) <= tolerance,
    `${label}: ${actual} != ${expected} (tolerance ${tolerance})`);
}
function calculate(p) {
  const result = core.calculate(p);
  assert.equal(result.valid, true, JSON.stringify(result.errors));
  return result;
}
function sum(values) { return values.reduce((total, value) => total + value, 0); }
function annuityPresentValue(rate, months) {
  // An independent discounted-cash-flow oracle, not the production PMT formula.
  let value = 0;
  for (let month = 1; month <= months; month += 1) value += (1 + rate) ** -month;
  return value;
}
function loanOracle(p) {
  const principal = p.price - p.downPayment;
  const months = p.loanYears * 12;
  const rate = p.rateType === 'nominal' ? p.annualInterest / 1200 :
    (1 + p.annualInterest / 100) ** (1 / 12) - 1;
  const indexFactor = (1 + p.balanceIndex / 100) ** (1 / 12);
  const fixedPayment = principal / annuityPresentValue(rate, months);
  const unindexedBalance = month => p.amortization === 'SAC' ?
    principal * (months - month) / months :
    fixedPayment * annuityPresentValue(rate, months - month);
  const rows = [];
  for (let month = 1; month <= p.horizonYears * 12; month += 1) {
    if (!principal || month > months) {
      rows.push({ payment: 0, interest: 0, indexation: 0, debt: 0 });
      continue;
    }
    const accumulatedIndex = indexFactor ** month;
    const beforeIndexation = unindexedBalance(month - 1) * indexFactor ** (month - 1);
    const interest = unindexedBalance(month - 1) * accumulatedIndex * rate;
    const payment = p.amortization === 'SAC' ?
      principal / months * accumulatedIndex + interest : fixedPayment * accumulatedIndex;
    rows.push({ payment, interest, indexation: beforeIndexation * (indexFactor - 1),
      debt: unindexedBalance(month) * accumulatedIndex });
  }
  return rows;
}
function wealthDifferenceOracle(p, loans) {
  // Future-value the signed expense difference directly. This does not reproduce
  // the implementation's common-budget calculation or either investment ledger.
  const months = p.horizonYears * 12;
  let difference = p.price * (1 + p.appreciation / 100) ** p.horizonYears *
    (1 - p.saleCostPct / 100) - p.saleTax - loans.at(-1).debt -
    (p.downPayment + p.price * p.purchaseCostPct / 100) *
    (1 + p.investmentReturn / 100) ** p.horizonYears;
  for (let month = 1; month <= months; month += 1) {
    const year = Math.ceil(month / 12) - 1;
    const expenseFactor = (1 + p.expenseGrowth / 100) ** year;
    const rentalCost = p.rent * (1 + p.rentGrowth / 100) ** year + p.renterMonthly * expenseFactor;
    const maintenance = p.price * (1 + p.appreciation / 100) ** ((month - 1) / 12) *
      p.annualMaintenance / 1200;
    const fees = p.price > p.downPayment && month <= p.loanYears * 12 ? p.loanMonthly : 0;
    const ownershipCost = loans[month - 1].payment + maintenance + (p.ownerMonthly + fees) * expenseFactor;
    difference += (rentalCost - ownershipCost) *
      (1 + p.investmentReturn / 100) ** ((months - month) / 12);
  }
  return difference;
}

test('defaults produce a valid, deterministic, finite result without mutating inputs', () => {
  const p = input({});
  const copy = structuredClone(p);
  const first = calculate(p);
  assert.deepEqual(core.calculate(p), first);
  assert.deepEqual(p, copy);
  assert.equal(first.yearly.length, p.horizonYears);
  assert.ok(Object.isFrozen(core.defaults));
  for (const value of Object.values(first)) {
    if (typeof value === 'number') assert.ok(Number.isFinite(value));
  }
});

test('annual effective and nominal conversions have independent numerical references', () => {
  close(core.monthlyEffective(12), 0.009488792934583046, '12% effective', 1e-15);
  close(core.monthlyEffective(12.682503013196977), 0.01, '1% monthly', 1e-15);
  assert.equal(core.monthlyEffective(0), 0);
  for (const annual of [-50, -12, -0.0001, 0, 0.0001, 4, 30, 100]) {
    close((1 + core.monthlyEffective(annual)) ** 12, 1 + annual / 100, `annual ${annual}`, 1e-13);
  }
  const nominal = calculate(neutral({ annualInterest: 12, rateType: 'nominal' }));
  const effective = calculate(neutral({ annualInterest: 12, rateType: 'effective' }));
  close(nominal.interestRate, 0.01, 'nominal monthly rate', 1e-15);
  close(effective.interestRate, 0.009488792934583046, 'effective monthly rate', 1e-15);
  assert.ok(nominal.firstPayment > effective.firstPayment);
});

test('equivalent annual rate conventions produce equivalent schedules and wealth', () => {
  const nominal = calculate(input({ annualInterest: 12, rateType: 'nominal' }));
  const effective = calculate(input({ annualInterest: ((1.01 ** 12) - 1) * 100, rateType: 'effective' }));
  for (const key of ['firstPayment', 'lastPayment', 'debt', 'totalInterest', 'difference']) {
    close(nominal[key], effective[key], key);
  }
});

test('payment has exact zero and near-zero limits', () => {
  assert.equal(core.payment(0, 0.01, 12), 0);
  assert.equal(core.payment(120000, 0, 12), 10000);
  for (const rate of [1e-20, 1e-16, 1e-12, 1e-9]) {
    close(core.payment(120000, rate, 600), 120000 / annuityPresentValue(rate, 600), `rate ${rate}`);
  }
  close(core.payment(100000, 0.01, 12), 8884.87886783416, 'reference Price payment');
  close(core.payment(100000, 0.01, 1), 101000, 'single remaining payment');
});

test('Price reference amortizes the principal and reports independently known interest', () => {
  const r = calculate(neutral({ annualInterest: 12 }));
  close(r.firstPayment, 8884.87886783416);
  close(r.lastPayment, 8884.87886783416);
  close(r.totalInterest, 6618.546414009936);
  close(r.totalLoanPayments, 106618.546414009936);
  assert.equal(r.debt, 0);
});

test('SAC reference has declining payments and a closed-form interest total', () => {
  const r = calculate(neutral({ downPayment: 0, annualInterest: 12, amortization: 'SAC' }));
  close(r.firstPayment, 11200);
  close(r.lastPayment, 10100);
  close(r.totalInterest, 7800);
  close(r.totalLoanPayments, 127800);
  assert.equal(r.debt, 0);
});

for (const amortization of ['PRICE', 'SAC']) {
  test(`${amortization}: zero-interest funding does not turn amortization into an expense`, () => {
    const r = calculate(neutral({ amortization, purchaseCostPct: 4 }));
    close(r.initialCash, 24800);
    close(r.renterInvestments, 112800);
    close(r.ownerInvestments, 0);
    close(r.ownerWealth, 120000);
    close(r.difference, 7200);
    close(r.difference, r.totalRent - r.purchaseCosts);
  });

  test(`${amortization}: repayment stops at maturity and both loan fees and interest stop`, () => {
    const r = calculate(neutral({ amortization, price: 12000, downPayment: 0,
      rent: 1100, loanMonthly: 100, horizonYears: 2, expenseGrowth: 10 }));
    close(r.totalLoanPayments, 12000);
    close(r.totalOwnerHousing, 13200);
    close(r.ownerInvestments, 13200);
    close(r.ownerWealth, 25200);
    close(r.renterInvestments, 0);
    close(r.lastPayment, 0);
    assert.equal(r.debt, 0);
    assert.equal(r.yearly[0].debt, 0);
  });

  test(`${amortization}: horizon shorter than loan retains the correct residual debt`, () => {
    const r = calculate(neutral({ amortization, loanYears: 2 }));
    close(r.debt, 50000);
    close(r.totalLoanPayments, 50000);
    close(r.netEquity, 70000);
    close(r.difference, 12000);
  });

  test(`${amortization}: zero and nearly zero interest agree over 50 years`, () => {
    const p = neutral({ amortization, loanYears: 50, horizonYears: 50 });
    const zero = calculate(p);
    const tiny = calculate({ ...p, annualInterest: 1e-12 });
    for (const key of ['firstPayment', 'totalInterest', 'totalLoanPayments', 'difference']) {
      close(tiny[key], zero[key], key, 0.00001);
    }
    assert.equal(tiny.debt, 0);
  });
}

test('cash purchase never incurs loan payments, correction or financing fees', () => {
  const p = neutral({ downPayment: 120000, annualInterest: 100, loanMonthly: 1000000, balanceIndex: 30 });
  const r = calculate(p);
  for (const key of ['financed', 'debt', 'firstPayment', 'lastPayment', 'totalInterest', 'totalIndexation', 'totalLoanPayments']) {
    assert.equal(r[key], 0, key);
  }
  close(r.ownerInvestments, 12000);
  close(r.renterInvestments, 120000);
  close(r.ownerWealth, 132000);
  close(r.difference, 12000);
});

test('end-of-month contributions receive no return in their contribution month', () => {
  const r = calculate(neutral({ price: 100000, downPayment: 100000, rent: 1000,
    investmentReturn: (1.01 ** 12 - 1) * 100 }));
  const futureAnnuity = 1000 * sum(Array.from({ length: 12 }, (_, k) => 1.01 ** k));
  close(r.ownerInvestments, futureAnnuity);
  close(r.renterInvestments, 100000 * 1.01 ** 12);
  close(r.difference, 0);
  assert.equal(r.outcome, 'close');
});

test('purchase costs join the renter investment at inception and compound for the full horizon', () => {
  const p = neutral({ price: 100000, downPayment: 100000, rent: 0,
    purchaseCostPct: 4, investmentReturn: 10, horizonYears: 2 });
  const r = calculate(p);
  close(r.initialCash, 104000);
  close(r.renterInvestments, 104000 * 1.1 ** 2);
  close(r.ownerWealth, 100000);
});

test('rent and other expenses adjust on the anniversary, not in month 12', () => {
  const r = calculate(neutral({ downPayment: 120000, horizonYears: 2,
    rentGrowth: 10, ownerMonthly: 100, renterMonthly: 50, expenseGrowth: 20 }));
  close(r.totalRent, 25200);
  close(r.totalOwnerHousing, 2640);
  close(r.totalRenterHousing, 26520);
  close(r.firstOwnerCost, 100);
  close(r.firstRenterCost, 1050);
  close(r.yearly[0].ownerInvestments, 11400);
  close(r.ownerInvestments, 23880);
});

test('negative annual rent and expense growth use the same anniversary convention', () => {
  const r = calculate(neutral({ downPayment: 120000, horizonYears: 3,
    rentGrowth: -50, ownerMonthly: 100, renterMonthly: 50, expenseGrowth: -50 }));
  close(r.totalRent, 21000);
  close(r.totalOwnerHousing, 2100);
  close(r.totalRenterHousing, 22050);
});

test('maintenance uses the beginning-of-month property value and annual rate divided by 12', () => {
  const r = calculate(neutral({ downPayment: 120000, rent: 0, annualMaintenance: 12, appreciation: 12 }));
  const maintenance = 1200 * sum(Array.from({ length: 12 }, (_, month) => 1.12 ** (month / 12)));
  close(r.firstOwnerCost, 1200);
  close(r.totalOwnerHousing, maintenance);
  close(r.property, 134400);
});

test('sale expenses are charged on the final property price and fixed tax exactly once', () => {
  const r = calculate(neutral({ downPayment: 120000, rent: 0, appreciation: 10,
    horizonYears: 2, saleCostPct: 6, saleTax: 8000 }));
  close(r.property, 145200);
  close(r.sellingCosts, 8712);
  close(r.saleTax, 8000);
  close(r.netEquity, 128488);
  close(r.ownerWealth, 128488);
  close(r.difference, 8488);
  close(r.yearly[0].saleTax, 8000);
});

test('negative equity and final wealth are preserved rather than capped at zero', () => {
  const r = calculate(neutral({ downPayment: 0, loanYears: 50, appreciation: -50,
    saleCostPct: 30, saleTax: 1000000, rent: 0 }));
  close(r.property, 60000);
  close(r.debt, 117600);
  close(r.netEquity, -1075600);
  assert.ok(r.ownerWealth < 0);
  assert.ok(r.difference < 0);
  assert.equal(r.outcome, 'rent');
});

test('the declared nominal sale-tax provision is not inferred from gains or annualized', () => {
  const p = neutral({ downPayment: 120000, appreciation: -20, horizonYears: 3 });
  const without = calculate(p);
  const withTax = calculate({ ...p, saleTax: 12345 });
  close(without.difference - withTax.difference, 12345);
  close(without.ownerInvestments, withTax.ownerInvestments);
  close(without.renterInvestments, withTax.renterInvestments);
});

test('the common budget can switch sides without negative contributions or fictitious borrowing', () => {
  const r = calculate(neutral({ price: 12000, downPayment: 0, rent: 500, horizonYears: 2 }));
  close(r.renterContributions, 6000);
  close(r.ownerContributions, 6000);
  close(r.renterInvestments, 6000);
  close(r.ownerInvestments, 6000);
  close(r.difference, 12000);
});

test('expenses equal on both sides do not change the comparison or investment balances', () => {
  const p = input({ expenseGrowth: 7 });
  const base = calculate(p);
  const shared = calculate({ ...p, ownerMonthly: p.ownerMonthly + 700, renterMonthly: p.renterMonthly + 700 });
  for (const key of ['difference', 'ownerInvestments', 'renterInvestments', 'ownerContributions', 'renterContributions']) {
    close(shared[key], base[key], key);
  }
});

test('when returns and appreciation are zero, financing principal is conserved', () => {
  for (const amortization of ['PRICE', 'SAC']) {
    const p = neutral({ amortization, annualInterest: 11, balanceIndex: 4, loanYears: 3,
      horizonYears: 2, purchaseCostPct: 3, saleCostPct: 5, annualMaintenance: 1,
      ownerMonthly: 80, renterMonthly: 40, loanMonthly: 60, saleTax: 2000 });
    const r = calculate(p);
    close(r.financed + r.totalIndexation + r.totalInterest - r.totalLoanPayments, r.debt, 'debt accounting');
    const otherOwner = r.totalOwnerHousing - r.totalLoanPayments;
    close(r.difference, r.totalRenterHousing - r.totalInterest - r.totalIndexation -
      otherOwner - r.purchaseCosts - r.sellingCosts - p.saleTax, 'wealth conservation');
    close(r.ownerContributions - r.renterContributions,
      r.totalRenterHousing - r.totalOwnerHousing, 'saving difference');
  }
});

for (const amortization of ['PRICE', 'SAC']) {
  for (const rateType of ['nominal', 'effective']) {
    for (const balanceIndex of [0, 4, 30]) {
      for (const horizonYears of [1, 4, 9]) {
        test(`independent cash-flow oracle: ${amortization}, ${rateType}, index ${balanceIndex}%, horizon ${horizonYears}y`, () => {
          for (const [appreciation, investmentReturn] of [[-12, -10], [0, 0], [7, 8]]) {
            const p = input({ price: 375000, downPayment: 75000, rent: 1700,
              amortization, rateType, annualInterest: 13, balanceIndex, loanYears: 4, horizonYears,
              appreciation, investmentReturn, purchaseCostPct: 4, saleCostPct: 5, saleTax: 3500,
              annualMaintenance: 1.2, ownerMonthly: 450, renterMonthly: 250, loanMonthly: 120,
              rentGrowth: 3.5, expenseGrowth: 2.5 });
            const r = calculate(p);
            const loans = loanOracle(p);
            close(r.firstPayment, loans[0].payment, 'first payment');
            close(r.lastPayment, loans.at(-1).payment, 'last payment');
            close(r.debt, loans.at(-1).debt, 'final debt');
            close(r.totalLoanPayments, sum(loans.map(row => row.payment)), 'loan payments');
            close(r.totalInterest, sum(loans.map(row => row.interest)), 'interest');
            close(r.totalIndexation, sum(loans.map(row => row.indexation)), 'indexation');
            close(r.difference, wealthDifferenceOracle(p, loans), 'wealth difference');
            close(r.ownerContributions - r.renterContributions,
              r.totalRenterHousing - r.totalOwnerHousing, 'contribution conservation');
            assert.ok(r.ownerContributions >= 0 && r.renterContributions >= 0);
            for (const row of r.yearly) {
              close(row.debt, loans[row.month - 1].debt, `year ${row.year} debt`);
              close(row.ownerWealth, row.netEquity + row.ownerInvestments, 'owner wealth');
              close(row.difference, row.ownerWealth - row.renterWealth, 'difference');
              assert.ok(row.debt >= 0 && row.ownerInvestments >= 0 && row.renterInvestments >= 0);
            }
          }
        });
      }
    }
  }
}

test('annual snapshots are independent endpoint simulations, not cumulative liquidation charges', () => {
  const p = input({ horizonYears: 5, loanYears: 3, balanceIndex: 2, saleTax: 9000 });
  const longer = calculate(p);
  for (const row of longer.yearly) {
    const shorter = calculate({ ...p, horizonYears: row.year });
    for (const key of Object.keys(row)) close(row[key], shorter[key], `${key} at year ${row.year}`);
  }
});

test('owner expenses monotonically reduce the relative advantage, even across budget switches', () => {
  for (const investmentReturn of [-30, 0, 12]) {
    const p = input({ loanYears: 3, horizonYears: 8, investmentReturn });
    const base = calculate(p);
    for (const [key, extra] of [['purchaseCostPct', 1], ['saleCostPct', 1], ['saleTax', 10000],
      ['ownerMonthly', 300], ['loanMonthly', 100], ['annualMaintenance', 0.5]]) {
      const more = calculate({ ...p, [key]: p[key] + extra });
      assert.ok(more.difference < base.difference, `${key} at return ${investmentReturn}`);
    }
    for (const [key, extra] of [['rent', 300], ['renterMonthly', 300]]) {
      const more = calculate({ ...p, [key]: p[key] + extra });
      assert.ok(more.difference > base.difference, `${key} at return ${investmentReturn}`);
    }
  }
});

test('zero-rate result is independent of down payment and repayment speed', () => {
  for (const downPayment of [0, 20000, 120000]) {
    for (const loanYears of [1, 3, 50]) {
      const r = calculate(neutral({ downPayment, loanYears, horizonYears: 3, purchaseCostPct: 4 }));
      close(r.difference, 36000 - 4800);
    }
  }
});

test('scaling monetary inputs preserves wealth and cash-flow proportionality', () => {
  const p = input({ saleTax: 5000, ownerMonthly: 100, renterMonthly: 80, loanMonthly: 60 });
  const scaled = { ...p };
  for (const key of ['price', 'downPayment', 'rent', 'saleTax', 'ownerMonthly', 'renterMonthly', 'loanMonthly']) scaled[key] *= 3;
  const a = calculate(p);
  const b = calculate(scaled);
  for (const key of ['firstPayment', 'totalInterest', 'debt', 'property', 'purchaseCosts',
    'sellingCosts', 'ownerInvestments', 'renterInvestments', 'ownerWealth', 'difference']) {
    close(b[key], a[key] * 3, key);
  }
});

test('sensitivity varies exactly two percentage points, recalculates all flows, and leaves input unchanged', () => {
  const p = input({ annualMaintenance: 3 });
  const copy = structuredClone(p);
  const rows = core.sensitivity(p);
  assert.equal(rows.length, 5);
  assert.deepEqual(rows.map(row => [row.key, row.delta]), [
    ['appreciation', -2], ['appreciation', 0], ['appreciation', 2],
    ['investmentReturn', -2], ['investmentReturn', 2]
  ]);
  for (const row of rows) {
    assert.equal(row.rate, p[row.key] + row.delta);
    assert.deepEqual(row.result, core.calculate({ ...p, [row.key]: p[row.key] + row.delta }));
  }
  assert.ok(rows[0].result.totalOwnerHousing < rows[1].result.totalOwnerHousing);
  assert.ok(rows[2].result.totalOwnerHousing > rows[1].result.totalOwnerHousing);
  assert.deepEqual(p, copy);
});

test('sensitivity reports out-of-domain endpoints honestly, without clamping or NaN', () => {
  for (const [key, boundary, direction] of [
    ['appreciation', -50, -2], ['appreciation', 100, 2],
    ['investmentReturn', -50, -2], ['investmentReturn', 100, 2]
  ]) {
    const rows = core.sensitivity(input({ [key]: boundary }));
    const outside = rows.find(row => row.key === key && row.delta === direction);
    assert.equal(outside.rate, boundary + direction);
    assert.equal(outside.result.valid, false);
    assert.ok(outside.result.errors[key]);
    assert.equal(rows.find(row => row.delta === 0).result.valid, true);
  }
  assert.deepEqual(core.sensitivity(input({ rent: '' })), []);
});

test('validation accepts numeric strings without silently defaulting valid zero values', () => {
  const p = neutral({ downPayment: 0, rent: 0 });
  for (const key of Object.keys(core.fields)) p[key] = String(p[key]);
  const checked = core.validate(p);
  assert.equal(checked.valid, true);
  assert.equal(checked.values.annualInterest, 0);
  assert.equal(checked.values.rent, 0);
  assert.equal(checked.values.downPayment, 0);
  assert.deepEqual(core.calculate(p), core.calculate(neutral({ downPayment: 0, rent: 0 })));
});

for (const [key, field] of Object.entries(core.fields)) {
  test(`validation rejects missing, blank, nonnumeric, nonfinite and out-of-domain ${key}`, () => {
    for (const value of [undefined, null, '', '   ', 'abc', NaN, Infinity, -Infinity, true, [], {},
      field.min - 1, field.max + 1]) {
      const p = input({ [key]: value });
      const validation = core.validate(p);
      assert.equal(validation.valid, false, `${key}: ${String(value)}`);
      assert.ok(validation.errors[key], `${key}: ${String(value)}`);
      const result = core.calculate(p);
      assert.equal(result.valid, false);
      assert.ok(result.errors[key]);
    }
  });

  test(`validation accepts inclusive ${key} limits in valid combinations`, () => {
    for (const value of [field.min, field.max]) {
      const p = input({ [key]: value });
      if (key === 'price') p.downPayment = Math.min(p.downPayment, value);
      if (key === 'downPayment') p.price = Math.max(p.price, value);
      assert.equal(core.validate(p).valid, true, `${key}: ${value}`);
      calculate(p);
    }
  });
}

test('negative rates are allowed only in explicitly supported domains', () => {
  for (const key of ['appreciation', 'rentGrowth', 'investmentReturn', 'expenseGrowth']) {
    calculate(input({ [key]: -1 }));
  }
  for (const key of ['annualInterest', 'balanceIndex', 'purchaseCostPct', 'saleCostPct', 'annualMaintenance']) {
    assert.equal(core.validate(input({ [key]: -0.01 })).valid, false, key);
  }
});

test('term and horizon must be whole years, and entry cannot exceed the property price', () => {
  for (const key of ['loanYears', 'horizonYears']) {
    for (const value of [0, 0.5, 1.5, 50.1, 51]) assert.ok(core.validate(input({ [key]: value })).errors[key]);
  }
  assert.ok(core.validate(input({ downPayment: core.defaults.price + 1 })).errors.downPayment);
  for (const [key, values] of [['rateType', ['', 'NOMINAL', 'other']], ['amortization', ['', 'price', 'OTHER']]]) {
    for (const value of values) assert.ok(core.validate(input({ [key]: value })).errors[key]);
  }
  for (const p of [undefined, null, {}]) {
    assert.equal(core.validate(p).valid, false);
    assert.equal(core.calculate(p).valid, false);
  }
});

test('minimum and maximum supported combinations stay finite over the longest horizon', () => {
  const high = input(Object.fromEntries(Object.entries(core.fields).map(([key, field]) => [key, field.max])));
  high.downPayment = 0;
  for (const amortization of ['PRICE', 'SAC']) {
    for (const rateType of ['nominal', 'effective']) {
      const r = calculate({ ...high, amortization, rateType });
      assert.equal(r.debt, 0);
      assert.equal(r.yearly.length, 50);
      assert.ok(r.ownerContributions >= 0 && r.renterContributions >= 0);
      for (const row of r.yearly) for (const value of Object.values(row)) assert.ok(Number.isFinite(value));
      calculate(input({ price: 1, downPayment: 0, loanYears: 50, horizonYears: 50,
        annualInterest: 0, appreciation: -50, investmentReturn: -50, expenseGrowth: -50,
        rentGrowth: -50, amortization, rateType }));
    }
  }
});

test('near-zero difference uses the declared R$1 comparison tolerance', () => {
  const tied = neutral({ downPayment: 120000, rent: 0 });
  assert.equal(calculate(tied).outcome, 'close');
  assert.equal(calculate({ ...tied, saleTax: 1 }).outcome, 'close');
  assert.equal(calculate({ ...tied, saleTax: 1.01 }).outcome, 'rent');
  assert.equal(calculate({ ...tied, rent: 1 }).outcome, 'buy');
});
