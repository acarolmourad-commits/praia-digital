#!/usr/bin/env python3
"""
Limpa duplicatas em docs/sales/followup-registro.md e gera versão limpa.
"""
import re
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
TRACKER = BASE / "docs/sales/followup-registro.md"
OUTPUT = BASE / "docs/sales/followup-registro-limpo.md"

texto = TRACKER.read_text(encoding="utf-8", errors="ignore")
linhas = texto.splitlines()
vistas = set()
filtradas = []
for linha in linhas:
    normal = re.sub(r"\s+", " ", linha).strip()
    if normal and normal not in vistas:
        vistas.add(normal)
        filtradas.append(linha)

saida = "\n".join(filtradas)
if not saida.endswith("\n"):
    saida += "\n"
OUTPUT.write_text(saida, encoding="utf-8")
print(f"Limpo: {OUTPUT}")
print(f"Linhas antes: {len(linhas)} | depois: {len(filtradas)} | removidas: {len(linhas)-len(filtradas)}")
