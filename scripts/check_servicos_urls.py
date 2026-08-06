import requests, re
paths = [
    '/servicos/cidade-servico/guaruja-automacao.html',
    '/servicos/cidade-servico/guaruja-avaliacao.html',
    '/servicos/automacao.html',
    '/servicos/avaliacao.html',
    '/bairros/ubatuba/index.html',
    '/bairros/ilhabela/index.html',
    '/bairros/sao-sebastiao/index.html',
]
needles = ['servicoscidade-servico']
for p in paths:
    txt = requests.get('https://praia.digital' + p, timeout=20).text
    bad = sum(txt.count(n) for n in needles)
    back = txt.count('\\')
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', txt)
    print(f"{p}: status=200, bad={bad}, backslash={back}, canon={canon.group(1) if canon else '-'}")
