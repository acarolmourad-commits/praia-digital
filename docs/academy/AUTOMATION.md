# Automação — Academy

## Objetivo
Tornar o deploy e a operação da Academy o mais autônomos possível, sem comprometer segurança ou inventar credenciais.

## Estado atual
- CI/CD: GitHub Actions em `.github/workflows/academy-ci.yml`
- Deploy preview: GitHub Pages automático em push para `main`
- Validação pré-deploy: `scripts/validate_render_deploy.py`
- Validação pós-deploy: `scripts/validate_academy_prod.py`
- Regressão: `scripts/regression_check.py`
- Monitoramento: `scripts/weekly_academy_check.py` + cron `academy-production-monitor`

## Matriz humano × automático

| Item | Automatizável? | Ação / Observação |
|------|----------------|-------------------|
| Build | sim | GitHub Actions instala deps e valida imports |
| Testes | sim | `pytest` rodado em `academy/tests/` |
| Deploy | parcial | GitHub Pages automático; deploy produção depende de provedor configurado |
| Secrets | não | Humanos devem configurar no provedor; nunca commitar |
| OAuth/2FA | não | Configuração manual quando aplicável |
| DNS | não | Configuração manual no registrador |
| Checkout | sim | Validado por `scripts/validate_academy_prod.py` |
| Webhook | sim | Validado por script pós-deploy |
| Entrega do curso | sim | Validada por script pós-deploy |
| Tracking | sim | Validado por checklist/manual; snippet GA4 presente |
| Smoke tests | sim | Automatizados em CI |
| Regressão | sim | `scripts/regression_check.py` |
| Rollback | parcial | Depende de provedor; GitHub Pages suporta rollback via workflow/redeploy |
| Monitoramento | sim | `academy-production-monitor` ativo |

## Sequência recomendada

1. Humano configura secrets no provedor
2. CI roda em push/PR: testes → validação pré-deploy → deploy preview → validação pós-deploy
3. Se provedor tiver deploy automático por webhook/branch, habilitar; senão, usar deploy manual quando solicitado
4. Em caso de falha: CI alerta; humano corrige; CI revalida

## Procedimentos

### Deploy automático
- Trigger: push em `main`
- Passos: install → lint/import check → pytest → pre-deploy validation → GitHub Pages deploy → production validation

### Deploy produção (Railway/Render)
- Necessário: secrets configurados no provedor
- Automático se provedor estiver ligado ao repo; senão, humano inicia deploy manualmente
- Pós-deploy: `python scripts/validate_academy_prod.py`

### Rollback
- GitHub Pages: reverter commit ou usar versão anterior do artifact
- Railway/Render: usar painel do provedor; se houver releases anteriores, selecionar release estável
- Gatilho: smoke test crítico falhando, homepage indisponível, rota `/health` indisponível, regressão estrutural grave

### Monitoramento
- Monitor diário: `academy-production-monitor`
- Check manual rápido: `python scripts/check_academy_prod.py`
- Validação pós-deploy: `python scripts/validate_academy_prod.py`
- Regressão: `python scripts/regression_check.py`

## Segurança
- Nunca commitar `.env` com credenciais
- Usar secrets do GitHub/variáveis do provedor
- Não expor tokens em logs
- Não desabilitar autenticação para facilitar deploy
- Se faltar variável obrigatória, parar etapa e informar exatamente qual variável humana deve configurar

## Limitações conhecidas
- Sem sandbox de pagamento configurado → testes de checkout/webhook são de leitura/validação, não simulação de compra
- Produção depende de provedor; este CI não substitui deploy do Railway/Render sem integração adicional
