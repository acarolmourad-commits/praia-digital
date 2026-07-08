from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Praia Digital API", version="1.0.0")

class AvaliacaoRequest(BaseModel):
    cidade: str
    tipo: str
    area: float
    quartos: int

class DescricaoRequest(BaseModel):
    tipo: str
    cidade: str
    diferenciais: str

class LeadRequest(BaseModel):
    origem: str
    tempo_resposta: int
    interacoes: int

@app.get("/")
def root():
    return {"service": "Praia Digital API", "status": "online"}

@app.post("/avaliar")
def avaliar_preco(req: AvaliacaoRequest):
    base_por_m2 = {
        "Santos": 7200, "Guarujá": 6800, "Praia Grande": 5400,
        "São Vicente": 4800, "Bertioga": 5100, "Itanhaém": 4600,
        "Peruíbe": 4200, "Mongaguá": 4400
    }
    fator_tipo = {"Apartamento": 1.0, "Casa": 1.15, "Cobertura": 1.35, "Flat": 1.1}
    base = base_por_m2.get(req.cidade, 5000)
    fator = fator_tipo.get(req.tipo, 1.0)
    faixa_min = base * req.area * 0.9 * fator
    faixa_max = base * req.area * 1.15 * fator
    sugestao = (faixa_min + faixa_max) / 2
    return {
        "cidade": req.cidade,
        "tipo": req.tipo,
        "area": req.area,
        "faixa_min": round(faixa_min, 2),
        "faixa_max": round(faixa_max, 2),
        "sugestao": round(sugestao, 2)
    }

@app.post("/descrever")
def gerar_descricao(req: DescricaoRequest):
    diffs = [d.strip() for d in req.diferenciais.split(",") if d.strip()]
    intro = f"Confortoso {req.tipo.lower()} em {req.cidade}, ideal para temporada e moradia."
    destaque = f" Destaques: {', '.join(diffs)}." if diffs else ""
    fechamento = "Agende uma visita e conheça pessoalmente."
    texto = " ".join([intro, destaque, fechamento])
    return {"descricao": texto}

@app.post("/priorizar")
def priorizar_lead(req: LeadRequest):
    score = req.interacoes * 12
    score += 20 if req.tempo_resposta < 30 else 10 if req.tempo_resposta < 60 else 0
    score += 25 if req.origem == "Indicação" else 18 if req.origem == "WhatsApp" else 15 if req.origem == "Google Maps" else 10
    temperatura = "Quente" if score >= 60 else "Morna" if score >= 35 else "Fria"
    acao = "Call em até 24h + proposta comercial." if temperatura == "Quente" else "Follow-up 3h + envio de imóveis parecidos." if temperatura == "Morna" else "Nutrição por conteúdo + follow-up em 7 dias."
    return {"score": score, "temperatura": temperatura, "acao": acao}

@app.get("/health")
def health():
    return {"status": "healthy"}
