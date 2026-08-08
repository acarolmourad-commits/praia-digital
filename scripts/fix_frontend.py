from pathlib import Path

base = Path('C:/Users/Carolina/praia-digital')
files = list(base.glob('education/**/*.html'))

WA_LINK = 'https://wa.me/5511954346288?text=Quero%20saber%20mais%20sobre%20o%20curso'

def process_file(path: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    original = text
    
    # Remove Tailwind CDN script tag (any whitespace)
    text = text.replace('cdn.tailwindcss.com', 'REPLACED_TAILWIND')
    
    # Remove tailwind.config script block
    if 'tailwind.config' in text:
        start = text.find('<script>\n    tailwind.config')
        end = text.find('</script>', start)
        if start != -1 and end != -1:
            text = text[:start] + text[end+9:]
    
    # Fix common Tailwind classes to inline styles
    replacements = {
        'bg-brand-bg text-brand-text min-h-screen flex items-center justify-center': 'background:#0b1220;color:#e8ecf1;min-height:100vh;display:flex;align-items:center;justify-content:center',
        'bg-brand-surface p-8 rounded border border-gray-800 w-full max-w-md': 'background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:18px 20px;width:100%;max-width:420px',
        'text-2xl font-bold text-white mb-2': 'font-size:1.5rem;font-weight:700;color:#fff;margin-bottom:.5rem',
        'text-gray-400 mb-6': 'color:#9ca3af;margin-bottom:1rem',
        'space-y-4': 'display:flex;flex-direction:column;gap:1rem',
        'block text-sm text-gray-300 mb-1': 'display:block;font-size:.875rem;color:#d1d5db;margin-bottom:.25rem',
        'w-full bg-gray-900 border border-gray-700 rounded px-3 py-2 text-white': 'width:100%;background:#111827;border:1px solid #374151;border-radius:8px;padding:8px 12px;color:#fff',
        'w-full bg-brand-accent text-black font-bold py-2 rounded': 'width:100%;background:#00B4D8;color:#000;font-weight:700;padding:.5rem;border-radius:8px;border:none;cursor:pointer',
        'text-red-400 text-sm hidden': 'color:#f87171;font-size:.875rem;display:none',
        'text-gray-400 text-sm mt-4': 'color:#9ca3af;font-size:.875rem;margin-top:1rem',
        'text-brand-accent': 'color:#00B4D8',
        'text-sm text-gray-300 mb-1': 'font-size:.875rem;color:#d1d5db;margin-bottom:.25rem',
        'bg-brand-bg text-brand-text': 'background:#0b1220;color:#e8ecf1',
        'min-h-screen': 'min-height:100vh',
        'flex items-center justify-center': 'display:flex;align-items:center;justify-content:center',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Fix grid-template-column typo
    text = text.replace('grid-template-column', 'grid-template-columns')
    
    # Fix empty href="#"
    if path.name in ['curso.html', 'index.html'] and 'href="#"' in text:
        text = text.replace('href="#"', 'href="/education/aluno/index.html"')
    
    # Replace axios with fetch in admin.html
    if path.name == 'admin.html':
        if 'import axios' in text:
            text = text.replace("import axios from 'https://cdn.skypack.dev/axios'", "// axios removed")
        text = text.replace('const res = await axios.post(apiBase +', 'const res = await fetch(apiBase +')
        if 'const data = res.data;' in text:
            text = text.replace('const data = res.data;', 'const data = await res.json();')
        text = text.replace('errorEl.textContent = err.response?.data?.detail', 'errorEl.textContent = err')
    
    # Add WhatsApp link to sales pages
    if path.name == 'vendas.html' and WA_LINK not in text:
        if 'Comprar' in text or 'Quero' in text or 'checkout' in text.lower():
            insert = f'<p style="margin-top:1rem"><a href="{WA_LINK}" target="_blank" rel="noopener" style="background:#0ea5e9;color:#fff;padding:.7rem 1.2rem;border-radius:999px;font-weight:700;text-decoration:none;display:inline-block">Falar no WhatsApp</a></p>'
            text = text.replace('</main>', insert + '</main>')
            text = text.replace('</body>', insert + '</body>')
    
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False

changed = []
for path in files:
    if process_file(path):
        changed.append(str(path.relative_to(base)))

print(f'Arquivos alterados: {len(changed)}')
for p in changed[:20]:
    print(f'- {p}')
if len(changed) > 20:
    print(f'... e mais {len(changed) - 20} arquivos')
