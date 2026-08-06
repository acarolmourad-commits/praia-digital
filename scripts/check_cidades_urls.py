import requests, re
from pathlib import Path

paths = [
    '/cidades/santos.html',
    '/cidades/guaruja.html',
    '/cidades/praia-grande.html',
    '/cidades/bertioga.html',
    '/cidades/itanhaem.html',
    '/cidades/mongagua.html',
    '/cidades/sao-vicente.html',
    '/cidades/peruibe.html',
]
needles = ['servicoscidade-servico', 'cidadesbertioga', 'praia.digitaleducation', '\\']

for p in paths:
    txt = requests.get('https://praia.digital' + p, timeout=20).text
    bad = sum(txt.count(n) for n in needles)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', txt)
    og = re.search(r'<meta property="og:url" content="([^"]+)"', txt)
    hreflang = re.search(r'<link rel="alternate" hreflang="x-default" href="([^"]+)"', txt)
    print(f"{p}: status=200 bad={bad} canon={canon.group(1) if canon else '-'} og={og.group(1) if og else '-'} hreflang={hreflang.group(1) if hreflang else '-'}")
