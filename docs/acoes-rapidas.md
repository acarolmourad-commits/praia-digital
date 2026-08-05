# Ações Rápidas — Praia Digital
Use este arquivo como atalho operacional.

## 1. Ajustar endpoints de formulário
- Revise arquivos em `lead/`, `education/` e `assets/`
- Garanta que apontem para:
  - `POST /leads`
  - `POST /academy/checkout`

## 2. Expandir SEO/GEO por bairros/cidades
- Scripts: `scripts/gerar_sitemap.py`, `scripts/gerar_bairros.py`
- Páginas: `bairros/*/index.html`, `lead/*/index.html`
- Ação: gerar/atualizar conteúdo local com CTAs para WhatsApp e Academy

## 3. Estado estável / deploy
- Docs: `docs/deploy-render.md`, `docs/post-deploy-activation.md`
- Scripts: `scripts/check_academy_deploy.py`, `scripts/frontend_health_check.py`, `scripts/validate_render_deploy.py`
- Ação: executar deploy manual no Render e validar saúde
