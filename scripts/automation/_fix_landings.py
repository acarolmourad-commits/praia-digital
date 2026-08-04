import csv, urllib.parse
from pathlib import Path

repo = Path('.').resolve()
csv_path = repo / 'imoveis' / 'landings.csv'

rows = [
    ('Apartamento 3 quartos suíte em Santos','Apartamento 3 quartos suíte em Santos: vista mar, lazer completo, 2 vagas. Oportunidade na orla mais valorizada do litoral.','santos','apartamento','apartamento-3-quartos-suite-santos','R$ 850.000–1.200.000','900000','3–4','110–160 m²','https://praia.digital/img/santos-apartamento-vista-mar.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20su%C3%ADte%20em%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Apartamento frente mar Guarujá','Apartamento frente mar Guarujá: varanda panorâmica, piscina, academia. Oferta para quem quer vista definitiva.','guaruja','apartamento','apartamento-frente-mar-guaruja','R$ 700.000–1.000.000','850000','2–3','90–140 m²','https://praia.digital/img/gua-casa-duplex.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Casa condomínio fechado Bertioga','Casa condomínio fechado Bertioga: segurança 24h, área verde, churrasqueira. Ideal para famílias.','bertioga','casa','casa-condominio-bertioga','R$ 650.000–980.000','800000','3–4','130–220 m²','https://praia.digital/img/berta-alto-padrao.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Cobertura duplex Santos','Cobertura duplex Santos: terraço privativo, piscina, 4 vagas. Acabamento alto padrão.','santos','cobertura','cobertura-duplex-santos','R$ 1.100.000–1.600.000','1300000','3–4','180–250 m²','https://praia.digital/img/santos-apartamento-vista-mar.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20duplex%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Studio temporada Itanhaém','Studio temporada Itanhaém: investimento com alta taxa de ocupação, lazer completo e fácil acesso à praia.','itanhaem','studio','studio-temporada-itanhaem','R$ 180.000–320.000','250000','1','35–55 m²','https://praia.digital/img/it-casa-terrea.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Studio%20temporada%20Itanha%C3%A9m&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Sobrado 3 dormitórios Mongaguá','Sobrado 3 dormitórios Mongaguá: quintal, garagem coberta, proximidade com orla.','mongagua','sobrado','sobrado-3-dormitorios-mongagua','R$ 420.000–680.000','550000','3–4','110–160 m²','https://praia.digital/img/mon-ap-compacto.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%203%20dormit%C3%B3rios%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Terreno plano Peruíbe','Terreno plano Peruíbe: infraestrutura pronta, documentação ok, boa valorização futura.','peruibe','terreno','terreno-plano-peruibe','R$ 150.000–280.000','200000','','200–450 m²','https://praia.digital/img/per-sobrado.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20plano%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Apartamento 2 quartos Praia Grande','Apartamento 2 quartos Praia Grande: lazer completo, fácil acesso à via Imigrantes.','praia-grande','apartamento','apartamento-2-quartos-praia-grande','R$ 300.000–520.000','420000','2–3','70–110 m²','https://praia.digital/img/pg-studio-moderno.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%202%20quartos%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Casa vila Santos','Casa vila Santos: tranquilidade, segurança, ótima localização residencial.','santos','casa','casa-vila-santos','R$ 550.000–820.000','700000','2–3','90–140 m²','https://praia.digital/img/santos-apartamento-vista-mar.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20vila%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Apartamento suíte vista mar São Vicente','Apartamento suíte vista mar São Vicente: sacada gourmet, lazer completo e vista definitiva.','sao-vicente','apartamento','apartamento-suite-vista-mar-sao-vicente','R$ 520.000–780.000','650000','2–3','85–130 m²','https://praia.digital/img/sv-cobertura-duplex.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20su%C3%ADte%20vista%20mar%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Cobertura penthouse Guarujá','Cobertura penthouse Guarujá: terraço exclusivo, piscina privativa, 3 vagas. Acabamento premium.','guaruja','cobertura','cobertura-penthouse-guaruja','R$ 980.000–1.450.000','1200000','3–4','170–240 m²','https://praia.digital/img/gua-casa-duplex.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20penthouse%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Apartamento 3 quartos Bertioga','Apartamento 3 quartos Bertioga: varanda, lazer completo e proximidade com natureza.','bertioga','apartamento','apartamento-3-quartos-bertioga','R$ 480.000–720.000','600000','3','100–150 m²','https://praia.digital/img/berta-alto-padrao.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Studio investimento Santos','Studio investimento Santos: alta liquidez, fácil locação, ideal para portfolio imobiliário.','santos','studio','studio-investimento-santos','R$ 220.000–380.000','300000','1','28–45 m²','https://praia.digital/img/santos-apartamento-vista-mar.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Studio%20investimento%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Sobrado condomínio Itanhaém','Sobrado condomínio Itanhaém: área de lazer, churrasqueira, espaço pet-friendly.','itanhaem','sobrado','sobrado-condominio-itanhaem','R$ 560.000–850.000','720000','3–4','130–190 m²','https://praia.digital/img/it-casa-terrea.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Itanha%C3%A9m&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Apartamento vista mar Santos','Apartamento vista mar Santos: sacada gourmet, lazer completo, 2 vagas. Perfeito para temporada e moradia.','santos','apartamento','apartamento-vista-mar-santos','R$ 750.000–1.100.000','780000','2–3','95–140 m²','https://praia.digital/img/santos-apartamento-vista-mar.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20vista%20mar%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Casa pé na areia Peruíbe','Casa pé na areia Peruíbe: acesso direto à praia, quintal, perfeita para temporada.','peruibe','casa','casa-pe-na-areia-peruibe','R$ 620.000–920.000','560000','2–4','120–200 m²','https://praia.digital/img/per-sobrado.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20p%C3%A9%20na%20areia%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Apartamento temporada Mongaguá','Apartamento temporada Mongaguá: estrutura completa para locação curta, alta procura na temporada.','mongagua','apartamento','apartamento-temporada-mongagua','R$ 260.000–420.000','340000','1–2','50–80 m²','https://praia.digital/img/mon-ap-compacto.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20temporada%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Cobertura vista mar Santos','Cobertura vista mar Santos: terraço panorâmico, piscina privativa, lazer completo e 3 vagas.','santos','cobertura','cobertura-vista-mar-santos','R$ 1.050.000–1.480.000','1250000','3–4','170–230 m²','https://praia.digital/img/santos-apartamento-vista-mar.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Terreno loteamento Praia Grande','Terreno loteamento Praia Grande: documento regular, topografia plana, excelente para construção.','praia-grande','terreno','terreno-loteamento-praia-grande','R$ 180.000–320.000','250000','','180–360 m²','https://praia.digital/img/pg-studio-moderno.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
    ('Sobrado 3 quartos São Vicente','Sobrado 3 quartos São Vicente: garagem coberta, quintal amplo, boa valorização.','sao-vicente','sobrado','sobrado-3-quartos-sao-vicente','R$ 430.000–690.000','560000','3','110–160 m²','https://praia.digital/img/sv-cobertura-duplex.jpg','','https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%203%20quartos%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'),
]

with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    existing = list(reader)

updates = {r['slug']: r for r in existing if r.get('slug')}
new_count = 0
for row in rows:
    slug = row[4]
    if slug not in updates:
        new = {k: '' for k in fieldnames}
        new.update(zip(fieldnames, row))
        updates[slug] = new
        new_count += 1

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in updates.values():
        writer.writerow(r)

print('new_rows', new_count)
print('csv_rows_now', len(updates))
