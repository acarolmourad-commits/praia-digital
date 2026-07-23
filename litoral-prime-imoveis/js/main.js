const imoveis = [
  {"id":1,"titulo":"Apto 2qtos Santos","cidade":"Santos","bairro":"Gonzaga","preco":450000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600"},
  {"id":2,"titulo":"Casa Guarujá","cidade":"Guarujá","bairro":"Enseada","preco":520000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1502005229766-5283522679e6?w=600"},
  {"id":3,"titulo":"Flat Praia Grande","cidade":"Praia Grande","bairro":"Boqueirão","preco":280000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1493809842364-78817add7e5b?w=600"},
  {"id":4,"titulo":"Apto 1quarto Bertioga","cidade":"Bertioga","bairro":"Centro","preco":210000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600"},
  {"id":5,"titulo":"Casa Itanhaém","cidade":"Itanhaém","bairro":"Jardim Suarão","preco":390000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600"},
  {"id":6,"titulo":"Apto São Vicente","cidade":"São Vicente","bairro":"Centro","preco":310000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600"},
  {"id":7,"titulo":"Flat Mongaguá","cidade":"Mongaguá","bairro":"Agenor de Campos","preco":195000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1502005229766-5283522679e6?w=600"},
  {"id":8,"titulo":"Casa Peruíbe","cidade":"Peruíbe","bairro":"Centro","preco":460000,"tipo":"venda","imagem":"https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600"}
];

function formatarMoeda(valor) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
}

function renderizarImoveis(lista) {
  const container = document.getElementById('lista-imoveis');
  if (!lista.length) { container.innerHTML = '<p>Nenhum imóvel encontrado.</p>'; return; }
  container.innerHTML = lista.map(imovel => `
    <div class="property-card">
      <img src="${imovel.imagem}" alt="${imovel.titulo}" loading="lazy" onerror="this.src='https://via.placeholder.com/600x360?text=Imóvel'">
      <div class="property-info">
        <div class="property-title">${imovel.titulo}</div>
        <div class="property-meta">${imovel.cidade} · ${imovel.bairro}</div>
        <div class="property-meta">${formatarMoeda(imovel.preco)}</div>
      </div>
    </div>
  `).join('');
}

function buscarImoveis() {
  const termo = document.getElementById('search').value.trim().toLowerCase();
  const filtrados = termo
    ? imoveis.filter(i => i.cidade.toLowerCase().includes(termo) || i.bairro.toLowerCase().includes(termo) || i.tipo.includes(termo))
    : imoveis;
  renderizarImoveis(filtrados);
}

document.getElementById('contato-form').addEventListener('submit', (e) => {
  e.preventDefault();
  alert('Mensagem enviada! Entraremos em contato em até 15 minutos.');
  e.target.reset();
});

renderizarImoveis(imoveis);
