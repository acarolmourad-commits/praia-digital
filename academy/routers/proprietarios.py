from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
from academy.core.database import get_db
from academy.core.models_proprietarios import (
    Proprietario,
    ProprietarioDocumento,
    ProprietarioFoto,
    ProprietarioLog,
    ProprietarioDeclaracao,
    TipoProprietario,
    StatusCadastro,
    StatusDocumentacao,
    VerificacaoNivel,
)
from academy.core.middleware import sanitize_text
from academy.core.owner_email_service import send_recebimento, send_pendencia, send_bloqueio, send_certificacao
from academy.core.publication_service import generate_public_page, update_sitemap
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os, re, uuid

router = APIRouter(tags=["proprietarios"])
CODIGO_RE = re.compile(r"^PD-\d{6}$")

class ProprietarioIn(BaseModel):
    nome_completo: str
    cpf_cnpj: str
    email: EmailStr
    whatsapp: str
    tipo_proprietario: TipoProprietario = TipoProprietario.fisica
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    bairro: Optional[str] = None
    tipo_imovel: Optional[str] = None
    area: Optional[str] = None
    quartos: Optional[str] = None
    suites: Optional[str] = None
    banheiros: Optional[str] = None
    vagas: Optional[str] = None
    condominio: Optional[str] = None
    iptu: Optional[str] = None
    caracteristicas: Optional[str] = None
    diferenciais: Optional[str] = None
    situacao: Optional[str] = None
    disponibilidade: Optional[str] = None
    descricao: Optional[str] = None
    valor_anunciado: Optional[int] = None
    valor_liquido_desejado: Optional[int] = None
    declaracao_versao: str = "v1"
    declaracao_aceite: bool = False

class ProprietarioOut(BaseModel):
    codigo: str
    nome_completo: str
    email: str
    whatsapp: str
    status: StatusCadastro
    nivel_verificacao: VerificacaoNivel
    status_documentacao: StatusDocumentacao
    valor_anunciado: Optional[int]
    valor_liquido_desejado: Optional[int]
    cidade: Optional[str]
    tipo_imovel: Optional[str]
    titulo: Optional[str]
    pagina_url: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class CorrecaoIn(BaseModel):
    campos: dict

class PublicacaoOut(BaseModel):
    codigo: str
    pagina_url: Optional[str]
    status: StatusCadastro
    tracking: Optional[str]

def _generate_codigo(db: Session) -> str:
    last = db.query(Proprietario).order_by(Proprietario.id.desc()).first()
    next_id = (last.id + 1) if last else 1
    return f"PD-{next_id:06d}"

def _log(db: Session, proprietario_id: int, estado_anterior: Optional[str], estado_novo: str, motivo: Optional[str] = None, origem: str = "api"):
    db.add(ProprietarioLog(proprietario_id=proprietario_id, estado_anterior=estado_anterior, estado_novo=estado_novo, motivo=motivo, origem=origem))

VALID_TRANSITIONS = {
    "RECEBIDO": ["AGUARDANDO_ANALISE"],
    "AGUARDANDO_ANALISE": ["EM_ANALISE"],
    "EM_ANALISE": ["APROVADO", "PENDENCIA", "BLOQUEADO"],
    "PENDENCIA": ["REANALISE"],
    "REANALISE": ["PENDENCIA", "BLOQUEADO", "APROVADO"],
    "APROVADO": ["PUBLICADO"],
    "PUBLICADO": ["SUSPENSO"],
    "BLOQUEADO": [],
    "SUSPENSO": ["PUBLICADO"],
}

def _transition(db: Session, proprietario: Proprietario, new_status: StatusCadastro, motivo: Optional[str] = None, origem: str = "api"):
    allowed = VALID_TRANSITIONS.get(proprietario.status.value, [])
    if new_status.value not in allowed:
        raise HTTPException(status_code=409, detail=f"Transição inválida: {proprietario.status.value} -> {new_status.value}")
    old = proprietario.status.value
    proprietario.status = new_status
    _log(db, proprietario.id, old, new_status.value, motivo, origem)
    db.commit()
    db.refresh(proprietario)

@router.post("/proprietarios", response_model=ProprietarioOut)
def create_proprietario(payload: ProprietarioIn, db: Session = Depends(get_db)):
    if not payload.declaracao_aceite:
        raise HTTPException(status_code=400, detail="Declaração de responsabilidade não aceita.")
    if payload.valor_liquido_desejado is not None and payload.valor_anunciado is not None and payload.valor_liquido_desejado > payload.valor_anunciado:
        raise HTTPException(status_code=400, detail="Valor líquido desejado não pode ser maior que o valor anunciado.")
    codigo = _generate_codigo(db)
    p = Proprietario(
        codigo=codigo,
        nome_completo=sanitize_text(payload.nome_completo),
        cpf_cnpj=sanitize_text(payload.cpf_cnpj),
        email=sanitize_text(payload.email),
        whatsapp=sanitize_text(payload.whatsapp),
        tipo_proprietario=payload.tipo_proprietario,
        endereco=sanitize_text(payload.endereco or ""),
        cidade=sanitize_text(payload.cidade or ""),
        bairro=sanitize_text(payload.bairro or ""),
        tipo_imovel=sanitize_text(payload.tipo_imovel or ""),
        area=sanitize_text(payload.area or ""),
        quartos=sanitize_text(payload.quartos or ""),
        suites=sanitize_text(payload.suites or ""),
        banheiros=sanitize_text(payload.banheiros or ""),
        vagas=sanitize_text(payload.vagas or ""),
        condominio=sanitize_text(payload.condominio or ""),
        iptu=sanitize_text(payload.iptu or ""),
        caracteristicas=sanitize_text(payload.caracteristicas or ""),
        diferenciais=sanitize_text(payload.diferenciais or ""),
        situacao=sanitize_text(payload.situacao or ""),
        disponibilidade=sanitize_text(payload.disponibilidade or ""),
        descricao=sanitize_text(payload.descricao or ""),
        valor_anunciado=payload.valor_anunciado,
        valor_liquido_desejado=payload.valor_liquido_desejado,
        status=StatusCadastro.RECEBIDO,
        nivel_verificacao=VerificacaoNivel.CADASTRO_RECEBIDO,
        status_documentacao=StatusDocumentacao.PENDENTE,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    db.add(ProprietarioDeclaracao(proprietario_id=p.id, versao_termo=sanitize_text(payload.declaracao_versao), aceite=True))
    db.add(ProprietarioLog(proprietario_id=p.id, estado_anterior=None, estado_novo=StatusCadastro.RECEBIDO.value, origem="api", motivo="criacao"))
    db.commit()
    db.refresh(p)
    _transition(db, p, StatusCadastro.AGUARDANDO_ANALISE, motivo="Cadastro recebido", origem="sistema")
    send_recebimento(p.email, p.codigo)
    return p

@router.get("/proprietarios/{codigo}", response_model=ProprietarioOut)
def get_proprietario(codigo: str, db: Session = Depends(get_db)):
    if not CODIGO_RE.match(codigo):
        raise HTTPException(status_code=400, detail="Código inválido.")
    p = db.query(Proprietario).filter(Proprietario.codigo == codigo).first()
    if not p:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado.")
    return p

@router.post("/proprietarios/{codigo}/documentos")
async def upload_documento(codigo: str, file: UploadFile = File(...), tipo_documento: str = Form(...), db: Session = Depends(get_db)):
    p = db.query(Proprietario).filter(Proprietario.codigo == codigo).first()
    if not p:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado.")
    if p.status.value in [StatusCadastro.BLOQUEADO.value, StatusCadastro.SUSPENSO.value]:
        raise HTTPException(status_code=409, detail="Cadastro bloqueado/suspenso.")
    uploads_root = os.path.abspath(os.path.join("uploads", "proprietarios", codigo, "documentos"))
    os.makedirs(uploads_root, exist_ok=True)
    ext = os.path.splitext(file.filename or "")[1].lower()
    allowed = {".pdf", ".jpg", ".jpeg", ".png", ".webp"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Formato de documento não permitido.")
    dest_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(uploads_root, dest_name)
    content = await file.read()
    with open(dest_path, "wb") as f:
        f.write(content)
    doc = ProprietarioDocumento(proprietario_id=p.id, tipo_documento=sanitize_text(tipo_documento), caminho_privado=dest_path, nome_arquivo=sanitize_text(file.filename or dest_name), tamanho_bytes=len(content), mime_type=file.content_type or "application/octet-stream", status="pendente")
    db.add(doc)
    db.commit()
    p.status_documentacao = StatusDocumentacao.RECEBIDA
    db.commit()
    db.refresh(p)
    return {"ok": True, "documento_id": doc.id}

@router.post("/proprietarios/{codigo}/fotos")
async def upload_foto(codigo: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    p = db.query(Proprietario).filter(Proprietario.codigo == codigo).first()
    if not p:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado.")
    if p.status.value in [StatusCadastro.BLOQUEADO.value, StatusCadastro.SUSPENSO.value]:
        raise HTTPException(status_code=409, detail="Cadastro bloqueado/suspenso.")
    uploads_root = os.path.abspath(os.path.join("uploads", "proprietarios", codigo, "fotos"))
    os.makedirs(uploads_root, exist_ok=True)
    ext = os.path.splitext(file.filename or "")[1].lower()
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Formato de foto não permitido.")
    dest_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(uploads_root, dest_name)
    content = await file.read()
    with open(dest_path, "wb") as f:
        f.write(content)
    foto = ProprietarioFoto(proprietario_id=p.id, caminho_publico=dest_path, nome_arquivo=sanitize_text(file.filename or dest_name), aprovada=False)
    db.add(foto)
    db.commit()
    db.refresh(foto)
    return {"ok": True, "foto_id": foto.id}

@router.post("/proprietarios/{codigo}/analisar", response_model=ProprietarioOut)
def analisar_cadastro(codigo: str, db: Session = Depends(get_db)):
    p = db.query(Proprietario).filter(Proprietario.codigo == codigo).first()
    if not p:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado.")
    _transition(db, p, StatusCadastro.EM_ANALISE, motivo="Inicio da analise automatica", origem="hermes")
    docs = db.query(ProprietarioDocumento).filter(ProprietarioDocumento.proprietario_id == p.id).all()
    fotos = db.query(ProprietarioFoto).filter(ProprietarioFoto.proprietario_id == p.id).all()
    pendencias = []
    if not docs:
        pendencias.append("documentacao_ausente")
    if len(fotos) < 2:
        pendencias.append("fotos_insuficientes")
    if pendencias:
        p.status_documentacao = StatusDocumentacao.PENDENTE if not docs else p.status_documentacao
        _transition(db, p, StatusCadastro.PENDENCIA, motivo=" | ".join(pendencias), origem="hermes")
        send_pendencia(p.email, p.codigo, pendencias, f"https://praia.digital/proprietarios/{p.codigo.lower()}/corrigir")
        return p
    p.status_documentacao = StatusDocumentacao.VALIDADA
    _transition(db, p, StatusCadastro.APROVADO, motivo="Documentos e fotos validados", origem="hermes")
    p.nivel_verificacao = VerificacaoNivel.DOCUMENTACAO_VALIDADA
    db.commit()
    db.refresh(p)
    return p

@router.post("/proprietarios/{codigo}/publicar", response_model=PublicacaoOut)
def publicar_cadastro(codigo: str, db: Session = Depends(get_db)):
    p = db.query(Proprietario).filter(Proprietario.codigo == codigo).first()
    if not p:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado.")
    if p.status.value != StatusCadastro.APROVADO.value:
        raise HTTPException(status_code=409, detail="Apenas cadastros APROVADOS podem ser publicados.")
    _transition(db, p, StatusCadastro.PUBLICADO, motivo="Publicacao automatica", origem="sistema")
    tracking_id = f"pub-{p.codigo.lower()}"
    url = generate_public_page(p, db=db)
    p.pagina_url = url
    update_sitemap([url])
    db.commit()
    db.refresh(p)
    send_certificacao(p.email, p.codigo, url, p.valor_anunciado or 0, p.nivel_verificacao.value)
    return {"codigo": p.codigo, "pagina_url": url, "status": p.status, "tracking": tracking_id}

@router.post("/proprietarios/{codigo}/corrigir", response_model=ProprietarioOut)
def corrigir_cadastro(codigo: str, payload: CorrecaoIn, db: Session = Depends(get_db)):
    p = db.query(Proprietario).filter(Proprietario.codigo == codigo).first()
    if not p:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado.")
    if p.status.value != StatusCadastro.PENDENCIA.value:
        raise HTTPException(status_code=409, detail="Somente cadastros em PENDENCIA podem ser corrigidos.")
    allowed_fields = {"nome_completo","cpf_cnpj","email","whatsapp","endereco","cidade","bairro","tipo_imovel","area","quartos","suites","banheiros","vagas","condominio","iptu","caracteristicas","diferenciais","situacao","disponibilidade","descricao","valor_anunciado","valor_liquido_desejado"}
    for k, v in payload.campos.items():
        if k not in allowed_fields:
            continue
        setattr(p, k, sanitize_text(str(v)) if v is not None else None)
    db.commit()
    db.refresh(p)
    _transition(db, p, StatusCadastro.REANALISE, motivo="Correcao enviada", origem="proprietario")
    return p
