from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from academy.core.database import Base
import enum

class StatusPagamento(str, enum.Enum):
    PAGAMENTO_PENDENTE = "PAGAMENTO_PENDENTE"
    COMPROVANTE_RECEBIDO = "COMPROVANTE_RECEBIDO_AGUARDANDO_VALIDACAO"
    PAGAMENTO_EM_VALIDACAO = "PAGAMENTO_EM_VALIDACAO"
    PAGAMENTO_CONFIRMADO = "PAGAMENTO_CONFIRMADO"
    PAGAMENTO_REJEITADO = "PAGAMENTO_REJEITADO"
    PAGAMENTO_NAO_ENCONTRADO = "PAGAMENTO_NAO_ENCONTRADO"
    PAGAMENTO_ESTORNADO = "PAGAMENTO_ESTORNADO"

class StatusEntrega(str, enum.Enum):
    BLOQUEADA = "BLOQUEADA"
    ENTREGUE = "ENTREGUE"
    CANCELADA = "CANCELADA"

class RegistroFinanceiro(Base):
    __tablename__ = "registros_financeiros"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=True)
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(200), nullable=True)
    product_id = Column(Integer, nullable=True)
    product_name = Column(String(200), nullable=True)
    order_id = Column(String(100), nullable=True)
    amount_expected = Column(Integer, nullable=False, default=0)
    amount_paid = Column(Integer, nullable=True)
    payment_method = Column(String(100), nullable=True)
    payment_status = Column(Enum(StatusPagamento), nullable=False, default=StatusPagamento.PAGAMENTO_NAO_ENCONTRADO)
    payment_proof = Column(String(500), nullable=True)
    payment_proof_source = Column(String(100), nullable=True)
    payment_proof_received_at = Column(DateTime(timezone=True), nullable=True)
    payment_verified_at = Column(DateTime(timezone=True), nullable=True)
    payment_verified_by = Column(String(100), nullable=True)
    revenue_confirmed = Column(Integer, nullable=False, default=0)
    delivery_status = Column(Enum(StatusEntrega), nullable=False, default=StatusEntrega.BLOQUEADA)
    delivery_released_at = Column(DateTime(timezone=True), nullable=True)
    delivery_released_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
