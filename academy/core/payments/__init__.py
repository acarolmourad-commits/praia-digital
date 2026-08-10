"""
Payments package.

Sandbox-first payment integration, with Hotmart-ready architecture.
No secret/API key is stored here; everything comes from env vars.
"""
from .service import (
    get_payment_provider,
    is_sandbox,
    payment_gateway_enum,
)
from .webhooks import verify_webhook, handle_payment_event
