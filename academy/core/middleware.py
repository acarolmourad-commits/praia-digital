import time
import logging
import re
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("academy")
logger.setLevel(logging.INFO)


_SANITIZE_RE = re.compile(r'<script.*?>.*?</script\s*>', re.IGNORECASE | re.DOTALL)
_TRUNCATE_LIMIT = 1024 * 1024  # 1MB


class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start = time.time()
        try:
            response = await self.app(scope, receive, send)
        except Exception as exc:
            logger.exception("Unhandled exception", exc_info=exc)
            raise
        elapsed = time.time() - start
        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": getattr(response, "status_code", "ERR"),
                "elapsed_ms": int(elapsed * 1000),
            },
        )
        return response


class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > _TRUNCATE_LIMIT:
            response = JSONResponse(status_code=413, content={"detail": "Payload too large"})
            await response(scope, receive, send)
            return

        async def send_with_security_headers(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-content-type-options", b"nosniff"))
                headers.append((b"x-frame-options", b"DENY"))
                headers.append((b"x-xss-protection", b"1; mode=block"))
                headers.append((b"referrer-policy", b"strict-origin-when-cross-origin"))
                headers.append((b"permissions-policy", b"camera=(), microphone=(), geolocation=()"))
                message = {**message, "headers": headers}
            await send(message)

        await self.app(scope, receive, send_with_security_headers)


class ErrorHandlerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        try:
            return await self.app(scope, receive, send)
        except Exception as exc:
            logger.exception("Unhandled exception", exc_info=exc)
            response = JSONResponse(status_code=500, content={"detail": "Internal server error"})
            await response(scope, receive, send)


def sanitize_text(value: str) -> str:
    if not value:
        return value
    return _SANITIZE_RE.sub("", value)[:4096]
