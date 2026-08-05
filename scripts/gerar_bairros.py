#!/usr/bin/env python3
"""
Regera páginas de bairro com slugs consistentes em UTF-8 NFC.
"""
from pathlib import Path
import unicodedata

BASE = Path(r"C:\Users\Carolina\praia-digital")
TEMPLATE = BASE / "templates" / "bairro-modelo.html"

cities = {
    "caraguatatuba": [
        ("Centro", "comércio, serviços e acesso rápido à orla"),
        ("Jaguaribe", "orla movimentada, vida noturna e estrutura turística"),
        ("Prainha", "famílias, calmaria e proximidade com a praia"),
    ],
    "ubatuba": [
        ("Centro", "acesso fácil, comércio forte e movimentação turística"),
        ("Itaguá", "acesso à praia e ponto de entrada da cidade"),
        ("São Lourenço", "paz, natureza e proximidade com o mar"),
    ],
    "ilhabela": [
        ("Vila", "centro da ilha com serviços e acesso rápido"),
        ("Pernambuco", "vila charmosa com estrutura e praia"),
        ("Bonete", "paz, trilhas e natureza preservada"),
    ],
    "sao-sebastiao": [
        ("Centro Histórico", "história, charme e comércio local"),
        ("Juquehy", "praia badalada, restaurantes e temporada"),
        ("Maresias", "surf, entretenimento e fluxo turístico"),
    ],
    "bertioga": [
        ("Centro", "acesso fácil, comércio e serviços"),
        ("Riviera", "conforto, condomínios e estrutura"),
        ("Guaratuba", "natureza, praia e tranquilidade"),
    ],
    "guaruja": [
        ("Enseada", "orla larga, comércio e famílias"),
        ("Asturias", "movimento, orla e temporada"),
        ("Pitangueiras", "vista mar, comércio e vida social"),
    ],
    "santos": [
        ("Gonzaga", "orla famosa, comércio e valorização"),
        ("Boqueirão", "vida noturna, orla e fluxo"),
        ("Embaré", "famílias, calmaria e acessos"),
    ],
    "praia-grande": [
        ("Tupi", "orla e investimento em expansão"),
        ("Guilhermina", "passeio, famílias e temporada"),
        ("Ocian", "vida social, orla e comércio"),
    ],
}

def slugify(name: str) -> str:
    nfkd = unicodedata.normalize('NFKD', name)
    ascii_name = nfkd.encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]+', '-', ascii_name.lower()).strip('-')

text = TEMPLATE.read_text(encoding="utf-8")
created = 0
for city, bairros in cities.items():
    city_dir = BASE / "bairros" / city
    city_dir.mkdir(parents=True, exist_ok=True)
    for bairro, desc in bairros:
        slug = slugify(bairro)
        file = city_dir / f"{slug}.html"
        content = (
            text.replace("[Bairro]", bairro)
            .replace("[Cidade]", city.title().replace("-", " "))
            .replace("[cidade-slug]", city)
            .replace("[bairro-slug]", slug)
            .replace("[característica principal]", desc)
            .replace("[acessos]", "rodovias e transporte público")
            .replace("[ponto de referência]", "orla e pontos turísticos")
        )
        file.write_text(content, encoding="utf-8")
        created += 1

print("bairro pages created:", created)
