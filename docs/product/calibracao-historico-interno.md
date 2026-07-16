# Calibração da Calculadora — Histórico Interno (Pré-requisito de Precisão)

**Status:** a calculadora está **ao vivo** (`praia.digital/assets/calculadora-widget-standalone.html`) mas roda em modo **"estimativa base"** porque o cache interno está vazio. Para virar **"precisão interna"** (ADR/ocupação reais por CEP), falta 1 exportação da Praia Digital.

## Por que não dá pra calibrar sozinho
- **ViaCEP**: só geografia (CEP→cidade). ✅ usado.
- **FipeZap**: sem API pública (domínio não resolve + CORS). ❌
- **Inside Airbnb**: bloqueado (AccessDenied). ❌
- **AirDNA**: pago. ❌
- **Blog da PD**: não tem preços estruturados extraíveis. ❌
- **Única fonte real**: os CONTRATOS DE GESTÃO da própria Praia Digital.

## Passo operacional (equipe PD, 1x)
1. Exportar do PMS a planilha de reservas/contratos (1 linha por imóvel/ano):
   `cep, tipo, quartos, adr_medio, ocupacao, n_noites_ano, receita_ano, periodo_inicio, periodo_fim`
   (ocupacao em 0..1, ex: 0.68)
2. Salvar em `docs/data/reservas-internas.csv` (ou gerar template: `python scripts/ingest_historico_interno.py --template`)
3. Rodar: `python scripts/ingest_historico_interno.py`
4. Resultado: `docs/data/historico_interno_cep.json` com `modo=precisao_interna` por CEP.
5. A calculadora (endpoint e standalone) passa a usar ocupação/ADR reais.

## Validação já feita
- `ingest_historico_interno.py --demo` gera cache sintético e o endpoint retorna `precisao_interna` (testado em 16/07).
- Template `--template` cria a planilha pronta para preenchimento.

## Decisão
Não inventar dados de mercado. Enquanto a exportação não vier, a calculadora entrega **estimativa base** honesta (marcada no resultado como "estimativa").
