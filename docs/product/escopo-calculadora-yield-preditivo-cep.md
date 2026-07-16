# Escopo — Calculadora de Yield Preditivo por CEP

**Produto:** Praia Digital · PropTech de gestão de temporada
**Autor:** PM (PropTech) · **Status:** Draft p/ refinamento com dev
**Versão:** 0.1 (MVP)

---

## 1. Visão do Produto

Ferramenta web self-service onde um proprietário (ou investidor) digita o **CEP do imóvel + características básicas** e recebe, em < 10s, uma **projeção de yield (retorno) de aluguel por temporada** para aquela micro-região — ocupação estimada, diária média, receita líquida anual e comparação com aluguel tradicional. O objetivo de negócio é **gerar "uau" e capturar o lead qualificado no final da simulação**, alimentando o funil de vendas (que hoje já roda via WhatsApp/e-mail).

> **Reuso (não reinventar):** já existe `assets/simulador-roi-proprietario.html` (calcula +28% diária e +12% ocupação). Esta feature é a **evolução geolocalizada** dele: em vez de inputs manuais de preço, puxa dados reais da região por CEP. O motor de cálculo atual vira um módulo interno.

---

## 2. Objetivo & Métricas de Sucesso (MVP)

| Métrica | Meta MVP |
|--------|----------|
| Taxa de conclusão da simulação | ≥ 65% |
| Taxa de captura de lead (form preenchido) | ≥ 35% dos que concluíram |
| Tempo até o 1º resultado "uau" | < 4s após CEP |
| Leads gerados/mês (pós-lançamento) | 200+ |
| % de leads que entram no follow-up automático | 100% (integração obrigatória) |

---

## 3. Inputs do Usuário Final

**Etapa 1 — Baixo atrito (3 campos, tela inicial):**
- **CEP** (obrigatório) — texto máscara `00000-000`, autocomplete de bairro/cidade
- **Tipo de imóvel** (obrigatório) — Apartamento / Casa / Studio / Cobertura / Kitnet
- **Nº de quartos** (obrigatório) — select 0–5+

**Etapa 2 — Enriquecimento (opcional, melhora precisão, usa progressive disclosure):**
- Nº de banheiros
- Capacidade máx. de hóspedes
- Metragem (m²)
- Comodidades (chips): piscina, ar-condicionado, vaga de garagem, varanda, churrasqueira, vista mar, portaria 24h
- **Valor de aquisição / investimento total** (para ROI sobre capital)
- Custos fixos mensais: condomínio + IPTU + taxas (para lucro líquido real)
- Já anuncia sozinho? (sim/não) + plataforma (Airbnb/Booking/ambas) — *triagem de autogestor (nossa melhor persona)*

> Regra de UX: a simulação roda com só a Etapa 1; a Etapa 2 refina o número e destrava o "relatório completo" (gating de lead).

---

## 4. Fontes de Dados & APIs Externas

| Fonte | Uso no cálculo | Custo | Fallback |
|------|----------------|-------|----------|
| **ViaCEP / BrasilAPI / Postmon** | CEP → bairro, cidade, UF, coords | Gratuito | Cache interno |
| **Google Maps Geocoding + Distance Matrix** | Distância até praia/centro/atrações (impacta ADR) | Pago/uso | OpenStreetMap Nominatim (grátis) |
| **AirDNA API** (ou AllTheRooms / KeyData) | Ocupação média real e ADR por micro-região (gold standard) | Pago (assim que escalar) | Inside Airbnb (dataset grátis, pipeline próprio) + histórico interno |
| **Histórico interno Praia Digital** (CRM) | Ocupação/ADR **reais** dos imóveis que já gerimos por CEP | Gratuito (já temos) | — (fonte prioritária por ser a mais próxima da verdade) |
| **feriados.com.br / calendário nacional-SP** | Sazonalidade de demanda (feriados prolongados) | Gratuito | Tabela estática interna |
| **Eventbrite / Ticketmaster API** | Eventos locais (virada ocupação) | Gratuito (free tier) | Scraping de portais de eventos |
| **Open-Meteo / INMET** | Sazonalidade climática de praia | Gratuito | — |
| **FipeZap / ZAP Imóveis** | Valor de mercado do m² e valorização (p/ ROI) | Scraping limitado / parceria | Entrada manual do usuário (Etapa 2) |

**Princípio de fonte:** priorizar sempre o **histórico interno** (mais preciso pro nosso modelo de gestão) > AirDNA (mercado) > Inside Airbnb (grátis, lag) > entrada manual.

---

## 5. Modelo de Cálculo (como vira "yield")

```
ADR_estimado = f(ADR_região, tipo, quartos, comodidades, distância_praia, sazonalidade)
Ocupação_estimada = f(ocupação_região, tipo, comodidades, eventos.locais, clima)
Receita_bruta_anual = ADR_estimado × ocupação × 365
Receita_liq_PraiaDigital = Receita_bruta × (1 - 0,20 comissão) - custos_fixos
Yield_s/temporada = Receita_liq_PraiaDigital / investimento_total
Comparativo = Receita_liq_PraiaDigital vs. aluguel_tradicional_longa(m² × preço/m²_local)
```

- **Precificação dinâmica** já aplicada no ADR (ajuste por dia da semana/evento) — herda do motor do simulador existente.
- Apresentar **intervalo de confiança** (pessimista/realista/otimista) em vez de número único → credibilidade.

---

## 6. Layout & UX (efeito "uau")

**Tela 1 — Hero:** fundo com mapa animado (Leaflet/Mapbox) mostrando o **raio do CEP** + **heatmap de demanda** da região. Campo CEP gigante no centro. Microcopy: *"Descubra quanto seu imóvel pode render sem você levantar um dedo."*

**Tela 2 — Resultado (acima da dobra):**
- **Gauge animado de Yield %** (ex: 11,4% a.a.) com contador subindo.
- **Três cards com contadores animados:** Receita líquida/ano · Ocupação estimada · Diária média.
- **Barra comparativa:** "Aluguel tradicional R$ X/mês 🆚 Gestão Praia Digital R$ Y/mês (2,8× mais)".

**Tela 3 — "Quanto você está deixando na mesa":**
- Slider de tempo (6m/1a/2a) que mostra o **dinheiro acumulado perdido** com autogestão vs. gestão. Efeito de perda → gatilho de ação.

**Tela 4 — Relatório completo (GATED):**
- Timeline de receita 12 meses (área animada).
- Break-even do investimento.
- Mapa de calor sazonal.
- **CTA final:** *"Receba esse relatório completo + seu plano personalizado no WhatsApp."*

---

## 7. Captura de Lead & Handoff (integração obrigatória)

- **Gating:** relatório completo (Tela 4) só após form: **Nome + WhatsApp + e-mail** (WhatsApp obrigatório, outros opcionais).
- **Consentimento LGPD:** checkbox "autorizo contato" explícito (art. 7º, VIII).
- **Handoff automático:** ao capturar, o lead entra no **tracker do outbound existente** (`tracker-whatsapp-proprietarios.csv`) com `Status=pendente_msg1` e origem=`calc-cep`. O cron das 18h já dispara a sequência de 3 mensagens + follow-up. **Zero trabalho manual de vendas no dia 1.**
- **Enriquecimento:** gravar CEP, tipo, quartos, yield estimado e flag `autogestor` no tracker → permite segmentar a abordagem.

---

## 8. MVP vs. Futuro

**MVP (6–8 sem):** CEP + tipo + quartos → yield/ocupação/comparativo + captura de lead + handoff no outbound. Fontes: ViaCEP + histórico interno + Inside Airbnb + feriados.
**Futuro:** AirDNA pago, eventos em tempo real, mapa 3D, export PDF do relatório, AB test de copy, retargeting.

---

## 9. Riscos & Compliance

- **LGPD:** dados de contato só com consentimento; não vazar origem de terceiros.
- **ToS Airbnb:** não exibir dados da plataforma como "oficiais"; rotular como "estimativa".
- **Precisão:** never prometer yield garantido — usar intervalo de confiança.
- **CPF/CNPJ do lead:** não coletar na simulação (reduz atrito); pegar no fechamento.

## 10. Requisitos Técnicos (sugestão)

- Front: React/Vite + Leaflet (mapa) + Framer Motion (animações de contador/gauge).
- Back: Python (FastAPI) — reaproveita `gerar_relatorio_executivo.py` e o motor do `simulador-roi-proprietario.html`.
- Cache: Redis p/ respostas por CEP (reduz custo de API).
- Storage lead: mesmo CSV/CRM do outbound (consistência).
