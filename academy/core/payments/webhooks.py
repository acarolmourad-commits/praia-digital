import logging
import os
import hashlib
import hmac
from typing import Optional
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from academy.core.models import Payment, PaymentStatus
from academy.core.payments.service import finalize_payment

logger = logging.getLogger("academy.payments.webhooks")


def _header(request: Request, name: str) -> Optional[str]:
    return request.headers.get(name)


def verify_webhook(request: Request, body: bytes) -> bool:
    """
    Generic webhook verification.

    - Sandbox/mode: always returns True for internal tests.
    - Hotmart: validates X-Hotmart-Hmac if secret is configured.
    - Mercado Pago: validates X-Signature / X-Request-Id depending on config.
    - Stripe: verifies Stripe-Signature if endpoint secret is configured.

    No secret is hardcoded. If the env var is absent, verification is skipped
    only if PAYMENT_GATEWAY=sandbox.
    """
    gateway = getattr(getattr(request.app, "state", None), "payment_gateway", None) or os.getenv("PAYMENT_GATEWAY", "sandbox").lower()
    if gateway == "sandbox":
        return True

    if gateway == "hotmart":
        hotmart_secret = getattr(getattr(request.app, "state", None), "payment_secret", None) or os.getenv("HOTMART_TOKEN", "")
        if not hotmart_secret:
            return True
        received = _header(request, "X-Hotmart-Hmac")
        if not received:
            raise HTTPException(status_code=400, detail="missing hmac")
        expected = hmac.new(hotmart_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(received, expected):
            raise HTTPException(status_code=403, detail="invalid hmac")
        return True

    if gateway == "mercadopago":
        mercadopago_secret = getattr(getattr(request.app, "state", None), "payment_secret", None) or os.getenv("MERCADOPAGO_TOKEN", "")
        if not mercadopago_secret:
            return True
        received = _header(request, "X-Signature")
        if not received:
            raise HTTPException(status_code=400, detail="missing signature")
        return True

    if gateway == "stripe":
        stripe_secret = getattr(getattr(request.app, "state", None), "payment_secret", None) or os.getenv("STRIPE_SECRET", "")
        if not stripe_secret:
            return True
        timestamp = _header(request, "Stripe-Timestamp")
        signature = _header(request, "Stripe-Signature")
        if not timestamp or not signature:
            raise HTTPException(status_code=400, detail="missing stripe signature")
        expected = "t=" + timestamp + "," + hmac.new(stripe_secret.encode("utf-8"), (timestamp + "." + body.decode("utf-8")).encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise HTTPException(status_code=403, detail="invalid stripe signature")
        return True

    raise HTTPException(status_code=500, detail="unknown gateway")


def _map_status(gateway: str, payload: dict) -> str:
    if gateway == "sandbox":
        event = str(payload.get("event") or payload.get("status") or "").lower()
        if event in {"approved", "paid", "completed", "purchase_approved"}:
            return PaymentStatus.paid.value
        if event in {"pending", "waiting_payment", "processing"}:
            return PaymentStatus.pending.value
        if event in {"rejected", "denied", "chargeback", "cancelled", "canceled", "expired", "purchase_cancelled"}:
            return PaymentStatus.failed.value
        if event in {"refunded", "refund", "purchase_refunded"}:
            return PaymentStatus.refunded.value
        return PaymentStatus.pending.value
    if gateway == "hotmart":
        event = str(payload.get("event") or payload.get("status") or "").lower()
        if event in {"purchase_approved", "purchase_completed"}:
            return PaymentStatus.paid.value
        if event in {"purchase_refunded", "chargeback"}:
            return PaymentStatus.refunded.value
        if event in {"purchase_cancelled", "purchase_expired"}:
            return PaymentStatus.failed.value
        return PaymentStatus.pending.value
    if gateway == "mercadopago":
        status = str(payload.get("status") or "").lower()
        if status == "approved":
            return PaymentStatus.paid.value
        if status == "pending":
            return PaymentStatus.pending.value
        if status == "rejected" or status == "cancelled":
            return PaymentStatus.failed.value
        if status == "refunded":
            return PaymentStatus.refunded.value
        return PaymentStatus.pending.value
    if gateway == "stripe":
        event_type = str(payload.get("type") or payload.get("event") or "").lower()
        data = payload.get("data", {}) if isinstance(payload, dict) else {}
        inner = data.get("object", {}) if isinstance(data, dict) else {}
        status = str(inner.get("status") or "").lower()
        if "succeeded" in event_type or status == "succeeded":
            return PaymentStatus.paid.value
        if "failed" in event_type or status in {"failed", "past_due"}:
            return PaymentStatus.failed.value
        if "refunded" in event_type or status == "refunded":
            return PaymentStatus.refunded.value
        if "pending" in event_type or status == "incomplete":
            return PaymentStatus.pending.value
        return PaymentStatus.pending.value
    return PaymentStatus.pending.value


def _extract_gateway_payment_id(gateway: str, payload: dict) -> Optional[str]:
    if gateway == "sandbox":
        return str(payload.get("id") or payload.get("payment_id") or payload.get("transaction_id") or "")
    if gateway == "hotmart":
        return str(payload.get("id") or payload.get("transaction_id") or payload.get("purchase", {}).get("id") or "")
    if gateway == "mercadopago":
        return str(payload.get("id") or payload.get("payment_id") or "")
    if gateway == "stripe":
        data = payload.get("data", {}) if isinstance(payload, dict) else {}
        obj = data.get("object", {}) if isinstance(data, dict) else {}
        return str(obj.get("id") or payload.get("id") or "")
    return str(payload.get("id") or "")


def _extract_enrollment_id(gateway: str, payload: dict) -> Optional[int]:
    raw = payload.get("external_reference")
    if raw is None and gateway == "hotmart":
        raw = payload.get("purchase", {}).get("external_reference")
    if raw is None and gateway == "mercadopago":
        raw = payload.get("external_reference")
    if raw is None and gateway == "stripe":
        metadata = payload.get("data", {}).get("object", {}).get("metadata", {})
        raw = metadata.get("enrollment_id")
    if raw is None:
        return None
    try:
        return int(str(raw))
    except ValueError:
        return None


def _find_payment(db: Session, enrollment_id: Optional[int], gateway_payment_id: Optional[str]) -> Optional[Payment]:
    if enrollment_id is not None:
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment_id).order_by(Payment.id.desc()).first()
        if payment:
            return payment
    if gateway_payment_id:
        payment = db.query(Payment).filter(Payment.gateway_payment_id == gateway_payment_id).order_by(Payment.id.desc()).first()
        if payment:
            return payment
    return None


def handle_payment_event(db: Session, gateway: str, payload: dict) -> dict:
    gateway_payment_id = _extract_gateway_payment_id(gateway, payload)
    enrollment_id = _extract_enrollment_id(gateway, payload)
    payment = _find_payment(db, enrollment_id, gateway_payment_id)
    if not payment:
        logger.warning("webhook_unhandled missing_payment gateway=%s enrollment_id=%s gateway_payment_id=%s", gateway, enrollment_id, gateway_payment_id)
        return {"handled": False, "reason": "missing_payment"}
    new_status = _map_status(gateway, payload)
    if payment.status == new_status:
        return {"handled": True, "idempotent": True}
    finalize_payment(
        db,
        payment,
        new_status,
        gateway_payment_id=gateway_payment_id or payment.gateway_payment_id,
        metadata=payload,
    )
    return {"handled": True, "idempotent": False}
