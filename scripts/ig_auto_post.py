#!/usr/bin/env python3
"""Gerador + publicador automatico de carrosseis no Instagram (Praia Digital).
Design v2: capa centralizada, cards coloridos com acento rotativo, CTA final.
Roda 4x/dia via GitHub Actions (7h, 9h, 15h, 20h BRT). Escolhe tema rotativo da fila,
gera artes 1080x1350, commita as imagens no repo e publica via Instagram Graph API."""
import argparse, os, sys, json, time, datetime, subprocess, requests
try:
    from .ig_content_validation import validate_queue
except ImportError:
    from ig_content_validation import validate_queue
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ.get('IG_ACCESS_TOKEN','')
IG = os.environ.get('IG_USER_ID','')
REPO = os.environ.get('GITHUB_REPOSITORY', '')
API = 'https://graph.facebook.com/v21.0'
RAW = f'https://raw.githubusercontent.com/{REPO}/main/social/auto'
SLOTS_UTC = [10, 12, 18, 23]  # 7h, 9h, 15h, 20h em Brasilia (UTC-3)
W, H = 1080, 1350
BG1=(15,23,42); BG2=(30,58,95)
PALETTE=[(34,211,238),(52,211,153),(251,191,36),(248,113,113),(167,139,250),(96,165,250)]
WHITE=(255,255,255); MUTED=(148,163,184)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(sz, bold=True): return ImageFont.truetype(FB if bold else FR, sz)

def gradient(top, bottom):
    img = Image.new('RGB',(W,H)); px = img.load()
    for y in range(H):
        t=y/H
        c=tuple(int(top[j]+(bottom[j]-top[j])*t) for j in range(3))
        for x in range(W): px[x,y]=c
    return img

def ctext(d, y, txt, f, fill=WHITE):
    w=d.textlength(txt,font=f); d.text(((W-w)/2,y),txt,font=f,fill=fill)

def wrap_center(d, text, f, y, maxw, fill=WHITE, lh=1.28):
    """Quebra o texto e centraliza cada linha; retorna o y final."""
    for para in text.split('\n'):
        words=para.split(); line=''
        for w_ in words:
            t=(line+' '+w_).strip()
            if d.textlength(t,font=f)<=maxw: line=t
            else:
                ctext(d,y,line,f,fill); y+=int(f.size*lh); line=w_
        ctext(d,y,line,f,fill); y+=int(f.size*lh)
    return y

def pill(d, y, txt, fill_pill, fill_txt, sz=30):
    f=font(sz); w=d.textlength(txt.upper(),font=f)
    d.rounded_rectangle([(W-w-52)/2,y,(W+w+52)/2,y+sz+36],radius=(sz+36)//2,fill=fill_pill)
    ctext(d,y+18,txt.upper(),f,fill_txt)

def cover(badge, title):
    img=gradient(BG1,BG2); d=ImageDraw.Draw(img)
    pill(d,400,badge,(251,191,36),BG1)
    y=wrap_center(d,title,font(72),540,W-160)
    ctext(d,y+40,'Arraste para ver  >>>',font(30,False),MUTED)
    ctext(d,1250,'praia.digital',font(36),PALETTE[0])
    return img

def card(kicker, big, small, accent):
    img=gradient(BG1,BG2); d=ImageDraw.Draw(img)
    pill(d,300,kicker,accent,BG1)
    y=wrap_center(d,big,font(76),440,W-160)
    wrap_center(d,small,font(34,False),y+50,W-200,MUTED)
    ctext(d,1250,'praia.digital',font(32),PALETTE[0])
    return img

def cta():
    img=gradient(BG2,(13,84,102)); d=ImageDraw.Draw(img)
    ctext(d,420,'Gostou?',font(72))
    ctext(d,520,'Saiba mais no site',font(48))
    d.rounded_rectangle([240,680,840,770],radius=45,fill=PALETTE[1])
    ctext(d,700,'LINK NA BIO',font(44),BG1)
    ctext(d,860,'WhatsApp: (11) 95434-6288',font(34,False),WHITE)
    ctext(d,930,'praia.digital',font(40),PALETTE[2])
    ctext(d,1150,'Imoveis • Dados • IA para corretores',font(28,False),MUTED)
    return img

def pick_topic(queue):
    now=datetime.datetime.now(datetime.timezone.utc)
    slot=min(range(4), key=lambda i: abs(now.hour-SLOTS_UTC[i]))
    idx=(now.toordinal()*4+slot)%len(queue)
    return queue[idx], idx

def run(cmd): subprocess.run(cmd,shell=True,check=True)

def api(method, url, **kw):
    r=requests.request(method,url,timeout=60,**kw)
    r.raise_for_status(); return r.json()

def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate and publish Instagram content")
    parser.add_argument('--queue', default='scripts/ig_content_queue.json')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate all content only: no images, writes, git or API')
    args = parser.parse_args(argv)
    with open(args.queue, encoding='utf-8') as source:
        queue = validate_queue(json.load(source))
    if args.dry_run:
        print(f"DRY-RUN OK: {len(queue)} topics, {sum(len(t['slides']) for t in queue)} slides; no side effects")
        return 0
    if not TOKEN or not IG or not REPO:
        raise ValueError('IG_ACCESS_TOKEN, IG_USER_ID and GITHUB_REPOSITORY are required before any side effects')
    topic,ti = pick_topic(queue)
    tag=f"{datetime.date.today().isoformat()}-{ti}"
    slides=[cover(topic['badge'],topic['title'])]
    for i,(kicker,big,small) in enumerate(topic['slides']):
        slides.append(card(kicker,big,small,PALETTE[i%len(PALETTE)]))
    slides.append(cta())
    total=len(slides)
    os.makedirs('social/auto',exist_ok=True)
    files=[]
    for i,img in enumerate(slides):
        # indicador de progresso
        d=ImageDraw.Draw(img)
        dots=' '.join('*' if j==i else 'o' for j in range(total))
        ctext(d,H-70,dots,font(26),WHITE)
        p=f'social/auto/{tag}-{i+1}.jpg'
        img.save(p,'JPEG',quality=92); files.append(p)
    run('git config user.name "github-actions[bot]"')
    run('git config user.email "github-actions[bot]@users.noreply.github.com"')
    run(f'git add social/auto && git commit -m "social: artes {tag}" || echo nada-a-commitar')
    run('git push')
    if not TOKEN or not IG:
        print('AVISO: IG_ACCESS_TOKEN/IG_USER_ID nao configurados - artes geradas e commitadas; publicacao pulada.')
        return
    time.sleep(20)
    urls=[f'{RAW}/{os.path.basename(p)}' for p in files]
    children=[]
    for u in urls:
        c=api('POST',f'{API}/{IG}/media',data={'image_url':u,'is_carousel_item':'true','access_token':TOKEN})
        children.append(c['id']); time.sleep(3)
    parent=api('POST',f'{API}/{IG}/media',data={'media_type':'CAROUSEL','children':','.join(children),'caption':topic['caption'],'access_token':TOKEN})['id']
    for _ in range(20):
        st=api('GET',f'{API}/{parent}?fields=status_code&access_token={TOKEN}').get('status_code')
        if st=='FINISHED': break
        if st in ('ERROR', 'EXPIRED'):
            raise RuntimeError('Instagram carousel processing failed; publication cancelled')
        time.sleep(5)
    else:
        raise RuntimeError('Instagram carousel did not finish; publication cancelled')
    pub=api('POST',f'{API}/{IG}/media_publish',data={'creation_id':parent,'access_token':TOKEN})
    print('PUBLICADO:', pub)

if __name__=='__main__':
    sys.exit(main())
