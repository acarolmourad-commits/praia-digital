# WhatsApp Automation — Praia Digital

## Configuração

1. Duplicate `.env.example` para `.env`
2. Preencha com suas credenciais

```
WHATSAPP_API_URL=https://sua-api.exemplo.com
WHATSAPP_API_TOKEN=seu_token_aqui
WHATSAPP_INSTANCE=sua_instancia_aqui
```

### Variáveis
- `WHATSAPP_API_URL` — URL base da API
- `WHATSAPP_API_TOKEN` — Token de autenticação
- `WHATSAPP_INSTANCE` — Nome da instância (Evolution API)

## Instalação
```bash
pip install python-dotenv requests
```

## Uso

### Dry-run (sem envio real)
```bash
python sender.py --csv contacts-example.csv --dry-run
```

### Envio real
```bash
python sender.py --csv contacts.csv --provider evolution
```

### Com delay customizado
```bash
python sender.py --csv contacts.csv --delay 10 --provider zapi
```

## Formato do CSV
```
nome,cidade,cidade_slug,telefone,perfil,data,metrica,link_guia,link_calculadora
```

## Templates
Os templates ficam em `templates/` e suportam variáveis:
- `{{nome}}`, `{{cidade}}`, `{{data}}`, `{{metrica}}`, `{{link_guia}}`, `{{link_calculadora}}`, `{{cidade_slug}}`
