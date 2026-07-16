# Expansão D — Funil B2C Norte (donos de imóvel)

**Descoberta de dados (16/07):** dos 63 artigos de SEO do Litoral Norte, **25–26 têm intenção B2C forte** (proprietário/renda/temporada/investir) e **zero B2B**. Ou seja, o tráfego de norte já atrai o DONO do imóvel — nosso público-core de Gestão Completa — mas o outbound B2C cobre só sul/centro. A Expansão B (CTA B2B) estava nos artigos certos, mas **deixava o proprietário escapar**.

## Plano
- `scripts/injetar_cta_b2c_norte.py` injeta CTA "Simule seu yield em {cidade}" nos 26 artigos B2C de norte (idempotente).
- CTA aponta para `assets/calculadora-widget-standalone.html?tenant=pd-norte`.
- `parceiro_id` desativado para tenant `pd-*` (cai no tracker B2C geral, não no white-label).
- Lead B2C norte entra no mesmo outbound de gestão completa (cron 18h dispara Msg1-3).

## Status: ✅ executada
- 26 artigos B2C norte com CTA de simulação.
- Calculadora standalone ajustada para não atribuir `pd-*` como white-label.
- Reuso total do funil B2C existente (sem nova base de leads).

## Próximos passos
- [ ] Publicar no GitHub Pages (landings + calculadora já estão no repo)
- [ ] Acompanhar leads norte no tracker B2C (cidade=Ubatuba/Ilhabela/Caraguatatuba)
