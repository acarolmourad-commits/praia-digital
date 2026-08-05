import os
import smtplib
from email.mime.text import MIMEText
from typing import Optional

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "no-reply@praia.digital")


def send_email(to_email: Optional[str], subject: str, body: str, html: bool = False):
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        return {"status": "skipped", "reason": "smtp not configured"}
    to = to_email or EMAIL_FROM
    if not to:
        return {"status": "skipped", "reason": "missing destination"}
    msg = MIMEText(body, "html" if html else "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return {"status": "sent", "to": to, "subject": subject}
    except Exception as e:
        return {"status": "error", "exception": str(e)}


def send_enrollment_confirmation(user_email: Optional[str], course_name: str, course_url: str):
    subject = "Seu acesso à Praia Digital Academy"
    body = f"""<p>Olá, seu acesso já está disponível.</p>
<p>Curso: <strong>{course_name}</strong></p>
<p>Acesse em: <a href="{course_url}">{course_url}</a></p>"""
    return send_email(user_email, subject, body, html=True)
