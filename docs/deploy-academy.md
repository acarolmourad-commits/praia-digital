# Deploy — Praia Digital Academy
**Status:** Pronto para produção

## Checklist de deploy
- [x] Código documentado
- [x] Testes automatizados passando (Fase 1 a 5)
- [x] Banco de dados modelado e migration-ready
- [x] CORS configurável por variável de ambiente
- [x] SECRET_KEY configurável
- [x] SMTP configurável
- [x] Arquivo `.env.example` criado
- [x] `render.yaml` criado
- [x] Frontend do aluno servido pelo FastAPI
- [x] Healthcheck implementado

## Como fazer deploy

### Opção 1: Render
1. Subir repositório para GitHub
2. No Render: New → Web Service → conectar repositório
3. Usar `render.yaml` como configuração
4. Banco PostgreSQL criado automaticamente
5. Após deploy, apontar DNS `academy.praia.digital`

### Opção 2: Railway
1. Subir repositório para GitHub
2. No Railway: New → Deploy from GitHub
3. Adicionar banco PostgreSQL
4. Configurar variáveis de ambiente

### Opção 3: Vercel + Railway
1. Backend no Railway
2. Frontend no Vercel
3. Conectar via variáveis de ambiente

## Variáveis de ambiente obrigatórias
```env
DATABASE_URL=postgresql://user:pass@host:5432/academy
SECRET_KEY=<chave_gerada_automaticamente>
SMTP_HOST=smtp.seudominio.com
SMTP_PORT=587
SMTP_USER=no-reply@praia.digital
SMTP_PASSWORD=<senha_smtp>
EMAIL_FROM=no-reply@praia.digital
ALLOWED_ORIGINS=https://praia.digital,https://www.praia.digital,https://academy.praia.digital
```

## Comando de start
```bash
cd academy
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Testes antes do deploy
```bash
PYTHONPATH=. python academy/tests/test_phase1.py
PYTHONPATH=. python academy/tests/test_phase2.py
PYTHONPATH=. python academy/tests/test_phase3.py
PYTHONPATH=. python academy/tests/test_phase4.py
PYTHONPATH=. python academy/tests/test_phase5.py
```

## Próximos passos após deploy
1. Configurar gateway de pagamento real
2. Popular regras de upsell/cross-sell
3. Implementar automação de WhatsApp
4. Implementar emissão de certificado PDF
5. Configurar domínio `academy.praia.digital`
6. Adicionar SSL/HTTPS
7. Monitoramento e logs
