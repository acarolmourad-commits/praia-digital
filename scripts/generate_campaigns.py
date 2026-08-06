from pathlib import Path
import json
from datetime import datetime

# Load outbound data
outbound_path = Path('education/marketing/lead-magnets-outbound.json')
if not outbound_path.exists():
    print('outbound JSON missing')
    raise SystemExit(1)

data = json.loads(outbound_path.read_text(encoding='utf-8'))

# Output directory
campaigns_dir = Path('education/marketing/campaigns')
campaigns_dir.mkdir(parents=True, exist_ok=True)

# Campaign metadata
campaign_date = datetime.now().strftime('%Y-%m-%d')
utm_template = 'utm_source=outbound&utm_medium=email&utm_campaign=lead-magnet-{city}-{date}'

# Generate campaign files
for city, content in data.items():
    city_dir = campaigns_dir / city
    city_dir.mkdir(exist_ok=True)

    # Email files
    email_dir = city_dir / 'email'
    email_dir.mkdir(exist_ok=True)

    subject_file = email_dir / 'subject.txt'
    body_file = email_dir / 'body.html'
    tracking_file = email_dir / 'tracking.txt'

    subject_file.write_text(content['email_subject'], encoding='utf-8')

    utm = utm_template.format(city=city, date=campaign_date)
    body_with_tracking = content['email_body'].replace(
        'href="https://praia.digital/',
        'href="https://praia.digital/?' + utm + '&redirect='
    )
    body_file.write_text(body_with_tracking, encoding='utf-8')

    tracking_file.write_text(
        "Campaign: " + content['title'] + "\n"
        "Date: " + campaign_date + "\n"
        "City: " + city + "\n"
        "UTM: " + utm + "\n"
        "Subject: " + content['email_subject'] + "\n"
        "Status: ready\n",
        encoding='utf-8'
    )

    # WhatsApp files
    whatsapp_dir = city_dir / 'whatsapp'
    whatsapp_dir.mkdir(exist_ok=True)

    whatsapp_file = whatsapp_dir / 'message.txt'
    whatsapp_tracking = whatsapp_dir / 'tracking.txt'

    whatsapp_text = content['whatsapp']
    whatsapp_text += '\n\n🔗 ' + utm_template.format(city=city, date=campaign_date)
    whatsapp_file.write_text(whatsapp_text, encoding='utf-8')

    whatsapp_tracking.write_text(
        "Campaign: " + content['title'] + "\n"
        "Date: " + campaign_date + "\n"
        "City: " + city + "\n"
        "Phone: (11) 95434-6288\n"
        "Status: ready\n",
        encoding='utf-8'
    )

    # Social media files
    social_dir = city_dir / 'social'
    social_dir.mkdir(exist_ok=True)

    instagram_file = social_dir / 'instagram.txt'
    linkedin_file = social_dir / 'linkedin.txt'
    hashtags_file = social_dir / 'hashtags.txt'

    instagram_file.write_text(content['instagram_caption'], encoding='utf-8')
    linkedin_file.write_text(content['linkedin_post'], encoding='utf-8')
    hashtags_file.write_text('\n'.join(content['hashtags']), encoding='utf-8')

# Generate campaign index
index = campaigns_dir / 'index.md'
index_lines = [
    '# Campanhas de Outbound — Lead Magnets',
    '',
    'Gerado em: ' + campaign_date,
    '',
    '## Estrutura',
    '',
    'Cada cidade contém:',
    '- `email/` — assunto, corpo HTML e tracking',
    '- `whatsapp/` — mensagem pronta e tracking',
    '- `social/` — Instagram, LinkedIn e hashtags',
    '',
    '## Cidades',
    ''
]

for city in data.keys():
    index_lines.append('- [' + city + '](' + city + '/)')

    city_path = campaigns_dir / city
    file_count = sum(1 for f in city_path.rglob('*') if f.is_file())
    index_lines.append('  — ' + str(file_count) + ' arquivos')

index_lines.extend([
    '',
    '## Tracking',
    '',
    'UTM base:',
    '```',
    utm_template,
    '```',
    '',
    'Exemplo:',
    '```',
    utm_template.format(city='santos', date=campaign_date),
    '```',
])

index.write_text('\n'.join(index_lines), encoding='utf-8')

print('Generated campaigns for ' + str(len(data)) + ' cities')
print('Output: ' + str(campaigns_dir))
print('Total files: ' + str(sum(1 for f in campaigns_dir.rglob('*') if f.is_file())))
