from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import logging

logger = logging.getLogger("academy")
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next):
        start = time.time()
        try:
            response = await call_next(request)
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
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception("Unhandled exception", exc_info=exc)
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})
