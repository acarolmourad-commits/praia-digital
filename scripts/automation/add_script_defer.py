from pathlib import Path
import re

root = Path('.')
pages = [
    'index.html',
    'servicos.html',
    'imoveis.html',
    'cases.html',
    'blog/index.html',
]

updated = 0
for rel in pages:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    new_text = re.sub(
        r'<script\s+([^>]*?)src="([^"]+)"\s*([^>]*?)>',
        lambda m: f'<script {m.group(1)}src="{m.group(2)}" defer {m.group(3)}>' if 'defer' not in m.group(0) and 'async' not in m.group(0) else m.group(0),
        text
    )
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    else:
        print('skip', rel)

print('updated', updated, 'pages')
