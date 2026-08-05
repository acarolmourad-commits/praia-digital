import os
import requests
from typing import Optional

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
WHATSAPP_TO_NUMBER = os.getenv("WHATSAPP_TO_NUMBER", "")

def send_text(to_number: Optional[str], text: str) -> dict:
    if not WHATSAPP_API_URL or not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        return {"status": "skipped", "reason": "not configured"}
    number = to_number or WHATSAPP_TO_NUMBER
    if not number:
        return {"status": "skipped", "reason": "no destination"}
    
    # Generic WhatsApp Cloud API shape
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": text},
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_ID}/messages", json=payload, headers=headers, timeout=20)
        if resp.status_code in (200, 201):
            return {"status": "sent", "provider_response": resp.json()}
        return {"status": "error", "code": resp.status_code, "body": resp.text}
    except requests.RequestException as e:
        return {"status": "error", "exception": str(e)}

def send_template(to_number: Optional[str], template_name: str, language_code: str = "pt_BR", components: Optional[list] = None) -> dict:
    if not WHATSAPP_API_URL or not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        return {"status": "skipped", "reason": "not configured"}
    number = to_number or WHATSAPP_TO_NUMBER
    if not number:
        return {"status": "skipped", "reason": "no destination"}
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
            "components": components or [],
        },
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_ID}/messages", json=payload, headers=headers, timeout=20)
        if resp.status_code in (200, 201):
            return {"status": "sent", "provider_response": resp.json()}
        return {"status": "error", "code": resp.status_code, "body": resp.text}
    except requests.RequestException as e:
        return {"status": "error", "exception": str(e)}

def send_media(to_number: Optional[str], media_url: str, caption: Optional[str] = None, media_type: str = "image") -> dict:
    if not WHATSAPP_API_URL or not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        return {"status": "skipped", "reason": "not configured"}
    number = to_number or WHATSAPP_TO_NUMBER
    if not number:
        return {"status": "skipped", "reason": "no destination"}
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": media_type,
        media_type: {"link": media_url, **({"caption": caption} if caption else {})},
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_ID}/messages", json=payload, headers=headers, timeout=20)
        if resp.status_code in (200, 201):
            return {"status": "sent", "provider_response": resp.json()}
        return {"status": "error", "code": resp.status_code, "body": resp.text}
    except requests.RequestException as e:
        return {"status": "error", "exception": str(e)}
