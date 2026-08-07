# Praia Digital Academy — Deploy Summary

## O que já está pronto
- Backend: 15 testes locais passando
- Frontend: páginas saneadas, sem JS/SEO crítico
- Segurança: headers, sanitização, SECRET_KEY obrigatória em prod
- Validação pós-deploy: `scripts/validate_academy_deploy.py`

## O que falta (você)
1. Acessar https://dashboard.render.com
2. New + Web Service
   - Repo: `acarolmourad-commits/praia-digital`
   - Branch: `main`
   - Nome: `praia-digital-academy`
3. New + PostgreSQL
   - Nome: `academy-db`
4. Copiar `DATABASE_URL` do banco para env vars do web service
5. Preencher env vars (ver `docs/deployment/RENDER_ACADEMY_ENV_VARS.md`)
6. Aguardar deploy automático
7. Me chamar: eu valido produção

## Comando pós-deploy
```
cd C:\Users\Carolina\praia-digital
python scripts/validate_academy_deploy.py
```

## Contato
- comercial@praia.digital
- (11) 95434-6288
