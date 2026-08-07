# Academy — pre-deploy checklist

## Local
- [x] Backend sobe com `PYTHONPATH=academy uvicorn academy.main:app`
- [x] `/health` retorna 200
- [x] `/docs` retorna 200
- [x] `/auth/register` retorna 200 com token
- [x] `/leads` aceita payload sem `magnet`
- [x] `/academy/checkout` cria pedido
- [x] `/admin/leads` retorna 403 sem auth
- [x] `/monitoring/status` retorna 200
- [x] `pytest -q` passa localmente

## Frontend
- [x] `education/aluno/login.html` JS syntax ok
- [x] `education/aluno/admin.html` token key e headers spread ok
- [x] `education/checkout.html` token fallback ok
- [x] `education/cursos/*/vendas.html` null coercion e SEO markup ok
- [x] `education/marketing/lead-magnets/*.html` null coercion ok

## Repo/config
- [x] `render.yaml` com `autoDeploy: true`
- [x] `render.yaml` start command com `PYTHONPATH=academy`
- [x] `docs/deployment/RENDER_ACADEMY.md` atualizado
- [x] `docs/deployment/RENDER_ACADEMY_TROUBLESHOOTING.md` criado
- [x] `scripts/validate_academy_deploy.py` criado

## Pendente (manual no Render)
- [ ] Criar serviço web `praia-digital-academy`
- [ ] Criar banco `academy-db`
- [ ] Vincular `DATABASE_URL`
- [ ] Preencher env vars de produção
- [ ] Validar deploy com `scripts/validate_academy_deploy.py`
