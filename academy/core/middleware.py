import time
import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("academy")
logger.setLevel(logging.INFO)


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
