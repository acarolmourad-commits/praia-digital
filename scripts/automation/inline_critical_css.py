from pathlib import Path
import re

root = Path('.')

pages = [
    'index.html',
    'servicos.html',
    'imoveis.html',
    'cases.html',
]

critical_css = '''<style>
  :root{color-scheme:light}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;line-height:1.6;background:#f8fafc;color:#0f172a;-webkit-font-smoothing:antialiased}
  header,nav,main,section,article,footer{display:block}
  img,svg,video{max-width:100%;height:auto;display:block}
  a{color:inherit;text-decoration:none}
  .container{width:92%;max-width:1200px;margin:0 auto}
  .skip-link{position:absolute;left:-9999px}
  .skip-link:focus{position:fixed;top:1rem;left:1rem;background:#0f172a;color:#fff;padding:.5rem .75rem;border-radius:8px;z-index:9999}
  .hero{padding:3.5rem 1rem;text-align:center;background:linear-gradient(135deg,#0ea5e9,#0a3a6b);color:#fff}
  .hero h1{font-size:clamp(1.6rem,4vw,2.6rem);line-height:1.2;margin-bottom:.75rem}
  .hero p{font-size:clamp(1rem,2.2vw,1.15rem);color:#e2e8f0;max-width:780px;margin:0 auto 1.25rem}
  .btn,a.btn{display:inline-block;background:#0ea5e9;color:#fff;padding:.85rem 1.4rem;border-radius:999px;font-weight:700;border:0}
  .card{background:#fff;border-radius:14px;padding:1.25rem;box-shadow:0 10px 30px rgba(15,23,42,.08)}
  .grid{display:grid;gap:1rem}
  @media (min-width:760px){.grid-3{grid-template-columns:repeat(3,1fr)}.grid-2{grid-template-columns:repeat(2,1fr)}}
  .section{padding:2rem 1rem}
  .section-alt{background:#e2e8f0}
  h1,h2,h3{letter-spacing:-.01em}
  h2{font-size:clamp(1.3rem,3vw,1.8rem);margin-bottom:.6rem}
  p{margin:.4rem 0}
</style>
'''

updated = 0
for rel in pages:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '<style>' in text or 'critical-css-inline' in text:
        print('skip', rel)
        continue
    new_text = text.replace('</head>', critical_css + '</head>', 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    else:
        print('no-insert', rel)

print('updated', updated)
