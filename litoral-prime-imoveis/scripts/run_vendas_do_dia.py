"""
Litoral Prime — runner do dia: gera extrato pronto para ação e atualiza sitemap.xml + social meta.
Saídas:
  outreach/do-dia/<data>/contatos.csv
  outreach/do-dia/<data>/reengajamentos.csv
  outreach/do-dia/<data>/ofertas.csv
  sitemap.xml atualizado automaticamente
  meta social atualizada nas páginas de cidades
"""
from pathlib import Path
import csv, datetime, os, re

from cross_sell import generate_cross_sell

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "outreach" / "do-dia" / datetime.date.today().isoformat()
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SANITIZED = BASE / "outreach" / "lote-001-sanitizado.csv"
LOTES_Prontos_DIR = BASE / "outreach" / "lotes-prontos"


def find_default_sanitized() -> Path:
    if DEFAULT_SANITIZED.exists():
        return DEFAULT_SANITIZED
    candidates = list(LOTES_Prontos_DIR.glob("*-sanitizado.csv")) if LOTES_Prontos_DIR.exists() else []
    if not candidates:
        raise SystemExit("Nenhum lote sanitizado encontrado. Rode sanitizar_todos_lotes.py primeiro.")
    best = max(candidates, key=lambda p: p.stat().st_size)
    return best


SANITIZED = find_default_sanitized()

STAGE_MESSAGES = {
    "primeiro_contato": lambda r: f"Olá, {r['nome']}! Tudo bem? Vi que você tem interesse em {r['tipo_interesse'].lower()} na região de {r['cidade_interesse']}. Quer que eu envie 3 opções compatíveis com o seu perfil?",
    "reengajamento": lambda r: f"Olá, {r['nome']}! Lembrete rápido: a Litoral Prime Imóveis tem novas opções no litoral de SP. Quer que eu envie as melhores oportunidades desta semana?",
    "oferta": lambda r: f"{r['nome']}, selecionei {r['tipo_interesse'].lower()}s exclusivos em {r['cidade_interesse']}. Se quiser, envio a pré-seleção agora por aqui.",
}


def find_html_files():
    paths = []
    for root, dirs, files in os.walk(BASE):
        for f in files:
            if f.endswith(".html"):
                paths.append(Path(root) / f)
    return paths


def url_from_path(base: Path, path: Path):
    rel = path.relative_to(base).as_posix()
    return f"https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/{rel}"


def update_sitemap():
    html_files = find_html_files()
    entries = []
    for p in html_files:
        loc = url_from_path(BASE, p)
        if "cidades/" in loc:
            prio = "0.8"
            cf = "weekly"
        elif p.name in ["index.html"]:
            prio = "1.0"
            cf = "daily"
        else:
            prio = "0.9"
            cf = "weekly"
        lastmod = datetime.date.today().isoformat()
        entries.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{prio}</priority>\n    <changefreq>{cf}</changefreq>\n  </url>"
        )
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
    sitemap = BASE / "sitemap.xml"
    sitemap.write_text(xml, encoding="utf-8")
    print(f"Sitemap atualizado: {sitemap} ({len(entries)} URLs)")


def read_daily_counts():
  counts = {}
  ready = OUT_DIR / "pronto-disparo.csv"
  if not ready.exists():
    return counts
  try:
    with ready.open("r", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        city = (row.get("cidade_interesse") or "").strip()
        if not city:
          continue
        counts[city] = counts.get(city, 0) + 1
  except Exception:
    return counts
  return counts


def build_momentum_section(counts, date_str="hoje"):
  cities = ["Santos","Guarujá","Praia Grande","São Vicente","Bertioga","Itanhaém","Mongaguá","Peruíbe"]
  cards = []
  for city in cities:
    n = counts.get(city, 0)
    if n > 0:
      label = city + ": " + str(n) + " contatos qualificados"
    else:
      label = city + ": sem movimentação"
    cards.append("        <article class=\"servico-card\"><h3>" + city + "</h3><p>" + label + "</p></article>")
  return "    <section class=\"servicos-section\">\n      <h2>Momentum do dia</h2>\n      <p class=\"subtitle\">Atividade de contatos qualificados por cidade no dia.</p>\n      <p class=\"subtitle\" style=\"margin-top:6px;color:#64748b\">Atualizado em " + date_str + "</p>\n      <div class=\"servicos-grid\">\n" + "\n".join(cards) + "\n      </div>\n    </section>"


def replace_section(txt: str, h2: str, new_section_html: str):
    start = txt.find("<h2>" + h2 + "</h2>")
    if start == -1:
        return txt, False
    section_start = txt.rfind("<section", 0, start)
    if section_start == -1:
        return txt, False
    section_end = txt.find("</section>", start)
    if section_end == -1:
        return txt, False
    section_end += len("</section>")
    new_txt = txt[:section_start] + new_section_html + txt[section_end:]
    return new_txt, True


def update_momentum_on_page(path: Path, date_str="hoje"):
    if not path.exists():
        return False
    counts = read_daily_counts()
    section_html = build_momentum_section(counts, date_str)
    txt = path.read_text(encoding="utf-8")
    new_txt, updated = replace_section(txt, "Momentum do dia", section_html)
    if updated and new_txt != txt:
        path.write_text(new_txt, encoding="utf-8")
        return True
    return False


def update_all_pages_momentum():
    date_str = datetime.date.today().isoformat()
    pages = [
        BASE / "index.html",
        BASE / "imoveis.html",
        BASE / "servicos.html",
        BASE / "encontrar-imovel.html",
    ]
    updated_any = False
    for page in pages:
        if update_momentum_on_page(page, date_str):
            print("Momentum atualizado em", page.name)
            updated_any = True
    return updated_any


def update_social_meta():
    DEFAULT_IMAGE = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=60"

    city_title_map = {
        "santos": "Imóveis em Santos — Litoral Prime Imóveis",
        "guaruja": "Imóveis no Guarujá — Litoral Prime Imóveis",
        "praia-grande": "Imóveis em Praia Grande — Litoral Prime Imóveis",
        "bertioga": "Imóveis em Bertioga — Litoral Prime Imóveis",
        "itanhaem": "Imóveis em Itanhaém — Litoral Prime Imóveis",
        "mongagua": "Imóveis em Mongaguá — Litoral Prime Imóveis",
        "sao-vicente": "Imóveis em São Vicente — Litoral Prime Imóveis",
        "peruibe": "Imóveis em Peruíbe — Litoral Prime Imóveis",
    }
    city_desc_map = {
        "santos": "Apartamentos, casas e coberturas em Santos. Oportunidades exclusivas no litoral de SP.",
        "guaruja": "Imóveis no Guarujá para temporada ou moradia. Casas, apartamentos e lançamentos.",
        "praia-grande": "Studios, casas e lançamentos em Praia Grande com entrada facilitada.",
        "bertioga": "Imóveis de alto padrão em Bertioga, com condomínios fechados e lazer completo.",
        "itanhaem": "Casas e imóveis perto da praia em Itanhaém com alto potencial de valorização.",
        "mongagua": "Apartamentos compactos em Mongaguá com ótimo custo-benefício.",
        "sao-vicente": "Coberturas e apartamentos com vista mar em São Vicente.",
        "peruibe": "Imóveis em Peruíbe: tranquilidade, lazer e contato direto pelo WhatsApp.",
    }

    def normalize_city_key(path: Path):
        raw = path.name.lower()
        mapping = {
            "sao-vicente.html": "sao-vicente",
            "itanhaem.html": "itanhaem",
            "mongagua.html": "mongagua",
            "praia-grande.html": "praia-grande",
            "peruibe.html": "peruibe",
            "santos.html": "santos",
            "guaruja.html": "guaruja",
            "bertioga.html": "bertioga",
        }
        if raw in mapping:
            return mapping[raw]
        return raw.replace(".html", "")

    def inject_once(path: Path):
        key = normalize_city_key(path)
        title = city_title_map.get(key)
        desc = city_desc_map.get(key)
        loc = url_from_path(BASE, path)
        if not title or not desc:
            return

        html = path.read_text(encoding="utf-8")
        if '<meta property="og:type" content="website">' in html:
            return

        first_title = re.search(r"<title>.*?</title>", html)
        current_title = first_title.group(0) if first_title else f"<title>{title}</title>"

        desired_head = (
            f"{current_title}\n"
            f'  <meta name="description" content="{desc}">\n'
            f'  <link rel="canonical" href="{loc}">\n'
            f'  <meta property="og:type" content="website">\n'
            f'  <meta property="og:title" content="{title}">\n'
            f'  <meta property="og:description" content="{desc}">\n'
            f'  <meta property="og:image" content="{DEFAULT_IMAGE}">\n'
            f'  <meta property="og:url" content="{loc}">\n'
            f'  <meta name="twitter:card" content="summary_large_image">\n'
            f'  <meta name="twitter:title" content="{title}">\n'
            f'  <meta name="twitter:description" content="{desc}">\n'
            f'  <meta name="twitter:image" content="{DEFAULT_IMAGE}">\n'
            '  <link rel="stylesheet" href="../css/style.css">'
        )

        html = re.sub(
            r"<head>.*?</head>",
            "<head>\n" + desired_head + "\n</head>",
            html,
            count=1,
            flags=re.S,
        )
        path.write_text(html, encoding="utf-8")

    for p in find_html_files():
        if p.parent.name == "cidades" and p.name.endswith(".html"):
            inject_once(p)

    print("Social meta injetada nas páginas de cidades.")


def run():
    if not SANITIZED.exists():
        raise SystemExit("Sanitize o lote antes de rodar o dia.")
    with SANITIZED.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for stage, builder in STAGE_MESSAGES.items():
        path = OUT_DIR / f"{stage}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["nome", "telefone", "cidade_interesse", "tipo_interesse", "estagio", "mensagem", "data_acao"],
            )
            writer.writeheader()
            for r in rows:
                writer.writerow(
                    {
                        "nome": r["nome"],
                        "telefone": r["telefone"],
                        "cidade_interesse": r["cidade_interesse"],
                        "tipo_interesse": r["tipo_interesse"],
                        "estagio": stage,
                        "mensagem": builder(r),
                        "data_acao": datetime.date.today().isoformat(),
                    }
                )
        print(f"Gerado: {path}")

    # Cross-sell
    generate_cross_sell(SANITIZED, OUT_DIR)

    update_sitemap()
    update_all_pages_momentum()
    update_social_meta()

    import subprocess, sys
    subprocess.run([sys.executable, str(BASE / "scripts" / "inject_jsonld.py")], check=False)
    subprocess.run([sys.executable, str(BASE / "scripts" / "pronto_disparo.py")], check=False)
    subprocess.run([sys.executable, str(BASE / "scripts" / "sequenciador_dia.py")], check=False)

    list_path = OUT_DIR / "resumo.txt"
    lines = [f"Litoral Prime — resumo do dia {datetime.date.today().isoformat()}",
             f"Leads no lote: {len(rows)}",
             f"Cidades: {', '.join(sorted(set(r['cidade_interesse'] for r in rows)))}",
             f"Tipos: {', '.join(sorted(set(r['tipo_interesse'] for r in rows)))}"]
    list_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Resumo: {list_path}")


if __name__ == "__main__":
    run()