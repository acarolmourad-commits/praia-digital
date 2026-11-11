const test = require('node:test');
const assert = require('node:assert/strict');
const { calculate, schedule, monthlyRate } = require('../js/compra-viabilidade-core.js');
const base = {
  goal: 'moradia', city: 'Santos', price: 500000, area: 65, purchase: 'financiado', entry: 100000,
  months: 360, annualRate: 11.5, system: 'price', financeFees: 0,
  acquisitionRate: 5, upfront: 0, condo: 600, tax: 150, maintenance: 150, otherCosts: 0,
  rent: 2250, tenantCosts: 750, years: 10, appreciation: 3, investmentReturn: 8,
  annualAdjustment: 4, saleRate: 6, dailyRate: 550, nights: 150,
  annualRent: 2250, vacancy: 5, variableRate: 20
};
const calc = overrides => calculate({ ...base, ...overrides });
const close = (actual, expected, tolerance = 0.00001) => assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} != ${expected}`);
test('Price uses effective monthly conversion and independently checked installment', () => {
  const r = calc({});
  assert.equal(r.valid, true);
  close(monthlyRate(11.5), 0.009112468436904608);
  close(r.firstPayment, 3789.64887035982);
  close(r.lastPayment, r.firstPayment);
  close(r.debtSchedule.at(-1).balance, 0);
  close(r.totalInterest, 964273.5933295353, 0.01);
});
test('Price and SAC at zero interest amortize correctly', () => {
  for (const system of ['price', 'sac']) {
    const rows = schedule(480000, 240, 0, system);
    close(rows[0].payment, 2000);
    close(rows[11].balance, 456000);
    close(rows.at(-1).balance, 0);
  }
});
test('SAC payments decline and amortization sums to original debt', () => {
  const rows = schedule(400000, 360, 11.5, 'sac');
  assert.ok(rows[0].payment > rows[1].payment);
  close(rows.reduce((sum, row) => sum + row.amortization, 0), 400000);
});
test('Housing zero-rate independent reference case', () => {
  const r = calc({ price: 600000, entry: 120000, months: 240, annualRate: 0, condo: 500, tax: 0, maintenance: 0,
    rent: 2500, tenantCosts: 0, years: 1, appreciation: 0, investmentReturn: 0, annualAdjustment: 0 });
  close(r.housing.buyerAfterSale, 108000);
  close(r.housing.renterInvestments, 150000);
  close(r.housing.difference, -42000);
});
test('Cash purchase: buyer invests monthly savings with equal budget', () => {
  const r = calc({ purchase: 'avista', price: 600000, condo: 500, tax: 0, maintenance: 0, rent: 2500,
    tenantCosts: 0, years: 1, appreciation: 0, investmentReturn: 0, annualAdjustment: 0, financeFees: 500 });
  close(r.principal, 0);
  close(r.ownerFirstMonth, 500);
  close(r.housing.buyerInvestments, 24000);
  close(r.housing.buyerAfterSale, 588000);
  close(r.housing.renterInvestments, 630000);
  close(r.housing.difference, -42000);
});
test('Loan stops at maturity, including fees; buyer invests later surplus', () => {
  const r = calc({ price: 12000, entry: 0, months: 12, annualRate: 0, financeFees: 100, acquisitionRate: 0,
    condo: 0, tax: 0, maintenance: 0, rent: 1100, tenantCosts: 0, years: 2,
    appreciation: 0, investmentReturn: 0, annualAdjustment: 0, saleRate: 0 });
  close(r.housing.residualDebt, 0);
  close(r.housing.buyerInvestments, 13200);
  close(r.housing.buyerAfterSale, 25200);
});
test('A full entry is debt-free and does not charge financing fees', () => {
  const r = calc({ entry: 500000, financeFees: 100 });
  close(r.principal, 0);
  close(r.ownerFirstMonth, 900);
});
test('Seasonal yields have no artificial cap or floor', () => {
  close(calc({ goal: 'temporada' }).rental.grossYield, 16.5);
  close(calc({ goal: 'temporada', price: 1e7 }).rental.grossYield, 0.825);
});
test('Zero occupied nights gives zero revenue and negative net yield, never a floor', () => {
  const r = calc({ goal: 'temporada', nights: 0 });
  close(r.rental.grossYield, 0);
  assert.ok(r.rental.operatingYield < 0);
  assert.ok(r.rental.cashflow < 0);
});
test('Operating return differs from cashflow after debt', () => {
  const r = calc({ goal: 'anual', price: 300000, entry: 60000, annualRate: 0, months: 240,
    annualRent: 1800, vacancy: 0, variableRate: 0, condo: 1100, tax: 0, maintenance: 0 });
  close(r.rental.grossYield, 7.2);
  close(r.rental.operatingYield, 2.8);
  close(r.rental.operatingNet / 12, 700);
  close(r.rental.cashflow / 12, -300);
});
test('Vacancy, fees and acquisition bases are explicit', () => {
  const r = calc({ goal: 'anual', annualRent: 2000, vacancy: 10, variableRate: 20 });
  close(r.rental.gross, 21600);
  close(r.rental.variableCosts, 4320);
  close(r.rental.operatingNet, 6480);
  close(r.rental.yieldOnTotalCost, 6480 / 525000 * 100);
});
test('Short loans charge only actual installments in first-year cashflow', () => {
  const r = calc({ goal: 'temporada', price: 10000, entry: 0, months: 6, annualRate: 0, financeFees: 100 });
  close(r.rental.firstYearDebt, 10600);
});
test('100% fees or zero daily rate yield unavailable break-even, not Infinity', () => {
  assert.equal(calc({ goal: 'temporada', variableRate: 100 }).rental.breakEvenNights, null);
  assert.equal(calc({ goal: 'temporada', dailyRate: 0 }).rental.breakEvenNights, null);
});
test('100% vacancy is valid zero annual revenue', () => close(calc({ goal: 'anual', vacancy: 100 }).rental.gross, 0));
test('Unknown benchmark is not silently fabricated', () => {
  assert.equal(calc({ city: 'Bertioga' }).reference, null);
  assert.equal(calc({ city: 'Santos' }).reference, 8678);
});
test('Negative growth and return scenarios remain finite', () => {
  const r = calc({ appreciation: -30, investmentReturn: -30, annualAdjustment: -20, years: 40 });
  assert.ok(Number.isFinite(r.housing.difference));
});
test('Inputs are not mutated', () => { const v = { ...base }; calculate(v); assert.deepEqual(v, base); });
for (const [key, value] of [['price', NaN], ['price', 0], ['price', -1], ['price', Infinity], ['entry', -1],
  ['entry', 600000], ['area', 0], ['months', 0], ['months', 1.5], ['annualRate', -1], ['financeFees', -1],
  ['condo', -1], ['years', 0], ['years', 1.5], ['investmentReturn', NaN], ['city', ''], ['system', 'consorcio']]) {
  test(`Reject invalid ${key}: ${value}`, () => { const r = calc({ [key]: value }); assert.equal(r.valid, false); assert.ok(r.errors[key]); });
}
test('Reject impossible occupied nights and invalid vacancy', () => {
  for (const nights of [-1, 366, 1.5, NaN]) assert.equal(calc({ goal: 'temporada', nights }).valid, false);
  assert.equal(calc({ goal: 'anual', vacancy: 101 }).valid, false);
});
test('Hidden irrelevant fields do not invalidate other modes', () => {
  assert.equal(calc({ purchase: 'avista', entry: NaN, annualRate: NaN, months: NaN, financeFees: NaN }).valid, true);
  assert.equal(calc({ goal: 'temporada', rent: NaN, years: NaN, annualRent: NaN }).valid, true);
});
