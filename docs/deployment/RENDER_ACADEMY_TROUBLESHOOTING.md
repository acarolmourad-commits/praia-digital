# Render Academy — troubleshooting pós-deploy

Use este arquivo quando o build/start falhar no Render.

## Build

### pip install trava em dependência pesada
- Verifique `academy/requirements.txt`
- Remova bibliotecas opcionais não usadas
- Teste local com `pip install -r academy/requirements.txt`

### Python version mismatch
- Render pode usar Python 3.11 por padrão; se o projeto exigir outra, defina `runtime: python-3.11` no `render.yaml`

## Start

### `ModuleNotFoundError: No module named 'academy'`
- Causa: `PYTHONPATH` errado no start command
- Fix já aplicado em `render.yaml`: `PYTHONPATH=academy uvicorn academy.main:app --host 0.0.0.0 --port $PORT`

### `ImportError` em routers/models
- Verifique se todos os arquivos em `academy/routers/*.py` existem no branch `main`
- Faça um novo deploy após ajustar

### Port/bind
- Render injeta `$PORT` automaticamente; não hardcode `8000`

## Banco

### `could not translate host name to address`
- Verifique se o banco `academy-db` está provisionado e vinculado
- Confirme que `DATABASE_URL` vem do `fromDatabase` no `render.yaml`

### `FATAL: database "academy" does not exist`
- Confirme `databaseName: academy` no recurso de banco

### Tabelas ausentes
- O app chama `Base.metadata.create_all(bind=engine)` no startup
- Se o banco estiver vazio, as tabelas são criadas no primeiro start

## Variáveis de ambiente

### `SECRET_KEY` vazia
- Gere um segredo forte no Render ou use `generateValue: true`
- Sem isso, auth/login quebram em produção

### CORS bloqueando frontend
- `ALLOWED_ORIGINS` deve incluir `https://praia.digital,https://www.praia.digital,https://academy.praia.digital`
- Em desenvolvimento pode usar `*`

### E-mail/WhatsApp/Mercado Pago
- Os serviços rodam mesmo com essas vars vazias, mas automações/pagamentos ficam no ar
- Preencha quando os integradores estiverem prontos

## Validar após deploy

```bash
python scripts/validate_academy_deploy.py
```

Esperado:
- `/health` 200
- `/docs` 200
- `/auth/register` 200 com token
- `/leads` 200 com lead criado

Se algo falhar, abra os logs do serviço no Render: eles mostram o traceback exato do startup.
