import shutil
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
    for d in CLEAN_DIRS:
        if d.exists():
            for f in d.glob("*.html"):
                f.unlink()
            for f in d.glob("*.txt"):
                f.unlink()
    print("Cleaned generated dirs.")

def main():
    clean()
    # Run generators
    import subprocess, sys
    scripts = [
        "scripts/gerar_blog_semanal.py",
        "scripts/gerar_landings_captacao.py",
        "scripts/gerar_servicos_cidade.py",
        "scripts/gerar_posts_redes.py",
        "scripts/gerar_leads_from_imoveis.py",
        "scripts/gerar_bairros.py",
        "scripts/create_bairros_hub.py",
        "scripts/create_posts_hub.py",
        "scripts/inject_lead_links_city.py",
        "scripts/inject_lead_forms.py",
        "scripts/refresh_sitemap.py",
        "scripts/refresh_leads_sitemap.py",
        "scripts/refresh_outreach_sitemap.py",
        "scripts/refresh_extra_sitemap.py",
    ]
    for s in scripts:
        print(f"Running {s} ...")
        r = subprocess.run([sys.executable, str(REPO / s)], capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            print("ERROR:", r.stderr.strip())
    print("Regeneration complete.")

if __name__ == "__main__":
    main()
