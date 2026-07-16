#!/usr/bin/env python3
"""
Expansao B — Litoral Norte: gera LANDING PAGES de parceria B2B para Ubatuba,
Ilhabela e Caraguatatuba, convertendo o trafego de SEO ja existente (322 mencoes
no blog) em leads de imobiliarias locais.

Cada landing tem:
- SEO local (title/description com a cidade)
- Pitch de parceria Praia Digital (levamos proprietarios + gestao completa)
- Form de captura (nome imobiliaria, contato, whatsapp) -> POST futuro p/ tracker B2B

Reusa o template dos artigos de SEO (mesma estrutura HTML).
Uso: python scripts/gerar_landing_parceria_norte.py
"""
import os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
OUT = os.path.join(REPO, "parcerias-norte")
CIDADES = {
    "Ubatuba": "ubatuba", "Ilhabela": "ilhabela", "Caraguatatuba": "caraguatatuba",
    "São Sebastião": "sao-sebastiao",
}
TODAY = date.today().isoformat()

TPL = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Parceria Praia Digital em {cidade} — Imobiliárias e Construtoras</title>
<meta name="description" content="Seja imobiliária parceira da Praia Digital em {cidade}: trazemos proprietários qualificados e cuidamos da gestão de temporada completa. Sem virar agência.">
</head><body style="font-family:Arial,sans-serif;max-width:760px;margin:auto;padding:20px;color:#112">
<h1>Parceria Praia Digital em {cidade} 🤝</h1>
<p>Você já anuncia imóveis em {cidade} e sabe: lotar o calendário de temporada sem depender só de anúncio pago é o desafio. A Praia Digital resolve os dois lados:</p>
<ul>
<li><b>Trazemos proprietários</b> qualificados pelo nosso funil de aquisição (blog com 1.300+ artigos de SEO no litoral).</li>
<li><b>Cuidamos da Gestão Completa</b> + Precificação Dinâmica (ocupação e diária no talo).</li>
<li><b>Você foca em fechar</b> — a operação e os leads entram por nós. Parceria, não concorrência.</li>
</ul>
<h2>Quer ver um case real em {cidade}?</h2>
<form onsubmit="alert('Obrigado! Entraremos em contato via WhatsApp.');return false;">
<p>Imobiliária: <input name="imob" required style="width:100%;padding:.6rem"></p>
<p>Contato: <input name="nome" required style="width:100%;padding:.6rem"></p>
<p>WhatsApp: <input name="tel" required style="width:100%;padding:.6rem" placeholder="(12) 99999-9999"></p>
<button style="background:#0a3a6b;color:#fff;border:0;padding:.8rem 1.2rem;border-radius:8px">Quero ser parceira em {cidade}</button>
</form>
<p style="font-size:.8rem;color:#667">Praia Digital · Gestão de temporada no litoral de SP · {data}</p>
</body></html>"""

def main():
    os.makedirs(OUT, exist_ok=True)
    for cidade, slug in CIDADES.items():
        path = os.path.join(OUT, f"parceria-{slug}.html")
        open(path, "w", encoding="utf-8").write(
            TPL.format(cidade=cidade, data=TODAY))
        print(f"Landing: {path}")
    print(f"\n{len(CIDADES)} landings de parceria norte geradas em {OUT}")

if __name__ == "__main__":
    main()
