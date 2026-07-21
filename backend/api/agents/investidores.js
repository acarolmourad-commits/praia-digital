const cities = require('../data/cities.json');

function fmt(v){ return 'R$ ' + Number(v||0).toLocaleString('pt-BR', {minimumFractionDigits:0, maximumFractionDigits:0}); }

module.exports = async (input, context) => {
  const priceMatch = input.match(/R\$\s*([\d.\s]+)/);
  const base = priceMatch ? Number(priceMatch[1].replace(/\s/g,'').replace(/\./g,'')) : 850000;
  const cityKey = (input || '').toLowerCase();
  let cityData = null;
  for (const c of cities) {
    if (cityKey.includes(c.name.toLowerCase())) { cityData = c; break; }
  }
  if (!cityData) {
    const yieldEst = 6.0;
    const rentabilidade = ((base * yieldEst / 100) / base) * 100;
    return `Preço base estimado: ${fmt(base)}. Rentabilidade estimada: ${rentabilidade.toFixed(1)}% a.a.`;
  }
  const faixaMin = Math.round(base * 0.92);
  const faixaMax = Math.round(base * 1.08);
  const yieldEst = cityData.yield || 6.0;
  const rentabilidade = ((base * yieldEst / 100) / base) * 100;
  return `Cidade: ${cityData.name}. Preço base: ${fmt(cityData.price)}. Faixa sugerida: ${fmt(faixaMin)} a ${fmt(faixaMax)}. Yield médio: ${yieldEst}% a.a. Rentabilidade estimada: ${rentabilidade.toFixed(1)}% a.a.`;
};
