#!/usr/bin/env python3
"""Praia Digital 2026-10-23: padroniza a rede de apps e corrige links quebrados conhecidos (issue #34).

Idempotente. Altera apenas:
- index.html e apps/index.html: /apps/<slug>/index.html -> /apps/<slug>/
- apps/index.html: insere a secao 'Use a rede em sequencia' (pd-network-journey), uma unica vez
- politica-editorial.html: /cidades.html -> /cidades/index.html (destino existente)
- servicos-ia.html e obrigado-segmentado.html: bairros/santos-gonzaga.html -> bairros/santos/gonzaga.html (destino existente)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_LINK = re.compile(r"(/apps/[a-z0-9\-]+)/index\.html")

JOURNEY = """<section class="pd-network-journey" style="max-width:880px;margin:0 auto;padding:8px 16px 28px">
<h2 style="font-size:1.25rem;margin:0 0 8px">Use a rede em sequencia</h2>
<p style="color:#475569;line-height:1.55;margin:0 0 12px">Os apps da Praia Digital foram feitos para se conectar: compare o destino, estime o valor, simule a rentabilidade e feche com a vistoria. Voce tambem pode entrar direto na sua etapa.</p>
<ol style="line-height:1.9;color:#0F172A;padding-left:20px">
<li><a href="/apps/comparador-cidades/">Comparador de Cidades</a> - escolha onde comprar ou investir</li>
<li><a href="/apps/valor-imovel/">Valor do Imovel</a> - estime o preco de mercado</li>
<li><a href="/apps/simulador-roi-temporada/">Simulador de ROI de Temporada</a> e <a href="/apps/temporada-ou-anual/">Temporada ou Anual</a> - compare rentabilidade</li>
<li><a href="/apps/calculadora-financiamento/">Calculadora de Financiamento</a> e <a href="/apps/planejador-entrada/">Planejador de Entrada</a> - viabilize a compra</li>
<li><a href="/apps/checklist-vistoria/">Checklist de Vistoria</a> - feche sem esquecer itens</li>
</ol>
<p style="line-height:1.6"><a href="/">Voltar para a Praia Digital</a> | <a href="/servicos.html">Servicos para proprietarios e imobiliarias</a> | <a href="/contato.html">Falar com a Praia Digital</a></p>
</section>
"""


def patch(path, transforms):
    p = ROOT / path
    if not p.exists():
        print(f"SKIP missing {path}")
        return 0
    text = p.read_text(encoding="utf-8", errors="ignore")
    original = text
    total = 0
    for fn in transforms:
        text, n = fn(text)
        total += n
    if text != original:
        p.write_text(text, encoding="utf-8")
    print(f"{path}: {total} substituicao(oes)")
    return total


def app_links(text):
    return APP_LINK.subn(r"\1/", text)


def cidades(text):
    return text.replace("/cidades.html", "/cidades/index.html"), text.count("/cidades.html")


def gonzaga(text):
    old = "bairros/santos-gonzaga.html"
    return text.replace(old, "bairros/santos/gonzaga.html"), text.count(old)


def journey(text):
    if "pd-network-journey" in text:
        return text, 0
    if "<footer" in text:
        return text.replace("<footer", JOURNEY + "<footer", 1), 1
    return text, 0


def main():
    total = 0
    total += patch("index.html", [app_links])
    total += patch("apps/index.html", [app_links, journey])
    total += patch("politica-editorial.html", [cidades])
    total += patch("servicos-ia.html", [gonzaga])
    total += patch("obrigado-segmentado.html", [gonzaga])
    print(f"TOTAL: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
