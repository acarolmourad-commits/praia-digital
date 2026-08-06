from pathlib import Path
import json

base = Path('education/marketing')
outbound_path = base / 'lead-magnets-outbound.json'
pages_dir = base / 'lead-magnets'
pages_dir.mkdir(parents=True, exist_ok=True)

data = json.loads(outbound_path.read_text(encoding='utf-8'))

for slug, item in data.items():
    title = item['title']
    description = item['email_body']
    whatsapp = item['whatsapp']
    email_subject = item['email_subject']
    email_body = item['email_body']
    instagram = item['instagram_caption']
    linkedin = item['linkedin_post']
    hashtags = item['hashtags']

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Praia Digital</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://praia.digital/education/marketing/lead-magnets/{slug}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title} | Praia Digital">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="https://praia.digital/education/marketing/lead-magnets/{slug}.html">
  <meta property="og:image" content="https://praia.digital/img/default-home.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | Praia Digital">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="https://praia.digital/img/default-home.jpg">
  <link rel="preconnect" href="https://praia.digital" crossorigin>
  <link rel="icon" type="image/x-icon" href="https://praia.digital/favicon.ico">
  <link rel="manifest" href="https://praia.digital/manifest.json">
  <link rel="alternate" hreflang="x-default" href="https://praia.digital/education/marketing/lead-magnets/{slug}.html" />
  <link rel="alternate" hreflang="pt-BR" href="https://praia.digital/education/marketing/lead-magnets/{slug}.html">
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f6fbf7; color:#064e3b; }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 24px; }}
    .hero {{ background:#0ea5e9; color:#fff; padding:32px 24px; border-radius:12px; }}
    .cta {{ display:inline-block; background:#25d366; color:#fff; padding:12px 16px; border-radius:8px; text-decoration:none; font-weight:bold; margin-top:12px; }}
    .card {{ background:#fff; border:1px solid #d8f3dc; border-radius:12px; padding:18px; margin-top:18px; }}
    .copy-box {{ background:#ffffff; border:1px solid #e5e7eb; border-radius:8px; padding:14px; margin-top:10px; white-space:pre-wrap; font-family:monospace; color:#064e3b; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <h1>{title}</h1>
      <p>{description}</p>
      <a class="cta" href="https://wa.me/5511954346288?text={whatsapp.replace(' ', '%20')}" target="_blank" rel="noopener">Quero receber o guia</a>
    </div>

    <div class="card">
      <h2>Copy para WhatsApp</h2>
      <div class="copy-box">{whatsapp}</div>
    </div>

    <div class="card">
      <h2>Copy para E-mail</h2>
      <p><strong>Assunto:</strong> {email_subject}</p>
      <div class="copy-box">{email_body}</div>
    </div>

    <div class="card">
      <h2>Copy para Instagram</h2>
      <div class="copy-box">{instagram}\n\n{hashtags}</div>
    </div>

    <div class="card">
      <h2>Copy para LinkedIn</h2>
      <div class="copy-box">{linkedin}\n\n{hashtags}</div>
    </div>

    <div class="card">
      <h2>Hashtags</h2>
      <div class="copy-box">{hashtags}</div>
    </div>
  </div>
</body>
</html>'''

    out_path = pages_dir / f'{slug}.html'
    out_path.write_text(html, encoding='utf-8')
    print(f'created {out_path}')

print('done')
