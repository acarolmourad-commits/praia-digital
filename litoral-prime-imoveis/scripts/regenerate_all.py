"""Regeneração diária da Litoral Prime.

Este driver orquestra todos os geradores do site numa única etapa.
Cada passo abaixo mapeia uma etapa histórica (referida na versão anterior
por scripts `gerar_*`/`refresh_*`/`inject_*` já removidos) para o script
moderno equivalente que existe no repositório atual.

Etapas históricas -> script atual:
  gerar_blog_semanal          -> automation/inject_blog_schema.py   (blog é conteúdo estático; injeta schema)
  gerar_landings_captacao     -> build_landings.py                  (landings de imóveis a partir de properties.json)
  gerar_servicos_cidade       -> build_city_pages.py                (páginas de serviços por cidade)
  gerar_posts_redes           -> build_marketing_assets.py          (copies de WhatsApp/e-mail por cidade)
  gerar_leads_from_imoveis    -> run_vendas_do_dia.py               (pipeline diário de leads)
  gerar_bairros               -> build_bairros.py                   (páginas de bairro por cidade)
  create_bairros_hub          -> (incluído em build_bairros.py)
  create_posts_hub            -> (incluído em build_marketing_assets.py)
  inject_lead_links_city      -> (incluído em build_city_pages.py / build_landings.py)
  inject_lead_forms           -> (incluído em build_landings.py)
  refresh_sitemap             -> build_sitemap.py                   (sitemap.xml com todas as URLs)
  refresh_leads_sitemap       -> update_sitemap_lastmod.py          (atualiza lastmod de todos)
  refresh_outreach_sitemap    -> (incluído em build_sitemap.py)
  refresh_extra_sitemap       -> (incluído em build_sitemap.py)

Diferença do driver anterior: falhas em um passo não são mais silenciosas.
O script registra OK/ERRO por passo e sai com código de erro se qualquer
passo falhar, para que o cron reflita o estado real da regeneração.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:/Users/Carolina/praia-digital/litoral-prime-imoveis")

CLEAN_DIRS = [
    REPO / "blog",
    REPO / "leads",
    REPO / "bairros",
    REPO / "captacao",
    REPO / "servicos" / "cidades",
    REPO / "outreach" / "posts-gerados",
]


def clean():
    """Remove arquivos gerados estáticos antes da regeneração (housekeeping)."""
    for d in CLEAN_DIRS:
        if d.exists():
            for f in d.glob("*.html"):
                f.unlink()
            for f in d.glob("*.txt"):
                f.unlink()
    print("Cleaned generated dirs.")


# Ordem importa: geração de conteúdo -> injeção de schema -> sitemap (último,
# para varrer todas as HTMLs recém-criadas).
STEPS = [
    ("property landings (gerar_landings_captacao)", "build_landings.py"),
    ("bairro pages (gerar_bairros)", "build_bairros.py"),
    ("city service pages (gerar_servicos_cidade)", "build_city_pages.py"),
    ("marketing assets (gerar_posts_redes)", "build_marketing_assets.py"),
    ("JSON-LD injection", "inject_jsonld.py"),
    ("blog schema (gerar_blog_semanal)", "automation/inject_blog_schema.py"),
    ("leads pipeline (gerar_leads_from_imoveis)", "run_vendas_do_dia.py"),
    ("sitemap.xml (refresh_sitemap)", "build_sitemap.py"),
    ("sitemap.html (refresh_sitemap)", "build_sitemap_html.py"),
    ("lastmod refresh (refresh_leads/outreach/extra_sitemap)", "update_sitemap_lastmod.py"),
]


def main():
    clean()
    failures = []
    for label, script in STEPS:
        path = REPO / "scripts" / script
        print(f"Running {script} ({label}) ...")
        if not path.exists():
            print(f"  [ERROR] Script not found: {path}")
            failures.append(script)
            continue
        r = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
        if r.stdout.strip():
            print(r.stdout.strip())
        if r.returncode != 0:
            print(f"  [ERROR] exit={r.returncode} stderr={r.stderr.strip()}")
            failures.append(script)
        else:
            print(f"  [OK] {script}")
    print("Regeneration complete.")
    if failures:
        print(f"FAILED STEPS ({len(failures)}): {failures}")
        sys.exit(1)
    print("All steps succeeded.")


if __name__ == "__main__":
    main()
