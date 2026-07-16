#!/usr/bin/env python3
"""
Expansao F — Injetar CTA de QUIZ de perfil de dono nos artigos B2C (norte + sul/centro).
Quiz client-side (sem backend): assets/quiz-perfil-dono.html.
CTA: bloco antes de </body> apontando para o quiz. Idempotente.
Uso: python scripts/injetar_cta_quiz_dono.py [--dry]
"""
import os, glob, re

REPO = r"C:/Users/Carolina/praia-digital"
BLOG = os.path.join(REPO, "blog")
QUIZ = "https://acarolmourad-commits.github.io/praia-digital/assets/quiz-perfil-dono.html"
MARK = "<!-- CTA-QUIZ-PERFIL-DONO-PRAIA-DIGITAL -->"
B2C = re.compile(r"\b(propriet|ario|dono|seu imo|alugar|renda|rendimento|invest|temporada|diaria|anunci)\b", re.I)

CTA = """
{MARK}
<div style="background:linear-gradient(135deg,#1e3a8a,#0a3a6b);border:1px solid #1e3a5f;border-radius:12px;padding:1.3rem;margin:1.5rem 0;text-align:center">
  <h3 style="color:#4ade80;margin:0 0 .4rem">🧭 Qual seu perfil de dono de temporada?</h3>
  <p style="color:#cbd5e1;font-size:.9rem;margin:0 0 .8rem">3 perguntas, 30 segundos: descubra como ganhar mais sem trabalhar. No fim, falamos com você no WhatsApp.</p>
  <a href="{url}" style="display:inline-block;background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:800;padding:.7rem 1.3rem;border-radius:9px;text-decoration:none">Fazer o quiz grátis →</a>
</div>
"""

def main(dry=False):
    n=0
    for f in glob.glob(os.path.join(BLOG,"*.html")):
        t=open(f,encoding="utf-8").read()
        if MARK in t: continue
        if len(B2C.findall(t)) < 2: continue
        if dry:
            print(f"[DRY] {os.path.basename(f)}"); n+=1; continue
        open(f,"w",encoding="utf-8").write(t.replace("</body>", CTA.format(MARK=MARK, url=QUIZ)+"\n</body>",1))
        n+=1
    print(f"{'DRY: ' if dry else ''}{n} artigos B2C receberam CTA de quiz de perfil.")

if __name__=="__main__":
    import sys
    main(dry="--dry" in sys.argv)
