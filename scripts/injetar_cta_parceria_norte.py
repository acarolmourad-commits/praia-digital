#!/usr/bin/env python3
"""
Expansao B — conecta o trafego SEO de norte as landings de parceria.
Injeta CTA de parceria no final dos artigos de norte do blog (idempotente).
Uso: python scripts/injetar_cta_parceria_norte.py [--dry]
"""
import glob, os, re

REPO = r"C:/Users/Carolina/praia-digital"
BLOG = os.path.join(REPO, "blog")
BASE = "https://acarolmourad-commits.github.io/praia-digital/parcerias-norte/parceria-{slug}.html"
NORTE = {
    "ubatuba": "ubatuba", "ilhabela": "ilhabela",
    "caraguatatuba": "caraguatatuba", "são sebastião": "sao-sebastiao",
}
MARK = "<!-- CTA-PARCEIRA-PRAIA-DIGITAL -->"

CTA = """
{MARK}
<div style="background:#0f2942;border:1px solid #1e3a5f;border-radius:12px;padding:1.2rem;margin:1.5rem 0;text-align:center">
  <h3 style="color:#22d3ee;margin:0 0 .4rem">🤝 Seja imobiliária parceira da Praia Digital em {cidade}</h3>
  <p style="color:#cbd5e1;font-size:.9rem;margin:0 0 .8rem">Levaremos proprietários qualificados pra você e cuidamos da gestão de temporada completa. Sem virar agência.</p>
  <a href="{url}" style="display:inline-block;background:linear-gradient(90deg,#22d3ee,#0ea5e9);color:#04141f;font-weight:800;padding:.7rem 1.3rem;border-radius:9px;text-decoration:none">Quero ser parceira em {cidade} →</a>
</div>
"""

def main(dry=False):
    feitos = 0
    for f in glob.glob(os.path.join(BLOG, "*.html")):
        txt = open(f, encoding="utf-8").read()
        lc = txt.lower()
        if MARK in txt:
            continue
        cid = None
        for k in NORTE:
            if k in lc:
                cid = k; break
        if not cid:
            continue
        slug = NORTE[cid]
        cidade = "São Sebastião" if slug == "sao-sebastiao" else slug.title()
        bloco = CTA.format(MARK=MARK, cidade=cidade, url=BASE.format(slug=slug))
        novo = txt.replace("</body>", bloco + "\n</body>", 1)
        if dry:
            print(f"[DRY] {os.path.basename(f)} -> {cidade}")
            feitos += 1
            continue
        open(f, "w", encoding="utf-8").write(novo)
        feitos += 1
    print(f"{'DRY: ' if dry else ''}{feitos} artigos de norte receberam CTA de parceria.")

if __name__ == "__main__":
    import sys
    main(dry="--dry" in sys.argv)
