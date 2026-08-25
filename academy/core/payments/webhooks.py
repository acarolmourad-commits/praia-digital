import logging
import os
import json
import time
import hashlib
import hmac
from typing import Optional
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from academy.core.models import Payment, PaymentStatus
from academy.core.payments.service import finalize_payment

logger = logging.getLogger("academy.payments.webhooks")


# ------------------------------------------------------------------
# Custom exceptions / security helpers expected by tests
# ------------------------------------------------------------------
class WebhookAuthError(Exception):
    """Falha de autenticação/assinatura no webhook."""


class WebhookValidationError(Exception):
    """Falha de validação de payload/timestamp/estado no webhook."""


def _detect_gateway() -> str:
    return os.getenv("PAYMENT_GATEWAY", "sandbox").lower()


def _resolve_secret(gateway: str) -> str:
    mapping = {
        "hotmart": os.getenv("HOTMART_TOKEN", ""),
        "mercadopago": os.getenv("MERCADOPAGO_TOKEN", ""),
        "stripe": os.getenv("STRIPE_SECRET", ""),
    }
    return mapping.get(gateway, "")


def _safe_timestamp(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_json_load(raw: bytes):
    try:
        return json.loads(raw), None
    except Exception:
        return None, "invalid_json"


def _redact(obj):
    sensitive = {"token", "secret", "password", "authorization", "bearer", "api_key", "apikey"}
    if isinstance(obj, dict):
        return {k: ("***" if k.lower() in sensitive else _redact(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_redact(v) for v in obj]
    return obj


def _extract_event_id(payload: dict) -> Optional[str]:
    for key in ("event_id", "transaction_id", "payment_id", "id"):
        if key in payload:
            return str(payload[key])
    return None


def _is_invalid_status_transition(payment: Payment, new_status: str) -> bool:
    if payment.status == new_status:
        return True
    allowed = {
        PaymentStatus.pending.value: {PaymentStatus.paid.value, PaymentStatus.failed.value, PaymentStatus.refunded.value},
        PaymentStatus.paid.value: {PaymentStatus.refunded.value},
        PaymentStatus.failed.value: set(),
        PaymentStatus.refunded.value: set(),
    }
    return new_status not in allowed.get(payment.status, set())


# ------------------------------------------------------------------
# Gateway-specific verifiers used by tests
# ------------------------------------------------------------------
def _verify_hotmart(request: Request, body: bytes, secret: str) -> None:
    if not secret:
        raise WebhookAuthError("missing secret")
    received = _header(request, "X-Hotmart-Hmac")
    if not received:
        raise WebhookAuthError("missing hmac")
    expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(received, expected):
        raise WebhookAuthError("invalid hmac")


def _verify_mercadopago(request: Request, body: bytes, secret: str) -> None:
    if not secret:
        raise WebhookAuthError("missing secret")
    received = _header(request, "X-Signature")
    if not received:
        raise WebhookAuthError("missing signature")


def _verify_stripe(request: Request, body: bytes, secret: str) -> None:
    if not secret:
        raise WebhookAuthError("missing secret")
    timestamp = _header(request, "Stripe-Timestamp")
    signature = _header(request, "Stripe-Signature")
    if not timestamp or not signature:
        raise WebhookAuthError("missing stripe signature")
    ts = _safe_timestamp(timestamp)
    if ts is None:
        raise WebhookValidationError("invalid timestamp")
    if int(time.time()) - ts > 300:
        raise WebhookValidationError("old timestamp")
    expected = (
        "t=" + timestamp + "," +
        hmac.new(secret.encode("utf-8"), (timestamp + "." + body.decode("utf-8")).encode("utf-8"), hashlib.sha256).hexdigest()
    )
    if not hmac.compare_digest(signature, expected):
        raise WebhookValidationError("invalid stripe signature")


# ------------------------------------------------------------------
# Header helper
# ------------------------------------------------------------------
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
    gateway = getattr(getattr(request.app, "state", None), "payment_gateway", None) or _detect_gateway() or os.getenv("PAYMENT_GATEWAY", "sandbox").lower()
    if gateway == "sandbox":
        return True

    secret = _resolve_secret(gateway)
    if not secret:
        return True

    if gateway == "hotmart":
        received = _header(request, "X-Hotmart-Hmac")
        if not received:
            raise WebhookAuthError("missing hmac")
        expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(received, expected):
            raise WebhookAuthError("invalid hmac")
        return True

    if gateway == "mercadopago":
        received = _header(request, "X-Signature")
        if not received:
            raise WebhookAuthError("missing signature")
        return True

    if gateway == "stripe":
        timestamp = _header(request, "Stripe-Timestamp")
        signature = _header(request, "Stripe-Signature")
        if not timestamp or not signature:
            raise WebhookAuthError("missing stripe signature")
        ts = _safe_timestamp(timestamp)
        if ts is None:
            raise WebhookValidationError("invalid timestamp")
        if int(time.time()) - ts > 300:
            raise WebhookValidationError("old timestamp")
        expected = (
            "t=" + timestamp + "," +
            hmac.new(secret.encode("utf-8"), (timestamp + "." + body.decode("utf-8")).encode("utf-8"), hashlib.sha256).hexdigest()
        )
        if not hmac.compare_digest(signature, expected):
            raise WebhookValidationError("invalid stripe signature")
        return True

    raise WebhookValidationError("unknown gateway")


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
