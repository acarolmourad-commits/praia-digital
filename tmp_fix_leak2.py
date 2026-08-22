from pathlib import Path
import re

base = Path('assets')
files = [
    'analise-retorno-aluguel-temporada-ia.html',
    'predicao-vendidos-litoral.html',
    'roi-ia-imobiliaria.html',
    'servico-assistente-virtual-compradores-litoral.html',
]
for fname in files:
    p = base / fname
    text = p.read_text(encoding='utf-8', errors='ignore')
    # Remove duplicate viewport in analise-retorno...
    if fname == 'analise-retorno-aluguel-temporada-ia.html':
        text = text.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots"', '<meta name="robots"', 1)
    # Fix pattern: </html>...<script>...</script></body> -> <script>...</script></body></html>
    def repl(m):
        body_tail = m.group(1)
        if body_tail.lstrip().startswith('<div') or body_tail.lstrip().startswith('<script'):
            return body_tail + '</html>'
        return m.group(0)
    text = re.sub(r'</html>([\s\S]*?)(</body>)', repl, text, count=1)
    # Ensure body is closed before html if not already
    if text.count('<body>') > text.count('</body>'):
        text = text.replace('</html>', '</body></html>', 1)
    # Ensure html is closed at end
    if not text.strip().endswith('</html>'):
        text = text.rstrip() + '\n</html>'
    p.write_text(text, encoding='utf-8')
    print('patched', fname)
