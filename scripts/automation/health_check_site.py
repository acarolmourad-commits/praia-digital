import requests
from pathlib import Path
from datetime import datetime

root = Path("C:/Users/Carolina/praia-digital")
base_url = "https://acarolmourad-commits.github.io/praia-digital/"
pages = [
    "index.html",
    "parcerias-imobiliarias-litoral.html",
    "checklist-corretores-litoral-download.html",
    "obrigado-segmentado.html",
    "form-tracker.html",
    "landing-captura-leads-litoral.html",
    "blog/primeiro-imovel-litoral-guia-iniciantes-2026.html",
    "blog/melhores-bairros-investir-litoral-paulista-2026.html",
    "blog/temporada-litoral-receita-imovel-2026.html",
    "blog/apartamentos-venda-na-praia-2026.html",
    "planos-assinatura.html",
    "sitemap.xml",
]
form_url = "https://formspree.io/f/xvgrzjza"

report = []
report.append(f"# Health Check — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report.append("")

# Check pages
for page in pages:
    url = base_url + page
    try:
        r = requests.get(url, timeout=15)
        status = "OK" if r.status_code == 200 else f"ERRO {r.status_code}"
        report.append(f"- {page}: {status}")
    except Exception as e:
        report.append(f"- {page}: ERRO ({e})")

report.append("")

# Check Formspree endpoint
try:
    r = requests.get(form_url, timeout=15)
    status = "OK" if r.status_code in [200, 404] else f"ERRO {r.status_code}"
    report.append(f"- Formspree endpoint: {status}")
except Exception as e:
    report.append(f"- Formspree endpoint: ERRO ({e})")

report.append("")
report.append("## Resumo")
report.append(f"Páginas verificadas: {len(pages)}")

print("\n".join(report))
