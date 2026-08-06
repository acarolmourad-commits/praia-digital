import requests, re
from pathlib import Path

samples = [
    '/cidades/guaruja-imoveis-venda.html',
    '/cidades/santos-elevador.html',
    '/cidades/praia-grande-seguranca.html',
    '/cidades/bertioga-pet-friendly.html',
    '/cidades/itanhaem-academia.html',
]
needles = ['praia.digitaleducation', 'cidadesbertioga']

for p in samples:
    try:
        txt = requests.get('https://praia.digital' + p, timeout=20).text
        bad = sum(txt.count(n) for n in needles)
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', txt)
        og = re.search(r'<meta property="og:url" content="([^"]+)"', txt)
        print(f"{p}: status=200 bad={bad} canon={canon.group(1) if canon else '-'} og={og.group(1) if og else '-'}")
    except Exception as e:
        print(f"{p}: ERROR {e}")
