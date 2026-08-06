import requests, re
p = '/bairros/caraguatatuba/index.html'
txt = requests.get('https://praia.digital' + p, timeout=20).text
needles = ['servicoscidade-servico', 'cidadesbertioga', 'praia.digitaleducation']
bad = sum(txt.count(n) for n in needles)
canon = re.search(r'<link rel="canonical" href="([^"]+)"', txt)
og = re.search(r'<meta property="og:url" content="([^"]+)"', txt)
print(f"{p}: status=200 bad={bad} canon={canon.group(1) if canon else '-'} og={og.group(1) if og else '-'}")
