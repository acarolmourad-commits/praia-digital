#!/usr/bin/env python3
"""Gerador + publicador automatico de carrosseis no Instagram (Praia Digital).
Roda 4x/dia via GitHub Actions. Escolhe tema rotativo da fila, gera artes 1080x1350,
commita as imagens no repo e publica via Instagram Graph API."""
import os, sys, json, time, datetime, subprocess, requests
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ['IG_ACCESS_TOKEN']
IG = os.environ['IG_USER_ID']
REPO = os.environ['GITHUB_REPOSITORY']
API = 'https://graph.facebook.com/v21.0'
RAW = f'https://raw.githubusercontent.com/{REPO}/main/social/auto'
W, H = 1080, 1350
DARK=(2,48,71); OCEAN=(0,119,182); LIGHT=(0,180,216); AMBER=(245,158,11); ACC=(144,224,239); WHITE=(255,255,255)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(sz, bold=True): return ImageFont.truetype(FB if bold else FR, sz)

def base():
    img = Image.new('RGB',(W,H)); px = img.load()
    for y in range(H):
        t=y/H
        if t<0.55: a,b,tt=DARK,OCEAN,t/0.55
        else: a,b,tt=OCEAN,LIGHT,(t-0.55)/0.45
        c=tuple(int(a[j]+(b[j]-a[j])*tt) for j in range(3))
        for x in range(W): px[x,y]=c
    return img

def wrap(d,text,f,maxw):
    lines=[]
    for para in text.split('\n'):
        words=para.split(); line=''
        for w in words:
            t=(line+' '+w).strip()
            if d.textlength(t,font=f)<=maxw: line=t
            else: lines.append(line); line=w
        lines.append(line)
    return lines

def slide(badge, blocks, idx, total):
    img=base(); d=ImageDraw.Draw(img)
    f=font(26); txt=badge.upper(); w=d.textlength(txt,font=f)
    d.rounded_rectangle([90,120,90+w+52,178],radius=29,fill=AMBER)
    d.text((116,134),txt,font=f,fill=DARK); y=218
    for kind,txt,sz,col in blocks:
        f=font(sz,bold=True)
        for ln in wrap(d,txt,f,W-180):
            d.text((90,y),ln,font=f,fill=col); y+=int(sz*1.28)
        y+=34
    d.text((90,H-100),'praia.digital',font=font(30),fill=WHITE)
    dots=' '.join('*' if i==idx else 'o' for i in range(total))
    d.text((W-90-d.textlength(dots,font=font(30)),H-102),dots,font=font(30),fill=WHITE)
    return img

def pick_topic():
    queue=json.load(open('scripts/ig_content_queue.json'))
    now=datetime.datetime.now(datetime.timezone.utc)
    slot=min(range(4), key=lambda i: abs(now.hour-[12,15,19,22][i]))
    idx=(now.toordinal()*4+slot)%len(queue)
    return queue[idx], idx

def run(cmd): subprocess.run(cmd,shell=True,check=True)

def api(method, url, **kw):
    r=requests.request(method,url,timeout=60,**kw)
    r.raise_for_status(); return r.json()

def main():
    topic,ti = pick_topic()
    tag=f"{datetime.date.today().isoformat()}-{ti}"
    blocks=[[('h',topic['title'],80,WHITE),('p','Arraste para ver  >>>',40,WHITE)]]
    for bdg,big,small in topic['slides']:
        blocks.append([('b',bdg.upper(),30,ACC),('h',big,88,AMBER),('p',small,38,WHITE)])
    blocks.append([('h','Link na bio',88,AMBER),('p','Saiba mais em praia.digital\nWhatsApp: (11) 95434-6288',38,WHITE)])
    total=len(blocks)
    os.makedirs('social/auto',exist_ok=True)
    files=[]
    for i,bl in enumerate(blocks):
        p=f'social/auto/{tag}-{i+1}.jpg'
        slide(topic['badge'], bl, i, total).save(p,'JPEG',quality=90)
        files.append(p)
    run('git config user.name "github-actions[bot]"')
    run('git config user.email "github-actions[bot]@users.noreply.github.com"')
    run(f'git add social/auto && git commit -m "social: artes {tag}" || echo nada-a-commitar')
    run('git push')
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
    sys.exit(main())
