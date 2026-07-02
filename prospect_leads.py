import re
import time
import csv
import os
import urllib.request
import urllib.parse
import urllib.error
import ssl
from html.parser import HTMLParser

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

cities = [
    ('Santos','Santos SP'),
    ('Guarujá','Guaruja SP'),
    ('Bertioga','Bertioga SP'),
    ('São Vicente','Sao Vicente SP'),
    ('Praia Grande','Praia Grande SP'),
    ('Mongaguá','Mongagua SP'),
    ('Itanhaém','Itanhaem SP'),
    ('Peruíbe','Peruibe SP'),
]

# ========== HTTP helpers ==========
def fetch_bytes(url, timeout=20):
    req = urllib.request.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xhtml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            b = r.read()
            return r.headers.get('content-type',''), b
    except urllib.error.HTTPError as e:
        try:
            with urllib.error.HTTPError(e.code, e.reason, e.file, e.fp) as resp:
                return 'text/html', resp.read()
        except Exception:
            return None, None
    except Exception:
        return None, None

def fetch(url, timeout=20):
    ct, b = fetch_bytes(url, timeout)
    if b is None:
        return None
    ctype = ct or ''
    if 'charset=' in ctype:
        enc = ctype.split('charset=')[-1].split(';')[0].strip()
    else:
        enc = 'utf-8'
    try:
        return b.decode(enc, errors='ignore')
    except Exception:
        try:
            return b.decode('latin-1', errors='ignore')
        except Exception:
            return None

# ========== Parser/Classifiers ==========
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.in_link=False
    def handle_starttag(self, tag, attrs):
        if tag.lower()=='a':
            href = dict(attrs).get('href','')
            if href and not href.startswith(('javascript:','#')):
                self.links.append(href)

def extract_text(html):
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.I|re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

email_pattern = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
kw_pattern = re.compile(r'(imobili[aá]r|im[óo]vel|corretor|construt|incorporador|administrador[a]?\s+de\s+im[óo]vel|gest[aã]o\s+de\s+temporada|loca[çc][ãa]o\s+de\s+im[óo]vel|temporada)', re.I)

ROLE_SYNONYMS = {
    'imobiliária':'Imobiliária',
    'imobiliaria':'Imobiliária',
    'imóveis':'Imobiliária',
    'imovel':'Imobiliária',
    'corretor':'Corretor',
    'construtora':'Construtora',
    'construção':'Construtora',
    'incorporadora':'Construtora',
    'incorporacao':'Construtora',
    'administradora':'Administradora',
    'administração':'Administradora',
    'gestão de temporada':'Gestor de temporada',
    'temporada':'Gestor de temporada',
    'locaçao':'Imobiliária',
}

def guess_role(text, domain):
    for token,role in ROLE_SYNONYMS.items():
        if token in domain:
            return role
    if kw_pattern.search(text or ''):
        return 'Imobiliária'
    return 'Imobiliária'

def extract_email(text, domain):
    emails = list({e.lower() for e in email_pattern.findall(text or '')})
    for e in emails:
        dom = e.split('@',1)[1].lower()
        if dom == domain:
            return e
    # return clear mailtos/emails first
    for e in emails:
        if not any(bad in e for bad in ['sentry','example.com','email.com']):
            return e
    return ''

def clean_domain(s):
    s = s.lower().strip()
    s = urllib.parse.unquote(s)
    if '://' in s:
        s = s.split('://',1)[1]
    s = s.split('/',1)[0]
    if s.startswith('www.'):
        s=s[4:]
    return s

# ========== Candidate discovery via DuckDuckGo HTML ==========
all_leads = {}

def add_lead(dom, nome, source, role, cidade, url):
    if re.match(r'^(www\.)?(google|bing|yahoo|duckduckgo|youtube|facebook|instagram|twitter|x|linkedin|wikipedia|wikimedia|cache|maps|realtor|zillow|vivareal|zapimoveis|olx)\.', dom):
        return
    if dom in all_leads:
        return
    all_leads[dom] = {
        'nome': nome or '',
        'dominio': dom,
        'email_publico': '',
        'papel': role or 'Imobiliária',
        'cidade': cidade,
        'fonte': source,
        'observacao': 'Encontrado via busca pública',
        'url': url,
    }

# search each city+query on DuckDuckGo lite
for cidade, query_city in cities:
    queries = [
        f'imobiliaria {query_city}',
        f'corretor imoveis {query_city}',
        f'imobiliaria temporada {query_city}',
        f'construtora {query_city}',
    ]
    for q in queries:
        url = 'https://lite.duckduckgo.com/lite/?q=' + urllib.parse.quote(q)
        html = fetch(url)
        if not html:
            time.sleep(3)
            continue
        # links are typically in <a rel="nofollow" class="result-link" href="...">title</a> OR within table links
        links = []
        parser = LinkParser()
        parser.feed(html)
        # for DDG lite, hrefs may be like //duckduckgo.com/l/?uddg=<url>&...
        for h in parser.links:
            if 'uddg=' in h:
                target = h.split('uddg=',1)[1].split('&',1)[0]
            else:
                target = h
            target = urllib.parse.unquote(urllib.parse.unquote(target))
            # external targets often quoted + hex; leave as is
            dom = clean_domain(target)
            if not dom:
                continue
            # keep only likely realty sites by domain endings and known patterns
            if re.search(r'\.(com|com\.br|imobiliaria|imovel)$', dom):
                add_lead(dom, '', f'DuckDuckGo: {q}', '', cidade, target)
        time.sleep(1.5)
        print(f'  discovery {q}: {len(parser.links)} links')

print('Discovered domains:', len(all_leads))

# ========== Face validation + email extraction per homepage ==========
emailed = set()
for dom, lead in list(all_leads.items()):
    url = lead['url']
    html = fetch(url)
    if not html:
        html = fetch('http://' + dom)
        if html:
            lead['url'] = 'http://' + dom
    if not html:
        lead['observacao'] += '; Falhou ao acessar a homepage'
        continue
    text = extract_text(html)
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I|re.S)
    title = re.sub(r'\s+',' ', title_m.group(1)).strip() if title_m else ''
    lead['nome'] = title[:80] if title else texto_safe(text[:80])
    lead['papel'] = guess_role(title + ' ' + text, dom)
    mail = extract_email(text, dom)
    if mail:
        lead['email_publico'] = mail
        emailed.add(dom)
    time.sleep(0.7)

def texto_safe(s):
    s = re.sub(r'[^\w\s\-\.À-ÿ]', ' ', s, flags=re.UNICODE)
    return s.strip()

# ========== Second pass: common contact pages for missed domains ==========
contact_paths = ['/', '/contato', '/contato.php', '/contato.html', '/fale-conosco', '/fale-conosco.php', '/contatos', '/orcamento']
for dom, lead in list(all_leads.items()):
    if lead['email_publico']:
        continue
    base = lead['url']
    if not base.startswith('http'):
        continue
    base = base.rstrip('/')
    for path in contact_paths[:3]:
        test = base + path
        ct, b = fetch_bytes(test, timeout=12)
        if not b:
            continue
        try:
            txt = b.decode('utf-8', errors='ignore')
        except Exception:
            txt = b.decode('latin-1', errors='ignore')
        text = extract_text(txt)
        mail = extract_email(text, dom)
        if mail:
            lead['email_publico'] = mail
            break
        time.sleep(0.4)

# ========== Write CSV ==========
out_dir = r'C:\Users\Carolina\praia-digital'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'lead-nichos.csv')
fields = ['nome','dominio','email_publico','papel','cidade','fonte','observacao']
with open(out_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    for lead in all_leads.values():
        writer.writerow({k: lead.get(k,'') for k in fields})

print('Leads saved to', out_path)
print('Total leads:', len(all_leads))
print('Leads with email:', len(emailed))
