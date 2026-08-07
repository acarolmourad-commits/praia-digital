# Render Academy — passo a passo rápido

1. Abra https://dashboard.render.com
2. New + Web Service
   - Repo: `acarolmourad-commits/praia-digital`
   - Branch: `main`
   - Nome: `praia-digital-academy`
3. New + PostgreSQL
   - Nome: `academy-db`
4. No web service, em Environment, adicione:
   - `DATABASE_URL` = `fromDatabase academy-db`
   - `SECRET_KEY` = `generateValue`
   - `APP_ENV` = `production`
   - Restante: ver `docs/deployment/RENDER_ACADEMY_ENV_VARS.md`
5. Aguarde deploy
6. Me chame: eu valido `/health`, `/docs`, `/auth/register` e `/leads` em `https://academy.praia.digital`
