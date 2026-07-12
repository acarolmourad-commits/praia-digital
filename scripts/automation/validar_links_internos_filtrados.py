import os, re
from pathlib import Path

root = Path("C:/Users/Carolina/praia-digital")
html_files = list(root.rglob("*.html"))

broken = []
checked = 0

for html in html_files:
    text = html.read_text(encoding="utf-8", errors="ignore")
    links = re.findall(r'href="([^"]+)"', text)
    for link in links:
        if link.startswith("#") or link.startswith("javascript:") or link.startswith("mailto:") or link.startswith("tel:") or link.startswith("http") or link.startswith("//"):
            continue
        if link.startswith("data:image/svg+xml"):
            continue
        if link.startswith("/assets/") or link.startswith("/praia-digital/") or link.startswith("/proptech/") or link.startswith("/blog/"):
            continue
        if link.endswith(".md"):
            continue
        target = (html.parent / link).resolve()
        if not target.exists():
            broken.append((str(html.relative_to(root)), link))
        checked += 1

print(f"Verificados: {len(html_files)} arquivos HTML")
print(f"Links internos relevantes quebrados: {len(broken)}")
for rel, link in broken[:100]:
    print(f"- {rel} -> {link}")
