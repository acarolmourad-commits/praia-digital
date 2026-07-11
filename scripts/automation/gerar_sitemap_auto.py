#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador automático de sitemap.xml para indexação no Google.
Inclui páginas principais, blog, imóveis, landing pages e docs.
"""
import os
from datetime import datetime
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE)
OUT = os.path.join(ROOT, "sitemap.xml")

URLS = [
    ("/", "1.0", "daily"),
    ("/index.html", "1.0", "daily"),
    ("/landing-parcerias-anuncios.html", "0.8", "weekly"),
    ("/landing-parcerias-captura-praia-digital-2026.html", "0.8", "weekly"),
    ("/landing-parcerias-conversao-praia-digital-2026.html", "0.8", "weekly"),
    ("/landing-parcerias-captura-praia-digital-conversao-2026.html", "0.8", "weekly"),
    ("/newsletter/assinatura.html", "0.6", "weekly"),
    ("/newsletter/edicao-001.html", "0.6", "weekly"),
    ("/assets/contadores-publicos-praia-digital.html", "0.5", "weekly"),
    ("/assets/planos-assinatura.html", "0.8", "weekly"),
    ("/lgpd-imobiliarias-litoral-2026.html", "0.5", "monthly"),
    ("/checklist-investidor-imoveis-litoral.html", "0.6", "weekly"),
]

FOLDERS = ["blog", "imoveis", "docs/sales", "docs/materiais"]
EXTENSIONS = {".html", ".htm"}

today = datetime.now().strftime("%Y-%m-%d")


def iter_files():
    seen = set()
    for folder in FOLDERS:
        fpath = os.path.join(ROOT, folder)
        if not os.path.isdir(fpath):
            continue
        for dirpath, dirnames, filenames in os.walk(fpath):
            for fn in filenames:
                if os.path.splitext(fn)[1].lower() not in EXTENSIONS:
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                if rel in seen:
                    continue
                seen.add(rel)
                st = os.stat(full)
                mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d")
                yield rel, mtime


def build():
    default_changefreq = "daily"
    entries = [(rel, mtime, freq) for rel, freq, mtime in URLS]
    for rel, mtime in iter_files():
        entries.append((rel, mtime, default_changefreq))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for rel, mtime, freq in entries:
        xml.append("  <url>")
        xml.append(f"    <loc>{escape('https://acarolmourad-commits.github.io/praia-digital{0}'.format(rel))}</loc>")
        xml.append(f"    <lastmod>{mtime}</lastmod>")
        xml.append(f"    <changefreq>{freq}</changefreq>")
        xml.append("  </url>")
    xml.append("</urlset>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    print(f"Sitemap gerado: {OUT}")
    print(f"URLs incluídas: {len(entries)}")


if __name__ == "__main__":
    build()
