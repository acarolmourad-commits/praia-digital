from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PaymentGateway(str, Enum):
    sandbox = "sandbox"
    hotmart = "hotmart"
    mercadopago = "mercadopago"
    stripe = "stripe"


@dataclass(frozen=True)
class PaymentContext:
    gateway: PaymentGateway
    is_sandbox: bool = True
    enrollment_id: int = 0
    amount: int = 0
    currency: str = "BRL"
    buyer_email: str = ""
    buyer_name: str = ""
    external_reference: str = ""
    user_id: Optional[int] = None
