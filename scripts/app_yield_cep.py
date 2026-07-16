#!/usr/bin/env python3
"""
API stub — Calculadora de Yield Preditivo por CEP (Praia Digital)
Endpoint: POST /api/v1/yield/estimate
Consome: ViaCEP (CEP->coords) + docs/data/historico_interno_cep.json (cache interno)
Motor de cálculo: herdado do simulador-roi-proprietario.html (+28% ADR, +12% ocup vs autogestao).

MVP: roda 100% offline (sem AirDNA). Se cache interno vazio -> "estimativa base".
Uso: uvicorn app_yield_cep:app --reload --port 8000
"""
import os, json, urllib.request
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
sys.path.insert(0, os.path.dirname(__file__))
import lead_capture

REPO = r"C:/Users/Carolina/praia-digital"
CACHE = os.path.join(REPO, "docs/data/historico_interno_cep.json")
FRONT = os.path.join(REPO, "assets/calculadora-yield-cep.html")
COMISSAO = 0.20  # Praia Digital

# Tenants white-label (Expansao C). Em produção viria de DB; aqui hardcoded p/ MVP.
TENANTS = {
    "padrao": {"nome": "Praia Digital", "cor": "#22d3ee", "logo": "📈 Praia Digital"},
    "santos-ancora": {"nome": "Prime Imóveis Santos", "cor": "#f59e0b", "logo": "🏢 Prime Imóveis"},
    "demo": {"nome": "Imobiliária Parceira", "cor": "#4ade80", "logo": "🤝 Parceira PD"},
}

app = FastAPI(title="Praia Digital — Yield Preditivo por CEP (White-label)", version="0.2")

# ---------- Schemas ----------
class EstimateIn(BaseModel):
    cep: str
    tipo: str = "apartamento"
    quartos: int = Field(1, ge=0, le=5)
    banheiros: Optional[int] = None
    hospedes_max: Optional[int] = None
    metragem_m2: Optional[float] = None
    comodidades: List[str] = []
    valor_aquisicao: Optional[float] = None
    custos_fixos_mensais: Optional[float] = None
    autogestor: Optional[bool] = None
    plataformas: List[str] = []

# ---------- Helpers ----------
def resolve_cep(cep: str) -> dict:
    digits = "".join(filter(str.isdigit, cep))
    if len(digits) != 8:
        raise HTTPException(404, "CEP inválido (precisa de 8 dígitos)")
    url = f"https://viacep.com.br/ws/{digits}/json/"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            d = json.load(r)
    except Exception:
        raise HTTPException(502, "Falha ao consultar ViaCEP")
    if d.get("erro"):
        raise HTTPException(404, "CEP não encontrado")
    return d

def load_cache() -> dict:
    if not os.path.exists(CACHE):
        return {}
    return json.load(open(CACHE, encoding="utf-8")).get("por_cep", {})

def calc_yield(inp: EstimateIn, cep_data: dict, cache: dict) -> dict:
    digits = "".join(filter(str.isdigit, inp.cep))
    interno = cache.get(digits) or cache.get(inp.cep)
    # ADR e ocupação base (modo degradado)
    if interno:
        adr_base = interno["adr_medio"]
        ocup_base = interno["ocupacao"]
        confianca = 0.8
        fontes = ["historico_interno"]
    else:
        # estimativa base por tipo/quartos (heurística MVP, rotulada)
        adr_base = 220 + inp.quartos * 90 + (40 if "casa" in inp.tipo else 0)
        ocup_base = 0.55
        confianca = 0.4
        fontes = ["viacep", "heuristica_mvp"]
    # ajustes de comodidade (impacto em ADR)
    bump = 0
    if "piscina" in inp.comodidades: bump += 0.08
    if "ar_condicionado" in inp.comodidades: bump += 0.04
    if "vagas_1" in inp.comodidades or "vagas_2" in inp.comodidades: bump += 0.03
    if "vista_mar" in inp.comodidades: bump += 0.12
    adr = adr_base * (1 + bump)
    ocup = min(ocup_base + (0.05 if inp.comodidades else 0), 0.92)
    # Precificação dinâmica: +28% ADR vs autogestão (herdado do simulador)
    adr_dinamico = adr * 1.28
    receita_bruta = adr_dinamico * ocup * 365
    custos_anuais = (inp.custos_fixos_mensais or 0) * 12
    receita_liq = receita_bruta * (1 - COMISSAO) - custos_anuais
    yield_a = (receita_liq / inp.valor_aquisicao) if inp.valor_aquisicao else None
    # comparativo aluguel tradicional (~ R$/m2 * m2, simplificado)
    m2 = inp.metragem_m2 or (30 + inp.quartos * 18)
    aluguel_longa = m2 * 38  # R$/m2 médio litoral/SP
    mult = (receita_liq / 12) / aluguel_longa if aluguel_longa else None
    sazonal = [{"mes": m, "ocup": round(min(ocup + (0.12 if m in (1,7,12,12) else 0) - (0.06 if m in (3,4,5) else 0), 0.95), 2)} for m in range(1, 13)]
    return {
        "cep_resolvido": {"bairro": cep_data.get("bairro"), "cidade": cep_data.get("localidade"),
                          "uf": cep_data.get("uf"), "ibge": cep_data.get("ibge")},
        "adr_medio": round(adr_dinamico, 2),
        "ocupacao_estimada": round(ocup, 3),
        "confianca": {"pessimista": round(ocup*0.85, 3), "realista": round(ocup, 3), "otimista": round(min(ocup*1.12, 0.95), 3)},
        "receita_bruta_anual": round(receita_bruta, 2),
        "receita_liq_praiadigital": round(receita_liq, 2),
        "yield_a_a": round(yield_a, 4) if yield_a else None,
        "comparativo_aluguel_longa": round(aluguel_longa, 2),
        "fator_multiplicador": round(mult, 2) if mult else None,
        "sazonalidade": sazonal,
        "modo": "precisao_interna" if interno else "estimativa_base",
        "fontes_usadas": fontes,
    }

# ---------- Rotas ----------
@app.post("/api/v1/yield/estimate")
def estimate(inp: EstimateIn):
    cep_data = resolve_cep(inp.cep)
    cache = load_cache()
    return calc_yield(inp, cep_data, cache)

@app.get("/health")
def health():
    return {"status": "ok", "data": date.today().isoformat()}

# ---------- Captura de lead ----------
class LeadIn(BaseModel):
    nome: str
    whatsapp: str
    email: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    yield_estimado: Optional[float] = None
    consentimento_lgpd: bool = False
    payload_estimate: Optional[dict] = None
    parceiro_id: Optional[str] = None

@app.post("/api/v1/lead/capture")
def capture(inp: LeadIn):
    try:
        res = lead_capture.capturar(
            nome=inp.nome, telefone=inp.whatsapp, cidade=inp.cidade,
            cep=inp.cep, yield_estimado=inp.yield_estimado,
            email=inp.email, consentimento_lgpd=inp.consentimento_lgpd,
            parceiro_id=inp.parceiro_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    if res["status"] == "ja_existente":
        return {"status": "ok", "detail": "lead ja existia no tracker", "telefone": res["telefone"]}
    return {"status": "created", "detail": "lead no tracker (origem=calc-cep, Status=pendente_msg1)",
            "telefone": res["telefone"], "parceiro_id": res.get("parceiro_id")}

# ---------- Widget white-label (Expansao C) ----------
from fastapi.responses import HTMLResponse
@app.get("/widget/{tenant}", response_class=HTMLResponse)
def widget(tenant: str):
    t = TENANTS.get(tenant, TENANTS["padrao"])
    try:
        html = open(FRONT, encoding="utf-8").read()
    except FileNotFoundError:
        raise HTTPException(404, "front nao encontrado")
    # injeta marca da parceira no titulo e no script (PARCEIRO_ID + cor)
    html = html.replace("📈 Calculadora de Yield Preditivo", f"{t['logo']} · Calculadora de Yield")
    html = html.replace("<title>Calculadora de Yield Preditivo — Praia Digital</title>",
                         f"<title>{t['logo']} · Calculadora de Yield — Praia Digital</title>")
    html = html.replace("--ciano:#22d3ee;", f"--ciano:{t['cor']};")
    html = html.replace("const API = \"http://127.0.0.1:8000\";",
                         f"const API = \"http://127.0.0.1:8000\";\nconst PARCEIRO_ID = \"{tenant}\";")
    # passa parceiro_id no capture
    html = html.replace("consentimento_lgpd:true})",
                         "consentimento_lgpd:true, parceiro_id: PARCEIRO_ID})")
    return HTMLResponse(html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
