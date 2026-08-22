from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from academy.financeiro.models import StatusPagamento, StatusEntrega

class RegistroFinanceiroIn(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    product_name: Optional[str] = None
    order_id: Optional[str] = None
    amount_expected: int = 0
    payment_method: Optional[str] = None
    payment_proof: Optional[str] = None
    payment_proof_source: Optional[str] = None

class RegistroFinanceiroUpdate(BaseModel):
    payment_status: Optional[StatusPagamento] = None
    amount_paid: Optional[int] = None
    payment_method: Optional[str] = None
    payment_proof: Optional[str] = None
    payment_proof_source: Optional[str] = None
    payment_verified_by: Optional[str] = None
    delivery_status: Optional[StatusEntrega] = None
    delivery_released_by: Optional[str] = None

class RegistroFinanceiroOut(BaseModel):
    id: int
    customer_name: str
    customer_email: Optional[str]
    product_name: Optional[str]
    order_id: Optional[str]
    amount_expected: int
    amount_paid: Optional[int]
    payment_method: Optional[str]
    payment_status: StatusPagamento
    payment_proof: Optional[str]
    payment_proof_source: Optional[str]
    payment_proof_received_at: Optional[datetime]
    payment_verified_at: Optional[datetime]
    payment_verified_by: Optional[str]
    revenue_confirmed: int
    delivery_status: StatusEntrega
    delivery_released_at: Optional[datetime]
    delivery_released_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
