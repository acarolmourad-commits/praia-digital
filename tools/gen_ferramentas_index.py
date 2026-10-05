import os, re, html

def info(p):
    t = open(p, encoding='utf-8').read()
    title = re.search(r'<title>([^<]*)', t)
    desc = re.search(r'name="description" content="([^"]*)', t)
    ti = title.group(1).replace(' | Praia Digital','').replace(' \u2014 Praia Digital','').strip() if title else os.path.basename(p)
    de = desc.group(1).strip() if desc else ''
    return html.escape(ti), html.escape(de)

def cards(subdir):
    out = []
    for f in sorted(os.listdir(f'ferramentas-gratuitas/{subdir}')):
        if not f.endswith('.html'): continue
        p = f'ferramentas-gratuitas/{subdir}/{f}'
        ti, de = info(p)
        out.append(f'<div class="card"><h3><a href="/ferramentas-gratuitas/{subdir}/{f}">{ti}</a></h3><p>{de}</p></div>')
    return '\n'.join(out)

imob = cards('imobiliarias')
leads = cards('captura-leads')

page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Ferramentas gratuitas para imobili\u00e1rias e corretores no litoral | Praia Digital</title>
<meta name="description" content="Ferramentas gratuitas da Praia Digital: calculadora de financiamento, simulador de temporada, gerador de descri\u00e7\u00e3o com IA, checklists, pr\u00e9-qualifica\u00e7\u00e3o de leads e capta\u00e7\u00e3o por cidade no litoral paulista."/>
<link href="https://praia.digital/ferramentas-gratuitas/" rel="canonical"/>
<meta content="index, follow" name="robots"/>
<meta content="website" property="og:type"/>
<meta content="Ferramentas gratuitas para imobili\u00e1rias e corretores no litoral" property="og:title"/>
<meta content="https://praia.digital/ferramentas-gratuitas/" property="og:url"/>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Ferramentas gratuitas para imobili\u00e1rias e corretores no litoral",
  "url": "https://praia.digital/ferramentas-gratuitas/",
  "publisher": {{"@type": "Organization", "name": "Praia Digital"}}
}}
</script>
<style>
body{{font-family:'Segoe UI',Arial,Helvetica,sans-serif;background:#F4EBD0;color:#023047;margin:0;padding:0;line-height:1.6}}
.container{{max-width:1000px;margin:20px auto;padding:20px;background:#FFFFFF;border-radius:12px;box-shadow:0 2px 12px rgba(2,48,71,.08)}}
a{{color:#0077B6}}
a:hover{{color:#00B4D8}}
.nav{{margin-bottom:20px}}
.nav a{{margin-right:10px;text-decoration:underline}}
h1{{color:#023047}}
h2{{color:#0077B6;margin-top:30px}}
.card{{background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 16px;margin:10px 0}}
.card h3{{margin:0 0 6px;font-size:17px}}
.card p{{margin:0;color:#41525f;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.cta{{background:#0077B6;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;display:inline-block;margin:16px 0}}
.cta:hover{{background:#023047;color:#fff}}
</style>
<link rel="stylesheet" href="https://praia.digital/css/style.css">
</head>
<body>
<meta name="pd-shared-nav">
<div class="container">
<div class="nav">
<a href="https://praia.digital/index.html">In\u00edcio</a>
<a href="https://praia.digital/blog/index.html">Blog</a>
</div>
<h1>Ferramentas gratuitas para imobili\u00e1rias e corretores</h1>
<p>Todas as ferramentas gratuitas da Praia Digital para quem atua no mercado imobili\u00e1rio do litoral paulista: simuladores, calculadoras, checklists, geradores com IA e capta\u00e7\u00e3o de leads por cidade.</p>

<h2>Ferramentas para imobili\u00e1rias</h2>
<div class="grid">
{imob}
</div>

<h2>Capta\u00e7\u00e3o de leads e parcerias por cidade</h2>
<div class="grid">
{leads}
</div>

<p><a class="cta" href="https://wa.me/5511954346288?text=Ol%C3%A1,%20quero%20saber%20mais%20sobre%20as%20ferramentas%20da%20Praia%20Digital">Falar com especialista no WhatsApp</a></p>
</div>
<meta name="pd-shared-footer">
<script src="https://praia.digital/js/shared.js?v=2.0"></script>
</body>
</html>
"""
open('ferramentas-gratuitas/index.html','w',encoding='utf-8').write(page)
print('ok', len(page), page.count('class="card"'))
