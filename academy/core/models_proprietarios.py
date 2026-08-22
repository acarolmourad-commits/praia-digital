from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from academy.core.database import Base
import enum


class TipoProprietario(str, enum.Enum):
    fisica = "fisica"
    juridica = "juridica"


class StatusCadastro(str, enum.Enum):
    RECEBIDO = "RECEBIDO"
    AGUARDANDO_ANALISE = "AGUARDANDO_ANALISE"
    EM_ANALISE = "EM_ANALISE"
    PENDENCIA = "PENDENCIA"
    REANALISE = "REANALISE"
    APROVADO = "APROVADO"
    PUBLICADO = "PUBLICADO"
    BLOQUEADO = "BLOQUEADO"
    SUSPENSO = "SUSPENSO"


class StatusDocumentacao(str, enum.Enum):
    PENDENTE = "DOCUMENTACAO_PENDENTE"
    RECEBIDA = "DOCUMENTACAO_RECEBIDA"
    VALIDADA = "DOCUMENTACAO_VALIDADA"
    DIVERGENTE = "DOCUMENTACAO_DIVERGENTE"
    REJEITADA = "DOCUMENTACAO_REJEITADA"


class VerificacaoNivel(str, enum.Enum):
    CADASTRO_RECEBIDO = "CADASTRO_RECEBIDO"
    IDENTIDADE_VERIFICADA = "IDENTIDADE_VERIFICADA"
    DOCUMENTACAO_VALIDADA = "DOCUMENTACAO_VALIDADA"
    ANUNCIO_APROVADO = "ANUNCIO_APROVADO"


class Proprietario(Base):
    __tablename__ = "proprietarios"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False, unique=True, index=True)
    nome_completo = Column(String(200), nullable=False)
    cpf_cnpj = Column(String(30), nullable=False)
    email = Column(String(200), nullable=False)
    whatsapp = Column(String(40), nullable=False)
    tipo_proprietario = Column(Enum(TipoProprietario), nullable=False, default=TipoProprietario.fisica)
    status = Column(Enum(StatusCadastro), nullable=False, default=StatusCadastro.RECEBIDO)
    nivel_verificacao = Column(Enum(VerificacaoNivel), nullable=False, default=VerificacaoNivel.CADASTRO_RECEBIDO)
    status_documentacao = Column(Enum(StatusDocumentacao), nullable=False, default=StatusDocumentacao.PENDENTE)

    valor_anunciado = Column(Integer, nullable=True)
    valor_liquido_desejado = Column(Integer, nullable=True)

    endereco = Column(String(300), nullable=True)
    cidade = Column(String(120), nullable=True)
    bairro = Column(String(120), nullable=True)
    tipo_imovel = Column(String(80), nullable=True)
    area = Column(String(40), nullable=True)
    quartos = Column(String(20), nullable=True)
    suites = Column(String(20), nullable=True)
    banheiros = Column(String(20), nullable=True)
    vagas = Column(String(20), nullable=True)
    condominio = Column(String(120), nullable=True)
    iptu = Column(String(60), nullable=True)
    caracteristicas = Column(Text, nullable=True)
    diferenciais = Column(Text, nullable=True)
    situacao = Column(String(120), nullable=True)
    disponibilidade = Column(String(200), nullable=True)
    descricao = Column(Text, nullable=True)
    titulo = Column(String(250), nullable=True)
    resumo = Column(Text, nullable=True)
    meta_description = Column(String(300), nullable=True)

    pagina_url = Column(String(500), nullable=True)
    sitemap_entries = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    documentos = relationship("ProprietarioDocumento", back_populates="proprietario", cascade="all, delete-orphan")
    fotos = relationship("ProprietarioFoto", back_populates="proprietario", cascade="all, delete-orphan")
    logs = relationship("ProprietarioLog", back_populates="proprietario", cascade="all, delete-orphan")
    declaracao = relationship("ProprietarioDeclaracao", back_populates="proprietario", uselist=False, cascade="all, delete-orphan")


class ProprietarioDocumento(Base):
    __tablename__ = "proprietarios_documentos"

    id = Column(Integer, primary_key=True, index=True)
    proprietario_id = Column(Integer, ForeignKey("proprietarios.id", ondelete="CASCADE"), nullable=False)
    tipo_documento = Column(String(120), nullable=False)
    caminho_privado = Column(String(500), nullable=False)
    nome_arquivo = Column(String(250), nullable=False)
    tamanho_bytes = Column(Integer, nullable=True)
    mime_type = Column(String(120), nullable=True)
    status = Column(String(40), nullable=False, default="pendente")
    motivo = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    proprietario = relationship("Proprietario", back_populates="documentos")


class ProprietarioFoto(Base):
    __tablename__ = "proprietarios_fotos"

    id = Column(Integer, primary_key=True, index=True)
    proprietario_id = Column(Integer, ForeignKey("proprietarios.id", ondelete="CASCADE"), nullable=False)
    caminho_publico = Column(String(500), nullable=False)
    nome_arquivo = Column(String(250), nullable=False)
    ordem = Column(Integer, nullable=True)
    aprovada = Column(Boolean, nullable=False, default=False)
    motivo_bloqueio = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    proprietario = relationship("Proprietario", back_populates="fotos")


class ProprietarioLog(Base):
    __tablename__ = "proprietarios_logs"

    id = Column(Integer, primary_key=True, index=True)
    proprietario_id = Column(Integer, ForeignKey("proprietarios.id", ondelete="CASCADE"), nullable=False)
    estado_anterior = Column(String(40), nullable=True)
    estado_novo = Column(String(40), nullable=False)
    motivo = Column(Text, nullable=True)
    origem = Column(String(120), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    proprietario = relationship("Proprietario", back_populates="logs")


class ProprietarioDeclaracao(Base):
    __tablename__ = "proprietarios_declaracoes"

    id = Column(Integer, primary_key=True, index=True)
    proprietario_id = Column(Integer, ForeignKey("proprietarios.id", ondelete="CASCADE"), nullable=False)
    versao_termo = Column(String(40), nullable=False)
    aceite = Column(Boolean, nullable=False, default=False)
    ip = Column(String(60), nullable=True)
    user_agent = Column(String(300), nullable=True)
    accepted_at = Column(DateTime(timezone=True), server_default=func.now())

    proprietario = relationship("Proprietario", back_populates="declaracao")
