from pathlib import Path

files = [
    'assets/roi-ia-imobiliaria.html',
    'assets/servico-assistente-virtual-compradores-litoral.html',
    'assets/predicao-vendidos-litoral.html',
]
for rel in files:
    p = Path(rel)
    text = p.read_text(encoding='utf-8', errors='ignore')
    # Remove any </html> before the last </body>
    last_body = text.rfind('</body>')
    if last_body != -1:
        pre = text[:last_body]
        post = text[last_body:]
        pre = pre.replace('</html>', '', 1)
        text = pre + post
    # Ensure file ends with </html>
    text = text.rstrip()
    if not text.endswith('</html>'):
        text += '\n</html>'
    p.write_text(text, encoding='utf-8')
    print('fixed', rel)
