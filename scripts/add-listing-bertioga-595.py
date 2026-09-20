#!/usr/bin/env python3
"""Add the Bertioga condo house listing (R$595.000) to the homepage listings array.
Idempotent: skips if id:25 already present."""
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
f = root / 'index.html'
text = f.read_text(encoding='utf-8')

if '{id:25,' in text:
    print('id:25 already present, nothing to do')
    sys.exit(0)

listing = (
    "  {id:25,tipo:'casa',cidade:'bertioga',cidadeLabel:'Bertioga — Condomíni"
    "o fechado (100m da praia)',titulo:'Casa em condomínio fechado — 2 dorms'"
    ",preco:595000,dormitorios:2,area:105,tags:['2 dorms','105m²','100m da pra"
    "ia','Piscina','1 vaga'],icon:'🏡',badge:'Novo',descricao:'Casa em condomí"
    "nio fechado em Bertioga a apenas 100 metros da praia. 105m² bem distribu"
    "ídos, 2 dormitórios, 2 banheiros e 1 vaga de garagem. Condomínio complet"
    "o com piscina, sauna, academia e sala de jogos. IPTU R$105/mês. Condomín"
    "io R$710 (água e internet inclusas). Detalhes em casa-condominio-fechado"
    "-bertioga.html',aiScore:93,aiReason:'Entry-point forte em Bertioga: 100m"
    " da praia com condomínio completo. ROI de temporada projetado em 19,4% b"
    "ruto / 11,3% líquido (AirDNA).',roi:11.3,url:'casa-condominio-fechado-be"
    "rtioga.html'},\n];"
)

anchor = "  {id:23,tipo:'terreno',cidade:'bertioga'"
lines = text.split('\n')
out = []
done = False
for line in lines:
    out.append(line)
    if not done and line.rstrip().endswith("roi:6.0}") and anchor.split(',')[0] not in line:
        # the id:23 line ends with roi:6.0} (no trailing comma) — next line is '];'
        pass
    if not done and line == '];' and any(anchor in l for l in out[-6:]):
        out.pop()
        prev = out[-1]
        if prev.rstrip().endswith('}'):
            out[-1] = prev.rstrip() + ','
        out.append(listing.rstrip('\n];') + '\n];' if False else listing)
        done = True

if not done:
    print('ERROR: listings array end not found')
    sys.exit(1)

text = ''.join(l + '\n' for l in out)
# fix double-comma risk / ensure array closes correctly: listing string already ends with ',\n];'
text = text.replace('placeholder="ID do imóvel (ex: 1)" min="1" max="12"',
                    'placeholder="ID do imóvel (ex: 1)" min="1" max="25"')
f.write_text(text, encoding='utf-8')
print('Added listing id:25 (Bertioga R$595.000) to index.html')
