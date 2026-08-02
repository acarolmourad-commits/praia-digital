from pathlib import Path

root = Path('.')

cta_block = '''    <section class="servicos-section" style="background: linear-gradient(135deg, #0ea5e9, #0a3a6b); padding: 2.5rem 1rem; text-align: center; color: #fff; border-radius: 12px; margin: 1.5rem auto; max-width: 900px;">
      <h2 style="color: #fff; margin-bottom: 0.5rem;">Quer vender ou alugar seu imóvel no litoral?</h2>
      <p style="margin-bottom: 1rem; font-size: 1.05rem; color: #e2e8f0;">Fale agora com um consultor especializado e receba uma avaliação sem compromisso.</p>
      <a href="https://wa.me/5511954346288?text=Ol%C3%A1!%20Quero%20avaliar%20meu%20im%C3%B3vel%20no%20litoral." target="_blank" rel="noopener" style="display: inline-block; background: linear-gradient(90deg, #25D366, #128C7E); color: #fff; font-weight: 800; padding: 0.9rem 1.6rem; border-radius: 50px; text-decoration: none; box-shadow: 0 6px 18px rgba(0,0,0,0.25);">Falar no WhatsApp agora</a>
      <p style="margin-top: 0.75rem; font-size: 0.9rem; color: #cbd5e1;">Atendimento rápido e humanizado • (11) 95434-6288</p>
    </section>
'''

pages = {
    'index.html': '<footer>',
    'servicos.html': '<footer>',
    'imoveis.html': '<footer>',
    'cases.html': '<footer>',
}

for rel, marker in pages.items():
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Quer vender ou alugar seu imóvel no litoral?' in text:
        print('skip', rel)
        continue
    if marker not in text:
        print('missing footer marker', rel)
        continue
    new_text = text.replace(marker, cta_block + marker, 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
    else:
        print('no-insert', rel)
