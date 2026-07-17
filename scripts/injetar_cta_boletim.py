#!/usr/bin/env python3
"""
Injeta CTA do Boletim Diario nos artigos do blog (retencao + cross-link SEO).
Idempotente. Link: arquivo de boletins + boletim corrente.
Uso: python scripts/injetar_cta_boletim.py [--dry]
"""
import os, glob
REPO = r"C:/Users/Carolina/praia-digital"
BLOG = os.path.join(REPO, "blog")
BOLETIM = "https://acarolmourad-commits.github.io/praia-digital/docs/inteligencia/boletim-diario.html"
MARK = "<!-- CTA-BOLETIM-PRAIA-DIGITAL -->"
CTA = f"""
{MARK}
<div style="background:linear-gradient(135deg,#0a3a6b,#063a5a);border:1px solid #1e3a5f;border-radius:12px;padding:1.2rem;margin:1.5rem 0;text-align:center">
  <h3 style="color:#4ade80;margin:0 0 .4rem">📡 Boletim Diário de Inteligência</h3>
  <p style="color:#cbd5e1;font-size:.9rem;margin:0 0 .8rem">Receba toda manhã o ranking das cidades, tendências e oportunidades do litoral paulista.</p>
  <a href="{BOLETIM}" style="display:inline-block;background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:800;padding:.7rem 1.3rem;border-radius:9px;text-decoration:none">Ler boletim de hoje →</a>
</div>
"""

def main(dry=False):
    n=0
    for f in glob.glob(os.path.join(BLOG,"*.html")):
        t=open(f,encoding="utf-8").read()
        if MARK in t: continue
        if dry: print(f"[DRY] {os.path.basename(f)}"); n+=1; continue
        open(f,"w",encoding="utf-8").write(t.replace("</body>", CTA+"\n</body>",1)); n+=1
    print(f"{'DRY: ' if dry else ''}{n} artigos receberam CTA do boletim.")

if __name__=="__main__":
    import sys
    main(dry="--dry" in sys.argv)
