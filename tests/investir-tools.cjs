const assert = require("node:assert/strict");
const c = require("../js/investir-tools-core");
const base = {
  valor: 200000,
  entrada: 40000,
  taxa: 11.19,
  tipo: "nominal",
  meses: 240,
  seguros: 0,
  comprometimento: 30,
};
let r = c.finance(base);
assert.ok(Math.abs(r.sac.first - 2158.6666667) < 0.001);
assert.ok(Math.abs(r.price.first - 1672.2400574) < 0.001);
assert.ok(Math.abs(r.sac.income - 7195.55556) < 0.001);
r = c.finance({ ...base, tipo: "effective" });
assert.ok(Math.abs(r.price.first - 1613.997881) < 0.001);
for (const tipo of ["nominal", "effective"]) {
  r = c.finance({ ...base, tipo, taxa: 0 });
  assert.equal(r.sac.interest, 0);
  assert.equal(r.price.interest, 0);
  assert.equal(r.sac.first, r.price.first);
}
r = c.finance({ ...base, entrada: 200000, seguros: 100 });
assert.equal(r.sac.total, 0);
assert.equal(r.price.income, 0);
r = c.finance({ ...base, seguros: 100 });
assert.ok(Math.abs(r.sac.income - 7528.888889) < 0.001);
assert.equal(r.sac.fees, 24000);
for (const field of [
  "valor",
  "entrada",
  "taxa",
  "meses",
  "seguros",
  "comprometimento",
])
  for (const value of [-1, NaN, Infinity])
    assert.equal(c.finance({ ...base, [field]: value }).valid, false);
assert.equal(c.finance({ ...base, meses: 1.5 }).valid, false);
assert.equal(c.finance({ ...base, entrada: 200001 }).valid, false);
r = c.valuation({ area: 75, referencia: 8678, ajuste: 0, variacao: 10 });
assert.equal(r.central, 650850);
assert.equal(r.low, 585765);
assert.ok(Math.abs(r.high - 715935) < 0.00001);
for (const value of [NaN, Infinity, 0, -1])
  assert.equal(
    c.valuation({ area: value, referencia: 8678, ajuste: 0, variacao: 10 })
      .valid,
    false,
  );
console.log(
  "Core: nominal/effective, SAC/Price, fees, cash, zero interest and invalid input checks passed.",
);
