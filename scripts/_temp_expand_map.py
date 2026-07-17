from pathlib import Path

path = Path('C:/Users/Carolina/praia-digital/mapa-inteligente.html')
text = path.read_text(encoding='utf-8')

# Novas camadas para expandir o mapa
novas_camadas = """
  // Transporte / Terminais
  const transporte = [
    { nome: 'Terminal Marítimo Santos', coords: [-23.95, -46.30], tipo: 'Terminal Marítimo' },
    { nome: 'Ferry Boat Guarujá', coords: [-24.00, -46.26], tipo: 'Terminal de Ferry' },
    { nome: 'Terminal Rodoviário Praia Grande', coords: [-24.00, -46.40], tipo: 'Rodoviária' },
    { nome: 'Porto de São Vicente', coords: [-23.95, -46.38], tipo: 'Porto' },
  ];

  // Gastronomia / Restaurantes
  const gastronomia = [
    { nome: 'Restaurante Peixe na Rede', coords: [-23.96, -46.33], cidade: 'Santos', nota: 4.7 },
    { nome: 'Bar do Zé', coords: [-24.00, -46.26], cidade: 'Guarujá', nota: 4.5 },
    { nome: 'Pizzaria da Orla', coords: [-24.00, -46.40], cidade: 'Praia Grande', nota: 4.6 },
    { nome: 'Restaurante Sabor do Mar', coords: [-24.18, -46.78], cidade: 'Itanhaém', nota: 4.8 },
  ];

  // Parques e áreas verdes
  const parques = [
    { nome: 'Jardim Botânico Santos', coords: [-23.97, -46.32], tipo: 'Jardim Botânico' },
    { nome: 'Parque do Guarujá', coords: [-24.00, -46.27], tipo: 'Parque Municipal' },
    { nome: 'Área de preservação Peruíbe', coords: [-24.30, -47.00], tipo: 'Reserva' },
    { nome: 'Parque Linear Itanhaém', coords: [-24.18, -46.79], tipo: 'Parque Linear' },
  ];

  // Corretoras / Imobiliárias parceiras
  const parceiros = [
    { nome: 'Santos Premium Launch', coords: [-23.96, -46.33], cidade: 'Santos', tipo: 'Imobiliária' },
    { nome: 'Guarujá Digital Tech', coords: [-24.00, -46.26], cidade: 'Guarujá', tipo: 'Imobiliária' },
    { nome: 'PG Blue Launch', coords: [-24.00, -46.40], cidade: 'Praia Grande', tipo: 'Construtora' },
    { nome: 'Itanhaém Tech View', coords: [-24.18, -46.78], cidade: 'Itanhaém', tipo: 'Imobiliária' },
    { nome: 'SV Premium Launch', coords: [-23.95, -46.38], cidade: 'São Vicente', tipo: 'Imobiliária' },
  ];

  // Mais praias
  const praias_extra = [
    { nome: 'Praia do Gonzaguinha', coords: [-23.96, -46.31], desc: 'Famosa por shows' },
    { nome: 'Praia da Enseada', coords: [-24.00, -46.24], desc: 'Águas calmas' },
    { nome: 'Praia do Sonho', coords: [-24.01, -46.39], desc: 'Ótima para famílias' },
    { nome: 'Praia de Itanhaém', coords: [-24.17, -46.77], desc: 'Surf e tranquilidade' },
    { nome: 'Praia de São Vicente', coords: [-23.94, -46.37], desc: 'Orla histórica' },
  ];

  // Mais surf spots
  const surf_extra = [
    { nome: 'Monteiro Lobato', coords: [-23.95, -46.35], tipo: 'Reef break' },
    { nome: 'Praia de São Vicente', coords: [-23.94, -46.36], tipo: 'Beach break' },
    { nome: 'Praia de Peruíbe', coords: [-24.29, -46.99], tipo: 'Point preservado' },
    { nome: 'Bertioga Norte', coords: [-23.86, -45.86], tipo: 'Onda consistente' },
  ];

  const praias_completas = praias.concat(praias_extra);
  const surf_completo = surf.concat(surf_extra);
"""

# Inserir novas constantes antes de "// Função para criar camadas"
text = text.replace('  // Função para criar camadas', novas_camadas + '  // Função para criar camadas')

# Atualizar array original de praias para incluir as extras
text = text.replace('const praias = [', 'const praias_base = [')
text = text.replace('const surf = [', 'const surf_base = [')

# Adicionar controles das novas camadas no final do script
novos_controles = """
  const layerTransporte = L.layerGroup(transporte.map(t => {
    const marker = L.marker(t.coords);
    marker.bindPopup(`<b>${t.nome}</b><br>${t.tipo}`);
    return marker;
  }));

  const layerGastronomia = L.layerGroup(gastronomia.map(g => {
    const marker = L.marker(g.coords);
    marker.bindPopup(`<b>${g.nome}</b><br>${g.cidade} — Nota ${g.nota}`);
    return marker;
  }));

  const layerParques = L.layerGroup(parques.map(p => {
    const marker = L.circleMarker(p.coords, { radius: 10, fillColor: '#22c55e', color: '#fff', weight: 2, opacity: 1, fillOpacity: 0.8 });
    marker.bindPopup(`<b>${p.nome}</b><br>${p.tipo}`);
    return marker;
  }));

  const layerParceiros = L.layerGroup(parceiros.map(p => {
    const marker = L.marker(p.coords);
    marker.bindPopup(`<b>${p.nome}</b><br>${p.cidade} — ${p.tipo}`);
    return marker;
  }));

  const layerPraiasCompleta = L.layerGroup(praias_completas.map(p => {
    const marker = createCircleMarker(p.coords, '#f59e0b', 12);
    marker.bindPopup(`<b>${p.nome}</b><br>${p.desc || ''}`);
    return marker;
  }));

  const layerSurfCompleto = L.layerGroup(surf_completo.map(s => {
    const marker = L.circleMarker(s.coords, { radius: 10, fillColor: '#ec4899', color: '#fff', weight: 2, opacity: 1, fillOpacity: 0.8 });
    marker.bindPopup(`<b>${s.nome}</b><br>${s.tipo}`);
    return marker;
  }));

  // Atualizar camadas padrão
  map.removeLayer(layerPraias);
  layerPraiasCompleta.addTo(map);

  // Atualizar surf
  if (map.hasLayer(layerSurf)) {
    map.removeLayer(layerSurf);
    layerSurfCompleto.addTo(map);
  }

  // Controles adicionais
  document.getElementById('layer-transporte').addEventListener('change', (e) => { e.target.checked ? layerTransporte.addTo(map) : map.removeLayer(layerTransporte); });
  document.getElementById('layer-gastronomia').addEventListener('change', (e) => { e.target.checked ? layerGastronomia.addTo(map) : map.removeLayer(layerGastronomia); });
  document.getElementById('layer-parques').addEventListener('change', (e) => { e.target.checked ? layerParques.addTo(map) : map.removeLayer(layerParques); });
  document.getElementById('layer-parceiros').addEventListener('change', (e) => { e.target.checked ? layerParceiros.addTo(map) : map.removeLayer(layerParceiros); });
"""

# Adicionar novos controles antes do fechamento do script
text = text.replace('  document.getElementById(\'layer-eventos\').addEventListener(\'change\', (e) => { e.target.checked ? layerEventos.addTo(map) : map.removeLayer(layerEventos); });', 
                     '  document.getElementById(\'layer-eventos\').addEventListener(\'change\', (e) => { e.target.checked ? layerEventos.addTo(map) : map.removeLayer(layerEventos); });' + novos_controles)

# Adicionar checkboxes no HTML
novos_checkboxes = """
    <div class="legend-item"><input type="checkbox" id="layer-transporte"><span class="legend-color" style="background:#64748b;"></span>Transporte</div>
    <div class="legend-item"><input type="checkbox" id="layer-gastronomia"><span class="legend-color" style="background:#f97316;"></span>Gastronomia</div>
    <div class="legend-item"><input type="checkbox" id="layer-parques"><span class="legend-color" style="background:#22c55e;"></span>Parques</div>
    <div class="legend-item"><input type="checkbox" id="layer-parceiros"><span class="legend-color" style="background:#6366f1;"></span>Parceiros</div>
"""

text = text.replace('    <div class="legend-item"><input type="checkbox" id="layer-eventos"', novos_checkboxes + '    <div class="legend-item"><input type="checkbox" id="layer-eventos"')

path.write_text(text, encoding='utf-8')
print('map layers expanded')
