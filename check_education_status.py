import os
base='education/cursos'
cursos=[]
for name in sorted(os.listdir(base)):
    root=os.path.join(base,name)
    if not os.path.isdir(root):
        continue
    files=[f for r,_,fs in os.walk(root) for f in fs]
    has_ficha=any(f=='ficha-completa.md' for f in files)
    has_index=any(f=='index.html' for f in files)
    has_landing=any(f in ('vendas.html','landing.html','lp.html') for f in files)
    has_email=any(f.startswith('email') or f.startswith('sequencia') for f in files)
    has_instagram=any(f in ('posts.md','instagram.md','reels.md') for f in files)
    has_seo=any(f.startswith('seo') or f.startswith('artigo') for f in files)
    cursos.append((name,has_ficha,has_index,has_landing,has_email,has_instagram,has_seo))
print('Curso|ficha|index|landing|email|instagram|seo')
for c in cursos:
    print(c[0], '|', 'Y' if c[1] else 'N', '|', 'Y' if c[2] else 'N', '|', 'Y' if c[3] else 'N', '|', 'Y' if c[4] else 'N', '|', 'Y' if c[5] else 'N', '|', 'Y' if c[6] else 'N')
