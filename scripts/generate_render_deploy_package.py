from pathlib import Path
import json

render_checklist = {
  "service_name": "academy-api",
  "repo": "acarolmourad-commits/praia-digital",
  "branch": "main",
  "runtime": "Python 3",
  "build_command": "pip install -r academy/requirements.txt",
  "start_command": "cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT",
  "database": {
    "name": "academy-db",
    "type": "PostgreSQL",
    "env_var": "DATABASE_URL"
  },
  "env": {
    "SECRET_KEY": "<REQUIRED>",
    "SMTP_HOST": "<REQUIRED>",
    "SMTP_PORT": "<REQUIRED>",
    "SMTP_USER": "<REQUIRED>",
    "SMTP_PASSWORD": "<REQUIRED>",
    "EMAIL_FROM": "no-reply@praia.digital",
    "ALLOWED_ORIGINS": "https://praia.digital,https://www.praia.digital,https://academy.praia.digital",
    "MERCADOPAGO_API_URL": "https://api.mercadopago.com/v1",
    "MERCADOPAGO_TOKEN": "<REQUIRED>",
    "MERCADOPAGO_PUBLIC_KEY": "<REQUIRED>",
    "WHATSAPP_API_URL": "<REQUIRED>",
    "WHATSAPP_TOKEN": "<REQUIRED>",
    "WHATSAPP_PHONE_ID": "<REQUIRED>",
    "WHATSAPP_TO_NUMBER": "<REQUIRED>",
    "BASE_URL": "https://academy.praia.digital"
  },
  "custom_domain": "academy.praia.digital",
  "validation": [
    "python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30",
    "python scripts/frontend_health_check.py --base https://praia.digital --wait 30"
  ]
}

Path('docs').mkdir(exist_ok=True)
Path('docs/render-academy-deploy-package.json').write_text(
  json.dumps(render_checklist, ensure_ascii=False, indent=2),
  encoding='utf-8'
)
print('written docs/render-academy-deploy-package.json')
