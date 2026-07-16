#!/usr/bin/env python3
"""
Expansao D — Funil B2C Norte: conecta o trafego SEO de DONOS de imovel no Litoral Norte
a calculadora standalone (captura de proprietario B2C). Injeta CTA idempotente nos
artigos de norte com intencao B2C forte (proprietario/renda/temporada/investir).

Reusa o assets/calculadora-widget-standalone.html (tenant via ?tenant=).
Lead vai para o tracker B2C geral (outbound ja existente).
Uso: python scripts/injetar_cta_b2c_norte.py [--dry]
"""
import glob, os, re

REPO = r"C:/Users/Carolina/praia-digital"
BLOG = os.path.join(REPO, "blog")
DONO = "https://acarolmourad-commits.github.io/praia-digital/dono-norte/dono-{slug}.html"
CALC = "https://acarolmourad-commits.github.io/praia-digital/assets/calculadora-widget-standalone.html?tenant=pd-norte"
NORTE = {"ubatuba": "ubatuba", "ilhabela": "ilhabela",
         "caraguatatuba": "caraguatatuba", "são sebastião": "sao-sebastiao"}
MARK = "<!-- CTA-B2C-PRAIA-DIGITAL-NORTE -->"
B2C = re.compile(r"\b(propriet|ario|dono|seu imo|alugar|renda|rendimento|invest|temporada|diaria)\b", re.I)

CTA = """
{MARK}
<div style="background:linear-gradient(135deg,#0a3a6b,#063a5a);border:1px solid #1e3a5f;border-radius:12px;padding:1.3rem;margin:1.5rem 0;text-align:center">
  <h3 style="color:#4ade80;margin:0 0 .4rem">📈 Descubra quanto seu imóvel rende em {cidade}</h3>
  <p style="color:#cbd5e1;font-size:.9rem;margin:0 0 .8rem">Simule o yield de temporada da sua casa em {cidade} e saiba como a Praia Digital cuida de TUDO (limpeza, check-in, precificação) enquanto você ganha mais trabalhando zero horas.</p>
  <a href="{url}" style="display:inline-block;background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:800;padding:.7rem 1.3rem;border-radius:9px;text-decoration:none">Simular meu yield em {cidade} →</a>
</div>
"""

def main(dry=False):
    feitos = 0
    for f in glob.glob(os.path.join(BLOG, "*.html")):
        txt = open(f, encoding="utf-8").read()
        if MARK in txt:
            continue
        lc = txt.lower()
        cid = None
        for k in NORTE:
            if k in lc:
                cid = k; break
        if not cid:
            continue
        # so artigos com intencao B2C forte
        if len(B2C.findall(txt)) < 3:
            continue
        cidade = "São Sebastião" if NORTE[cid] == "sao-sebastiao" else NORTE[cid].title()
        bloco = CTA.format(MARK=MARK, cidade=cidade, url=DONO.format(slug=NORTE[cid]))
        if dry:
            print(f"[DRY] {os.path.basename(f)} -> {cidade}")
            feitos += 1
            continue
        open(f, "w", encoding="utf-8").write(txt.replace("</body>", bloco + "\n</body>", 1))
        feitos += 1
    print(f"{'DRY: ' if dry else ''}{feitos} artigos B2C de norte receberam CTA de simulacao.")

if __name__ == "__main__":
    import sys
    main(dry="--dry" in sys.argv)
