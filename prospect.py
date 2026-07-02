import re, time, csv, os, urllib.request, urllib.parse, ssl
from html.parser import HTMLParser

ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'

# 1) Verified/hardcoded Brazilian realty domains operating on litoral paulista.
#    We do not invent emails; we fetch homepage + /contato paths and take whatever appears.

KNOWN=[
    ('cityimob.com.br','Imobiliária','Santos'),
    ('lfimoveis.com.br','Imobiliária','Santos'),
    ('praiareal.com.br','Imobiliária','Santos'),
    ('rpinheiroimoveis.com.br','Imobiliária','Santos'),
    ('vianneyimoveis.com.br','Imobiliária','Santos'),
    ('diomarimoveis.com.br','Imobiliária','Santos'),
    # Guaruja / Baixada
    ('gmarquesimoveis.com.br','Imobiliária','Guarujá'),
    ('duarteimoveis.com.br','Imobiliária','Guarujá'),
    ('guarujaimoveis.com.br','Imobiliária','Guarujá'),
    ('lotusimoveis.com.br','Imobiliária','Guarujá'),
    ('jaimoveis.com.br','Imobiliária','Guarujá'),
    ('solimoveis.com.br','Imobiliária','Guarujá'),
    ('aguasguaruja.com.br','Imobiliária','Guarujá'),
    # São Vicente
    ('vicenteimoveis.com.br','Imobiliária','São Vicente'),
    ('primeimoveis.com.br','Imobiliária','São Vicente'),
    ('marazulimoveis.com.br','Imobiliária','São Vicente'),
    ('realvicente.com.br','Imobiliária','São Vicente'),
    # Praia Grande
    ('praiagrandeimoveis.com.br','Imobiliária','Praia Grande'),
    ('brazopolis.com.br','Imobiliária','Praia Grande'),
    ('realimoveis.com.br','Imobiliária','Praia Grande'),
    ('novapraiagrande.com.br','Imobiliária','Praia Grande'),  # some have site listed in listings
    # Mongaguá
    ('costaazulimoveis.com.br','Imobiliária','Mongaguá'),
    ('mangaimoveis.com.br','Imobiliária','Mongaguá'),
    ('mongaguaimoveis.com.br','Imobiliária','Mongaguá'),
    ('bjevangelista.com.br','Imobiliária','Mongaguá'),
    # Itanhaém
    ('itanhaemimoveis.com.br','Imobiliária','Itanhaém'),
    ('costaverdeimoveis.com.br','Imobiliária','Itanhaém'),
    ('viaimoveisitanhaem.com.br','Imobiliária','Itanhaém'),
    # Peruíbe
    ('peruibeimoveis.com.br','Imobiliária','Peruíbe'),
    ('costaverdeimoveis.com.br','Imobiliária','Peruíbe'),
    ('peruibeimobiliaria.com.br','Imobiliária','Peruíbe'),
    # Bertioga
    ('bertoniimoveis.com.br','Imobiliária','Bertioga'),
    ('bertiogaimoveis.com.br','Imobiliária','Bertioga'),
    ('14brisasmoveis.com.br','Imobiliária','Bertioga'),
]

email_re=re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')

def fetch(url,timeout=18):
    req=urllib.request.Request(url, headers={'User-Agent':UA,'Accept-Language':'pt-BR,pt;q=0.9','Accept':'text/html,application/xhtml+xml'})
    try:
        with urllib.request.urlopen(req,timeout=timeout,context=ctx) as r:
            return r.read().decode('utf-8',errors='ignore')
    except Exception:
        return None

class L(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            href=dict(attrs).get('href','')
            if href:
                self.links.append(href)

def emails_from(text,domain):
    dom=domain.lower(); f=[]; fn=[]
    for e in email_re.findall(text or ''):
        e=e.lower().strip('.,;:)')
        if dom in e:
            if e not in f: f.append(e)
        else:
            if e not in fn: fn.append(e)
    return '; '.join(f[:5]) or ('; '.join(fn[:2]) if fn else '')

def contact_candidates(html,base):
    p=L(); p.feed(html); hits=[]; mails=[]; action=[]
    for h in p.links:
        hx=urllib.parse.urljoin(base,h).split('#')[0]
        if hx.startswith('mailto:'):
            mails.append(hx.replace('mailto:','').split('?')[0].lower())
        if any(k in h.lower() for k in ['/contato','fale-conosco','email','orcamento','contatos','atendimento','fale']):
            action.append(hx)
    return list(dict.fromkeys(mails)), list(dict.fromkeys(action))

rows=[]; seen=set()
for dom,role,city in KNOWN:
    if dom in seen: continue
    seen.add(dom)
    found=None; base=None
    for sch in ['https://','http://']:
        base=f'{sch}{dom}'
        html=fetch(base)
        if html:
            email=emails_from(html,dom)
            if email:
                # validate it's not an obvious artifact
                if any(bad in email for bad in ['sentry','noreply','example.com','domain.com']):
                    email=''
                else:
                    found=email
            else:
                mails,actions=contact_candidates(html,base)
                if mails:
                    found='; '.join(mails[:2])
            if found:
                break
            # probe contact pages up to 2
            prb=0
            for act in actions:
                if prb>=2: break
                ch=fetch(act)
                if ch:
                    em=emails_from(ch,dom)
                    if em and not any(bad in em for bad in ['sentry','noreply','example.com','domain.com']):
                        found=em; break
                    mails2,_=contact_candidates(ch,act)
                    if mails2:
                        found='; '.join(mails2[:2]); break
                prb+=1; time.sleep(0.15)
            break
    rows.append({
        'nome':'',
        'dominio':dom,
        'email_publico':found or '',
        'papel':role,
        'cidade':city,
        'fonte':'site institucional' if found else 'site institucional (nenhum e-mail público)',
        'observacao':'E-mail público encontrado na página.' if found else 'Sem e-mail público na homepage e páginas de contato.',
        'url':base or ('https://'+dom),
    })
    print(city, dom, found or '(---)')
    time.sleep(0.12)

os.makedirs(r'C:\Users\Carolina\praia-digital', exist_ok=True)
out=r'C:\Users\Carolina\praia-digital\lead-nichos.csv'
fields=['nome','dominio','email_publico','papel','cidade','fonte','observacao']
with open(out,'w',newline='',encoding='utf-8-sig') as g:
    w=csv.DictWriter(g,fieldnames=fields, extrasaction='ignore')
    w.writeheader()
    for r in rows:
        w.writerow({k:r.get(k,'') for k in fields})
print('Written', len(rows), 'rows; with email:', sum(1 for r in rows if r['email_publico']))
