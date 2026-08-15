# Rollback — Academy

## Objetivo
Reverter para o último estado bom quando um deploy causar falha estrutural.

## Gatilhos de rollback
- `/health` indisponível após deploy
- `/courses` retornando erro ou lista vazia
- Checkout indisponível para slugs reais
- Erro 5xx em rotas públicas
- Regressão estrutural detectada por `scripts/regression_check.py`
- Deploy do GitHub Pages com site indisponível

## Procedimento rápido
1. Identificar último commit/artifact bom
2. Reverter alterações no repositório quando aplicável
3. Reaplicar variáveis de ambiente
4. Redeploy do estado bom
5. Rodar `scripts/validate_academy_prod.py`
6. Confirmar estabilidade

## GitHub Pages
- Reverter commit que causou quebra
- Ou usar versão anterior do artifact no Actions
- Validar homepage e rotas públicas

## Railway/Render
- Usar releases/versões anteriores do provedor
- Confirmar variáveis de ambiente mantidas
- Validar `/health`, `/courses`, checkout

## Observações
- Não fazer rollback por diferenças pequenas de conteúdo
- Registrar causa-raiz antes de reaplicar deploy
- Nunca apagar histórico de deploy sem necessidade
