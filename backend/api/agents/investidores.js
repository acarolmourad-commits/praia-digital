const cities = require('../data/cities.json');
module.exports = async (input, context) => {
  const match = input.match(/R\$\s*(\d[\d\s]*)/);
  const price = match ? Number(match[1].replace(/\s/g,'')) : 850000;
  const yieldEst = 6.0;
  const rentabilidade = ((price * yieldEst / 100) / price) * 100;
  return `[IA Investidores] Preço base estimado: R$ ${price.toLocaleString('pt-BR')}. Rentabilidade estimada: ${rentabilidade.toFixed(1)}% a.a.`;
};
