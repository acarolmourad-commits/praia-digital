import requests
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

root=Path('.').resolve()
base='https://praia.digital/'
checked=0
broken=0
seen=set()
for p in root.rglob('*.html'):
    rel=p.relative_to(root)
    txt=p.read_text(encoding='utf-8',errors='ignore')
    links=re.findall(r'href="([^"#]+)"', txt)
    for link in links:
        if link.startswith(('mailto:', 'tel:', 'javascript:', 'data:', '#')):
            continue
        if link.startswith('http'):
            url=link
        else:
            url=urljoin(base+str(rel.parent).replace('\\','/')+'/', link)
        if url in seen:
            continue
        seen.add(url)
        if not url.startswith('https://praia.digital'):
            continue
        try:
            r=requests.get(url,timeout=10,allow_redirects=True)
            if r.status_code>=400:
                broken+=1
                print(r.status_code, url)
        except Exception as e:
            broken+=1
            print('ERR', url, type(e).__name__, e)
        checked+=1
print('checked', checked, 'broken', broken)
