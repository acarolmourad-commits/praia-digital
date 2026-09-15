#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplificação de navegação 2026-09 — Praia Digital
1) Menu principal da home: 4 grupos com duplicidades -> 3 personas
   (Quero Investir / Quero Comprar / Sou Corretor) + CTA WhatsApp.
2) Assistente IA flutuante: 9 links (com 'Mapa Inteligente' duplicado) -> 3 atalhos.
Idempotente: se já aplicado, sai sem erro. Roda na raiz do repo.
"""
CHANGES = []

s = open('index.html', encoding='utf-8', errors='ignore').read()

# ---------- 1) Menu principal ----------
old_nav = '''  <nav aria-label="Navegação principal" class="pd-nav-menu">
    <div class="pd-nav-group">
      <span class="pd-nav-label">Quero Investir</span>
      <a href="#rental">Simulador de ROI</a>
      <a href="exclusivos/relatorio-mercado-2026.html">Relatórios</a>
      <a href="cases.html">Oportunidades</a>
    </div>
    <div class="pd-nav-group">
      <span class="pd-nav-label">Quero Comprar</span>
      <a href="#buscar">Busca de Imóveis</a>
      <a href="bairros/index.html">Guia de Bairros</a>
      <a href="cases.html">Cases</a>
    </div>
    <div class="pd-nav-group">
      <span class="pd-nav-label">Ferramentas IA</span>
      <a href="servicos.html">Serviços</a>
      <a href="planos-assinatura.html">Planos</a>
    </div>
    <div class="pd-nav-group">
      <span class="pd-nav-label">Inteligência</span>
      <a href="blog/index.html">Blog & Estudos</a>
      <a href="exclusivos/relatorio-mercado-2026.html">Relatórios</a>
      <a href="cases.html">Cases</a>
    </div>
    <a href="https://wa.me/5511954346288" class="nav-highlight-sale pd-nav-cta">Fale conosco</a>
  </nav>'''

new_nav = '''  <nav aria-label="Navegação principal" class="pd-nav-menu">
    <div class="pd-nav-group">
      <span class="pd-nav-label">Quero Investir</span>
      <a href="#rental">Simulador de ROI</a>
      <a href="exclusivos/relatorio-mercado-2026.html">Relatórios de Valorização</a>
      <a href="cases.html">Oportunidades</a>
    </div>
    <div class="pd-nav-group">
      <span class="pd-nav-label">Quero Comprar</span>
      <a href="#buscar">Busca de Imóveis</a>
      <a href="bairros/index.html">Guia de Bairros</a>
      <a href="cases.html">Cases</a>
    </div>
    <div class="pd-nav-group">
      <span class="pd-nav-label">Sou Corretor</span>
      <a href="servicos.html">Serviços com IA</a>
      <a href="planos-assinatura.html">Planos</a>
      <a href="blog/index.html">Blog & Estudos</a>
    </div>
    <a href="https://wa.me/5511954346288" class="nav-highlight-sale pd-nav-cta">Falar no WhatsApp</a>
  </nav>'''

if old_nav in s:
    s = s.replace(old_nav, new_nav, 1); CHANGES.append('menu simplificado para 3 personas')
elif 'Sou Corretor' in s:
    CHANGES.append('menu já simplificado')
else:
    raise SystemExit('FALHA: bloco de menu não encontrado em index.html')

# ---------- 2) Links do assistente IA ----------
start_marker = '<a href="dashboard/index.html" class="action-btn secondary"'
end_marker = '🧭 Painel de prospecção</a>'
i = s.find(start_marker)
if i >= 0:
    j = s.find(end_marker, i)
    if j < 0:
        raise SystemExit('FALHA: fim do bloco de links do assistente não encontrado')
    j += len(end_marker)
    new_links = ('<a href="#rental" class="action-btn secondary">📈 Simular ROI do meu imóvel</a>\n'
                 '    <a href="exclusivos/relatorio-mercado-2026.html" class="action-btn secondary" target="_blank" rel="noopener">📊 Relatórios de Valorização</a>\n'
                 '    <a href="https://praia.digital/anfitrioes/index.html" class="action-btn secondary" target="_blank" rel="noopener">🌟 Área do Anfitrião</a>')
    s = s[:i] + new_links + s[j:]
    CHANGES.append('assistente IA: 9 links -> 3 atalhos')
elif 'Simular ROI do meu imóvel' in s:
    CHANGES.append('assistente IA já simplificado')
else:
    raise SystemExit('FALHA: bloco de links do assistente não encontrado')

open('index.html', 'w', encoding='utf-8').write(s)
print('=== ALTERAÇÕES ===')
for c in CHANGES: print('-', c)
print('OK')
