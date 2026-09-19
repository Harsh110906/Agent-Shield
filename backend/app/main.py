from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base

settings = get_settings()

# We will create tables directly for demo purposes (Alembic can be added for prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Runtime security & governance layer for autonomous AI agents."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": settings.VERSION}

from app.api import agents, actions, approvals, policies, metrics, simulator, demo, audit

app.include_router(agents.router, prefix="/api")
app.include_router(actions.router, prefix="/api")
app.include_router(approvals.router, prefix="/api")
app.include_router(policies.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(simulator.router, prefix="/api")
app.include_router(demo.router, prefix="/api")
app.include_router(audit.router, prefix="/api")
