import csv, os, random
from datetime import datetime

base = r'C:\Users\Carolina\praia-digital'
leads_csv = os.path.join(base, 'docs', 'sales', 'leads-litoral-enriquecido.csv')
outreach_dir = os.path.join(base, 'outreach')
csv_dir = os.path.join(base, 'csv-lotes-email')
docs_dir = os.path.join(base, 'docs', 'sales')
os.makedirs(outreach_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)

# Load all leads
leads = []
with open(leads_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        leads.append(dict(row))

# Exclude used lead IDs for this demo set (expand as needed)
used_ids = set([
    229,260,263,280,306,352,475,528,545,555,
    6,15,21,34,54,59,83,92,98,102,106,111,119,122,128,139,142,148,156,162,168,177,187,193,202,
    229,232,280,282,306,352,378,392,401,405,462,475,476,513,545,
    260,263,280,306,34,352,475,528,545,555,6,
])

candidates = []
for l in leads:
    if l.get('status','').strip().lower() == 'contato_inicial_enviado' and l.get('id','').strip() not in used_ids:
        candidates.append(l)

random.shuffle(candidates)
batch = candidates[:20]

# Choose offer type by dor
oferta_map = {
    'conteudo': 'fotografia + edição profissional',
    'anuncios': 'fotografia + edição profissional',
    'midia': 'vídeo profissional para imóveis',
    'conversao': 'mini site para imobiliária local',
    'leads': 'mini site para imobiliária local',
}

base_emails = {
    'fotografia + edição profissional': "Olá, {contato}!\n\nMe chamo Carolina Moura, CEO da Praia Digital.\n\nNotei que a {empresa} ({cidade}) está buscando melhorar conteúdo e anúncios. Por isso, quero apresentar uma solução rápida para aumentar vendas em até 7 dias:\n\nServiço: Fotografia Profissional + Edição Profissional de Imóveis\n\n- Imóveis com fotos profissionais recebem até 3x mais contatos\n- Entrega em 48h\n- Pacote mensal disponível\n\nAcesso gratuito às nossas ferramentas: https://praia.digital\nConheça nosso site: https://acarolmourad-commits.github.io/praia-digital/\n\nPodemos conversar 15 minutos?\n\nAtt,\nCarolina Moura\nCEO Praia Digital\nWhatsApp: (11) 95434-6288",
    'vídeo profissional para imóveis': "Olá, {contato}!\n\nMe chamo Carolina Moura, CEO da Praia Digital.\n\nNotei que a {empresa} ({cidade}) pode melhorar sua presença digital com conteúdo em vídeo.\n\nServiço: Vídeo Profissional para Imóveis\n\n- Imóveis com vídeo recebem até 50% mais visualizações\n- Formatos para Reels, TikTok, YouTube, site e WhatsApp\n- Entrega em 48h\n\nAcesso gratuito às nossas ferramentas: https://praia.digital\nConheça nosso site: https://acarolmourad-commits.github.io/praia-digital/\n\nPodemos conversar 15 minutos?\n\nAtt,\nCarolina Moura\nCEO Praia Digital\nWhatsApp: (11) 95434-6288",
    'mini site para imobiliária local': "Olá, {contato}!\n\nMe chamo Carolina Moura, CEO da Praia Digital.\n\nNotei que a {empresa} ({cidade}) pode captar mais leads diretamente com um mini site próprio.\n\nServiço: Mini Site para Imobiliária Local\n\n- Site one-page profissional\n- Formulário de captura + WhatsApp direto\n- SEO local forte por cidade/bairro\n- Entrega em até 7 dias\n\nAcesso gratuito às nossas ferramentas: https://praia.digital\nConheça nosso site: https://acarolmourad-commits.github.io/praia-digital/\n\nPodemos conversar 15 minutos?\n\nAtt,\nCarolina Moura\nCEO Praia Digital\nWhatsApp: (11) 95434-6288",
}

today = datetime.now().strftime('%Y%m%d')
folder = os.path.join(outreach_dir, f'lote-automatico-{today}')
os.makedirs(folder, exist_ok=True)

csv_path = os.path.join(csv_dir, f'lote-automatico-{today}.csv')
csv_rows = []
for lead in batch:
    dor = lead.get('dor_principal', '').strip().lower()
    oferta = oferta_map.get(dor, 'fotografia + edição profissional')
    txt = base_emails[oferta].format(contato=lead['pessoa_de_contato'], empresa=lead['nome_da_imobiliaria'], cidade=lead['cidade'])
    with open(os.path.join(folder, f'prospeccao-{lead["id"]}.txt'), 'w', encoding='utf-8') as f:
        f.write(txt)
    csv_rows.append({
        'Nome': lead['pessoa_de_contato'],
        'Empresa': lead['nome_da_imobiliaria'],
        'Cidade': lead['cidade'],
        'Email': lead['email'],
        'Assunto': f'{oferta.title()} para {lead["nome_da_imobiliaria"]}',
        'Mensagem': txt.replace('\n',' '),
        'DataEnvio': datetime.now().strftime('%Y-%m-%d')
    })

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Nome','Empresa','Cidade','Email','Assunto','Mensagem','DataEnvio'])
    writer.writeheader()
    writer.writerows(csv_rows)

print('Lote automático criado:', csv_path)
print('Leads:', len(csv_rows))
