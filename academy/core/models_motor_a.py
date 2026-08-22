from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from academy.core.database import Base
import enum


class MotorATipoCliente(str, enum.Enum):
    proprietario = "proprietario"
    imobiliaria = "imobiliaria"
    corretor = "corretor"
    outro = "outro"


class MotorAStatus(str, enum.Enum):
    NOVO = "NOVO"
    VALIDADO = "VALIDADO"
    QUALIFICADO = "QUALIFICADO"
    PRIORIZADO = "PRIORIZADO"
    PRONTO_D2 = "PRONTO_D2"
    D2_ENVIADO = "D2_ENVIADO"
    RESPONDEU = "RESPONDEU"
    INTERESSADO = "INTERESSADO"
    PROPOSTA = "PROPOSTA"
    CONVERTIDO = "CONVERTIDO"
    SEM_RESPOSTA = "SEM_RESPOSTA"
    ENCERRADO = "ENCERRADO"
    BLOQUEADO = "BLOQUEADO"


class MotorAEstoque(Base):
    __tablename__ = "motor_a_estoque"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String(50), nullable=False, unique=True, index=True)
    cidade = Column(String(120), nullable=True)
    bairro = Column(String(120), nullable=True)
    tipo_cliente = Column(Enum(MotorATipoCliente), nullable=True)
    nome_empresa = Column(String(250), nullable=True)
    url = Column(String(500), nullable=True)
    canal_contato = Column(String(80), nullable=True)
    servico_potencial = Column(String(250), nullable=True)
    evidencia = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    status = Column(String(80), nullable=False, default="NOVO_ESTOQUE")
    d0_enviado_em = Column(String(20), nullable=True)
    d2_enviado_em = Column(String(20), nullable=True)
    d5_enviado_em = Column(String(20), nullable=True)
    d10_enviado_em = Column(String(20), nullable=True)
    resposta = Column(Text, nullable=True)
    data_resposta = Column(String(20), nullable=True)
    tipo_resposta = Column(String(80), nullable=True)
    servico_interesse = Column(String(250), nullable=True)
    valor_potencial = Column(String(120), nullable=True)
    estagio = Column(String(120), nullable=True)
    proxima_acao = Column(String(250), nullable=True)
    responsavel = Column(String(120), nullable=True)
    objeção = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class MotorAFila(Base):
    __tablename__ = "motor_a_fila"

    id = Column(Integer, primary_key=True, index=True)
    estoque_id = Column(Integer, ForeignKey("motor_a_estoque.id", ondelete="CASCADE"), nullable=False, unique=True)
    status = Column(Enum(MotorAStatus), nullable=False, default=MotorAStatus.NOVO)
    prioridade = Column(Integer, nullable=True)
    motivo_prioridade = Column(Text, nullable=True)
    estado_anterior = Column(String(80), nullable=True)
    evento = Column(String(120), nullable=True)
    origem = Column(String(120), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    estoque = relationship("MotorAEstoque", backref="fila", uselist=False)

    __table_args__ = (
        UniqueConstraint("estoque_id", name="uq_motor_a_fila_estoque_id"),
    )
