#!/usr/bin/env python3
from pathlib import Path

def replace_once(path, old, new):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly 1 anchor, found {count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")

partner = '  <p class="lead" style="margin-top:22px">Rede parceira: quem vive o litoral também surfa. Conheça os <a href="/apps/#apps-asf-parceiro">apps da ASF — Associação de Surf Feminino</a> (quiz do surf, prancha ideal, trip planner e mais), interligados à rede Praia Digital.</p>\n'
home = Path("index.html").read_text(encoding="utf-8")
if "Rede parceira: quem vive" not in home:
    start = home.find('<section id="jornadas-apps"')
    if start < 0:
        raise SystemExit("index.html: jornadas-apps section not found")
    end = home.find('</section>', start)
    if end < 0:
        raise SystemExit("index.html: jornadas-apps close not found")
    Path("index.html").write_text(home[:end] + partner + home[end:], encoding="utf-8")

nav = '<nav class="rede-nav" aria-label="Redes Praia Digital e parceiros" style="text-align:center;padding:10px 16px"><a href="/">Praia Digital</a> &middot; <a href="/apps/">Apps Praia Digital</a> &middot; <a href="https://acarolmourad-commits.github.io/asf-app/apps/" target="_blank" rel="noopener">Apps ASF (parceiro)</a></nav>\n'
apps = Path("apps/index.html").read_text(encoding="utf-8")
if '<nav class="rede-nav"' not in apps:
    replace_once("apps/index.html", '<div class="wrap">', nav + '<div class="wrap" id="apps-praia-digital">')
apps = Path("apps/index.html").read_text(encoding="utf-8")
if 'id="apps-asf-parceiro"' not in apps:
    replace_once("apps/index.html", '<a class="card" href="https://acarolmourad-commits.github.io/asf-app/apps/"', '<a class="card" id="apps-asf-parceiro" href="https://acarolmourad-commits.github.io/asf-app/apps/"')

for path, markers in {
    "index.html": ["Rede parceira: quem vive", 'id="jornadas-apps"'],
    "apps/index.html": ['<nav class="rede-nav"', 'id="apps-praia-digital"', 'id="apps-asf-parceiro"'],
}.items():
    text = Path(path).read_text(encoding="utf-8")
    for marker in markers:
        if text.count(marker) != 1:
            raise SystemExit(f"{path}: marker {marker!r} count={text.count(marker)}")
    if text.count("<h1") != 1:
        raise SystemExit(f"{path}: expected exactly one h1")
print("apps-network crosslink applied and validated")
