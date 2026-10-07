#!/usr/bin/env python3
"""Gerador + publicador automatico de carrosseis no Instagram (Praia Digital).
Design v2: capa centralizada, cards coloridos com acento rotativo, CTA final.
Roda 4x/dia via GitHub Actions (7h, 9h, 15h, 20h BRT). Escolhe tema rotativo da fila,
gera artes 1080x1350, commita as imagens no repo e publica via Instagram Graph API."""
import os, sys, json, time, datetime, subprocess, requests
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ.get('IG_ACCESS_TOKEN','')
IG = os.environ.get('IG_USER_ID','')
REPO = os.environ.get('GITHUB_REPOSITORY', 'acarolmourad-commits/praia-digital')
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

def normalize_slide(slide):
    if not isinstance(slide, (list, tuple)) or len(slide) not in (3, 4):
        raise ValueError('Each slide must contain 3 or 4 text fields')
    if not all(isinstance(value, str) and value.strip() for value in slide):
        raise ValueError('Slide fields must be non-empty strings')
    kicker, big, small = slide[:3]
    if len(slide) == 4:
        small = small + '\n' + slide[3]
    return kicker, big, small


def validate_queue(queue):
    if not isinstance(queue, list) or not queue:
        raise ValueError('Content queue must be a non-empty list')
    ids = set()
    for topic in queue:
        if not isinstance(topic, dict):
            raise ValueError('Each topic must be an object')
        for key in ('id', 'badge', 'title', 'caption'):
            if not isinstance(topic.get(key), str) or not topic[key].strip():
                raise ValueError('Missing or invalid topic field: ' + key)
        if topic['id'] in ids:
            raise ValueError('Duplicate topic id: ' + topic['id'])
        ids.add(topic['id'])
        slides = topic.get('slides')
        if not isinstance(slides, list) or not 1 <= len(slides) <= 8:
            raise ValueError('Topic must have 1 to 8 slides, plus cover and CTA')
        for slide in slides:
            normalize_slide(slide)
    return queue


def pick_topic():
    with open('scripts/ig_content_queue.json', encoding='utf-8') as handle:
        queue = validate_queue(json.load(handle))
    now=datetime.datetime.now(datetime.timezone.utc)
    slot=min(range(4), key=lambda i: abs(now.hour-SLOTS_UTC[i]))
    idx=(now.toordinal()*4+slot)%len(queue)
    return queue[idx], idx

def run(cmd): subprocess.run(cmd,shell=True,check=True)

def api(method, url, **kw):
    r=requests.request(method,url,timeout=60,**kw)
    r.raise_for_status(); return r.json()

def main(dry_run=False):
    topic,ti = pick_topic()
    tag=f"{datetime.date.today().isoformat()}-{ti}"
    slides=[cover(topic['badge'],topic['title'])]
    for i, slide in enumerate(topic['slides']):
        kicker, big, small = normalize_slide(slide)
        slides.append(card(kicker,big,small,PALETTE[i%len(PALETTE)]))
    slides.append(cta())
    total=len(slides)
    output_dir = 'social/dry-run' if dry_run else 'social/auto'
    os.makedirs(output_dir, exist_ok=True)
    files=[]
    for i,img in enumerate(slides):
        # indicador de progresso
        d=ImageDraw.Draw(img)
        dots=' '.join('*' if j==i else 'o' for j in range(total))
        ctext(d,H-70,dots,font(26),WHITE)
        p=f'{output_dir}/{tag}-{i+1}.jpg'
        img.save(p,'JPEG',quality=92); files.append(p)
    if dry_run:
        print('DRY RUN: local images generated; no git or Instagram calls.')
        return
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
        time.sleep(5)
    pub=api('POST',f'{API}/{IG}/media_publish',data={'creation_id':parent,'access_token':TOKEN})
    print('PUBLICADO:', pub)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Generate local previews without git or Instagram calls')
    args = parser.parse_args()
    sys.exit(main(dry_run=args.dry_run))
