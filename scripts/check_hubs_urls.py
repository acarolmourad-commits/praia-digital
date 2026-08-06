import requests, re
from pathlib import Path

hubs = [
    '/bairros/santos/index.html',
    '/bairros/guaruja/index.html',
    '/bairros/praia-grande/index.html',
    '/bairros/bertioga/index.html',
    '/bairros/ilhabela/index.html',
    '/bairros/ubatuba/index.html',
    '/bairros/sao-sebastiao/index.html',
    '/bairros/caraguatatuba/index.html',
]
bad_needles = [
    'servicoscidade-servico',
    '/Caraguatatuba/',
    'cidadesbertioga',
    'praia.digitaleducation',
    '\\',
]
issues = []
for p in hubs:
    txt = requests.get('https://praia.digital' + p, timeout=20).text
    bad = sum(txt.count(n) for n in bad_needles)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', txt)
    og = re.search(r'<meta property="og:url" content="([^"]+)"', txt)
    issues.append({
        'path': p,
        'status': 200,
        'bad': bad,
        'canon': canon.group(1) if canon else '-',
        'og': og.group(1) if og else '-',
    })

for item in issues:
    print(item)
print('issues_total_bad=', sum(i['bad'] for i in issues))
