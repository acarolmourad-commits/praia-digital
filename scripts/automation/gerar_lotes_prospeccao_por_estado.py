import csv
from pathlib import Path

REPO = Path(r'C:/Users/Carolina/praia-digital')
LEADS_CSV = REPO / 'docs/sales/leads-litoral-enriquecido.csv'
OUT_DIR = REPO / 'outreach'
OUT_DIR.mkdir(exist_ok=True)

city_article_map = {
    'Santos': 'santos-orla-gastronomia-passeios-2026-sp-2026-07-14.html',
    'Guarujá': 'guaruja-ilha-panqueca-fim-semana-2026-sp-2026-07-14.html',
    'Praia Grande': 'guia-completo-praia-grande-familia-2026-sp-2026-07-14.html',
    'Ubatuba': 'ubatuba-trilhas-praias-guia-2026-sp-2026-07-14.html',
    'Peruíbe': 'peruibe-centro-historico-praias-2026-sp-2026-07-14.html',
    'São Vicente': 'sao-vicente-historico-monumentos-2026-sp-2026-07-14.html',
    'Bertioga': 'bertioga-riviera-sao-francisco-guia-2026-sp-2026-07-14.html',
    'Itanhaém': 'itanhaem-centro-antigo-lagoa-2026-sp-2026-07-14.html',
    'Mongaguá': 'mongagua-praias-familiares-2026-sp-2026-07-14.html',
    'Cabo Frio': 'cabo-frio-roteiro-casais-2026-sp-2026-07-14.html',
    'Búzios': 'buzios-praias-famosas-guia-2026-sp-2026-07-14.html',
    'Paraty': 'paraty-historico-ilhas-2026-rj-2026-07-14.html',
    'Florianópolis': 'florianopolis-praias-guia-2026-sc-2026-07-14.html',
    'Balneário Camboriú': 'balneario-camboriu-compras-praia-2026-sc-2026-07-14.html',
}

rows = []
with open(LEADS_CSV, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

batch = 40
created = []
seen = set()

for row in rows:
    city = (row.get('cidade') or '').strip().title()
    if not city or city not in city_article_map:
        continue
    email = (row.get('email') or '').strip().lower()
    if not email or email in seen:
        continue
    seen.add(email)
    nome = (row.get('pessoa_de_contato') or row.get('nome') or '').title() or 'Contato'
    imobiliaria = (row.get('nome_da_imobiliaria') or '').title() or ''
    telefone = (row.get('whatsapp') or row.get('telefone') or '').strip()
    article_slug = city_article_map[city]
    article_name = article_slug.replace('-', ' ').replace('2026', '').title()
    first_name = nome.split()[0] if nome.split() else nome
    slug = f"lote-prospeccao-{batch}-{city.lower().replace(' ', '-').replace('á','a').replace('ó','o').replace('é','e').replace('í','i').replace('ú','u').replace('ã','a')}-2026-07-14"
    path = OUT_DIR / f"{slug}.html"
    if path.exists():
        batch += 1
        continue
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lote {batch} - Prospecção {city}</title>
</head>
<body style="margin:0;font-family:Segoe UI,Arial,sans-serif;background:#f4f6f9;color:#1f2937;">
  <div style="max-width:800px;margin:0 auto;padding:2rem;">
    <div style="background:linear-gradient(135deg,#0a1628,#1a3a5c);color:#fff;padding:2rem;border-radius:12px;margin-bottom:1.5rem;text-align:center;">
      <div style="opacity:.8;font-size:.9rem;">Praia Digital · Lote {batch} · {city}</div>
      <h1>Prospecção {city}</h1>
      <div style="opacity:.8;font-size:.9rem;">Conteúdo: {article_name}</div>
    </div>
    <div style="background:#fff;border-radius:12px;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:1.5rem;">
      <h2>Dados do lead</h2>
      <p>Nome: {nome}</p>
      <p>E-mail: {email}</p>
      <p>Telefone: {telefone}</p>
      <p>Cidade: {city}</p>
      <p>Origem: outreach</p>
    </div>
    <div style="background:#fff;border-radius:12px;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:1.5rem;">
      <h2>E-mail de primeiro contato</h2>
      <p style="white-space:pre-wrap;">Olá, {first_name}!

Sou Carolina Mourad, CEO da Praia Digital. Acompanho o mercado imobiliário em {city} e preparei um artigo exclusivo que pode ajudar a {imobiliaria or 'sua imobiliária'}:

👉 {article_name}

Case modelo: Barra Norte Imóveis (Guarujá)
• +40% leads qualificados em 30 dias
• -60% tempo de atendimento
• 3x mais agendamentos
• 0% investimento em anúncios

Quer um diagnóstico gratuito de 15 minutos?

Abraço,
Carolina Mourad
CEO · Praia Digital
(11) 95434-6288
https://acarolmourad-commits.github.io/praia-digital/</p>
      <a href="mailto:{email}?subject=Prospecção%20{city}%20-%20Praia%20Digital&body=Ol%C3%A1%2C%20{first_name}!%0A%0ASou%20Carolina%20Mourad%2C%20CEO%20da%20Praia%20Digital.%20Acompanho%20o%20mercado%20em%20{city}%20e%20preparei%20um%20artigo%20exclusivo.%0A%0A👉%20{article_name.replace(' ', '%20')}%0A%0ACase%3A%20Barra%20Norte%20Im%C3%B3veis%0A%E2%80%A2%20%2B40%25%20leads%20qualificados%0A%E2%80%A2%20-60%25%20tempo%20de%20atendimento%0A%E2%80%A2%203x%20mais%20agendamentos%0A%0AQuer%20um%20diagn%C3%B3stico%20gratuito%3F%0A%0A(11)%2095434-6288" style="display:inline-block;margin-top:1rem;background:linear-gradient(135deg,#00d4ff,#7b2ff7);color:#fff;padding:.9rem 1.4rem;border-radius:999px;text-decoration:none;font-weight:700;">📧 Abrir no cliente de e-mail</a>
    </div>
    <div style="background:linear-gradient(135deg,rgba(0,212,255,0.1),rgba(123,47,247,0.1));border:2px solid rgba(0,212,255,0.3);border-radius:12px;padding:1.5rem;text-align:center;">
      <h3 style="margin-bottom:.5rem;">Próximos passos</h3>
      <p style="color:#e0e0e0;line-height:1.7;">Salvar no tracker → agendar follow-up 3d/7d → usar auto-respostas se houver retorno.</p>
      <a href="docs/sales/send-execution-tracker-2026.html" target="_blank" style="color:#00d4ff;text-decoration:none;font-weight:700;">Abrir tracker</a>
    </div>
  </div>
</body>
</html>"""
    path.write_text(html, encoding='utf-8')
    created.append((batch, city, email, str(path), article_slug))
    batch += 1

print(f"Criados {len(created)} lotes por cidade")
for item in created[:10]:
    print(f"- Lote {item[0]}: {item[1]} -> {Path(item[3]).name}")
