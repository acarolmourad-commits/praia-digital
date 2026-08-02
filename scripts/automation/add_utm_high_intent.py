from pathlib import Path
import re

root = Path('.')
exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

utm = 'utm_source=site&utm_medium=whatsapp&utm_campaign=geral'

target_roots = {
    'landing-parcerias-anuncios.html',
    'landing-parcerias-captura-praia-digital-2026.html',
    'landing-parcerias-captura-praia-digital-conversao-2026.html',
    'landing-parcerias-conversao-praia-digital-2026.html',
    'landing-parcerias-imobiliarias-litoral.html',
    'avaliacao-preco-imoveis.html',
    'consultoria-transformacao-digital-imobiliarias.html',
    'descricao-imoveis-ia.html',
    'encontrar-imovel.html',
    'investidores.html',
    'obrigado-segmentado.html',
    'parcerias-litoral-paulista.html',
    'proposta-comercial-padrao-2026.html',
    'seo-local-imobiliarias.html',
    'servicos-ia-investidores.html',
    'servicos-proptech-2026.html',
}

def is_target(rel):
    name = rel.name
    if name in target_roots:
        return True
    if rel.parts[0] == 'servicos':
        return True
    if name.startswith('guia-'):
        return True
    return False

updated = 0
for p in root.rglob('*.html'):
    rel = p.relative_to(root)
    if any(part in exclude for part in rel.parts):
        continue
    if not is_target(rel):
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    if 'utm_' in text:
        continue
    def add_utm(m):
        url = m.group(1)
        if '?' in url:
            return url + '&' + utm
        return url + '?' + utm
    new_text = re.sub(r'(https://wa\.me/5511954346288)(\?[^"\'>\s]*)?', add_utm, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
print('updated', updated)
