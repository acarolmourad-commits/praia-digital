from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from academy.core.database import engine, Base
from academy.core.middleware import RequestLoggingMiddleware, ErrorHandlerMiddleware, SecurityHeadersMiddleware, RateLimitMiddleware
from academy.routers import auth, courses, academy, admin, payments, recommendations, automation, automation_whatsapp, certificates, monitoring, automation_email, leads, admin_leads, content, admin_content, student
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Praia Digital Academy API", version="0.2.0")

# Middlewares
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# CORS baseado em variável de ambiente
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins != "*":
    allowed_origins = [o.strip() for o in allowed_origins.split(",") if o.strip()]
else:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(academy.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(recommendations.router)
app.include_router(automation.router)
app.include_router(automation_whatsapp.router)
app.include_router(certificates.router)
app.include_router(monitoring.router)
app.include_router(automation_email.router)
app.include_router(leads.router)
app.include_router(admin_leads.router)
app.include_router(content.router)
app.include_router(admin_content.router)
app.include_router(student.router)

# Servir área do aluno como frontend sob /education/aluno
frontend_dir = Path(__file__).resolve().parent.parent / "education" / "aluno"
if frontend_dir.exists():
    app.mount("/education/aluno", StaticFiles(directory=str(frontend_dir), html=True), name="aluno-frontend")

# Servir arquivos estáticos da API sob /static
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir), html=False), name="api-static")

@app.get("/health")
def health():
    return {"status": "ok", "service": "academy-api"}
