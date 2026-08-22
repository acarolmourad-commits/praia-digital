from pathlib import Path

files = {
    'roi-ia-imobiliaria.html': 'assets/roi-ia-imobiliaria.html',
    'servico-assistente-virtual-compradores-litoral.html': 'assets/servico-assistente-virtual-compradores-litoral.html',
    'predicao-vendidos-litoral.html': 'assets/predicao-vendidos-litoral.html',
}
for name, rel in files.items():
    p = Path(rel)
    text = p.read_text(encoding='utf-8', errors='ignore')
    if name == 'roi-ia-imobiliaria.html':
        text = text.replace('<footer>\n</html>\n<div', '<footer>\n</div>\n<div', 1)
        text = text.replace('</html>\n</body>', '</div>\n</body>\n</html>', 1)
    if name == 'servico-assistente-virtual-compradores-litoral.html':
        text = text.replace('</html>\r\n<div id="result-servico-assistente-virtual-compradores-litoral"', '</div>\n<div id="result-servico-assistente-virtual-compradores-litoral"', 1)
        text = text.replace('<p class=\\"error\\">Preencha todos os campos.</p>', '<p class="error">Preencha todos os campos.</p>', 1)
        text = text.replace('`região central`.', '`região central`.', 1)
    if name == 'predicao-vendidos-litoral.html':
        text = text.replace('</html>\n<div id="result-predicao-vendidos-litoral"', '</div>\n<div id="result-predicao-vendidos-litoral"', 1)
        text = text.replace('</html>\n</body>', '</div>\n</body>\n</html>', 1)
    p.write_text(text, encoding='utf-8')
    print('patched', name)
